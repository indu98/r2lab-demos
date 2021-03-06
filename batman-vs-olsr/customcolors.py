from operator import le, lt

class CustomColors:
    """
    A little smarter colormap than the linear model offered in bokeh.
    You provide:

      * n numerical ticks; let's call them t0 .. tn-1
      * n+1 colors: c0 .. cn
      * side ('left' or 'right')

    c0 is selected for a value if
       value <  t0
    c1 is selected if
          t0 < value < t1
    cn is selected if
          tn-1 < value

    when the value is equal to a tick, then 'side' determines
    which color we get; side=left -> the color for the area below,
    etc.
     """

    @staticmethod
    def develop(tick, default_side):
        try:
            value, side = tick
            assert side in {'left', 'right'}
            return tick
        except:
            return tick, default_side

    def __init__(self, ticks, colors, side='left'):
        self.ticks = [self.develop(tick, side) for tick in ticks]
        self.ticks.sort(key=lambda tick: tick[0])
        self.colors = colors
        self.side = side
        assert len(ticks) == len(colors)-1

    def color(self, value):
        for ((tick, side), color) in zip (self.ticks, self.colors):
            compare = le if side == 'left' else lt
            if compare(value, tick):
                return color
        return self.colors[-1]


def test():

    ticks = [0., 1., 3, 5, 10, 30, 100]
    #we have 7 ticks we need 8 colors
    from bokeh.palettes import inferno
    colors = inferno(8)

    scale = CustomColors(ticks, colors, side='left')
    inputs = (-2, 0., 0.5, 20, 90, 100, 101)
    expected = (0, 0, 1, 5, 6, 6, 7)

    for i, e in zip(inputs, expected):
        result = scale.color(i)
        expected = colors[e]
        print(f"{i} -> {result} == {expected} - {result == expected}")

    scale = CustomColors(ticks, colors, side='right')
    inputs = (-2, 0., 0.5, 20, 90, 100, 101)
    expected = (0, 1, 1, 5, 6, 7, 7)

    for i, e in zip(inputs, expected):
        result = scale.color(i)
        expected = colors[e]
        print(f"{i} -> {result} == {expected} - {result == expected}")

    advanced_ticks = [(0., 'left'), 0.5, (1., 'right')]
    colors = ['green', 'yellow', 'orange', 'red']
    scale = CustomColors(advanced_ticks, colors, side='right')
    inputs = (-2, 0., 0.4, 0.5, 0.7, 1., 1.1)
    expected = (0, 0, 1, 2, 2, 3, 3)

    for i, e in zip(inputs, expected):
        result = scale.color(i)
        expected = colors[e]
        print(f"{i} -> {result} == {expected} - {result == expected}")


if __name__ == '__main__':
    test()
