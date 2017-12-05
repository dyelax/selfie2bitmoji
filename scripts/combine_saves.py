import tensorflow as tf
from models.avatar_synth_model import AvatarSynthModel
from models.s2b_model import Selfie2BitmojiModel

class TempArgs:
    def __init__(self):
        self.keep_prob = 1
        self.lr = 1
        self.batch_size = 128

sess = tf.Session()

args = TempArgs()
avsynth = AvatarSynthModel(args)
avsynth_inputs = (tf.zeros(300), tf.zeros((128, 64, 64, 3)))
avsynth._build_graph(avsynth_inputs)

s2b = Selfie2BitmojiModel(args)
s2b_inputs = (tf.zeros((128, 64, 64, 3)), tf.zeros((128, 64, 64, 3)))
s2b._build_graph(s2b_inputs)

sess.run(tf.global_variables_initializer())

saver = tf.train.Saver()
saver.restore(sess, '../save/vae_gan/model.ckpt')
saver.restore(sess, '../save/log/2017-11-29.01:53:29/model-10')

saver.save(sess, '../save/combined')
