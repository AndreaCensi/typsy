from typsy.interface import typsy_type, set_typsy_type, get_typsy_type

# def wrap(f):
#     """ 
#         Wraps a built-in as a normal function object so we 
#         can add attributes to it.
#     """
#     def f2(unused, *args, **kwargs):
#         return f(*args, **kwargs)
#     
#     from decorator import decorator
#     wrapper = decorator(f2, f)
#     wrapper.__name__ = f.__name__
#     wrapper.__module__ = f.__module__
#     return wrapper


def test_inference():
    import typsy_python  # @UnusedImport

    @typsy_type('UniformSequence(A) x UniformSequence(B) -> UniformSequence(A x B)')
    def zip1(a, b):
        return zip(a, b)
    
    class UserList(list):
        
        def get_typsy_type(self):
            from typsy.parsing.parsin import parse_spec
            return parse_spec('UniformSequence(A)')
        
    s1 = UserList([1, 2, 3, 4])
    s2 = UserList([1.1, 2.1, 3.2, 4.3])
    ftype = get_typsy_type(zip1)
    res1 = ftype(get_typsy_type(s1), get_typsy_type(s2))
    res2 = ftype(s1, s2)
    assert res1 == res2
    
    # Now, notice that we shouldn't get
    # => UniformSequence(A x A)
    # because the scope of the variables should be limited
    
    from typsy_python.uniform_sequence import UniformSequence
    assert isinstance(res1, UniformSequence)
    o = res1.o
    from typsy.library.product import ProductSpace
    assert isinstance(o, ProductSpace)
    sp1 = o.spaces[0] 
    sp2 = o.spaces[1]
    print sp1
    print sp2
    assert not sp1 == sp2, (sp1, sp2)
    
    
    