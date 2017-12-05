from glob import glob
import os

png_paths = glob('../data/bitmoji/*/*.png')
npy_paths = glob('../data/bitmoji/*/*.npy')

png_set = set([os.path.splitext(p)[0] for p in png_paths])
npy_set = set([os.path.splitext(p)[0] for p in npy_paths])

sym_diff = png_set ^ npy_set

print len(sym_diff)
print sym_diff