from typing import Union

import numpy
from matplotlib import pyplot
from scipy import stats

LEGEND_LOCATION = 'upper right'
COLORS = ["#9b59b6", "#e74c3c", "#34495e", "#2ecc71", "#D0D1E6", "#A6BDDB", "#74A9CF", "#2B8CBE", "#045A8D"]
BACKGROUND_GREY88 = "#e0e0e0"


class Plot:
    def __init__(self):
        self.plot_tool = pyplot

    def plot_a_stackplot(self, x_axis: Union[list, range], y_axis: list, labels: list[str]) -> None:
        # Make length the same
        self.edit_and_unify_y_axis_length(y_axis)

        # Upper boarder line
        boarder_line = numpy.array(y_axis).sum(0)

        # set background color
        self.plot_tool.axes().set_facecolor(BACKGROUND_GREY88)
        self.plot_tool.stackplot(x_axis, y_axis, colors=COLORS, labels=labels, alpha=0.9)
        self.plot_tool.plot(x_axis, boarder_line, lw=1.5, color="white")
        self.plot_tool.legend(loc=LEGEND_LOCATION)
        self.plot_tool.show()

    @staticmethod
    def edit_and_unify_y_axis_length(y_axis) -> None:
        maxLen = max(map(len, y_axis))
        [payment_list.extend([0] * (maxLen - len(payment_list))) for payment_list in y_axis]

    @staticmethod
    def gaussian_smooth(x, y, grid, standard_deviation):
        weights = numpy.transpose([stats.norm.pdf(grid, m, standard_deviation) for m in x])
        weights = weights / weights.sum(0)
        return (weights * y).sum(1)
