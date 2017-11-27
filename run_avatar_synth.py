from os import environ
environ['TENSORPACK_TRAIN_API'] = 'v2'
from tensorpack import logger, QueueInput
from tensorpack.train import (
    TrainConfig, SyncMultiGPUTrainerParameterServer, launch_train_with_config)
from tensorpack import callbacks as cb
from tensorpack.utils.gpu import get_nr_gpu
from numpy import ceil

from models.avatar_synth_model import AvatarSynthModel
from utils.cli import get_avatar_synth_args
from utils.data import avatar_synth_df


def get_config(args, model, num_gpus):
    """
    Create the TensorPack Trainer configuration.

    :param args: The cli arguments.
    :param model: The model object to train.
    :param num_gpus: The number of gpus on which to train

    :return: A TrainConfig object.
    """
    num_towers = max(num_gpus, 1)

    logger.info("Running on {} towers. Batch size per tower: {}".format(
        num_towers, args.batch_size))

    df_train = avatar_synth_df(args.train_dir, args.batch_size)
    df_test = avatar_synth_df(args.test_dir, args.batch_size)

    callbacks = [
        cb.ModelSaver(),
        cb.MinSaver('val-error-top1'),
        cb.HumanHyperParamSetter('tower0/Avatar_Synth/LR:0'),
        cb.MergeAllSummaries(period=args.summary_freq)
    ]
    infs = [cb.ScalarStats('Avatar_Synth/Cost')]

    # if num_gpus > 0:
    #     callbacks.append(cb.GPUUtilizationTracker())

    if num_towers == 1:
        # single-GPU inference with queue prefetch
        callbacks.append(cb.InferenceRunner(QueueInput(df_test), infs))
    else:
        # multi-GPU inference (with mandatory queue prefetch)
        callbacks.append(cb.DataParallelInferenceRunner(
            df_test, infs, list(range(num_towers))))

    return TrainConfig(
        model=model,
        dataflow=df_train,
        callbacks=callbacks,
        # steps_per_epoch=ceil(df_train.size() / args.batch_size),
        max_epoch=args.epochs,
        nr_tower=num_towers
    )

def run(args):
    num_gpus = get_nr_gpu()
    config = get_config(args, AvatarSynthModel(args), num_gpus)
    trainer = SyncMultiGPUTrainerParameterServer(max(num_gpus, 1))
    launch_train_with_config(config, trainer)

    pass

if __name__ == '__main__':
    run(get_avatar_synth_args())