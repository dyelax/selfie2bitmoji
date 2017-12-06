import numpy as np
from tensorpack.dataflow import (
    MultiThreadMapData, imgaug, PrefetchDataZMQ,
    RNGDataFlow, BatchData, MapData)
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
                            map_func=lambda dp: [np.load(dp[0]), augmentor.augment(imread(dp[1]))])

    # df = MapData(df, lambda dp: [np.load(dp[0]), augmentor.augment(imread(dp[1]))])
    df = PrefetchDataZMQ(df, nr_proc=num_threads)
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


class S2BBDataFlow(RNGDataFlow):
    """
    Produce images for the Selfie2BitmojiModel from lists of image files for faces and bitmoji.
    """
    def __init__(self, face_dir, bitmoji_dir, shuffle=True):
        """
        :param face_dir: Directory with images of real faces.
        :param bitmoji_dir: Directory with images of bitmoji.
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


def process_s2b_data(df, batch_size, num_threads):
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
                            map_func=lambda dp: [np.load(dp[0]), augmentor.augment(imread(dp[1]))])

    # df = MapData(df, lambda dp: [np.load(dp[0]), augmentor.augment(imread(dp[1]))])
    df = PrefetchDataZMQ(df, nr_proc=num_threads)
    df = BatchData(df, batch_size, remainder=True)

    return df


def s2b_df(dir, batch_size, num_threads):
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

