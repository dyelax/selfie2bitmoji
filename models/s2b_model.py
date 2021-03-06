import tensorflow as tf
from tensorpack import InputDesc, ModelDesc, TowerTrainer
from tensorpack.tfutils.tower import TowerContext, TowerFuncWrapper
from tensorpack.models.regularize import Dropout as tpDropout

import model_architectures as archs

from utils.s2b import narrow_truncated_normal_initializer
from utils.bitmoji_api import BITMOJI_PARAM_SPLIT, BITMOJI_PARAM_SIZE
from utils import vae_gan


COEFF_L_GAN = 0.01
COEFF_L_CONST = 100.0
COEFF_L_TID = 1.0
COEFF_L_TV = 0.0005


# noinspection PyMethodMayBeStatic
class Selfie2BitmojiModel(ModelDesc):
    """
    The "e" network from the paper. Trained to emulate the Bitmoji rendering
    engine by producing images from parameters.
    """
    def __init__(self, args):
        """
        :param args: The cli arguments.
        """
        self.args = args

    def _get_inputs(self):
        """
        :return: The input descriptions for TensorPack.
        """
        # TODO: Get back to None for batch_size
        return [InputDesc(tf.float32, (self.args.batch_size,) + archs.IMG_DIMS, 'Face_Images'),
                InputDesc(tf.float32, (self.args.batch_size,) + archs.IMG_DIMS, 'Bitmoji_Images')]

    def _build_graph(self, inputs):
        """
        Construct the graph and define self.cost.

        :param inputs: The input tensors fed in by TensorPack. A batch of real
                       face images.
        """
        face_imgs, bitmoji_imgs = inputs

        # Pipeline from face image to Bitmoji
        face_encodings = self._face_encoder(face_imgs)
        gen_faces = self._generator(face_encodings)
        params = self._param_encoder(gen_faces)
        avatar_synth_faces = self._avatar_synth(params)

        # GAN discriminator predictions
        # Use instance noise to stabilize training
        noise_stddev = tf.Variable(0.1, trainable=False, name='Instance_Noise_Stddev')
        instance_noise = tf.random_normal(tf.shape(face_imgs), stddev=noise_stddev)
        noisy_bitmoji_imgs = bitmoji_imgs + instance_noise
        noisy_gen_faces = gen_faces + instance_noise

        d_preds_real = self._discriminator(noisy_bitmoji_imgs)
        d_preds_fake = self._discriminator(noisy_gen_faces)

        # Use these to only update the discriminator if above a level of uncertainty
        self.d_uncertainty = tf.reduce_mean(tf.concat([(1 - d_preds_real), d_preds_fake], 0), name='D_Uncertainty')
        self.d_uncertainty_threshold = tf.Variable(0.3, trainable=False, name='D_Uncertainty_Threshold')

        # Other misc results for losses
        gen_face_encodings = self._face_encoder(gen_faces)
        regen_bitmoji = self._generator(self._face_encoder(bitmoji_imgs))

        # Get shifted versions of the generated faced to compute pixel-wise gradients for l_tv
        batch_size, height, width, channels = gen_faces.shape
        gen_faces_left_shift = tf.concat(
            [gen_faces[:, :,1:,:], tf.zeros((batch_size, height, 1, channels))], axis=2)
        gen_faces_up_shift = tf.concat(
            [gen_faces[:, 1:,:,:], tf.zeros((batch_size, 1, width, channels))], axis=1)

        ##
        # Losses:
        ##

        # L2 diff between first generated image and image generated by running
        # parameters through e. Enforces that G learns to generate images close
        # to those generated by e
        self.l_c = tf.reduce_mean(tf.square(gen_faces - avatar_synth_faces), name='L_c')

        # L2 loss between the embedding of the input image and the embedding of
        # the first generated image. Generator learns to maintain structural
        # information from the embedding.
        self.l_const = tf.multiply(COEFF_L_CONST,
                                   tf.reduce_mean(tf.square(face_encodings - gen_face_encodings)),
                                   name='L_const')

        # Regular ol' gan loss. Enforces that generator generates in the style
        # of the target images
        self.l_gan_d = tf.multiply(COEFF_L_GAN,
                                   tf.reduce_mean(-1 * (tf.log(1 - d_preds_fake) + tf.log(d_preds_real))),
                                   name='L_gan_d')
        self.l_gan_g = tf.multiply(COEFF_L_GAN,
                                   tf.reduce_mean(-1 * (tf.log(d_preds_fake))),
                                   name='L_gan_g')

        # L2 loss between rendered Bitmoji images and those same images
        # regenerated (fed through the face encoder and generator). Encourages
        # the generator to be the identity function for Bitmoji images.
        self.l_tid = tf.multiply(COEFF_L_TID,
                                 tf.reduce_mean(tf.square(bitmoji_imgs - regen_bitmoji)),
                                 name='L_tid')

        # Sum of the pixel-wise gradients
        # Add small constant to avoid NaN gradient from sqrt(0)
        self.l_tv = tf.multiply(COEFF_L_TV,
                                tf.reduce_mean(tf.sqrt(tf.square(gen_faces_left_shift - gen_faces) +
                                                       tf.square(gen_faces_up_shift - gen_faces) + 1e-8)),
                                name='L_tv')


        ##
        # Misc:
        ##

        # Dynamic learning rate
        self.lr = tf.Variable(self.args.lr, trainable=False, name='LR')

        # Variable groups
        self.g_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Generator')
        self.d_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Discriminator')
        self.c_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Param_Encoder')

        with tf.name_scope('Summaries'):
            pred_comp = tf.concat([face_imgs, gen_faces, avatar_synth_faces], axis=2)
            tf.summary.image('Preds', pred_comp)

            tf.summary.scalar('L_c', self.l_c)
            tf.summary.scalar('L_const', self.l_const)
            tf.summary.scalar('L_gan_d', self.l_gan_d)
            tf.summary.scalar('L_gan_g', self.l_gan_g)
            tf.summary.scalar('L_tid', self.l_tid)
            tf.summary.scalar('L_tv', self.l_tv)

            tf.summary.scalar('LR', self.lr)
            tf.summary.scalar('D_Uncertainty', self.d_uncertainty)

    def _get_optimizer(self):
        return tf.train.AdamOptimizer(learning_rate=self.lr, beta1=0.5)

    ##
    # Models
    ##

    def _face_encoder(self, imgs):
        """
        Constructs and computes the face encoder model. Architecture taken from
        https://github.com/zhangqianhui/vae-gan-tensorflow

        :param imgs: The batch of images to encode into facial features.

        :return: A batch of facial feature encodings for imgs.
        """
        with tf.variable_scope('Face_Encoder', reuse=tf.AUTO_REUSE):
            conv1 = tf.nn.relu(vae_gan.batch_normal(
                vae_gan.conv2d(imgs, output_dim=64, name='Conv_0'), scope='BN_0'))
            conv2 = tf.nn.relu(vae_gan.batch_normal(
                vae_gan.conv2d(conv1, output_dim=128, name='Conv_1'), scope='BN_1'))
            conv3 = tf.nn.relu(vae_gan.batch_normal(
                vae_gan.conv2d(conv2, output_dim=256, name='Conv_2'), scope='BN_2'))

            conv3 = tf.reshape(conv3, [-1, 256 * 8 * 8])

            fc1 = tf.nn.relu(vae_gan.batch_normal(
                vae_gan.fully_connect(conv3, output_size=1024, scope='FC_0'), scope='BN_3'))

            z_mean = vae_gan.fully_connect(fc1, output_size=archs.FACE_ENCODING_SIZE, scope='FC_1')
            z_sigma = vae_gan.fully_connect(fc1, output_size=archs.FACE_ENCODING_SIZE, scope='FC_2')

            z_x = z_mean + (tf.sqrt(tf.exp(z_sigma)) *
                            tf.random_normal((self.args.batch_size, archs.FACE_ENCODING_SIZE)))

            return z_x

    def _generator(self, encodings):
        """
        Constructs and computes the generator model.

        :param encodings: A batch of facial feature encodings from which to to
                          generate Bitmoji-style faces.

        :return: A batch of Bitmoji-style faces generated from encodings.
        """
        with tf.variable_scope('Generator', reuse=tf.AUTO_REUSE):
            arch = archs.generator_model

            # Unshared fc layer to make sure face and bitmoji encodings (different sizes) can both
            # be used as inputs
            preds = tf.layers.dense(encodings,
                                    archs.GENERATOR_INPUT_SIZE,
                                    activation=tf.nn.relu,
                                    kernel_initializer=narrow_truncated_normal_initializer,
                                    bias_initializer=tf.zeros_initializer,
                                    name='FC',
                                    reuse=False)
            preds = tf.reshape(preds, (-1, 1, 1, archs.GENERATOR_INPUT_SIZE))

            for i in xrange(len(arch['conv_filters']) - 1):
                # Apply ReLU on all but the last layer
                activation = tf.nn.leaky_relu
                if i == len(arch['conv_filters']) - 2:
                    activation = tf.nn.tanh

                preds = tf.layers.conv2d_transpose(
                    preds,
                    arch['conv_filters'][i + 1],
                    arch['filter_widths'][i],
                    arch['strides'][i],
                    padding=arch['padding'][i],
                    activation=tf.nn.leaky_relu,
                    kernel_initializer=narrow_truncated_normal_initializer,
                    bias_initializer=tf.zeros_initializer,
                    name='Deconv_' + str(i),
                )

                preds = tf.layers.conv2d(
                    preds,
                    arch['conv_filters'][i + 1],
                    1,
                    1,
                    padding='SAME',
                    activation=activation,
                    kernel_initializer=narrow_truncated_normal_initializer,
                    bias_initializer=tf.zeros_initializer,
                    name='Conv_' + str(i),
                )

                # Apply batch norm on all but the last layer
                if i < len(arch['conv_filters']) - 2:
                    preds = tf.layers.batch_normalization(preds, name='BN_' + str(i))
                    preds = tpDropout(preds, keep_prob=self.args.keep_prob)

        return preds

    def _discriminator(self, imgs):
        """
        Constructs and computes the discriminator model.

        :param imgs: A batch of real or generated images.

        :return: A batch of predictions, whether each image in imgs is real or
                 generated.
        """
        with tf.variable_scope('Discriminator', reuse=tf.AUTO_REUSE):
            arch = archs.avatar_synth_model

            preds = imgs
            for i in xrange(len(arch['conv_filters']) - 1):
                # Apply leaky ReLU on all but the last layer
                activation = tf.nn.leaky_relu
                if i == len(arch['conv_filters']) - 2:
                    activation = tf.nn.sigmoid

                preds = tf.layers.conv2d(
                    preds,
                    arch['conv_filters'][i + 1],
                    arch['filter_widths'][i],
                    arch['strides'][i],
                    padding=arch['padding'][i],
                    activation=activation,
                    kernel_initializer=narrow_truncated_normal_initializer,
                    bias_initializer=tf.zeros_initializer,
                    name='Conv_' + str(i),
                )

                # Apply batch norm and dropout on all but the last layer
                if i < len(arch['conv_filters']) - 2:
                    preds = tf.layers.batch_normalization(preds, name='BN_' + str(i))
                    preds = tpDropout(preds, keep_prob=self.args.keep_prob)

            # Clip the discriminator values for stability
            preds = tf.clip_by_value(preds, 0.1, 0.9)

        return preds

    # TODO: Pretrain this with supervised data?
    def _param_encoder(self, gen_faces):
        """
        Constructs and computes the parameter encoder model.

        :param gen_faces: A batch of Bitmoji-style faces generated by the
                          generator model.

        :return: A batch of predicted Bitmoji parameter vectors for gen_faces.
        """
        with tf.variable_scope('Param_Encoder', reuse=tf.AUTO_REUSE):
            arch = archs.param_encoder_model

            preds = gen_faces
            for i in xrange(len(arch['conv_filters']) - 1):
                # Apply leaky ReLU on all but the last layer
                activation = tf.nn.leaky_relu
                if i == len(arch['conv_filters']) - 2:
                    activation = tf.nn.sigmoid

                preds = tf.layers.conv2d(
                    preds,
                    arch['conv_filters'][i + 1],
                    arch['filter_widths'][i],
                    arch['strides'][i],
                    padding=arch['padding'][i],
                    activation=activation,
                    bias_initializer=tf.zeros_initializer,
                    name='Conv_' + str(i),
                )

                # Apply batch norm and dropout on all but the last layer
                if i < len(arch['conv_filters']) - 2:
                    preds = tf.layers.batch_normalization(preds, name='BN_' + str(i))
                    preds = tpDropout(preds, keep_prob=self.args.keep_prob)

            # Split param types and softmax to get binary vector with only one
            # truth value for each param type
            preds = tf.layers.flatten(preds, name='Flatten')
            param_sets = tf.split(preds, BITMOJI_PARAM_SPLIT, axis=1, name='Split')
            # TODO: softmax with low temp to act as sharp max?
            preds = tf.concat([tf.nn.softmax(param_set) for param_set in param_sets], 1,
                              name='Concat')


        return preds

    def _avatar_synth(self, params):
        """
        Constructs and computes the avatar synthesis model. This should be
        pretrained by run_avatar_synth.py and not trained in this complete
        model.

        :param params: The Bitmoji parameters to synthesize into Bitmoji images.

        :return: A batch of Bitmoji images synthesized from params.
        """
        with tf.variable_scope('Avatar_Synth', reuse=tf.AUTO_REUSE):
            arch = archs.avatar_synth_model

            # Reshape params into a 1x1 'image' for convolution
            preds = tf.reshape(params, (-1, 1, 1, BITMOJI_PARAM_SIZE))
            for i in xrange(len(arch['conv_filters']) - 1):
                # Apply ReLU on all but the last layer
                activation = tf.nn.relu
                if i == len(arch['conv_filters']) - 2:
                    activation = tf.nn.tanh

                preds = tf.layers.conv2d_transpose(
                    preds,
                    arch['conv_filters'][i + 1],
                    arch['filter_widths'][i],
                    arch['strides'][i],
                    padding=arch['padding'][i],
                    activation=tf.nn.relu,
                    name='Deconv_' + str(i),
                    trainable=False
                )
                preds = tf.layers.conv2d(
                    preds,
                    arch['conv_filters'][i + 1],
                    1,
                    1,
                    padding='SAME',
                    activation=activation,
                    bias_initializer=tf.zeros_initializer,
                    name='Conv_' + str(i),
                    trainable=False
                )

                # Apply batch norm on all but the last layer
                if i < len(arch['conv_filters']) - 2:
                    preds = tf.layers.batch_normalization(preds, name='BN_' + str(i), trainable=False)

        return preds


