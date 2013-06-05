import types

        
def make_generic_decorator(dec1):
    def generic_decorator(*args, **kwargs):
        # OK, this is black magic. You are not expected to understand this.
        if args and isinstance(args[0], types.FunctionType):
            # We were called without parameters
            function = args.pop(0)
            return dec1(function, *args, **kwargs)
        else: 
            def tmp_wrap(function):
                return dec1(function, *args, **kwargs)
            return tmp_wrap
    return generic_decorator
