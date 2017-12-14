# From https://github.com/zhangqianhui/vae-gan-tensorflow

import tensorflow as tf
from tensorflow.contrib.layers.python.layers import batch_norm


def conv2d(input_, output_dim,
           k_h=5, k_w=5, d_h=2, d_w=2, stddev=0.02,
           name="conv2d"):
    with tf.variable_scope(name):
        w = tf.get_variable('w', [k_h, k_w, input_.get_shape()[-1], output_dim],
                            initializer=tf.truncated_normal_initializer(stddev=stddev),
                            trainable=False)
        conv = tf.nn.conv2d(input_, w, strides=[1, d_h, d_w, 1], padding='SAME')
        biases = tf.get_variable('biases', [output_dim], initializer=tf.constant_initializer(0.0),
                                 trainable=False)
        conv = tf.reshape(tf.nn.bias_add(conv, biases), conv.get_shape())

        return conv


def fully_connect(input_, output_size, scope=None, stddev=0.02, bias_start=0.0, with_w=False):
    shape = input_.get_shape().as_list()
    with tf.variable_scope(scope or "Linear"):

        matrix = tf.get_variable("Matrix", [shape[1], output_size], tf.float32,
                                 tf.random_normal_initializer(stddev=stddev),
                                 trainable=False)
        bias = tf.get_variable("bias", [output_size],
                               initializer=tf.constant_initializer(bias_start),
                               trainable=False)

        if with_w:
            return tf.matmul(input_, matrix) + bias, matrix, bias
        else:
            return tf.matmul(input_, matrix) + bias


def batch_normal(input, scope="scope", reuse=False):
    return batch_norm(input, epsilon=1e-5, decay=0.9, scale=True, scope=scope, reuse=reuse,
                      updates_collections=None, trainable=False)
