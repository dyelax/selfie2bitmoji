import tensorflow as tf

def narrow_truncated_normal_initializer(shape, dtype=None, partition_info=None):
    """
    A version of tf.truncated_normal_initializer with a stddev of 0.1, for use
    with tf.layers.
    """
    initializer = tf.truncated_normal_initializer(stddev=0.05)
    return initializer(shape, dtype=dtype, partition_info=partition_info)