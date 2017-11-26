import tensorflow as tf

from models.avatar_synth_model import AvatarSynthModel
from utils.cli import get_avatar_synth_args

def run(args):
    model = AvatarSynthModel(args)

    pass

if __name__ == '__main__':
    run(get_avatar_synth_args())