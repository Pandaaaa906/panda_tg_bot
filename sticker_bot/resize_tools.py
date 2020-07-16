from io import BytesIO

from cv2 import cv2
from loguru import logger
import numpy as np

from seam_carving import seam_carve


MAX_LENGTH = 512


def open_img(fp):
    if isinstance(fp, BytesIO):
        file_bytes = np.asarray(bytearray(fp.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    else:
        img = cv2.imread(fp)
    return img


def normal_resize(fp):
    img = open_img(fp)
    h, w, *_ = img.shape
    ratio = w / h
    new_size = w > h and (MAX_LENGTH, int(MAX_LENGTH / ratio)) or (int(MAX_LENGTH * ratio), MAX_LENGTH)
    return cv2.resize(img, new_size, interpolation=cv2.INTER_CUBIC)


@logger.catch
def seam_carving_resize(fp):
    img = open_img(fp)
    h, w, *_ = img.shape
    ratio = w / h
    new_size = w < h and (MAX_LENGTH, int(MAX_LENGTH / ratio)) or (int(MAX_LENGTH * ratio), MAX_LENGTH)
    img = cv2.resize(img, new_size, interpolation=cv2.INTER_CUBIC)
    h, w, *_ = img.shape

    return seam_carve(img, MAX_LENGTH-h, MAX_LENGTH-w)
