import sys, pygame, re
from pygame.locals import *
from cykey_map import cykey_map, Key
from anagram import anagram
import time
from glob import glob


BLACK  = 0,0,0
WHITE  = 0xff, 0xff, 0xff
ORANGE = 220, 180, 10
GREY   = 0x80, 0x80, 0x80
GREEN  = 50, 205, 50
RED    = 0xc0, 0, 0

KEY_POSITION = [
    (94, 283),
    (72, 203),
    (161, 201),
    (217, 115),
    (316, 94),
    (413, 110),
    (475, 193),
    (559, 190),
    (552, 270),
]


pygame.init()
fpsClock = pygame.time.Clock() # Frame per second clock
screen =  pygame.display.set_mode( (640, 360,) )
pygame.display.set_caption( "CyKey tutor" )

    
small_font = pygame.font.Font(None, 16)
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 48)
huge_font = pygame.font.Font(None, 100)


def draw_char_keys(screen, shrink, origin, keys):
    # Draw an icon-like gyph of an unshifted key
    # return the position for continuing printing
    # sides are 1/shrink of the screen
    x0, y0 = origin
    xLen = screen.get_width() / shrink
    yLen = screen.get_height() / shrink
    y0 -= yLen / 2
    rect = pygame.Rect( (x0 + 1, y0 + 1), (xLen - 1, yLen - 1) )

    pygame.draw.rect(screen, WHITE, rect, 1)
    for p in KEY_POSITION:
        x, y = [n / shrink for n in p] # Shrink the key coordinates
        pygame.draw.circle(screen, WHITE, (x0 + x, y0 + y), 4, 1)
    for p in keys:
        x, y = [n / shrink for n in KEY_POSITION[p]]
        pygame.draw.circle(screen, ORANGE, (x0 + x, y0 + y), 3)
    return x0 + xLen, origin[1]


def draw_char_keys_and_shift(screen, c, pos):
    """
    Draw an icon-like version of the keys to press for a letter

    Throws KeyError for an invalid character, LookupError (KeyError's parent class) for an invalid shift.
    """
    SHRINK = 10 # Amount to shrink the screen by, e.g. the icon is 10% of the full screen area.

    shift, keys = cykey_map[c]

    if shift == 'NO':
        pos = draw_char_keys(screen, SHRINK, pos, keys)
    else:
        shift, shift_keys = cykey_map[shift]
        if shift != 'NO':
            raise LookupError("shifted shift for '" + c + "'")

        pos = draw_char_keys(screen, SHRINK, pos, shift_keys)
        pos = draw_char_keys(screen, SHRINK, pos, keys)
    return pos


def get_press_char(expectChar):
    """
    Return the screen display text for a character, e.g. 'x', 'SPACE'
    """
    if cykey_map.has_key(expectChar.lower()):
        if expectChar == '\n':
            return "NEWLINE"
        if expectChar == ' ':
            return "SPACE"
        return expectChar

    return "(unknown key)"

#
# WRAP_LENGTH = x
#
# If return text > x
#   if len(done) > (wl - len(pc)) / 2:
#     chop off the end and start with elipsis
#   likewise for toDo
#
def modify_long_line(done, pressChar, toDo):
    """
    If the line is too long, shorten it with ... at one or both ends.
    """
    WRAP_LENGTH = 50
    
    lenDone  = len(done)
    lenPress = len(pressChar)
    lenToDo  = len(toDo)

    if lenDone + lenPress + lenToDo > WRAP_LENGTH:
        if lenDone > (WRAP_LENGTH - lenPress) / 2:
            lenForDone = WRAP_LENGTH / 2 - 3 - lenPress
            done = "..." + done[-lenForDone:]
        if lenToDo > (WRAP_LENGTH - lenPress) / 2:
            lenForToDo = WRAP_LENGTH / 2 - 3 - lenPress
            toDo = toDo[:lenForToDo] + "..."
    return done, pressChar, toDo


def getDisplayText( text, textIndex, delete ):
    start = text[:textIndex].rfind('\n') + 1
    end = text[textIndex:].find('\n')
    if end == -1:
        end = len(text)
    end += textIndex # Change from relative to the cursor to absolute

    done = text[start:textIndex]
    if delete:
        pressChar = "DEL"
        toDo = text[textIndex:end]
    else:
        pressChar = get_press_char( text[textIndex] )
        toDo = text[textIndex+1:end]

    return modify_long_line(done, pressChar, toDo)


