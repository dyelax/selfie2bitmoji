import numpy as np
from tensorpack.dataflow.base import RNGDataFlow
from tensorpack.dataflow.common import BatchData
from tensorpack.dataflow.prefetch import PrefetchDataZMQ
import cv2
from imageio import imread
from glob import glob
from os.path import join
from os import remove

from models.model_architectures import IMG_DIMS


class AvatarSynthDataFlowNPZ(RNGDataFlow):
    """ Produce parameters and images from a list of .npz files. """
    def __init__(self, dir, dims=None, val_range=(-1, 1), shuffle=True):
        """
        :param dir: The paths of .npz files containing 'parameters' and 'image' arrays.
        :param dims: (h, w) tuple. If given, resize images to these dimensions.
        :param val_range: (min, max) tuple. Rescale images to this range.
        :param shuffle: Shuffle the input order for each epoch.
        """
        paths = glob(join(dir, '*.npz'))
        assert len(paths) > 0, 'No .npz files in dir %s.' % dir
        self.paths = paths
        self.dims = dims
        self.val_range = val_range
        self.shuffle = shuffle

    def size(self):
        return len(self.paths)

    def get_data(self):
        if self.shuffle:
            self.rng.shuffle(self.paths)

        for path in self.paths:
            with np.load(path) as arrs:
                try:
                    params =  arrs['parameters']
                    img = arrs['image'].astype(float)

                    if self.dims is not None:
                        img = cv2.resize(
                            img, self.dims[:-1], interpolation=cv2.INTER_AREA)

                    # Rescale
                    diff = self.val_range[1] - self.val_range[0]
                    img /= (255. / diff)
                    img += self.val_range[0]

                    yield [params, img]

                except KeyError:
                    print ".npz file missing either 'parameters' or 'image' keys."
                    remove(path)

class AvatarSynthDataFlow(RNGDataFlow):
    """
    Produce parameters and images from a list of .npy and .png files.
    """
    def __init__(self, dir, dims=None, val_range=(-1, 1), shuffle=True):
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
        self.dims = dims
        self.val_range = val_range
        self.shuffle = shuffle

    def size(self):
        return len(self.npy_paths)

    def get_data(self):
        if self.shuffle:
            self.rng.shuffle(self.npy_paths)

        for npy_path in self.npy_paths:
            filename = npy_path[:-4]
            img_path = filename + '.png'

            try:
                # params = np.load(npy_path)
                params = np.zeros(300)
                # img = imread(img_path).astype(float)
                img = np.random.random(self.dims)

                # if self.dims is not None:
                #     img = cv2.resize(
                #         img, self.dims[:-1], interpolation=cv2.INTER_AREA)
                #
                # # Rescale
                # diff = self.val_range[1] - self.val_range[0]
                # img /= (255. / diff)
                # img += self.val_range[0]

                yield [params, img]
            except Exception as e:
                print 'get_data failed for filename %s' % filename
                print e

def process_avatar_synth_data(df, batch_size):
    """
    Perform preprocessing for the avatar synth data.

    :param df: An AvatarSynthDataFlow.
    :param batch_size: The minibatch size.

    :return: A dataflow with extra processing steps applied.
    """
    df = BatchData(df, batch_size, remainder=True)
    df = PrefetchDataZMQ(df, 4) # start 4 processes to run the dataflow in parallel

    return df


def avatar_synth_df(dir, batch_size, npz=False):
    """
    Get data for training and evaluating the AvatarSynthModel.

    :param dir: The data directory.
    :param batch_size: The minibatch size.
    :param npz: Whether to load files from packed npz files or unpacked npy and pngs.

    :return: A dataflow for parameter to bitmoji data
    """
    if npz:
        df = AvatarSynthDataFlowNPZ(dir, dims=IMG_DIMS)
    else:
        df = AvatarSynthDataFlow(dir, dims=IMG_DIMS)

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
