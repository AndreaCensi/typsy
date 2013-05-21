import decorator

def wrap(f):
    """ 
        Wraps a built-in as a normal function object so we 
        can add attributes to it.
    """
    def f2(unused, *args, **kwargs):
        return f(*args, **kwargs)
    
    from decorator import decorator
    wrapper = decorator(f2, f)
    wrapper.__name__ = f.__name__
    wrapper.__module__ = f.__module__
    return wrapper

@decorator
def typsy_type(f):
    pass



def test_inference():
    
    @typsy_type(type='iterable(A) x iterable(B) -> iterable(A x B)')
    def zip_():
        pass
        

    
