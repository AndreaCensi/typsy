
class NotMatch(Exception):
    def __init__(self, msg, context=[]):
        self.context = context
        self.msg = msg
        Exception.__init__(self, msg)
        
class FailedMatch(NotMatch):
    def __init__(self, me, other):
        self.me = me
        self.other = other
        msg = 'Could not match:'
        msg += '\n spec %s' % me  
        msg += '\n with %s' % other
     
