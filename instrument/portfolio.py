# coding=utf-8
"""definition of portfolio for payoff estimation"""

from copy import deepcopy
from enum import Enum
from instrument import InstType, option_type
from instrument.default_param import env_default_param
from instrument.env_param import EnvParam
from numpy import arange, transpose


class CurveType(Enum):
    """supported curve type for portfolio curve generator"""
    Payoff = 'Payoff'
    NetPayoff = 'Net Payoff'
    PnL = 'PnL'
    PV = 'PV'
    Delta = 'Delta'
    Gamma = 'Gamma'


class Portfolio(object):
    """
    portfolio class
    can estimate all components total payoff
    """
    def __init__(self, inst_list_):
        self._components = inst_list_
        self._components_show = []
        self._mkt_data = None
        self._engine = None
        self._center = env_default_param[EnvParam.UdSpotForPrice.value]
        self._maturity = self._check_maturity()
        self._has_stock = self._check_stock()
        self._func_map = {
            CurveType.Payoff.value: ('payoff', False),
            CurveType.NetPayoff.value: ('net_payoff', False),
            CurveType.PnL.value: ('pnl', True),
            CurveType.PV.value: ('pv', True),
            CurveType.Delta.value: ('delta', True),
            CurveType.Gamma.value: ('gamma', True),
        }

    def gen_curve(self, type_, margin_=20, step_=1, full_=False):
        """generate x (spot / ISP) and y (payoff or) for portfolio payoff curve"""
        _curve_func = [self._comp_sum(type_)]
        _engine = self._func_map[type_][1]
        if full_:
            for _comp in self._components_show:
                _curve_func.append(_comp.__getattribute__(self._func_map[type_][0]))

        _x = self._x_range(margin_, step_)
        _y = []
        for _spot in _x:
            _mkt = deepcopy(self.mkt_data)
            _mkt[EnvParam.UdSpotForPrice.value] = _spot
            _input = (_mkt, self.engine) if _engine else (_mkt, )
            _y.append([_func(*_input) for _func in _curve_func])
        _y = transpose(_y)
        return _x, _y

    def set_show(self, inst_show_):
        """set components that be plotted with portfolio"""
        self._components_show = list(set(inst_show_) - set(self._components))

    def set_mkt(self, mkt_data_):
        """set market data"""
        self.mkt_data = mkt_data_

    def set_engine(self, engine_):
        """set pricing engine"""
        self.engine = engine_

    def maturity(self):
        """return common maturity of portfolio"""
        return self._maturity

    def center(self):
        """return plotting center"""
        return self._center

    def has_stock(self):
        """return if the portfolio contains stock"""
        return self._has_stock

    @property
    def mkt_data(self):
        """market data"""
        if self._mkt_data is None:
            raise ValueError("market data not specified")
        return self._mkt_data

    @mkt_data.setter
    def mkt_data(self, mkt_data_):
        self._mkt_data = mkt_data_

    @property
    def engine(self):
        """pricing engine"""
        if self._engine is None:
            raise ValueError("pricing engine not specified")
        return self._engine

    @engine.setter
    def engine(self, engine_):
        self._engine = engine_

    def _comp_sum(self, value_type_):
        def _sum_func(*args):
            return sum([_comp.__getattribute__(self._func_map[value_type_][0])(*args) for _comp in self._components])
        return _sum_func

    def _x_range(self, margin_, step_):
        _strike_list = [_comp.strike for _comp in self._components if _comp.type in option_type]
        _min = min(_strike_list) if _strike_list else self._center
        _max = max(_strike_list) if _strike_list else self._center
        _dist = max([self._center - _min, _max - self._center])
        _x = arange(max(self._center - _dist - margin_, 0), self._center + _dist + margin_ + step_, step_)
        return _x

    def _check_maturity(self):
        _maturity = set([_comp.maturity for _comp in self._components if _comp.type in option_type])
        if len(_maturity) > 1:
            raise ValueError("maturity of all components should be same")
        return _maturity.pop() if len(_maturity) == 1 else 0

    def _check_stock(self):
        return len(list(filter(lambda x: x.type == InstType.Stock.value, self._components))) > 0
