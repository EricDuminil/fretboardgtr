class Fingering():
    #TODO: Find better names
    #TODO: Add doc
    def __init__(self, frets):
        self.frets = frets
        # Possibly flattened
        self.all_frets = []
        #TODO: Apply composite pattern?
        for string, x in enumerate(frets):
            if isinstance(x, (list, tuple)):
                for y in x:
                    self.all_frets.append((string, y))
            else:
                self.all_frets.append((string, x))
        self.no_none = [0 if v is None else v for _, v in self.all_frets]
        self.count = len(self.no_none)

    def offset(self, by_frets):
        result = []
        for string, fret in self.all_frets:
            result.append((string, None if fret is None else fret - by_frets +
                      1 if fret != 0 else fret))
        return result

    @property
    def max(self):
        return max(self.no_none)

    @property
    def min(self):
        positive = [x for x in self.no_none if x > 0]
        if positive:
            return min(positive)
        else:
            return 0

    def __iter__(self):
        return iter(self.frets)

    def __getitem__(self, item):
        return self.frets[item]