def draw_text( screen, text, font, colour, pos, pos_type='left' ):
    assert pos_type in ('left', 'centre')

    if text == '':
        return pos

    text = font.render(text, 1, colour)
    x, y = pos
    if pos_type == 'centre':
        x, y = x - text.get_width() / 2, y - text.get_height() / 2
    elif pos_type == 'left':
        y = y - text.get_height() / 2
    screen.blit(text, (x,y,) )
    return pos[0] + text.get_width(), pos[1]


def drawKeySet( screen, keys, colour, radius, text='', offset=(0,0) ):
    textColour = WHITE
    if sum(colour) > 0x180:
        textColour = BLACK

    for n in keys:
        x, y = KEY_POSITION[n]
        x += offset[0]
        y += offset[1]
        pygame.draw.circle( screen, colour, (x,y), radius )
        if text:
            textImage = font.render(text, 1, textColour)
            screen.blit( textImage,
                         (x - textImage.get_width() / 2,
                          y - textImage.get_height()/ 2) )


def drawKeySequence( screen, key, colour, radius, offset=(0,0), cancelShift=False ):
    if not cancelShift and key.shift == 'NO':
        drawKeySet( screen, key.keys, colour, radius, offset = offset )
        return

    x, y = offset
    shiftKey = Key( key.shift )
    drawKeySet( screen, shiftKey.keys, colour, radius, text = '1', offset = (x-16, y) )
    drawKeySet( screen, key.keys, colour, radius, text = '2', offset = offset )


def draw_text_line( screen, text, textIndex, delete ):
    start, middle, end = getDisplayText(text, textIndex, delete)

    pos = (20, 20)
    pos = draw_text( screen, start,  font,     ORANGE, pos )
    pos = draw_text( screen, middle, big_font, WHITE,  pos )
    pos = draw_text( screen, end,    font,     GREY,   pos )

    draw_text( screen, middle, huge_font, WHITE, (screen.get_width()/2, screen.get_height()/2), pos_type = 'centre' )


def drawErrorMessage( screen, font, errorMessage ):
    pos = (190, screen.get_height() - font.get_height() - 3)
    draw_text( screen, errorMessage, font, WHITE, pos )


def drawMnemonic( screen, key ):
    if key in ('a', 'A'):
        pygame.draw.line(screen, WHITE, (185, 145), (332,  74), 1)
        pygame.draw.line(screen, WHITE, (332,  74), (429, 137), 1)
        pygame.draw.line(screen, WHITE, (226, 115), (409, 106), 1)
    if key in ('t', 'T'):
        pygame.draw.line(screen, WHITE, (218, 112), (411, 112), 1)
        pygame.draw.line(screen, WHITE, (317, 112), (317, 245), 1)


def refresh( typedChar, text, textIndex, error_state, errorMessage, show_keys ):
    """
    Refresh the display.

    Display the keys for text[textIn    If that doesn't represent typedChar, display typedChar, smaller and on top.
    """
    if error_state == 2 and show_keys == False:
        show_keys = True

    screen.fill(BLACK)
    if not hasattr(refresh, 'cykey_image'):
        refresh.cykey_image = pygame.image.load('cy_key_on_black_640x360.png')
    screen.blit(refresh.cykey_image, (0,0))

    if typedChar in cykey_map:
        haveKey = Key(typedChar)
    else:
        haveKey = None

    wantChar = text[textIndex]
    if wantChar in cykey_map:
        wantKey = Key(wantChar)
    else:
        wantKey = None
        errorMessage = "The program doesn't understand '{0}'".format(wantChar)

    if error_state == 1:
        text = ""
        cancelShift = False

        if haveKey:
            if wantKey:
                errorMessage = repr(typedChar)[1:] + " : " + haveKey.diffMessage(wantKey)
                cancelShift = wantKey.shift == 'NO' and haveKey.shift != wantKey.shift
            drawKeySequence( screen, haveKey, WHITE, 10, offset = (0, 26) )

        drawKeySequence( screen, Key("del"), ORANGE, 16, cancelShift = cancelShift )
    elif show_keys and wantKey:
            drawKeySequence( screen, wantKey, ORANGE, 16 )
            drawMnemonic( screen, wantChar )

    if errorMessage:
        drawErrorMessage( screen, font, errorMessage )

    draw_text_line( screen, text, textIndex, error_state == 1 )


def keyPress( c, text, textIndex, error_state, shift ):
    done = False
    
    if c == '\r':
        c = '\n'
    
    if not cykey_map.has_key(c):
        print "Unknown key: ", c
        error_state = 1

    elif error_state == 1:
        if c == '\x08': # correct delete
            c = None # We only need the old C if it was an error
            error_state = 2

    elif ( shift and c.upper() == text[textIndex] or
          not shift and c == text[textIndex] ):
        error_state = 0 # well done
        if (textIndex + 1) == len(text):
            done = True
        else:
            textIndex += 1
        c = None # We only want the old C if it was an error
    else:
        error_state = 1

    if c and shift:
        print "SHIFT"
        c = c.upper()

    return c, textIndex, error_state, done

