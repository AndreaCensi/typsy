
class TypsyException(Exception):
    pass

class NotMatch(TypsyException):
    def __init__(self, msg, context=[]):
        self.context = context
        self.msg = msg
        Exception.__init__(self, msg)
        
class FailedMatch(NotMatch):
    def __init__(self, me, other, msg=''):
        self.me = me
        self.other = other
        m = 'Could not match:'
        m += '\n spec %s' % me.__repr__()  
        m += '\n with %s' % other.__repr__()
        m += '\n' + msg
        NotMatch.__init__(self, msg)
        
     
