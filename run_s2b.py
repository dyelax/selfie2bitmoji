from os import environ
environ['TENSORPACK_TRAIN_API'] = 'v2'
from tensorpack import logger, QueueInput
from tensorpack.tfutils.sessinit import SaverRestore
from tensorpack import callbacks as cb
from tensorpack.utils.gpu import get_nr_gpu

from models.s2b_model import Selfie2BitmojiModel, S2BTrainer
from utils.cli import get_s2b_args
from utils.data import s2b_df


def run(args):
    df_train = s2b_df(args.train_dir_face, args.train_dir_bitmoji, args.batch_size,
                      args.num_threads)
    df_test = s2b_df(args.test_dir_face, args.test_dir_bitmoji, args.batch_size, args.num_threads)

    def update_lr(epoch, cur_lr):
        """ Approximate exponential decay of the learning rate """
        if args.resume_lr:
            return cur_lr * args.decay
        else:
            return args.lr * args.decay ** epoch

    callbacks = [
        cb.ModelSaver(),
        cb.MinSaver('val-error-top1'),
        cb.HyperParamSetterWithFunc('LR', update_lr),
        cb.HyperParamSetterWithFunc('Instance_Noise_Stddev', lambda epoch, stddev: stddev * args.decay),
        # cb.HyperParamSetterWithFunc('D_Uncertainty_Threshold', lambda epoch, threshold: threshold * args.decay),
        cb.MergeAllSummaries(period=args.summary_freq),
    ]
    infs = [cb.ScalarStats(['L_c', 'L_const', 'L_gan_d', 'L_gan_g', 'L_tid', 'L_tv'])]

    if get_nr_gpu() > 0:
        callbacks.append(cb.GPUUtilizationTracker())

    callbacks.append(cb.InferenceRunner(QueueInput(df_test), infs))

    S2BTrainer(QueueInput(df_train), Selfie2BitmojiModel(args)).train_with_defaults(
        callbacks=callbacks,
        max_epoch=args.epochs,
        steps_per_epoch=df_train.size(),
        session_init=SaverRestore(args.load_path)
    )

if __name__ == '__main__':
    run(get_s2b_args())