keyPress.DONE = 1
keyPress.CASE_ERROR = -1
keyPress.NUM_SHIFT_ERROR = -2
keyPress.E_SHIFT_ERROR = -3
keyPress.OK = 0


def run_text(screen, text, image, show_keys):
    errorMessage = ""
    running = True
    done = False

    textIndex = 0
    c = None # last character typed
    error_state = 0 # 1: Ask for delete following a miss-key; 2: Repeating
    shift = False

    while(running):
        try:
            for event in pygame.event.get():
                if event.type == 6:
                    print event
                if event.type == QUIT:
                    running = False
                elif event.type == KEYUP:
                    if event.key in (K_RSHIFT, K_LSHIFT):
                        shift = False
                elif event.type == KEYDOWN:
                    errorMessage = ""
                    if event.key in (K_RSHIFT, K_LSHIFT):
                        shift = True
                    else:
                        c, textIndex, error_state, done = keyPress(event.unicode, text, textIndex, error_state, shift)
                        if done:
                            return True

            refresh(c, text, textIndex, error_state, errorMessage, show_keys)
            pygame.display.update()
            fpsClock.tick(30)

        except ValueError as e:
            errorMessage = "c = {c}, event key = {event_key}".format(c=c, event_key = event.key)
            error_state = 1
            print errorMessage
        except:
            print "Died of unknown causes"
            raise
    return False # Didn't complete the exercise


def show_image(screen, img):
    x = (screen.get_width() - img.get_width()) / 2
    y = (screen.get_height() - img.get_height()) / 2
    if x < 0:
        x + 0
    if y < 0:
        y + 0

    screen.fill((0,0,0))
    screen.blit(img, (x, y))

    for event in pygame.event.get():
        pass; # Flush the event queue
    
    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYUP):
                return
        pygame.display.update()
        fpsClock.tick(30)


def get_image(textFileName, title):
    # xxx redundant
    imgFileName = textFileName[:-4] + '.png'
    try:
        return pygame.image.load(imgFileName)
    except:
        return font.render(title, 1, WHITE)


class MenuScreen:
    # It presents a list of choices in the format:
    #   image of keys to press ; letter to press ; text description
    # Pressing a key calls it's object's run method, which usually triggers another screen.

    def __init__( self, items, icon_space=1 ):
        # render a list of (key, text, instance) where instance has a method: run(screen)
        #
        # key: anything in cykey_map, usually a single character
        # text: Menu item text
        # run: Method to run if key is pressed. If True, quit.
        # icon_space: More space for key icons: Use 2 for shifted keys
        self._screen = screen
        self._items = items
        self._item_dict = dict([ (key, obj) for key, ignore, obj in items ])
        self._icon_space = icon_space

    def refresh(self, screen):
        screen.fill((0,0,0))
        for i, item in enumerate(self._items):
            key, title, instance = item
            x, y = 5, 40 * i+1 + 30
            tab = screen.get_width() * self._icon_space / 10 + 5

            draw_char_keys_and_shift(screen, key, (x, y))
            pos = draw_text( screen, key, font, ORANGE, (x + tab, y,) )
            draw_text( screen, title, font, WHITE, (pos[0]+5, pos[1]) )

    def bad_key(self, screen):
        return False # Virtual. Action on pressing the wrong key. If True, quit.

    def key_down(self, screen, key):
        try:
            if self._item_dict[key].run(screen):
                return True
        except KeyError:
            if self.bad_key(screen): # Normally we let them try again.
                return True
        # Further exceptions are application errors - let it die.

    def run(self, screen):
        # Event loop.
        # Return True for an orderly exit, False for disorderly.
        while (True):
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                if event.type == KEYDOWN:
                    if self.key_down(screen, event.unicode):
                        return True

            self.refresh(screen)
            pygame.display.update()
            fpsClock.tick(30)
        return False # disorderly exit. Unreachable?


class QuitAction:
    def run(self, screen):
        return True


class AnagramAction:
    # Menu action callback. Run the game screen for the anagram game
    def __init__(self, word):
        self._word = word

    def run(self, screen):
        words = anagram(self._word, 20)
        PoemAction("Anagrams of " + self._word, ' '.join(words), None, False).run(screen)
        return True


