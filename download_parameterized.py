import requests
import shutil
import numpy as np
import bitmoji_api as api


# def get_url():

def get_random_parameters():
    """
    Generates a set of random bitmoji face parameters.

    :return: A tuple (vecs, url), where vecs is an array of the one-hot encoding
             for each parameter and url is the url to render a bitmoji face with
             the parameters.
    """
    ##
    # Pick parameters
    ##

    # Non-gendered parameters
    proportion_i = np.random.randint(len(api.proportions))

    skin_color_i  = np.random.randint(len(api.skin_colors))
    hair_color_i  = np.random.randint(len(api.hair_colors))
    lip_color_i   = np.random.randint(len(api.lip_colors))
    brow_color_i  = np.random.randint(len(api.brow_colors))
    eye_color_i   = np.random.randint(len(api.eye_colors))
    blush_color_i = np.random.randint(len(api.blush_colors))
    has_blush = blush_color_i > 0

    eye_details_i   = np.random.randint(len(api.eye_details))
    cheek_details_i = np.random.randint(len(api.cheek_details))
    face_lines_i    = np.random.randint(len(api.face_lines))
    # glasses_style_i = np.random.randint(len(api.glasses_styles))

    # Gendered parameters
    gender_i   = np.random.randint(len(api.genders))
    gender_str = 'male' if gender_i == 0 else 'female'

    hair_style_i  = np.random.randint(len(api.hair_styles[gender_str]))
    brow_style_i  = np.random.randint(len(api.brow_styles[gender_str]))
    nose_style_i  = np.random.randint(len(api.nose_styles[gender_str]))
    mouth_style_i = np.random.randint(len(api.mouth_styles[gender_str]))

    # Female-only parameters
    eyeshadow_style_i = np.random.randint(len(api.eyeshadow_styles))
    eyeshadow_color_i = np.random.randint(len(api.eyeshadow_colors))
    has_eyeshadow = gender_str == 'female' and eyeshadow_style_i > 0

    # Male-only parameters
    beard_style_i = np.random.randint(len(api.beard_styles))
    beard_color_i = np.random.randint(len(api.beard_colors))
    has_beard = gender_str == 'male' and beard_style_i > 0


    ##
    # Generate URL
    ##

    base_url = api.gender_base_urls[gender_i]

    gender_param = api.genders[gender_i]
    proportion_param = api.proportions[proportion_i]

    styles = []
    styles.append(api.eye_details[eye_details_i])
    styles.append(api.cheek_details[cheek_details_i])
    styles.append(api.face_lines[face_lines_i])
    # styles.append(api.glasses_styles[glasses_style_i])
    styles.append(api.hair_styles[gender_str][hair_style_i])
    styles.append(api.brow_styles[gender_str][brow_style_i])
    styles.append(api.nose_styles[gender_str][nose_style_i])
    styles.append(api.mouth_styles[gender_str][mouth_style_i])
    if has_eyeshadow: styles.append(api.eyeshadow_styles[eyeshadow_style_i])
    if has_beard:     styles.append(api.beard_styles[beard_style_i])
    styles_param = 'pd2={' + ','.join(styles) + '}'

    colors = []
    colors.append(api.skin_colors[skin_color_i])
    colors.append(api.hair_colors[hair_color_i])
    colors.append(api.lip_colors[lip_color_i])
    colors.append(api.eye_colors[eye_color_i])
    colors.append(api.brow_colors[brow_color_i])
    if has_blush:     colors.append(api.blush_colors[blush_color_i])
    if has_eyeshadow: colors.append(api.eyeshadow_colors[eyeshadow_color_i])
    if has_beard:     colors.append(api.beard_colors[beard_color_i])
    colors_param = 'colours={' + ','.join(colors) + '}'

    request_params = '&'.join(
        [gender_param, proportion_param, styles_param, colors_param])

    url = base_url + request_params


    ##
    # Generate vectors
    ##

    vecs = []
    vecs.append(one_hot(len(api.genders), gender_i))
    vecs.append(one_hot(len(api.proportions), proportion_i))
    vecs.append(one_hot(len(api.eye_details), eye_details_i))
    vecs.append(one_hot(len(api.cheek_details), cheek_details_i))
    vecs.append(one_hot(len(api.face_lines), face_lines_i))
    # vecs.append(one_hot(len(api.glasses_styles), glasses_style_i))
    vecs.append(one_hot(len(api.hair_styles[gender_str]), hair_style_i))
    vecs.append(one_hot(len(api.brow_styles[gender_str]), brow_style_i))
    vecs.append(one_hot(len(api.nose_styles[gender_str]), nose_style_i))
    vecs.append(one_hot(len(api.mouth_styles[gender_str]), mouth_style_i))
    if has_eyeshadow:
        vecs.append(one_hot(len(api.eyeshadow_styles), eyeshadow_style_i))
    else:
        vecs.append(np.zeros(len(api.eyeshadow_styles)))
    if has_beard:
        vecs.append(one_hot(len(api.beard_styles), beard_style_i))
    else:
        vecs.append(np.zeros(len(api.beard_styles)))

    vecs.append(one_hot(len(api.skin_colors), skin_color_i))
    vecs.append(one_hot(len(api.hair_colors), hair_color_i))
    vecs.append(one_hot(len(api.lip_colors), lip_color_i))
    vecs.append(one_hot(len(api.eye_colors), eye_color_i))
    vecs.append(one_hot(len(api.brow_colors), brow_color_i))
    # Don't need to if case with has_blush because blush_colors has a 0
    # index that means none. has_blush is just to make sure that fake index
    # doesn't get added to the URL.
    vecs.append(one_hot(len(api.blush_colors), blush_color_i))
    if has_eyeshadow:
        vecs.append(one_hot(len(api.eyeshadow_colors), eyeshadow_color_i))
    else:
        vecs.append(np.zeros(len(api.eyeshadow_colors)))
    if has_beard:
        vecs.append(one_hot(len(api.beard_colors), beard_color_i))
    else:
        vecs.append(np.zeros(len(api.beard_colors)))

    return np.array(vecs), url

def one_hot(size, i):
    a = np.zeros(size)
    a[i] = 1
    return a


from uuid import uuid1
def download(url):
    # for url in urls:
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open('data/%s.png' % uuid1().hex, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print r.status_code
        print url

import multiprocessing
from time import time, sleep
from os import system
if __name__ == '__main__':
    system('rm data/*.png')
    # print 'Single process'
    # single_start = time()
    # download(80)
    # single_end = time()

    urls = []
    for i in xrange(80):
        urls.append(get_random_parameters()[1])
        # sleep(0.1)

    # download(urls)

    pool = multiprocessing.Pool(processes=8)
    pool_outputs = pool.map(download, urls)
    pool.close()
    pool.join()
    # ps = []
    # for i in xrange(8):
    #     p = Process(target=download, args=(urls[i:i+10],))
    #     ps.append(p)
    #     p.start()
    #
    # for p in ps:
    #     p.join()

    print 'Done!'

    # print
