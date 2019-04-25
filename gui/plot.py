# coding=utf-8
"""plotting template"""

from enum import Enum
from gui.custom import CustomMplCanvas
from numpy import array, zeros
from utils import PRECISION_ZERO


class PlotParam(Enum):
    """plotting parameters"""
    Show = 'Show'


plot_default_param = {
    PlotParam.Show.value: False,
}


class PayoffCurve(CustomMplCanvas):
    """figure canvas for plotting payoff curve"""

    def _plot_figure(self, data_):
        """
        plot payoff curve using given data
        :param data_: a dict consists with x (numpy array) and y (numpy array) in same dimension
        """
        _x = data_.get('x', array([]))
        _y = array(data_.get('y', [array([])]))
        _type = data_.get('type')
        _x_ref = data_.get('x_ref', 0)
        _y_ref = data_.get('y_ref', 100)

        if not _type:
            raise ValueError("plot type is required")

        if _x.size and _y.size:
            self._axes.clear()
            self._axes.plot((_y_ref, _y_ref), (_y.min(), _y.max()), color="grey", linewidth=1.5)

            if _y.min() <= _x_ref <= _y.max() \
                    or abs(_y.min() - _x_ref) <= PRECISION_ZERO or abs(_y.max() - _x_ref) <= PRECISION_ZERO:
                self._axes.plot(_x, zeros(_x.size) + _x_ref, color="grey", linewidth=1.5)

            if len(_y) > 1:
                for _line in _y[1:]:
                    self._axes.plot(_x, _line, color="blue", linestyle='--')
            self._axes.plot(_x, _y[0], color="red", linestyle='-')

        self._set_axis(_type)

    def update_figure(self, data_):
        """
        update payoff curve using new data
        :param data_: a dict consists with x (numpy array) and y (list of numpy array)
            each array should be in same dimension
        """
        self._plot_figure(data_)
        self.draw()
        
    def save(self, file_path_):
        """
        save figure to file using given path
        :param file_path_: a str indicating path to save figure file
        """
        self.print_png(file_path_)

    def _set_axis(self, type_):
        self._axes.set_xlabel("Spot")
        # self._axes.set_ylabel(type_)
        self._axes.set_title("Option Portfolio {} Curve".format(type_))
        self._axes.grid(axis='x', linewidth=0.75, linestyle='-', color='0.75')
        self._axes.grid(axis='y', linewidth=0.75, linestyle='-', color='0.75')
