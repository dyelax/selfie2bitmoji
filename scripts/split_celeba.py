from glob import glob
import os
import shutil
import numpy as np
from utils.misc import get_dir

train_dir = '../data/face/train/'
test_dir = '../data/face/test/'

test_percent = 0.2

paths = glob(os.path.join(train_dir, '*.jpg'))
np.random.shuffle(paths)

test_paths = paths[:np.floor(test_percent * len(paths))]
for path in test_paths:
    shutil.move(path, test_dir)
