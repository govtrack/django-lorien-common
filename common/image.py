import time
from random import randint
from hashlib import sha1
import os
import Image
import ImageDraw

from django.core.files import File

def random_color():
    return 'rgb(%d, %d, %d)' % (randint(0, 255), randint(0, 255), randint(0, 255))


def generate_image(size):
    img = Image.new('RGBA', size=size)
    draw = ImageDraw.Draw(img)
    for x in xrange(30):
        diameter = int(min(*size) / float(randint(4, 8)))
        topleft = (0 + randint(0, size[0]),
                   0 + randint(0, size[1]))
        bottomright = (topleft[0] + diameter,
                       topleft[1] + diameter)
        draw.pieslice((topleft + bottomright), 0, 360, fill=random_color())
    return img


def random_image(size=(200, 200)):
    source = '%d%d' % (time.time(), id({}))
    hashname = sha1(source).hexdigest() + '.jpg'
    tmpname = os.tmpnam()
    img = generate_image(size)
    img.save(tmpname, 'JPEG')
    return File(open(tmpname), name=hashname)
