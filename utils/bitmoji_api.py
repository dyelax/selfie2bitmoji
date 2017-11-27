"""
Bitmoji API (11/20/17)

Bitstrips style
https://render.bitstrips.com/render/10215854/231475438_7-s1-v3.png?cropped="head"

Bitmoji style (female)
https://render.bitstrips.com//render/6688424/122369401_1_s4-v1.png

Bitmoji style (male)
https://render.bitstrips.com//render/6688424/122369389_1_s4-v1.png
"""

NONE_TOKEN = ''

gender_base_urls = [
    'https://render.bitstrips.com//render/6688424/122369389_1_s4-v1.png?', # Male
    'https://render.bitstrips.com//render/6688424/122369389_1_s4-v1.png?'  # Female
]

# &sex= (mostly affects head width)
# 1 - Male, (wider)
# 2 - Female (narrower)
genders = [
    'sex=1',
    'sex=2',
]

###
# Non-gendered:
###

# &proportion= (face shape + eye separation)
proportions = [
    'proportion=0',
    'proportion=1',
    'proportion=2',
    'proportion=3',
    'proportion=4',
    'proportion=5',
    'proportion=6',
    'proportion=7',
    'proportion=8',
]

# &colours={<colors>} (list of color options)

# "ffcc99": (colours.skin)
skin_colors = [
    '"ffcc99":16443344',
    '"ffcc99":15257000',
    '"ffcc99":11897407',
    '"ffcc99":8080170',
    '"ffcc99":16764057',
    '"ffcc99":14664067',
    '"ffcc99":12159077',
    '"ffcc99":6963494',
    '"ffcc99":16691590',
    '"ffcc99":13544297',
    '"ffcc99":11170379',
    '"ffcc99":6240025',
    '"ffcc99":12684916',
    '"ffcc99":13280865',
    '"ffcc99":9657655',
    '"ffcc99":4732712',
    '"ffcc99":12624259',
    '"ffcc99":13151395',
    '"ffcc99":14926519',
    '"ffcc99":16772846',

    # Unrealistic colors:
    # '"ffcc99":14363906',
    # '"ffcc99":15304777',
    # '"ffcc99":16240700',
    # '"ffcc99":1416510',
    # '"ffcc99":898981',
    # '"ffcc99":9545463',
    # '"ffcc99":12881912',
]

# "926715": (colours.hair)
hair_colors = [
    '"926715":8672042',
    '"926715":6632737',
    '"926715":4795690',
    '"926715":2566954',
    '"926715":16750848',
    '"926715":14178816',
    '"926715":11093553',
    '"926715":10027008',
    '"926715":16250871',
    '"926715":13618371',
    '"926715":10725013',
    '"926715":8291180',
    '"926715":16777164',
    '"926715":16776960',

    # Unrealistic colors:
    # '"926715":10079436',
    # '"926715":16751052',
    # '"926715":13421823',
    # '"926715":65280',
    # '"926715":13382451',
    # '"926715":3381759',
    # '"926715":39270',
    # '"926715":13369497',
    # '"926715":26367',
    # '"926715":14797722',
    # '"926715":12360500',
    # '"926715":10910758',
    # '"926715":5587258',
]

# "ff9866": (colours.lips)
lip_colors = [
    # Natural lip colors:
    '"ff9866":16041410',
    '"ff9866":14530688',
    '"ff9866":7549993',
    '"ff9866":16750694',
    '"ff9866":14199915',
    '"ff9866":11558746',
    '"ff9866":6173474',
    '"ff9866":14128499',
    '"ff9866":13076077',
    '"ff9866":10506048',
    '"ff9866":5908506',
    '"ff9866":11824997',
    '"ff9866":11242835',
    '"ff9866":8997431',
    '"ff9866":4138525',
    '"ff9866":11832960',
    '"ff9866":12554125',
    '"ff9866":14397092',
    '"ff9866":16766421',
    '"ff9866":4732712',
    '"ff9866":14970915',
    '"ff9866":15515147',
    '"ff9866":1211954',
    '"ff9866":827023',
    '"ff9866":7572978',
    '"ff9866":11166195',

    # Lipstick colors:
    '"ff9866":13442115',
    '"ff9866":15354474',
    '"ff9866":14373436',
    '"ff9866":13334634',
    '"ff9866":10361428',
    '"ff9866":15683906',
    '"ff9866":10904915',
    '"ff9866":7671346',
    '"ff9866":4855067',
    '"ff9866":3103091',
    '"ff9866":2517439',
    '"ff9866":10667506',
    '"ff9866":7110076',
    '"ff9866":15918037',
    '"ff9866":2236962',
    '"ff9866":13421772',
    '"ff9866":6710886',
]

