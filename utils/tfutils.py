import tensorflow as tf
import numpy as np


def w(shape, stddev=0.01):
    """
    @return A weight layer with the given shape and standard deviation. Initialized with a
            truncated normal distribution.
    """
    return tf.Variable(tf.truncated_normal(shape, stddev=stddev))


def b(shape, const=0.1):
    """
    @return A bias layer with the given shape.
    """
    return tf.Variable(tf.constant(const, shape=shape))


def conv_out_shape(in_shape, out_fms, p, k, s):
    """
    Gets the output shape [height, width] for a 2D convolution.
    (Assumes square kernel).

    @param in_shape: The input shape [batch, height, width, channels].
    @param out_fms: The number of feature maps in the output.
    @param p: The padding type (either 'SAME' or 'VALID').
    @param k: The side length of the kernel.
    @param s: The stride.

    @return The shape of the output after convolution.
    """
    # convert p to a number
    if p == 'SAME':
        p = k // 2
    elif p == 'VALID':
        p = 0
    else:
        raise ValueError('p must be "SAME" or "VALID".')

    h, w = in_shape[1:3]
    return [in_shape[0],
            int(((h + (2 * p) - k) / s) + 1),
            int(((w + (2 * p) - k) / s) + 1),
            out_fms]


def narrow_truncated_normal_initializer(shape, dtype=None, partition_info=None):
    """
    A version of tf.truncated_normal_initializer with a stddev of 0.05, for use
    with tf.layers.
    """
    initializer = tf.truncated_normal_initializer(stddev=0.35)
    return initializer(shape, dtype=dtype, partition_info=partition_info)


def softmax(input, temperature=1):
    """
    Softmax function with a temperature parameter.

    :param input: The tensor to be softmaxed.
    :param temperature: The temperature of the softmax function. Lower temp
                        pushes the max closer to 1. Higher temps make values
                        more uniform.

    :return: The tensor after softmaxing with the given temperature.
    """
    return

def log10(t):
    """
    Calculates the base-10 log of each element in t.

    @param t: The tensor from which to calculate the base-10 log.

    @return: A tensor with the base-10 log of each element in t.
    """

    numerator = tf.log(t)
    denominator = tf.log(tf.constant(10, dtype=numerator.dtype))
    return numerator / denominator


def batch_pad_to_bounding_box(images, offset_height, offset_width,
                              target_height, target_width):
    """
    Zero-pads a batch of images with the given dimensions.

    @param images: 4-D tensor with shape [batch_size, height, width, channels]
    @param offset_height: Number of rows of zeros to add on top.
    @param offset_width: Number of columns of zeros to add on the left.
    @param target_height: Height of output images.
    @param target_width: Width of output images.

    @return: The batch of images, all zero-padded with the specified dimensions.
    """
    batch_size, height, width, channels = tf.Session().run(tf.shape(images))

    if not offset_height >= 0:
        raise ValueError('offset_height must be >= 0')
    if not offset_width >= 0:
        raise ValueError('offset_width must be >= 0')
    if not target_height >= height + offset_height:
        raise ValueError('target_height must be >= height + offset_height')
    if not target_width >= width + offset_width:
        raise ValueError('target_width must be >= width + offset_width')

    num_tpad = offset_height
    num_lpad = offset_width
    num_bpad = target_height - (height + offset_height)
    num_rpad = target_width - (width + offset_width)

    tpad = np.zeros([batch_size, num_tpad, width, channels])
    bpad = np.zeros([batch_size, num_bpad, width, channels])
    lpad = np.zeros([batch_size, target_height, num_lpad, channels])
    rpad = np.zeros([batch_size, target_height, num_rpad, channels])

    padded = images
    if num_tpad > 0 and num_bpad > 0:
        padded = tf.concat(1, [tpad, padded, bpad])
    elif num_tpad > 0:
        padded = tf.concat(1, [tpad, padded])
    elif num_bpad > 0:
        padded = tf.concat(1, [padded, bpad])
    if num_lpad > 0 and num_rpad > 0:
        padded = tf.concat(2, [lpad, padded, rpad])
    elif num_lpad > 0:
        padded = tf.concat(2, [lpad, padded])
    elif num_rpad > 0:
        padded = tf.concat(2, [padded, rpad])

    return padded


