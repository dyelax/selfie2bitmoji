NUM_PARAMS = 300
IMG_DIMS = (64, 64, 3)

# Model "e"
avatar_synth_model = {
    'conv_filters': [NUM_PARAMS, 512, 512, 256, 128, 64, 3],
    'filter_widths': [4, 4, 4, 4, 4, 4],
    'strides': [2, 2, 2, 2, 2, 2],
    'padding': ['SAME', 'SAME', 'SAME', 'SAME', 'SAME', 'SAME'],
}