# "4f453e": (colours.brows)
brow_colors = [
    '"4f453e":6700322',
    '"4f453e":5844766',
    '"4f453e":3218460',
    '"4f453e":1579802',
    '"4f453e":11569973',
    '"4f453e":9663272',
    '"4f453e":7162651',
    '"4f453e":3615014',
    '"4f453e":14386178',
    '"4f453e":11618049',
    '"4f453e":8203556',
    '"4f453e":7733505',
    '"4f453e":15132390',
    '"4f453e":7696224',
    '"4f453e":9343614',
    '"4f453e":3553071',
    '"4f453e":13816322',

    # Unrealistic colors:
    # '"4f453e":7518392',
    # '"4f453e":16672691',
    # '"4f453e":11250942',
    # '"4f453e":248322',
    # '"4f453e":11152171',
    # '"4f453e":164093',
    # '"4f453e":95815',
    # '"4f453e":10486146',
    # '"4f453e":152522',
]

# "36a7e9": (colours.eyes)
eye_colors = [
    '"36a7e9":5977116',
    '"36a7e9":8404014',
    '"36a7e9":11174994',
    '"36a7e9":3763125',
    '"36a7e9":6064564',
    '"36a7e9":7693930',
    '"36a7e9":2384950',
    '"36a7e9":5474915',
    '"36a7e9":1118481',
    '"36a7e9":6639732',
    '"36a7e9":5793385',
    '"36a7e9":5789030',
    '"36a7e9":4611439',
    '"36a7e9":3307665',
    '"36a7e9":7448799',
    '"36a7e9":11767108',
    '"36a7e9":11119494',
    '"36a7e9":11188685',
]

# "ff9999": (colours.blush) - OPTIONAL
blush_colors = [
    NONE_TOKEN,
    '"ff9999":15972784',
    '"ff9999":16624025',
    '"ff9999":16488850',
    '"ff9999":14391183',
    '"ff9999":13798776',
    '"ff9999":13336701',
    '"ff9999":15310260',
    '"ff9999":13730450',
    '"ff9999":12676987',
    '"ff9999":3103091',
    '"ff9999":2517439',
    '"ff9999":10667506',
    '"ff9999":7110076',
    '"ff9999":15918037',
    '"ff9999":2236962',
    '"ff9999":13421772',
    '"ff9999":6710886',
]

# &pd2={<options>} (list of other parameter options)

# Eye details:
eye_details = [
    '"detail_E_L":"_blank","detail_E_R":"_blank"',
    '"detail_E_L":"detail_E_bm1","detail_E_R":"detail_E_bm1"',
    '"detail_E_L":"detail_E_bm2","detail_E_R":"detail_E_bm2"',
    '"detail_E_L":"detail_E_bm3","detail_E_R":"detail_E_bm3"',
    '"detail_E_L":"detail_E_bm4","detail_E_R":"detail_E_bm4"',
    '"detail_E_L":"detail_E_bm5","detail_E_R":"detail_E_bm5"',
    '"detail_E_L":"detail_E_bm6","detail_E_R":"detail_E_bm6"',
    '"detail_E_L":"detail_E_bm7","detail_E_R":"detail_E_bm7"',
]

