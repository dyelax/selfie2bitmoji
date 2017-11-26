import os
import argparse

from utils.misc import get_dir

def get_avatar_synth_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir',
                        help='Directory of train data',
                        default='./data/bitmoji/train')
    parser.add_argument('--test_dir',
                        help='Directory of test data',
                        default='./data/bitmoji/test')
    parser.add_argument('--model_save_dir',
                        help='Directory to save model checkpoints',
                        default='./save/models/')
    parser.add_argument('--model_load_dir',
                        help='Directory from which to load a model checkpoint')
    parser.add_argument('--epochs',
                        help='Number of epochs to train',
                        default=1)
    parser.add_argument('--lr',
                        help='Learning rate',
                        default=3e-5)
    parser.add_argument('--keep_prob',
                        help='The keep probability for dropout (always 1 for testing)',
                        default=0.5)
    parser.add_argument('--gpu', help='Comma separated list of GPU(s) to use.')

    args = parser.parse_args()

    if args.gpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

    get_dir(args.model_save_dir)

    return args