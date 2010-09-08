def iterate(qs, step=5000):
    """
    Reduce memory usage by splitting query into a number of queries using offset, limit
    """

    total = qs.count()
    for start in xrange(0, total, step):
        for obj in qs[start:start + step]:
            yield obj