# Cheek details:
cheek_details = [
    '"detail_L":"_blank","detail_R":"_blank"',
    '"detail_L":"detail_L_bm1","detail_R":"detail_L_bm1"',
    '"detail_L":"detail_L_bm7","detail_R":"detail_L_bm7"',
    '"detail_L":"detail_L_bm8","detail_R":"detail_L_bm8"',
    '"detail_L":"detail_L_bm9","detail_R":"detail_L_bm9"',
    '"detail_L":"detail_L_bm10","detail_R":"detail_L_bm10"',
    '"detail_L":"detail_L_bm11","detail_R":"detail_L_bm11"',
]

# Face lines:
face_lines = [
    '"detail_T":"_blank"',
    '"detail_T":"detail_T_bm1"',
    '"detail_T":"detail_T_bm2"',
    '"detail_T":"detail_T_bm3"',
    '"detail_T":"detail_T_bm4"',
    '"detail_T":"detail_T_bm5"',
    '"detail_T":"detail_T_bm6"',
    '"detail_T":"detail_T_bm7"',
    '"detail_T":"detail_T_bm8"',
    '"detail_T":"detail_T_bm9"',
    '"detail_T":"detail_T_bm10"',
    '"detail_T":"detail_T_bm11"',
    '"detail_T":"detail_T_bm12"',
    '"detail_T":"detail_T_bm13"',
    '"detail_T":"detail_T_bm14"',
]

# Glasses styles:
glasses_styles = [
    '"glasses":"_blank"',
    '"glasses":"glasses_bm1"',
    '"glasses":"glasses_bm1d"',
    '"glasses":"glasses_bm2"',
    '"glasses":"glasses_bm2d"',
    '"glasses":"glasses_bm3"',
    '"glasses":"glasses_bm3d"',
    '"glasses":"glasses_bm4"',
    '"glasses":"glasses_bm4d"',
    '"glasses":"glasses_bm5"',
    '"glasses":"glasses_bm5d"',
    '"glasses":"glasses_bm6"',
    '"glasses":"glasses_bm6d"',
    '"glasses":"glasses_bm7"',
    '"glasses":"glasses_bm7d"',
    '"glasses":"glasses_bm8"',
    '"glasses":"glasses_bm8d"',
    '"glasses":"glasses_bm9"',
    '"glasses":"glasses_bm9d"',
    '"glasses":"glasses_bm10"',
    '"glasses":"glasses_bm10d"',
    '"glasses":"glasses_bm11"',
    '"glasses":"glasses_bm12"',
    '"glasses":"glasses_bm13"',
    '"glasses":"glasses_bm13d"',
    '"glasses":"glasses_bm14"',
    '"glasses":"glasses_bm15"',
    '"glasses":"glasses_bm15d"',
    '"glasses":"glasses_bm16"',
    '"glasses":"glasses_bm16d"',
    '"glasses":"glasses_bm17"',
    '"glasses":"glasses_bm17d"',
    '"glasses":"glasses_bm18"',
    '"glasses":"glasses_bm19"',
    '"glasses":"glasses_bm19d"',
    '"glasses":"glasses_bm20"',
    '"glasses":"glasses_bm21"',
    '"glasses":"glasses_bm22"',
    '"glasses":"glasses_bm23"',
    '"glasses":"glasses_bm24"',
]

###
# GENDERED:
###

