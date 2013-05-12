from genblocks.interfaces import Space

from sts import HasComponents


class BlackBox(Space, HasComponents):
    short = 'bb'
    
    def __init__(self, i, o, t):
        self.i = i
        self.o = o
        self.t = t
        
    def belongs(self, a):
        raise NotImplemented
        
    def equals(self, a, b):
        raise NotImplemented

    def __str__(self):
        return 'BB(%s;%s;%s)' % (self.o, self.i, self.t)


