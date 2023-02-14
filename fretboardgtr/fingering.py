class Fingering():
    def __init__(self, frets):
        self.frets = frets
        self.strings_and_frets = []
        for string, x in enumerate(frets):
            if isinstance(x, (list, tuple)):
                for y in x:
                    self.strings_and_frets.append((string, y))
            else:
                self.strings_and_frets.append((string, x))
        self.defined_frets = [0 if fret is None else fret
                              for _, fret in self.strings_and_frets]

    def offset(self, by_frets):
        result = []
        for string, fret in self.strings_and_frets:
            result.append((string, None if fret is None else fret - by_frets +
                           1 if fret != 0 else fret))
        return result

    @property
    def max(self):
        return max(self.defined_frets)

    @property
    def min(self):
        positive = [fret for fret in self.defined_frets if fret > 0]
        if positive:
            return min(positive)
        else:
            return 0

    def __iter__(self):
        return iter(self.frets)

    def __getitem__(self, item):
        return self.frets[item]