# Hair style: (Not gendered in API, but I'm separating them for easier learning)
hair_styles = {
    'female': [
        '"cranium":"cranium_bm2","forehead":"forehead_bm2","hair_back":"hair_back_blank","hair_front":"hair_front_bm2","hairbottom":"hairbottom_bm2"',
        '"cranium":"cranium_bm8","forehead":"forehead_bm2","hair_back":"hair_back_blank","hair_front":"hair_front_bm8","hairbottom":"hairbottom_bm8"',
        '"cranium":"cranium_bm14","forehead":"forehead_bm2","hair_back":"hair_back_blank","hair_front":"hair_front_bm14","hairbottom":"hairbottom_bm14"',
        '"cranium":"cranium_bm4","forehead":"forehead_bm2","hair_back":"hair_back_bm4","hair_front":"hair_front_bm4","hairbottom":"hairbottom_bm4"',
        '"cranium":"cranium_bm10","forehead":"forehead_bm2","hair_back":"hair_back_bm10","hair_front":"hair_front_bm10","hairbottom":"hairbottom_bm10"',
        '"cranium":"cranium_bm16","forehead":"forehead_bm2","hair_back":"hair_back_bm16","hair_front":"hair_front_bm16","hairbottom":"hairbottom_bm16"',
        '"cranium":"cranium_bm46","forehead":"forehead_bm2","hair_back":"hair_back_bm46","hair_front":"hair_front_bm46","hairbottom":"hairbottom_bm46"',
        '"cranium":"cranium_bm38","forehead":"forehead_bm2","hair_back":"hair_back_bm38","hair_front":"hair_front_bm38","hairbottom":"hairbottom_bm38"',
        '"cranium":"cranium_bm18","forehead":"forehead_bm2","hair_back":"hair_back_bm18","hair_front":"hair_front_bm18","hairbottom":"hairbottom_bm18"',
        '"cranium":"cranium_bm42","forehead":"forehead_bm2","hair_back":"hair_back_bm42","hair_front":"hair_front_bm42","hairbottom":"hairbottom_bm42"',
        '"cranium":"cranium_bm6","forehead":"forehead_bm2","hair_back":"hair_back_bm6","hair_front":"hair_front_bm6","hairbottom":"hairbottom_bm6"',
        '"cranium":"cranium_bm12","forehead":"forehead_bm2","hair_back":"hair_back_bm12","hair_front":"hair_front_bm12","hairbottom":"hairbottom_bm12"',
        '"cranium":"cranium_bm30","forehead":"forehead_bm2","hair_back":"hair_back_bm30","hair_front":"hair_front_bm30","hairbottom":"hairbottom_bm30"',
        '"cranium":"cranium_bm20","forehead":"forehead_bm2","hair_back":"hair_back_bm20","hair_front":"hair_front_bm20","hairbottom":"hairbottom_bm20"',
        '"cranium":"cranium_bm32","forehead":"forehead_bm2","hair_back":"hair_back_bm32","hair_front":"hair_front_bm32","hairbottom":"hairbottom_bm32"',
        '"cranium":"cranium_bm40","forehead":"forehead_bm2","hair_back":"hair_back_bm40","hair_front":"hair_front_bm40","hairbottom":"hairbottom_bm40"',
        '"cranium":"cranium_bm28","forehead":"forehead_bm2","hair_back":"hair_back_bm28","hair_front":"hair_front_bm28","hairbottom":"hairbottom_bm28"',
        '"cranium":"cranium_bm48","forehead":"forehead_bm2","hair_back":"hair_back_bm48","hair_front":"hair_front_bm48","hairbottom":"hairbottom_bm48"',
        '"cranium":"cranium_bm22","forehead":"forehead_bm2","hair_back":"hair_back_bm22","hair_front":"hair_front_bm22","hairbottom":"hairbottom_bm22"',
        '"cranium":"cranium_bm36","forehead":"forehead_bm2","hair_back":"hair_back_bm36","hair_front":"hair_front_bm36","hairbottom":"hairbottom_bm36"',
        '"cranium":"cranium_bm26","forehead":"forehead_bm2","hair_back":"hair_back_bm26","hair_front":"hair_front_bm26","hairbottom":"hairbottom_bm26"',
        '"cranium":"cranium_bm34","forehead":"forehead_bm2","hair_back":"hair_back_bm34","hair_front":"hair_front_bm34","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm24","forehead":"forehead_bm2","hair_back":"hair_back_bm24","hair_front":"hair_front_bm24","hairbottom":"hairbottom_bm24"',
        '"cranium":"cranium_bm44","forehead":"forehead_bm2","hair_back":"hair_back_bm44","hair_front":"hair_front_bm44","hairbottom":"hairbottom_bm44"',
    ],
    'male': [
        '"cranium":"cranium_bm1","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm1","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm7","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm7","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm13","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm13","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm23","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm23","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm25","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm25","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm27","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm27","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm19","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm19","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm35","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm35","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm29","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm29","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm3","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm3","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm9","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm9","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm15","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm15","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm5","forehead":"forehead_bm1","hair_back":"hair_back_bm5","hair_front":"hair_front_bm5","hairbottom":"hairbottom_bm5"',
        '"cranium":"cranium_bm11","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm11","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm17","forehead":"forehead_bm1","hair_back":"hair_back_bm17","hair_front":"hair_front_bm17","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm37","forehead":"forehead_bm1","hair_back":"hair_back_bm37","hair_front":"hair_front_bm37","hairbottom":"hairbottom_bm37"',
        '"cranium":"cranium_bm39","forehead":"forehead_bm1","hair_back":"hair_back_bm39","hair_front":"hair_front_bm39","hairbottom":"hairbottom_bm39"',
        '"cranium":"cranium_bm41","forehead":"forehead_bm1","hair_back":"hair_back_bm41","hair_front":"hair_front_bm41","hairbottom":"hairbottom_bm41"',
        '"cranium":"cranium_bm33","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_blank","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm31","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm31","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm21","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm21","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm45","forehead":"forehead_bm3","hair_back":"hair_back_blank","hair_front":"hair_front_bm45","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm43","forehead":"forehead_bm1","hair_back":"hair_back_blank","hair_front":"hair_front_bm43","hairbottom":"hairbottom_blank"',
        '"cranium":"cranium_bm47","forehead":"forehead_bm1","hair_back":"hair_back_bm47","hair_front":"hair_front_bm47","hairbottom":"hairbottom_bm47"',
    ]
}

