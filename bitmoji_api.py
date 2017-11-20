"""
Bitmoji API

Bitstrips style
https://render.bitstrips.com/render/10215854/231475438_7-s1-v3.png?cropped=%22head%22

Bitmoji style (female)
https://render.bitstrips.com//render/6688424/122369401_1_s4-v1.png

Bitmoji style (male)
https://render.bitstrips.com//render/6688424/122369389_1_s4-v1.png
"""

###
# Female Options:
###

# &sex= (mostly affects head width)
# 1 – Male, (wider)
# 2 – Female (narrower)
sex_options = [1, 2]

# &proportion= (face shape + eye separation)
proportion_options = range(9) # int 0-8. No semantic mapping

# &colours=%7B<color_options>%7D (list of color options)

# %22ffcc99%22: (colours.skin)
skin_color_options = [
    16443344,
    15257000,
    11897407,
    8080170,
    16764057,
    14664067,
    12159077,
    6963494,
    16691590,
    13544297,
    11170379,
    6240025,
    12684916,
    13280865,
    9657655,
    4732712,
    12624259,
    13151395,
    14926519,
    16772846,
    14363906,
    15304777,
    16240700,
    1416510,
    898981,
    9545463,
    12881912,
]



# %22ff9866%22: (colours.lips)
lip_color_options = [
    # Natural lip colors:
    16041410,
    14530688,
    7549993,
    16750694,
    14199915,
    11558746,
    6173474,
    14128499,
    13076077,
    10506048,
    5908506,
    11824997,
    11242835,
    8997431,
    4138525,
    11832960,
    12554125,
    14397092,
    16766421,
    4732712,
    14970915,
    15515147,
    1211954,
    827023,
    7572978,
    11166195,

    # Lipstick colors:
]



###
# Male Options:
###