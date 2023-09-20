from decorator import decorator

@decorator
def workaround_decorator(f, *args, **kwargs):
    f(*args, **kwargs)
    if args[1] == 2:
        print('The second argument is 2!')

@workaround_decorator
def my_func(arg1, arg2, kwarg1=None):
    print('arg1: {} arg2: {}, kwargs: {}'.format(arg1, arg2, kwarg1))



my_func(1,2)