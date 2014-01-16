

cykey_map = {
    '\x08': ('NO', (1,3,4)), # Del as pressed
    '\t':('NO', (1,3, 5)),
    ' ': ('NO', (0,)),
    '!': ('NS', (3, 6)),
    '"': ('ES', ()),
    '#': ('NO', ( 2, 4, 5)),
    '$': ('NO', ( 2, 5)),
    '%': ('ES', (0,4,6)),
    '&': ('ES', (0,5)),
    "'": ('NO', (0,3,4,6)),
    '(': ('NS', (4,)),
    ')': ('ES', (4,)),
    '*': ('ES', (3, 4, 5, 6)),
    '+': ('NS', (3, 4)),
    ',': ('NO', (3, 5, 6)),
    '-': ('NO', (2, 3, 4, 6)),
    '.': ('NO', (3, 4, 5)),
    '/': ('NS', (4, 6)),
    '0': ('NO', (2, 4)),
    '1': ('NO', (2,)),
    '2': ('NO', (2, 3)),
    '3': ('NO', (2, 3, 4)),
    '4': ('NO', (2, 3, 4, 5)),
    '5': ('NO', (2, 3, 4, 5, 6)),
    '6': ('NO', (2, 6)),
    '7': ('NO', (2, 5, 6)),
    '8': ('NO', (2, 4, 5, 6)),
    '9': ('NO', (2, 3, 5, 6)),
    ':': ('ES', (3, 4, 5)),
    ';': ('ES', (3, 5, 6)),
    '<': ('ES', (5, 6)),
    '=': ('NS', (3,)),
    '>': ('NS', (5, 6)),
    '?': ('ES', (0, 4, 5)),
    '@': ('ES', (3, 4 )),
    '[': ('NS', (5, )),
    '\\':('ES', (4, 6)),
    ']': ('ES', (5, )),
    '^': ('ES', (6, )),
    '_': ('NS', (6, )),
#    '`': ( ),
    '{': ('NS', (4,5,6)),
    '|': ('ES', (3,6)),
    '}': ('ES', (4,5,6)),
    '~': ('ES', (4,5)),
    'a': ('NO', (3, 4)),
    'b': ('NO', (4, 5, 6)),
    'c': ('NO', (0, 4)),
    'd': ('NO', (0, 3, 4)),
    'e': ('NO', (3,)),
    'f': ('NO', (0, 3, 4, 5)),
    'g': ('NO', (5, 6)),
    'h': ('NO', (0, 6)),
    'i': ('NO', (0, 3)),
    'j': ('NO', (0, 5, 6)),
    'k': ('NO', (0, 5)),
    'l': ('NO', (0, 3, 6)),
    'm': ('NO', (3, 4, 5, 6)),
    'n': ('NO', (4, 5)),
    'o': ('NO', (4,)),
    'p': ('NO', (0, 3, 4, 5, 6)),
    'q': ('NO', (4, 6)),
    'r': ('NO', (0, 3, 5)),
    's': ('NO', (5,)),
    't': ('NO', (3, 5)),
    'u': ('NO', (6,)),
    'v': ('NO', (3, 6)),
    'w': ('NO', (0, 3, 5, 6)),
    'x': ('NO', (0, 4, 5, 6)),
    'y': ('NO', (0, 4, 5)),
    'z': ('NO', (0, 4, 6)),
    'A': ('SH', (3, 4)),
    'B': ('SH', (4, 5, 6)),
    'C': ('SH', (0, 4)),
    'D': ('SH', (0, 3, 4)),
    'E': ('SH', (3,)),
    'F': ('SH', (0, 3, 4, 5)),
    'G': ('SH', (5, 6)),
    'H': ('SH', (0, 6)),
    'I': ('SH', (0, 3)),
    'J': ('SH', (0, 5, 6)),
    'K': ('SH', (0, 5)),
    'L': ('SH', (0, 3, 6)),
    'M': ('SH', (3, 4, 5, 6)),
    'N': ('SH', (4, 5)),
    'O': ('SH', (4,)),
    'P': ('SH', (0, 3, 4, 5, 6)),
    'Q': ('SH', (4, 6)),
    'R': ('SH', (0, 3, 5)),
    'S': ('SH', (5,)),
    'T': ('SH', (3, 5)),
    'U': ('SH', (6,)),
    'V': ('SH', (3, 6)),
    'W': ('SH', (0, 3, 5, 6)),
    'X': ('SH', (0, 4, 5, 6)),
    'Y': ('SH', (0, 4, 5)),
    'Z': ('SH', (0, 4, 6)),
    '1': ('NO', (2,)),
    '2': ('NO', (2,3)),
    '3': ('NO', (2,3,4)),
    '4': ('NO', (2,3,4,5)),
    '5': ('NO', (2,3,4,5,6)),
    '6': ('NO', (2,6)),
    '7': ('NO', (2,5,6)),
    '8': ('NO', (2,4,5,6)),
    '9': ('NO', (2,3,5,6)),
    '0': ('NO', (2,4)),
    'del': ('NO', (1,3,4)), # Del requested by the program
    'NO': ('NO', (0,1)), # Cancel all shifts
    'SH': ('NO', (1,)), # Capital shift
    'NS': ('NO', (0,2)), # Num shift - opening brackets etc
    'ES': ('NO', (1,2)), # Extra shift - Closing brackets and function keys
    'cancel': ('NO', (0,1)),
    '\n' : ('NO', (3,4,7)),
    '\r' : ('NO', (3,4,7)),
    '\x08': ('NO', (1,3,4)),
}
 
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXX   XX   XX   XXXXXXXXXXX
# XXXXXXXXX 3 XX 4 XX 5 XXXXXXXXXXX
# XXXXXXXXX   XX   XX   XXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XX   XX   XXXXXXXXXXX   XX   XXXX
# XX 1 XX 2 XXXXXXXXXXX 6 XX 7 XXXX
# XX   XX   XXXXXXXXXXX   XX   XXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XX       XXXXXXXXXXXXX       XXXX
# XX   0   XXXXXXXXXXXXX   8   XXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Notes on duplicates and unused keys
# SH-.  == NO-. (check)
# SH-\n == NO-\n
# Open and close angle brackets are back to front!


