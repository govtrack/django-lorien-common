from random import choice, randint
import string

def random_string(size):
    return ''.join(choice(string.letters) for x in xrange(size))


def random_words(count=20):
    words = []
    for x in xrange(count):
        word = random_string(randint(4, 10))
        if randint(0, 10) == 0:
            word += choice(('.', ','))
        words.append(word)
    return ' '.join(words)


def random_phone():
    def number(size):
        return ''.join(choice(string.digits) for x in xrange(size))
    return '+%s %s %s' % (number(1), number(3), number(7))


