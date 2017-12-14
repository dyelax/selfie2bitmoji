import tensorflow as tf
from models.s2b_model import Selfie2BitmojiModel

VAEGAN_PATH = '../save/vaegan-encoder/model'
AVSYNTH_PATH = '../save/avsynth/model'


class TempArgs:
    def __init__(self):
        self.keep_prob = 1
        self.lr = 1
        self.batch_size = 128

sess = tf.Session()

args = TempArgs()

s2b = Selfie2BitmojiModel(args)
s2b_inputs = (tf.zeros((128, 64, 64, 3)), tf.zeros((128, 64, 64, 3)))
s2b._build_graph(s2b_inputs)

sess.run(tf.global_variables_initializer())
sess.run(tf.local_variables_initializer())

# print tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Face_Encoder')

vaegan_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Face_Encoder')
avsynth_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Avatar_Synth')

saver_vaegan = tf.train.Saver(var_list=vaegan_vars)
saver_avsynth = tf.train.Saver(var_list=avsynth_vars)
saver_vaegan.restore(sess, '../save/vaegan-encoder/model')
saver_avsynth.restore(sess, '../save/avsynth/model-1388913')

saver_all = tf.train.Saver(var_list=vaegan_vars + avsynth_vars)
saver_all.save(sess, '../save/s2b/default/model')
