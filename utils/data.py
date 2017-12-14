import numpy as np
from tensorpack.dataflow import (
    MultiThreadMapData, imgaug, PrefetchDataZMQ,
    RNGDataFlow, BatchData, MapData)
from imageio import imread
from glob import glob
from os.path import join, exists


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
        self.face_paths = glob(join(face_dir, '*.jpg'))
        self.bitmoji_paths = glob(join(bitmoji_dir, '*.png'))
        self.shuffle = shuffle

        assert len(self.face_paths) > 0, 'No .jpg files in face dir %s.' % face_dir
        assert len(self.bitmoji_paths) > 0, 'No .png files in bitmoji dir %s.' % bitmoji_dir

    def size(self):
        return min(len(self.face_paths), len(self.bitmoji_paths))

    def get_data(self):
        if self.shuffle:
            self.rng.shuffle(self.bitmoji_paths)
            self.rng.shuffle(self.face_paths)

        for i in xrange(self.size()):
            face_path = self.face_paths[i]
            bitmoji_path = self.bitmoji_paths[i]

            yield [face_path, bitmoji_path]


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

    def get_imgs(dp):
        """
        :param dp: A datapoint tuple, (path_to_face.jpg, path_to_bitmoji.jpg)
        """
        face_img = augmentor.augment(imread(dp[0]))
        bitmoji_img = augmentor.augment(imread(dp[1]))
        if len(face_img.shape) == 2: face_img = np.stack([face_img] * 3, axis=-1)
        if len(bitmoji_img.shape) == 2: bitmoji_img = np.stack([bitmoji_img] * 3, axis=-1)

        return [face_img, bitmoji_img]

    df = MultiThreadMapData(df, nr_thread=num_threads, map_func=get_imgs, buffer_size=min(df.size(), 200))
    df = PrefetchDataZMQ(df, nr_proc=num_threads)

    # TODO: switch back to remainder=True when s2b input batch size switched back to None
    df = BatchData(df, batch_size, remainder=False)
    # df = BatchData(df, batch_size, remainder=True)

    return df


def s2b_df(face_dir, bitmoji_dir, batch_size, num_threads):
    """
    Get data for training and evaluating the AvatarSynthModel.

    :param face_dir: Directory with images of real faces.
    :param bitmoji_dir: Directory with images of bitmoji.
    :param batch_size: The minibatch size.
    :param num_threads: The number of threads to read and process data.

    :return: A dataflow for parameter to bitmoji data
    """
    df = S2BBDataFlow(face_dir, bitmoji_dir)
    df = process_s2b_data(df, batch_size, num_threads)

    return df

