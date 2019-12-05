# -*- coding:utf-8 -*-
import os

import PIL.Image
import cv2


def make_square_PIL(im, min_size=256, fill_color=(0, 0, 0)):
    """
    将图片转成正方形，取黑色补齐短边
    :param im: PIL.Image的对象
    :param min_size: 256,默认
    :param fill_color:黑色，默认
    :return: 新的图像(PIL.Image的对象)
    """
    x, y = im.size
    size = max(min_size, x, y)
    new_im = PIL.Image.new('RGBA', (size, size), fill_color)
    # new_im.paste(im, ((size - x) // 2, (size - y) // 2))
    new_im.paste(im, (0, 0))
    return new_im


def make_square_cv(im, fill_color=(0, 0, 0)):
    """
    将图片转成正方形，取黑色补齐短边
    :param im: cv2对象
    :param fill_color:黑色，默认
    :return: 新的图像(cv2对象)
    """
    x, y = im.size
    new_size = max(x, y)
    im = cv2.copyMakeBorder(im, 0, new_size - x, 0, new_size - y, cv2.BORDER_CONSTANT, value=fill_color)
    return im

def img_recover(im, w=640, h=360):
    """
    恢复图片的大小
    :param im: 需要时PIL.Image的对象
    :param w: 原始宽度
    :param h: 原始高度
    :return: 恢复后图片
    """
    return im.crop((0, 0, w, h))

def video_together(input=".", fps=10, outdir='video', fmt='.avi', outname='outvideo', outshape=(640, 360)):
    """
    图像拼接成视频函数
    :param inputdir:
    :param fps:
    :param outdir:
    :param fmt:
    :param outname:
    :param outshape:
    :return:
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)
        print("系统自动创建输出文件夹%s" % outdir)
    print("拼接结果保存在%s中" % outdir)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')   #XVID是一个开放源代码的MPEG-4视频编解码器
    fourcc = cv2.CV_FOURCC('P', 'I', 'M', '1') # MPEG-1 codec
    # fourcc = cv2.CV_FOURCC('M', 'J', 'P', 'G') # motion-jpeg codec
    # fourcc = cv2.CV_FOURCC('M', 'P', '4', '2') # MPEG-4.2 codec
    # fourcc = cv2.CV_FOURCC('D', 'I', 'V', '3') # MPEG-4.3 codec
    # fourcc = cv2.CV_FOURCC('D', 'I', 'V', 'X') # MPEG-4 codec
    # fourcc = cv2.CV_FOURCC('U', '2', '6', '3') # H263 codec
    # fourcc = cv2.CV_FOURCC('I', '2', '6', '3') # H263I codec
    # fourcc = cv2.CV_FOURCC('F', 'L', 'V', '1') # FLV1 codec
    # fourcc = cv2.CV_FOURCC('M', 'J', 'P', 'G')
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
    files = os.listdir(input)
    videoWriter = cv2.VideoWriter(os.path.join(outdir, outname+fmt), fourcc, fps, outshape)
    for i, o in enumerate(files):
        img = cv2.imread(o)
        print(o)
    videoWriter.write(img)
    videoWriter.release()
    print("拼接结果保存在%s中" % outdir)
    return
