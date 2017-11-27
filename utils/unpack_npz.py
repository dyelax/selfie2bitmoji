import numpy as np
import argparse
import multiprocessing
from glob import glob
from os.path import join
from os import remove
from imageio import imwrite


def unpack_npz(path):
    """
    Reads a .npz file containing 'parameters', 'image' and 'url' arrays and
    re-writes as a .npy file for parameters, a .png file for image and a .txt
    file for url.
    """
    with np.load(path) as arrs:
        filename = path[:-4]
        try:
            params = arrs['parameters']
            img = arrs['image']
            url = arrs['url']

            imwrite(filename + '.png', img)
            np.save(filename + '.npy', params)
            with open(filename + '-url.txt', 'w') as f:
                f.write(url)

            remove(path)
        except KeyError:
            print ".npz file missing either 'parameters' or 'image' keys."
            remove(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir',
                        help='The directory to unpack')
    parser.add_argument('--processes',
                        help='The number of processes to use to parallelize '
                             'the unpacking',
                        default=8,
                        type=int)
    args = parser.parse_args()

    paths = glob(join(args.dir, '*.npz'))

    pool = multiprocessing.Pool(processes=args.processes)
    pool_outputs = pool.map(unpack_npz, paths)
    pool.close()
    pool.join()

    print 'Done!'