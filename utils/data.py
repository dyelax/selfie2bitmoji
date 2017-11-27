import numpy as np
from tensorpack.dataflow.base import RNGDataFlow
from tensorpack.dataflow.common import BatchData
from tensorpack.dataflow.prefetch import PrefetchDataZMQ
# from skimage.transform import resize
from cv2 import resize
from glob import glob
from os.path import join

from models.model_architectures import IMG_DIMS


class AvatarSynthDataFlow(RNGDataFlow):
    """ Produce parameters and images from a list of .npz files. """
    def __init__(self, dir, dims=None, shuffle=False):
        """
        :param dir: The paths of .npz files containing 'parameters' and 'image' arrays.
        :param dims: (h, w) tuple. If given, resize images to these dimensions.
        :param shuffle: Shuffle the input order for each epoch.
        """
        paths = glob(join(dir, '*.npz'))
        assert len(paths) > 0, 'No .npz files in dir %s.' % dir
        self.paths = paths
        self.dims = dims
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
                    img = arrs['image']

                    if self.dims is not None:
                        img = resize(img, self.dims)

                    yield [params, img]

                except KeyError:
                    print ".npz file missing either 'parameters' or 'image' keys."


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


def avatar_synth_df(dir, batch_size):
    """
    Get data for training and evaluating the AvatarSynthModel.

    :param dir: The data directory.
    :param batch_size: The minibatch size.

    :return: A dataflow for parameter to bitmoji data
    """
    df = AvatarSynthDataFlow(dir, dims=IMG_DIMS, shuffle=True)
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