def batch_crop_to_bounding_box(images, offset_height, offset_width,
                               target_height, target_width):
    """
    Crops a batch of images to the given dimensions.

    @param images: 4-D tensor with shape [batch, height, width, channels]
    @param offset_height: Vertical coordinate of the top-left corner of the result in the input.
    @param offset_width: Horizontal coordinate of the top-left corner of the result in the input.
    @param target_height: Height of output images.
    @param target_width: Width of output images.

    @return: The batch of images, all cropped the specified dimensions.
    """
    batch_size, height, width, channels = tf.Session().run(tf.shape(images))

    if not offset_height >= 0:
        raise ValueError('offset_height must be >= 0')
    if not offset_width >= 0:
        raise ValueError('offset_width must be >= 0')
    if not target_height + offset_height <= height:
        raise ValueError('target_height + offset_height must be <= height')
    if not target_width <= width - offset_width:
        raise ValueError('target_width + offset_width must be <= width')

    top = offset_height
    bottom = target_height + offset_height
    left = offset_width
    right = target_width + offset_width

    return images[:, top:bottom, left:right, :]


def leaky_relu(tensor, leak=0.2):
    """
    Computes a leaky ReLU with the given alpha.

    @param tensor: The input tensor.
    @param leak: The slope of the relu on negative inputs.
    @return: The tensor after applying the leaky ReLU.
    """
    return tf.maximum(leak * tensor, tensor)


##
# I/O
##

def read_img(img_path):
    """
    Reads an image from disk.

    :param img_path: An example image path from the input queue.

    :return: An example image.
    """
    file_contents = tf.read_file(img_path)
    image_example = tf.image.decode_image(file_contents)

    return image_example


def preprocess(img, in_shape, out_shape=None):
    """
    Preprocess an image Tensor.

    :param img: An example image from the queue.
    :param in_shape: The shape of the image (height, width, channels) on file.
    :param out_shape: The shape to which the images should be resized
                      (height, width). Default: None - no resizing.

    :return:
    """
    img_processed = img

    # Resize
    img_processed.set_shape(in_shape)
    if out_shape is not None:
        img_processed = tf.image.resize_images(img_processed, out_shape)

    # Normalize values
    img_processed = tf.image.per_image_standardization(img_processed)

    return img_processed


def img_input_queue(img_paths,
                    in_shape,
                    out_shape=None,
                    labels=None,
                    batch_size=1,
                    num_epochs=None):
    """
    :param img_paths: A list of the relative path to each image file.
    :param in_shape: The shape of the images (height, width, channels) on file.
    :param out_shape: The shape to which the images should be resized
                      (height, width). Default: None - no resizing.
    :param labels: A list of the label for each file in filenames.
    :param batch_size: The size of the minibatch to return.
    :param num_epochs: The number of epochs to generate. If None, generates
                       indefinitely.

    :return: A tuple, (imgs, labels), of input Tensors. If no labels provided,
             ignore the output labels.
    """
    if labels is None:
        labels = np.empty(len(img_paths))  # Create fake labels.

    input_queue = tf.train.slice_input_producer(
        [img_paths, labels], num_epochs=num_epochs, shuffle=True)

    img = read_img(input_queue[0])
    label = input_queue[1]

    img_processed = preprocess(img, in_shape, out_shape=out_shape)

    # min_after_dequeue defines how big a buffer we will randomly sample
    #   from -- bigger means better shuffling but slower start up and more
    #   memory used.
    # capacity must be larger than min_after_dequeue and the amount larger
    #   determines the maximum we will prefetch.  Recommendation:
    #   min_after_dequeue + (num_threads + a small safety margin) * batch_size
    min_after_dequeue = 10000
    capacity = min_after_dequeue + 3 * batch_size
    img_batch, label_batch = tf.train.shuffle_batch(
        [img_processed, label], batch_size=batch_size, capacity=capacity,
        min_after_dequeue=min_after_dequeue)

    return img_batch, label_batch