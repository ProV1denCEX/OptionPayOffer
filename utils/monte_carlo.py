# coding=utf-8
"""Monte-Carlo engine"""

from numpy.ma import exp, sqrt
from numpy.random import normal as rand_norm
from utils import parse_kwargs


class MonteCarlo(object):
    """Monte Carlo Engine"""

    @classmethod
    def stock_price(cls, iteration_=1, **kwargs):
        """generate stock spot through stochastic process"""
        _rand = rand_norm(0, 1, iteration_)
        _isp, _rate, _div, _vol, _t = parse_kwargs(kwargs, ['isp', 'rate', 'div', 'vol', 't'], 0)
        return _isp * exp((_rate - _div - _vol ** 2 / 2) * _t + _vol * sqrt(_t) * _rand)
