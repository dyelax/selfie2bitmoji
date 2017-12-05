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
        :param shuffle: Shuffle the input order for each epoch.
        """
        png_paths = glob(join(dir, '*.png'))
        assert len(png_paths) > 0, 'No .png files in dir %s.' % dir
        self.png_paths = png_paths
        self.shuffle = shuffle

    def size(self):
        return len(self.png_paths)

    def get_data(self):
        if self.shuffle:
            self.rng.shuffle(self.png_paths)

        for png_path in self.png_paths:
            npy_path = png_path.rpartition('.')[0] + '.npy'

            if exists(npy_path):
                yield [npy_path, png_path]
            else:
                print 'File not found: %s' % npy_path


def process_avatar_synth_data(df, batch_size, num_threads):
    """
    Perform preprocessing for the avatar synth data.

    :param df: An AvatarSynthDataFlow.
    :param batch_size: The minibatch size.
    :param num_threads: The number of threads to read and process data.

    :return: A dataflow with extra processing steps applied.
    """
    augmentor = imgaug.AugmentorList([
        imgaug.MinMaxNormalize(min=-1, max=1)
    ])

    df = MultiThreadMapData(df, nr_thread=num_threads,
                            map_func=lambda dp: [np.load(dp[0]), augmentor.augment(imread(dp[1]))],
                            buffer_size=min(1000, df.size()))
    df = PrefetchDataZMQ(df, nr_proc=1)
    df = BatchData(df, batch_size, remainder=True)

    return df


def avatar_synth_df(dir, batch_size, num_threads):
    """
    Get data for training and evaluating the AvatarSynthModel.

    :param dir: The data directory.
    :param batch_size: The minibatch size.
    :param num_threads: The number of threads to read and process data.

    :return: A dataflow for parameter to bitmoji data
    """
    df = AvatarSynthDataFlow(dir)
    df = process_avatar_synth_data(df, batch_size, num_threads)

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
