# err_reraise.py

def foo(s):
    n = int(s)
    if n == 0:
        raise ValueError('invalid value: %s' % s)
    return 10 / n

def bar(s):
    try:
        foo(s)
    except ValueError as e:
        print('ValueError!')
        raise

bar()