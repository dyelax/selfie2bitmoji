from os import environ
environ['TENSORPACK_TRAIN_API'] = 'v2'
from tensorpack import logger, QueueInput
from tensorpack.train import (
    TrainConfig, SyncMultiGPUTrainerParameterServer, launch_train_with_config,
    SimpleTrainer, QueueInputTrainer, SyncMultiGPUTrainerReplicated)
from tensorpack.tfutils.sessinit import SaverRestore
from tensorpack import callbacks as cb
from tensorpack.utils.gpu import get_nr_gpu

from models.avatar_synth_model import AvatarSynthModel
from utils.cli import get_s2b_args
from utils.data import s2b_df


def get_config(args, model, num_gpus, num_towers):
    """
    Create the TensorPack Trainer configuration.

    :param args: The cli arguments.
    :param model: The model object to train.
    :param num_gpus: The number of gpus on which to train
    :param num_towers: The number of data parallel towers to create

    :return: A TrainConfig object.
    """
    logger.info("Running on {} towers. Batch size per tower: {}".format(num_towers, args.batch_size))

    df_train = s2b_df(args.train_dir_face, args.train_dir_bitmoji, args.batch_size, args.num_threads)
    df_test = s2b_df(args.test_dir_face, args.test_dir_bitmoji, args.batch_size, args.num_threads)

    def update_lr(epoch, cur_lr):
        """ Approximate exponential decay of the learning rate """
        if args.resume_lr:
            return cur_lr * args.lr_decay
        else:
            return args.lr * args.lr_decay ** epoch

    callbacks = [
        cb.ModelSaver(),
        cb.MinSaver('val-error-top1'),
        cb.HyperParamSetterWithFunc('tower0/LR:0', update_lr),
        cb.MergeAllSummaries(period=args.summary_freq),
    ]
    infs = [cb.ScalarStats(['L_c', 'L_const', 'L_gan_d', 'L_gan_g', 'L_tid', 'L_tv'])]

    if num_gpus > 0:
        callbacks.append(cb.GPUUtilizationTracker())

    if num_towers == 1: # single-GPU inference with queue prefetch
        callbacks.append(cb.InferenceRunner(QueueInput(df_test), infs))
    else: # multi-GPU inference (with mandatory queue prefetch)
        callbacks.append(cb.DataParallelInferenceRunner(df_test, infs, list(range(num_towers))))

    return TrainConfig(
        model=model,
        dataflow=df_train,
        callbacks=callbacks,
        max_epoch=args.epochs,
        nr_tower=num_towers
    )


def run(args):
    num_gpus = get_nr_gpu()
    num_towers = max(num_gpus, 1)

    config = get_config(args, AvatarSynthModel(args), num_gpus, num_towers)

    if args.load_path:
        config.session_init = SaverRestore(args.load_path)

    trainer = SyncMultiGPUTrainerReplicated(num_towers)
    launch_train_with_config(config, trainer)


if __name__ == '__main__':
    run(get_s2b_args())