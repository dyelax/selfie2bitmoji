import tensorflow as tf
from models.avatar_synth_model import AvatarSynthModel
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

saver_vaegan = tf.train.Saver(var_list=tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Face_Encoder'))
saver_avsynth = tf.train.Saver(var_list=tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Avatar_Synth'))
saver_vaegan.restore(sess, '../save/vaegan-encoder/model')
saver_avsynth.restore(sess, '../save/avsynth/model-1388913')

vaegan_vars = [var_name for var_name, _ in tf.contrib.framework.list_variables(VAEGAN_PATH)]
# print vaegan_vars

saver_all = tf.train.Saver()
saver_all.save(sess, '../save/s2b/model')