class S2BTrainer(TowerTrainer):
    def __init__(self, input, model):
        super(S2BTrainer, self).__init__()
        # assert isinstance(model, GANModelDesc), model
        inputs_desc = model.get_inputs_desc()

        # Setup input
        cbs = input.setup(inputs_desc)
        for cb in cbs:
            self.register_callback(cb)

        """
        We need to set tower_func because it's a TowerTrainer,
        and only TowerTrainer supports automatic graph creation for inference during training.
        If we don't care about inference during training, using tower_func is
        not needed. Just calling model.build_graph directly is OK.
        """
        # Build the graph
        self.tower_func = TowerFuncWrapper(model.build_graph, inputs_desc)
        with TowerContext('', is_training=True):
            self.tower_func(*input.get_input_tensors())
        opt = model.get_optimizer()

        # Define the training iteration
        # by default, run one d_min after one g_min
        with tf.name_scope('Optimize'):
            self.train_op_d = opt.minimize(model.l_gan_d, var_list=model.d_vars, name='Train_Op_d')

            # with tf.control_dependencies([train_op_d]):
            train_op_gan_g = opt.minimize(model.l_gan_g, var_list=model.g_vars, name='Train_Op_gan_g')
            train_op_const = opt.minimize(model.l_const, var_list=model.g_vars, name='Train_Op_const')
            train_op_tid = opt.minimize(model.l_tid, var_list=model.g_vars, name='Train_Op_tid')
            train_op_tv = opt.minimize(model.l_tv, var_list=model.g_vars, name='Train_Op_tv')

            train_op_g = tf.group(train_op_gan_g, train_op_const, train_op_tid, train_op_tv)

            with tf.control_dependencies([train_op_g]):
                train_op_c_g = opt.minimize(model.l_c, var_list=model.c_vars + model.g_vars,
                                            name='Train_Op_c_g')

            self.train_op_c_g = train_op_c_g

            self.d_uncertainty = model.d_uncertainty
            self.threshold = model.d_uncertainty_threshold


    def run_step(self):
        # self.hooked_sess.run(self.train_op_gan_d)
        # self.hooked_sess.run(self.train_op_gan_g)
        # self.hooked_sess.run(self.train_op_c)
        # self.hooked_sess.run(self.train_op_const)
        # self.hooked_sess.run(self.train_op_tid)
        # self.hooked_sess.run(self.train_op_tv)

        _, d_uncertainty, threshold = self.hooked_sess.run(
            [self.train_op_c_g, self.d_uncertainty, self.threshold])

        if d_uncertainty > threshold:
            self.hooked_sess.run(self.train_op_d)

