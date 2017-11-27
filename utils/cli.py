import os
import argparse

from tensorpack.utils.logger import set_logger_dir

from utils.misc import get_dir, date_str

def get_avatar_synth_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir',
                        help='Directory of train data',
                        default='./data/bitmoji/train')
    parser.add_argument('--test_dir',
                        help='Directory of test data',
                        default='./data/bitmoji/test')
    parser.add_argument('--logger_dir',
                        help='Directory to save logs and model checkpoints',
                        default=os.path.join('save', 'log', date_str()))
    parser.add_argument('--model_load_dir',
                        help='Directory from which to load a model checkpoint')
    parser.add_argument('--epochs',
                        help='Number of epochs to train',
                        default=1,
                        type=int)
    parser.add_argument('--batch_size',
                        help='Minibatch size',
                        default=128,
                        type=int)
    parser.add_argument('--lr',
                        help='Learning rate',
                        default=3e-5,
                        type=float)
    parser.add_argument('--keep_prob',
                        help='The keep probability for dropout (always 1 for testing)',
                        default=0.5,
                        type=float)
    parser.add_argument('--gpu',
                        help='Comma separated list of GPU(s) to use.')

    args = parser.parse_args()

    if args.gpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

    set_logger_dir(args.logger_dir)

    return args