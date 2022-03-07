import dataclasses
import typing

import matplotlib.pyplot as plt


@dataclasses.dataclass
class Line:
    x_values: typing.List[typing.Any]
    y_values: typing.List[typing.Any]
    color: str
    line_style: str
    label: str


@dataclasses.dataclass
class Plot:
    x_label: str
    y_label: str
    x_min: typing.Any
    x_max: typing.Any
    y_min: typing.Any
    y_max: typing.Any
    lines: typing.List[Line]

    _fig: plt.Figure
    _ax: plt.Axes

    def __init__(self, x_label: str, y_label: str, x_min, x_max, y_min, y_max, lines: typing.List[Line]):
        self.x_label = x_label
        self.y_label = y_label
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.lines = lines

        fig, ax = plt.subplots()
        plot_lines = [
            ax.plot(line.x_values, line.y_values, color=line.color, linestyle=line.line_style, label=line.label)[0]
            for line in self.lines
        ]
        ax.axis([self.x_min, self.x_max, self.y_min, self.y_max])
        ax.legend(handles=plot_lines)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        self._fig, self._ax = fig, ax

    def save_to_file(self, filename: str):
        self._fig.savefig(filename)
