FACE_ENCODING_SIZE = 256
BITMOJI_PARAM_SIZE = 300
IMG_DIMS = (64, 64, 3)

# Model "e"
avatar_synth_model = {
    'conv_filters': [BITMOJI_PARAM_SIZE, 512, 512, 256, 128, 64, 3],
    'filter_widths': [4, 4, 4, 4, 4, 4],
    'strides': [2, 2, 2, 2, 2, 2],
    'padding': ['SAME', 'SAME', 'SAME', 'SAME', 'SAME', 'SAME'],
}

# Model "DeepFace"
# face_encoder_model = {
#     'conv_filters': [3, 64, 128, 256, 512, 512, FACE_ENCODING_SIZE],
#     'filter_widths': [4, 4, 4, 4, 4, 4],
#     'strides': [1, 1, 1, 1, 1, 1],
#     'pooling': [2, 2, 2, 2, 2, 2],
#     'padding': ['SAME', 'SAME', 'SAME', 'SAME', 'SAME', 'SAME'],
# }

# Model "g"
generator_model = {
    # Each deconv here is followed by a 1x1 conv with the same filter number
    'conv_filters': [FACE_ENCODING_SIZE, 512, 512, 256, 128, 64, 3],
    'filter_widths': [4, 4, 4, 4, 4, 4],
    'strides': [2, 2, 2, 2, 2, 2],
    'padding': ['SAME', 'SAME', 'SAME', 'SAME', 'SAME', 'SAME'],
}

# Model "d"
discriminator_model = {
    'conv_filters': [3, 64, 128, 256, 512, 512, 1],
    'filter_widths': [4, 4, 4, 4, 4, 4],
    'strides': [2, 2, 2, 2, 2, 2],
    'padding': ['SAME', 'SAME', 'SAME', 'SAME', 'SAME', 'SAME'],
}

# Model "c"
param_encoder_model = {
    'conv_filters': [3, 64, 128, 256, 512, 512, BITMOJI_PARAM_SIZE],
    'filter_widths': [4, 4, 4, 4, 4, 4],
    'strides': [2, 2, 2, 2, 2, 2],
    'padding': ['SAME', 'SAME', 'SAME', 'SAME', 'SAME', 'SAME'],
}