import tensorflow as tf
from tensorflow.contrib.layers.python.layers import batch_norm

from model_architectures import FACE_ENCODING_SIZE, IMG_DIMS

# noinspection PyAttributeOutsideInit
class vaegan(object):

    #build model
    def __init__(self):
        self.images = tf.placeholder(tf.float32, (None,) + IMG_DIMS)
        self.ep = tf.random_normal(shape=(None, FACE_ENCODING_SIZE))
        self.build_model_vaegan()

    def build_model_vaegan(self):
        with tf.name_scope('Face_Encoder/Model'):
            self.z_mean, self.z_sigm = self._encode(self.images)
            self.z_x = tf.add(self.z_mean, tf.sqrt(tf.exp(self.z_sigm))*self.ep)

    @staticmethod
    def _encode(x):
        with tf.variable_scope('Face_Encoder/Encode'):
            conv1 = tf.nn.relu(batch_normal(conv2d(x, output_dim=64, name='e_c1'), scope='e_bn1'))
            conv2 = tf.nn.relu(batch_normal(conv2d(conv1, output_dim=128, name='e_c2'), scope='e_bn2'))
            conv3 = tf.nn.relu(batch_normal(conv2d(conv2, output_dim=256, name='e_c3'), scope='e_bn3'))
            conv3 = tf.reshape(conv3, [-1, 256 * 8 * 8])
            fc1 = tf.nn.relu(batch_normal(fully_connect(conv3, output_size=1024, scope='e_f1'), scope='e_bn4'))
            z_mean = fully_connect(fc1, output_size=FACE_ENCODING_SIZE, scope='e_f2')
            z_sigma = fully_connect(fc1, output_size=FACE_ENCODING_SIZE, scope='e_f3')

            return z_mean, z_sigma


def conv2d(input_, output_dim,
           k_h=5, k_w=5, d_h=2, d_w=2, stddev=0.02,
           name="conv2d"):

    with tf.variable_scope(name):
        w = tf.get_variable('w', [k_h, k_w, input_.get_shape()[-1], output_dim],
                            initializer=tf.truncated_normal_initializer(stddev=stddev))
        conv = tf.nn.conv2d(input_, w, strides=[1, d_h, d_w, 1], padding='SAME')
        biases = tf.get_variable('biases', [output_dim], initializer=tf.constant_initializer(0.0))
        conv = tf.reshape(tf.nn.bias_add(conv, biases), conv.get_shape())

        return conv

def fully_connect(input_, output_size, scope=None, stddev=0.02, bias_start=0.0, with_w=False):
  shape = input_.get_shape().as_list()
  with tf.variable_scope(scope or "Linear"):

    matrix = tf.get_variable("Matrix", [shape[1], output_size], tf.float32,
                 tf.random_normal_initializer(stddev=stddev))
    bias = tf.get_variable("bias", [output_size],
      initializer=tf.constant_initializer(bias_start))

    if with_w:
      return tf.matmul(input_, matrix) + bias, matrix, bias
    else:
      return tf.matmul(input_, matrix) + bias

def batch_normal(input , scope="scope" , reuse=False):
    return batch_norm(input , epsilon=1e-5, decay=0.9 , scale=True, scope=scope, reuse=reuse,
                      updates_collections=None)
