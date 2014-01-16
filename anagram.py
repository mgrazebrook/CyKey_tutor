

def _select_best(words, max_words):
    if len(words) <= max_words:
        return words

    words = words[:]
    ret = []
    all_letters = ''.join(words)
    letter_set = set(all_letters)

    letter_freq = [ (c, all_letters.count(c)) for c in letter_set ]
    letter_freq.sort( key=lambda lf: lf[1] ) # sort by frequency
    want_letter_count = min(len(words), len(letter_freq) / max_words)

    while True:
        for c, ignore in letter_freq:
            ret_letters = ''.join(ret)
            if ret_letters.count(c) >= want_letter_count:
                continue

            for i, word in enumerate(words):
                if c in word:
                    ret.append(words.pop(i))
                    if len(ret) == max_words:
                        return ret
                    else:
                        break
        want_letter_count += 1


def anagram(chars, max_words):
    # Not strictly an anagram, but rather words which can be made using some of the letters.
    # max_words : Don't return more than max_words, selected to have a good letter distribution
    ret = []

    if not hasattr( anagram, 'words' ):
        anagram.words = []
        with open('all_english.txt') as f:
            for word in f:
                word = word.strip()
                anagram.words.append(word)

    char_set = set(chars)
    for word in anagram.words:
        if set(word).issubset(char_set):
            ret.append(word)
    return _select_best(ret, max_words)


if __name__ == "__main__":
    print anagram('quabcdefghij', 10)
    #for word in ["macaque", "jagged", "vortex", "whisky", "zounds", "pacifiable" ]:
    #    print word, anagram(word, 15)
