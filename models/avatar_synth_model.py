import tensorflow as tf
# from tensorpack.graph_builder.model_desc import ModelDesc
# from tensorpack.input_source.input_source import BatchQueueInput
# from tensorpack.dataflow import BatchQueueInput
from tensorpack import InputDesc, ModelDesc
from tensorpack.models.regularize import Dropout as tpDropout

from model_architectures import NUM_PARAMS, IMG_DIMS
from model_architectures import avatar_synth_model as arch
#from utils.tfutils import w, b

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
        with tf.name_scope('Avatar_Synth'):
            return [InputDesc(tf.float32, (None, NUM_PARAMS), 'parameters'),
                    InputDesc(tf.float32, (None,) + IMG_DIMS, 'images')]

    def _build_graph(self, inputs):
        """
        Construct the graph and define self.cost.

        :param inputs: The input tensors fed in by TensorPack.
        """
        with tf.name_scope('Avatar_Synth'):
            self.params, self.imgs = inputs

            # Reshape params into a 1x1 'image' for convolution
            self.preds = tf.reshape(self.params, (-1, 1, 1, NUM_PARAMS))
            for i in xrange(len(arch['conv_filters']) - 1):
                self.preds = tf.layers.conv2d_transpose(
                    self.preds,
                    arch['conv_filters'][i + 1],
                    arch['conv_widths'][i],
                    arch['strides'][i],
                    padding=arch['padding'][i],
                    # Apply PReLU activation on all but the last layer
                    activation=(tf.keras.layers.PReLU if i < len(arch['conv_filters']) - 2 else None),
                    kernel_initializer=tf.keras.initializers.glorot_normal,
                    bias_initializer=tf.initializers.ones,
                    activity_regularizer=tf.layers.batch_normalization,
                    name='Deconv_' + str(i)
                )
                self.preds = tpDropout(self.preds, keep_prob=self.args.keep_prob)


            self.cost = tf.reduce_mean(tf.square(self.imgs - self.preds),
                                       name='Cost')

    def _get_optimizer(self):
        return tf.train.AdamOptimizer(learning_rate=self.args.lr)


###########################################

        # self.ws = []
        # self.bs = []
        # for i in xrange(len(arch['conv_filters']) - 1):
        #     with tf.name_scope('Layer_' + str(i)):
        #         # conv2d_transpose takes shape [height, width, out, in]
        #         self.ws.append(w((arch['filter_widths'][i],
        #                           arch['filter_widths'][i],
        #                           arch['conv_filters'][i + 1],
        #                           arch['conv_filters'][i])))
        #         self.bs.append(b((arch['conv_filters'][i + 1],)))

    # with tf.name_scope('Computation'):
    #     self.preds = self._get_preds(self.params)
    # def _get_preds(self, inputs):
    #     """
    #     Perform computation to generate Bitmoji image tensors given parameters.
    #
    #     :param inputs: The bitmoji parameter vectors.
    #
    #     :return: The generated image tensors for each parameter set in inputs.
    #     """
    #     preds = inputs
    #
    #     with tf.name_scope('Deconv'):
    #         for i, (ws, bs) in zip(self.ws, self.bs):
    #             with tf.name_scope('Layer_' + str(i)):
    #                 out_shape = ()
    #                 preds = tf.nn.conv2d_transpose(
    #                     preds,
    #                     ws,
    #                     out_shape,
    #                     [1, arch['strides'][i], arch['strides'][i], 1],
    #                     padding=arch['padding'][i])
    #                 preds = tpDropout(preds + bs)
    #
    #                 # Apply ReLU to all but last layer
    #                 if i < len(self.ws) - 1:
    #                     preds = tf.keras.layers.PReLU(preds)
    #
    #     return preds