# Eyebrow style:
brow_styles = {
    'female': [
        '"brow_L":"brow_bm4","brow_R":"brow_bm4"',
        '"brow_L":"brow_bm6","brow_R":"brow_bm6"',
        '"brow_L":"brow_bm12","brow_R":"brow_bm12"',
        '"brow_L":"brow_bm14","brow_R":"brow_bm14"',
    ],
    'male': [
        '"brow_L":"brow_bm1","brow_R":"brow_bm1"',
        '"brow_L":"brow_bm3","brow_R":"brow_bm3"',
        '"brow_L":"brow_bm5","brow_R":"brow_bm5"',
        '"brow_L":"brow_bm7","brow_R":"brow_bm7"',
    ]
}

# Nose style:
nose_styles = {
    'female': [
        '"nose":"nose_bm2"',
        '"nose":"nose_bm4"',
        '"nose":"nose_bm6"',
        '"nose":"nose_bm8"',
        '"nose":"nose_bm10"',
        '"nose":"nose_bm12"',
        '"nose":"nose_bm14"',
        '"nose":"nose_bm18"',
        '"nose":"nose_bm20"',
    ],
    'male': [
        '"nose":"nose_bm1"',
        '"nose":"nose_bm3"',
        '"nose":"nose_bm5"',
        '"nose":"nose_bm7"',
        '"nose":"nose_bm9"',
        '"nose":"nose_bm11"',
        '"nose":"nose_bm13"',
        '"nose":"nose_bm15"',
        '"nose":"nose_bm17"',
    ]

}

# Mouth style:
mouth_styles = {
    'female': [
        '"mouth":"mouth_bm2"',
        '"mouth":"mouth_bm4"',
        '"mouth":"mouth_bm6"',
    ],
    'male': [
        '"mouth":"mouth_bm1"',
        '"mouth":"mouth_bm3"',
        '"mouth":"mouth_bm5"',
    ]
}

###
# FEMALE ONLY:
###

# Eyeshadow styles:
eyeshadow_styles = [
    '"detail_E2_L":"_blank","detail_E2_R":"_blank","eyelid_L":"_blank","eyelid_R":"_blank"',
    '"detail_E2_L":"detail_E2_bm1","detail_E2_R":"detail_E2_bm1","eyelid_L":"eyelid_bm2_2","eyelid_R":"eyelid_bm2_2"',
]

