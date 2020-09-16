#!/usr/bin/env python3

import argparse
import platform
import os
import sys
import tempfile
import time

from PIL import Image, ImageDraw, ImageFont
import mss
import img2pdf


def parse_args():
    parser = argparse.ArgumentParser(
        description='Periodically take screenshots and save them to PDF.'
    )
    parser.add_argument('-d',
                        '--directory',
                        nargs=1,
                        default=[os.getcwd()],
                        help='working directory, defaults to current')
    parser.add_argument('-q',
                        '--quality',
                        type=int,
                        nargs=1,
                        default=[10],
                        help='JPEG compression quality, defaults to 10')
    font_default = None
    plat = platform.system()
    if plat == 'Linux':
        font_default = 'LiberationMono-Regular'
    elif plat == 'Windows':
        font_default = 'arial.ttf'
    elif plat == 'Darwin':
        font_default = 'Monaco'
    else:
        font_default = 'Unknown'
    parser.add_argument('-f',
                        '--font',
                        type=str,
                        nargs=1,
                        default=[font_default],
                        help='Font to use for watermarks')
    args = parser.parse_args()
    return args


def get_timestamp():
    return time.strftime('%Y%m%dT%H%M%S')


def add_watermark(image, text, pos, font, size):
    drawing = ImageDraw.Draw(image)
    font_ttf = ImageFont.truetype(font, size=size)
    drawing.text(pos, text, fill=(255, 0, 0), font=font_ttf)


def main():
    args = parse_args()
    print('Base directory:', args.directory[0])
    print('Watermark font:', args.font[0])
    print('JPEG compression quality:', args.quality[0])
    tmp_dir = tempfile.mkdtemp(dir=args.directory[0])
    with mss.mss() as screenshoter:
        try:
            while True:
                timestamp = get_timestamp()
                image_mss = screenshoter.grab(screenshoter.monitors[0])
                image_pil = Image.frombytes('RGB',
                                            image_mss.size,
                                            image_mss.bgra,
                                            'raw',
                                            'BGRX')
                add_watermark(image_pil,
                              timestamp,
                              (0, 0),
                              args.font[0],
                              40)
                screen_orig = os.path.join(tmp_dir, timestamp + '.png')
                image_pil.save(screen_orig)
                print('New original screenshot:', screen_orig)
                screen_compr = os.path.join(tmp_dir, timestamp + '.jpg')
                image_pil.save(screen_compr,
                               quality=args.quality[0])
                print('New compressed screenshot:', screen_compr)
                time.sleep(5)
        except KeyboardInterrupt:
            print('Caught interrupt!!!')
            print('Generating PDF...')
            filename = os.path.join(tmp_dir, 'result.pdf')
            images = os.listdir(tmp_dir)
            images = filter(lambda file: file.endswith('.jpg'), images)
            images = sorted(images)
            images = list(map(lambda img: os.path.join(tmp_dir, img), images))
            with open(filename, 'wb') as file:
                file.write(img2pdf.convert(images))
            print('Generated PDF:', filename)


if __name__ == '__main__':
    main()
