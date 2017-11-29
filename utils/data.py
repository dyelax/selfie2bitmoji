import numpy as np
from tensorpack.dataflow import (
    MultiThreadMapData, imgaug, PrefetchDataZMQ,
    RNGDataFlow, BatchData)
import cv2
from imageio import imread
from glob import glob
from os.path import join, exists
from os import remove

from models.model_architectures import IMG_DIMS


class AvatarSynthDataFlow(RNGDataFlow):
    """
    Produce parameters and images from a list of .npy and .png files.
    """
    def __init__(self, dir, shuffle=True):
        """
        :param dir: Directory with .npy and .png files containing parameters and
                    images. Paired params and images should have the same
                    filename (except extension).
        :param dims: (h, w) tuple. If given, resize images to these dimensions.
        :param val_range: (min, max) tuple. Rescale images to this range.
        :param shuffle: Shuffle the input order for each epoch.
        """
        npy_paths = glob(join(dir, '*.npy'))
        assert len(npy_paths) > 0, 'No .npy files in dir %s.' % dir
        self.npy_paths = npy_paths
        self.shuffle = shuffle

    def size(self):
        return len(self.npy_paths)

    def get_data(self):
        if self.shuffle:
            self.rng.shuffle(self.npy_paths)

        for npy_path in self.npy_paths:
            img_path = npy_path[:-4] + '.png'

            if exists(img_path):
                yield [npy_path, img_path]
            else:
                print 'Image does not exist: %s' % img_path


def process_avatar_synth_data(df, batch_size):
    """
    Perform preprocessing for the avatar synth data.

    :param df: An AvatarSynthDataFlow.
    :param batch_size: The minibatch size.

    :return: A dataflow with extra processing steps applied.
    """
    augmentor = imgaug.AugmentorList([
        imgaug.Resize(IMG_DIMS[:-1], interp=cv2.INTER_AREA),
        imgaug.MinMaxNormalize(min=-1, max=1)
    ])

    df = MultiThreadMapData(df, nr_thread=4,
                            map_func=lambda dp: [np.load(dp[0]), augmentor.augment(imread(dp[1]))],
                            buffer_size=min(1000, df.size()))
    df = PrefetchDataZMQ(df, nr_proc=1)
    df = BatchData(df, batch_size, remainder=True)

    return df


def avatar_synth_df(dir, batch_size):
    """
    Get data for training and evaluating the AvatarSynthModel.

    :param dir: The data directory.
    :param batch_size: The minibatch size.

    :return: A dataflow for parameter to bitmoji data
    """
    df = AvatarSynthDataFlow(dir)
    df = process_avatar_synth_data(df, batch_size)

    return df


# def get_avatar_synth_epoch(train_dir, test_dir, batch_size):
#     """
#     Get data for training and evaluating the AvatarSynthModel.
#
#     :param train_dir: The train data directory.
#     :param test_dir: The test data directory.
#     :param batch_size: The minibatch size.
#
#     :return: A tuple (train_generator, test_generator). Generators for train and
#              test batches, respectively.
#     """
#     train_df = AvatarSynthDataFlow(train_dir, dims=IMG_DIMS, shuffle=True)
#     test_df = AvatarSynthDataFlow(test_dir, dims=IMG_DIMS, shuffle=True)
#
#     train_df = process_avatar_synth_data(train_df, batch_size)
#     test_df = process_avatar_synth_data(test_df, batch_size)
#
#     return train_df.get_data(), test_df.get_data()