class PoemAction:
    # Object for the action callback for selecting a poem
    def __init__(self, title, text, file_name, show_keys=True):
        self._title = title
        self._text = text
        self._file_name = file_name
        self._show_keys = show_keys

    def run(self, screen):
        try:
            image_file_name = self._file_name[:-4] + '.png'
            image = pygame.image.load(image_file_name)
        except:
            image = font.render(self._title, 1, WHITE)

        if run_text(screen, self._text, image, self._show_keys):
            show_image( screen, image )

        return False


class PoemChoiceAction:
    
    def run(self, screen):
        choice = glob('text/*.txt')
        menu_items = []
        for fileName in choice:
            with open(fileName) as f:
                text = f.read()
                firstLine = text[:text.find('\n')].strip()
                key = str(len(menu_items)+1)
                menu_items.append( (key, firstLine, PoemAction(firstLine, text, fileName)) )
        menu_items.append( ('q', 'Quit', QuitAction()) )

        menu_screen = MenuScreen(menu_items)
        menu_screen.run(screen)


class EnterAnagramAction:

    def __init__(self):
        self._user_text = ""
        self._error = ""

    def refresh(self, screen):
        MARGIN = 20
        y = 30
        line_height = 40
        screen.fill( BLACK )
        pos = draw_text( screen, "Type some characters, then ENTER ", font, WHITE, (MARGIN, y) )
        pos = draw_char_keys_and_shift(screen, '\n', pos)
        draw_text( screen, " to start",  font, WHITE, pos )
        y += line_height

        pos = draw_text( screen, "Type a full stop '.' ", font, WHITE, (MARGIN, y) )
        pos = draw_char_keys_and_shift(screen, '.', pos)
        draw_text( screen, " to quit", font, WHITE, pos )
        y += line_height
        y += line_height
        draw_text( screen, self._user_text, big_font, ORANGE, (MARGIN, y) )

        if self._error:
            NEAR_THE_BOTTOM =  screen.get_height() * 0.8
            draw_text( screen, self._error, font, RED, (MARGIN, NEAR_THE_BOTTOM) )

    def run(self, screen):
        # "Or full stop " <icon> to quit
        # a-z are accepted, other characters generate an error.
        # Error if there are no anagrams of the chosen word.
        while True:
            try:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return
                    if event.type == KEYDOWN:
                        if event.unicode == '\x08': # delete
                            self._user_text = self._user_text[:-1]
                        elif event.unicode == '.':
                            return
                        elif event.unicode in ('\n', '\r'):
                            words = anagram(self._user_text)
                            PoemAction("Anagrams of " + self._user_text, ' '.join(words), None, False).run(screen)
                        elif event.unicode.isalpha():
                            if event.unicode.islower():
                                self._error = ''
                                self._user_text = self._user_text + event.unicode
                            else:
                                self._error = event.unicode + ' : you can only use lower case letters'
                        else:
                            self._error = event.unicode + ' : only letters (a-z)'
            except Exception as e:
                self._error = str(e)
            self.refresh(screen)
            pygame.display.update()
            fpsClock.tick(30)


class AnagramChoiceAction:
    # A screen to let you select an anagram, or make your own.
    def run(self, screen):
        words = [ 'macaque', 'jagged', 'vortex', 'whisky', 'zounds', 'pacifiable' ]

        menu_items = []
        for i, word in enumerate(words):
            menu_items.append( (str(i+1), word, AnagramAction(word)) )
        menu_items.append( ('d', 'DIY: anagrams of letters you choose', EnterAnagramAction()) )
        menu_items.append( ('q', 'Quit', QuitAction()) )

        menu_screen = MenuScreen(menu_items)
        menu_screen.run(screen)


class SnapGameAction:
    def run():
        pass # xxx some day


class GameSelectAction:

    def run(self, screen):
        menu_items = [
            ('a', 'Anagrams: Learning a few letters at a time', AnagramChoiceAction()),
            ('p', 'Poetry: Typing practice', PoemChoiceAction()),
            ('s', 'Snap game', SnapGameAction()),
            ('q', 'Quit', QuitAction()),
        ]
        menu_screen = MenuScreen(menu_items)
        menu_screen.run(screen)



if __name__ == "__main__":
    app = GameSelectAction()
    app.run(screen)
    pygame.quit()


# Backlog
#
# Make useable for a mobile device
# 'query mode' where you type a character in by some other means
# Success feedback
# Top level menu
# Anagram game
# Snap decision game
# Scoring time and accuracy

# Change requests for CyKey:
# Some way to know if shift lock is on - maybe shift lock sends K_RSHIFT instead of K_LSHIFT?
# Handle all kinds of shifts
# re-do to meet PEP-8 http://www.python.org/dev/peps/pep-0008/, consider also http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
# Run pylint
