import argparse
import multiprocessing
from io import BytesIO
from os.path import join
from uuid import uuid1

import numpy as np
import requests
from PIL import Image

import misc.bitmoji_api as api
from misc import get_dir


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

    # Get absolute indices for gendered parameters
    hair_styles_abs_len  = len(api.hair_styles['female'])  + len(api.hair_styles['male'])
    brow_styles_abs_len  = len(api.brow_styles['female'])  + len(api.brow_styles['male'])
    nose_styles_abs_len  = len(api.nose_styles['female'])  + len(api.nose_styles['male'])
    mouth_styles_abs_len = len(api.mouth_styles['female']) + len(api.mouth_styles['male'])

    hair_style_abs_i  = hair_style_i
    brow_style_abs_i  = brow_style_i
    nose_style_abs_i  = nose_style_i
    mouth_style_abs_i = mouth_style_i
    if gender_str == 'male':
        hair_style_abs_i  += len(api.hair_styles['female'])
        brow_style_abs_i  += len(api.brow_styles['female'])
        nose_style_abs_i  += len(api.nose_styles['female'])
        mouth_style_abs_i += len(api.mouth_styles['female'])

    vecs = []
    vecs.append(one_hot(len(api.genders), gender_i))
    vecs.append(one_hot(len(api.proportions), proportion_i))
    vecs.append(one_hot(len(api.eye_details), eye_details_i))
    vecs.append(one_hot(len(api.cheek_details), cheek_details_i))
    vecs.append(one_hot(len(api.face_lines), face_lines_i))
    # vecs.append(one_hot(len(api.glasses_styles), glasses_style_i))
    vecs.append(one_hot(hair_styles_abs_len, hair_style_abs_i))
    vecs.append(one_hot(brow_styles_abs_len, brow_style_abs_i))
    vecs.append(one_hot(nose_styles_abs_len, nose_style_abs_i))
    vecs.append(one_hot(mouth_styles_abs_len, mouth_style_abs_i))
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
    # Don't need to check if has_blush because blush_colors has a 0
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

    param_vec = np.concatenate(vecs)

    return param_vec, url


def one_hot(size, label):
    """
    Returns a zero-vector of length size, with a single 1
    """
    a = np.zeros(size)
    a[label] = 1
    return a

def npz2png(paths):
    for path in paths:
        with np.load(path) as arr:
            img = Image.fromarray(arr['image'], 'RGB')
            img.save(path[:-3] + 'png')

def download(params_url):
    params, url = params_url
    try:
        r = requests.get(url, stream=True)

        if r.status_code == 200:
            # Successful download. Save the parameters and URL
            out_path = join(get_dir(join('data', 'bitmoji')), uuid1().hex + '.npz')
            img = np.array(Image.open(BytesIO(r.content)))[:, :, :3]
            url_array = np.array(url)

            np.savez_compressed(out_path, parameters=params, image=img, url=url_array)
        else:
            print r.status_code
            print url
    except requests.exceptions.ConnectionError as e:
        print e


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n',
                        help='The number of bitmoji to download',
                        default=1,
                        type=int)
    parser.add_argument('--processes',
                        help='The number of processes to use to parallelize '
                             'the download',
                        default=8,
                        type=int)
    args = parser.parse_args()

    params_urls = [get_random_parameters() for i in xrange(args.n)]

    pool = multiprocessing.Pool(processes=args.processes)
    pool_outputs = pool.map(download, params_urls)
    pool.close()
    pool.join()

    print 'Done!'

    # # Test np save:
    #
    # with np.load('/Users/matt/Programming/Deep-Learning/projects/selfie2bitmoji/data/bitmoji/1cbb7366ce8711e7860e3c15c2c6135c.npz') as arr:
    #     print arr['parameters']
    #     print arr['url']
    #     img = Image.fromarray(arr['image'], 'RGB')
    #     img.show()

    # paths = glob('data/bitmoji/*.npz')
    # npz2png(paths)
    # print paths