class Key:
    def __init__(self, char):
        self.char = char
        self.shift, self.keys = cykey_map[ char ]


    def diffMessage(self, wantKey):
        "Error message: this is the key pressed, wantKey is the one you should have pressed"

        if self.shift == wantKey.shift:
            if self.keys == wantKey.keys:
                return "" # Matches
            return "Wrong keys"
        else: # shift error
            if self.keys != wantKey.keys:
                return "wrong keys and use '{0}'".format( wantKey.getShiftName() )

            if self.shift == 'NO':
                return "use {0}".format( wantKey.getShiftName() )

            if wantKey.shift == 'NO':
                return "don't use {0}".format( self.getShiftName() )

            return "use {0} not {1}".format( wantKey.getShiftName(), self.getShiftName() )



    def __str__(self):
        return "'{0}' = {1} {2}".format(self.char, self.shift, repr(self.keys))


    def getShiftName(self):
        if self.shift == 'NO':
            return 'no shift'
        if self.shift == 'SH':
            return 'capitals shift'
        if self.shift == 'NS':
            return 'number shift'
        if self.shift == 'ES':
            return 'extra shift'
        raise ValueError("{0} is not a valid shift code".format(self.shift))


def test_diffMessage():
    a = Key('a')
    b =  Key('b')
    aa = Key('A')
    openBracket =  Key('{')
    closeBracket =  Key('}')
    print a
    print "diff a A:", a.diffMessage(aa)
    print "diff A a:", aa.diffMessage(a)
    print "diff a b:", a.diffMessage(b)
    print "diff A b:", aa.diffMessage(b)
    print "diff { }:", openBracket.diffMessage(closeBracket)


if __name__ == "__main__":
    
    for c in cykey_map:
        try:
            k = Key(c)
        except:
            print c
            raise
    test_diffMessage()