# "b88eb6": (colours.eyeshadow) - Only works with eyeshadow style on.
eyeshadow_colors = [
    '"b88eb6":16443344',
    '"b88eb6":13473681',
    '"b88eb6":12162955',
    '"b88eb6":9468012',
    '"b88eb6":8888500',
    '"b88eb6":11054004',
    '"b88eb6":15921906',
    '"b88eb6":10724985',
    '"b88eb6":9467477',
    '"b88eb6":5855577',
    '"b88eb6":14732734',
    '"b88eb6":13611946',
    '"b88eb6":13082545',
    '"b88eb6":12571607',
    '"b88eb6":13222882',
    '"b88eb6":11042454',
    '"b88eb6":11506308',
    '"b88eb6":8016458',
]

###
# MALE ONLY:
###

# Beard styles:
beard_styles = [
    '"beard":"_blank","stachin":"_blank","stachout":"_blank"',
    '"beard":"beard_bm4_1","stachin":"_blank","stachout":"stachout_bm4_1"',
    '"beard":"beard_bm1_1","stachin":"stachin_bm1_1","stachout":"stachout_bm1_1"',
    '"beard":"beard_bm3_1","stachin":"_blank","stachout":"stachout_bm5_1"',
    '"beard":"beard_bm3_1","stachin":"stachin_bm1_1","stachout":"stachout_bm1_1"',
    '"beard":"beard_bm2_1","stachin":"stachin_bm1_1","stachout":"stachout_bm1_1"',
    '"beard":"beard_bm3_1","stachin":"_blank","stachout":"stachout_bm6_1"',
    '"beard":"beard_bm3_1","stachin":"_blank","stachout":"stachout_bm7_1"',
    '"beard":"beard_bm4_1","stachin":"stachin_bm1_1","stachout":"stachout_bm1_1"',
    '"beard":"beard_bm4_1","stachin":"_blank","stachout":"stachout_bm5b_1"',
    '"beard":"beard_bm4_1","stachin":"_blank","stachout":"stachout_bm6b_1"',
    '"beard":"beard_bm4_1","stachin":"_blank","stachout":"stachout_bm7b_1"',
]

# "6f4b4b": (colours.beard) - Only works with beard style on.
beard_colors = [
    '"4f453e":6700322',
    '"4f453e":5844766',
    '"4f453e":3218460',
    '"4f453e":1579802',
    '"4f453e":11569973',
    '"4f453e":9663272',
    '"4f453e":7162651',
    '"4f453e":3615014',
    '"4f453e":14386178',
    '"4f453e":11618049',
    '"4f453e":8203556',
    '"4f453e":7733505',
    '"4f453e":15132390',
    '"4f453e":7696224',
    '"4f453e":9343614',
    '"4f453e":3553071',
    '"4f453e":13816322',

    # Unrealistic colors:
    # '"4f453e":7518392',
    # '"4f453e":16672691',
    # '"4f453e":11250942',
    # '"4f453e":248322',
    # '"4f453e":11152171',
    # '"4f453e":164093',
    # '"4f453e":95815',
    # '"4f453e":10486146',
    # '"4f453e":152522',
]


# num_permutations = \
#     ((len(beard_colors) *
#       len(beard_styles) *
#       len(brow_styles['male']) *
#       len(nose_styles['male']) *
#       len(mouth_styles['male']) +
#       len(eyeshadow_colors) *
#       len(eyeshadow_styles) *
#       len(brow_styles['female']) *
#       len(nose_styles['female']) *
#       len(mouth_styles['female'])) *
#      len(proportions) *
#      len(skin_colors) *
#      len(hair_colors) *
#      len(lip_colors) *
#      len(brow_colors) *
#      len(eye_colors) *
#      len(blush_colors) *
#      len(hair_styles) *
#      len(eye_details) *
#      len(face_lines) *
#      len(cheek_details) *
#      len(glasses_styles)
#     )
#
# print num_permutations



# "brow_L":"brow_bm4","brow_R":"brow_bm4""brow_L":"brow_bm6","brow_R":"brow_bm6""brow_L":"brow_bm12","brow_R":"brow_bm12""brow_L":"brow_bm14","brow_R":"brow_bm14"}