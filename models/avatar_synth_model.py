import tensorflow as tf
from tensorpack import InputDesc, ModelDesc
from tensorpack.models.regularize import Dropout as tpDropout

from model_architectures import IMG_DIMS
from model_architectures import avatar_synth_model as arch
from utils.bitmoji_api import BITMOJI_PARAM_SIZE
from utils.tfutils import narrow_truncated_normal_initializer

class AvatarSynthModel(ModelDesc):
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
        return [InputDesc(tf.float32, (None, BITMOJI_PARAM_SIZE), 'Avatar_Synth/Parameters'),
                InputDesc(tf.float32, (None,) + IMG_DIMS, 'Avatar_Synth/Images')]

    def _build_graph(self, inputs):
        """
        Construct the graph and define self.cost.

        :param inputs: The input tensors fed in by TensorPack.
        """
        # with tf.variable_scope('', reuse=tf.AUTO_REUSE):
        self.params, self.imgs = inputs

        # Reshape params into a 1x1 'image' for convolution
        self.preds = tf.reshape(self.params, (-1, 1, 1, BITMOJI_PARAM_SIZE))
        for i in xrange(len(arch['conv_filters']) - 1):
            # Apply ReLU on all but the last layer
            activation = tf.nn.relu
            if i == len(arch['conv_filters']) - 2:
                activation = tf.nn.tanh

            self.preds = tf.layers.conv2d_transpose(
                self.preds,
                arch['conv_filters'][i + 1],
                arch['filter_widths'][i],
                arch['strides'][i],
                padding=arch['padding'][i],
                activation=tf.nn.relu,
                name='Deconv_' + str(i),
                reuse=tf.AUTO_REUSE,
                trainable=False
            )
            self.preds = tf.layers.conv2d_transpose(
                self.preds,
                arch['conv_filters'][i + 1],
                1,
                1,
                padding='SAME',
                activation=activation,
                kernel_initializer=narrow_truncated_normal_initializer,
                bias_initializer=tf.zeros_initializer,
                name='Conv_' + str(i),
                reuse=tf.AUTO_REUSE,
                trainable=False
            )

            # Apply batch norm on all but the last layer
            if i < len(arch['conv_filters']) - 2:
                self.preds = tf.layers.batch_normalization(self.preds, name='BN_' + str(i),
                                                           reuse=tf.AUTO_REUSE)
                self.preds = tpDropout(self.preds, keep_prob=self.args.keep_prob)

        self.cost = tf.reduce_mean(tf.square(self.imgs - self.preds), name='Cost')

        self.lr = tf.Variable(self.args.lr, trainable=False, name='LR')

        with tf.name_scope('Summaries'):
            pred_comp = tf.concat([self.imgs, self.preds], axis=2)
            tf.summary.image('Preds', pred_comp)
            tf.summary.scalar('Cost', self.cost)

    def _get_optimizer(self):
        return tf.train.AdamOptimizer(learning_rate=self.lr)
