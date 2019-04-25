# coding=utf-8
"""definition of base instrument"""

from enum import Enum
from numpy.ma import exp
from instrument.env_param import EngineMethod, EngineParam, EnvParam, RateFormat
from utils import to_continuous_rate


class InstParam(Enum):
    """instrument parameters"""
    InstISP = 'InstISP'
    InstType = 'InstType'
    InstUnit = 'InstUnit'
    InstCost = 'InstCost'
    OptionType = 'OptionType'
    OptionStrike = 'OptionStrike'
    OptionMaturity = 'OptionMaturity'


class InstType(Enum):
    """instrument type"""
    CallOption = 'CALL'
    PutOption = 'PUT'
    Stock = 'STOCK'


option_type = [InstType.CallOption.value, InstType.PutOption.value]


class Instrument(object):
    """
    financial instrument class
    use class method - get_inst to get correct type of instrument
    """
    _name = "instrument"
    _inst_dict = None
    _type = None
    _unit = None
    _price = None

    def __init__(self, inst_dict_):
        self._inst_dict = inst_dict_
        self.type = inst_dict_.get(InstParam.InstType.value)
        self.unit = inst_dict_.get(InstParam.InstUnit.value)
        self.price = inst_dict_.get(InstParam.InstCost.value)

    def __str__(self):
        return "{} * {}".format(self.unit, self.type)

    @classmethod
    def get_inst(cls, inst_dict_):
        """get instrument through instrument dictionary"""
        type_ = inst_dict_.get(InstParam.InstType.value)
        if type_ in option_type:
            from instrument.option import Option
            return Option(inst_dict_)
        elif type_ == InstType.Stock.value:
            from instrument.stock import Stock
            return Stock(inst_dict_)
        if type_ is None:
            raise ValueError("instrument type not specified")

    def payoff(self, mkt_dict_):
        """get instrument payoff for given spot"""
        raise NotImplementedError("'payoff' method need to be defined in sub-classes")

    def net_payoff(self, mkt_dict_):
        """get instrument net payoff for given spot"""
        return self.payoff(mkt_dict_) - self.unit * self.price

    def profit_discount(self, mkt_dict_, time_):
        """get instrument pnl for given spot"""
        _rate, _spot = tuple(self._load_market(mkt_dict_, [EnvParam.RiskFreeRate.value, EnvParam.UdSpotForPrice.value]))
        return self.payoff(_spot) * exp(-_rate * time_) - self.unit * self.price

    def pnl(self, mkt_dict_, engine_):
        """get instrument pnl for given spot"""
        return (self.pv(mkt_dict_, engine_, unit_=1) - self.price) * self.unit

    def pv(self, mkt_dict_, engine_, unit_=None):
        """evaluate instrument PV on given market"""
        raise NotImplementedError("'pv' method need to be defined in sub-classes")

    def delta(self, mkt_dict_, engine_, unit_=None):
        """evaluate instrument DELTA with market data and engine"""
        raise NotImplementedError("'delta' method need to be defined in sub-classes")

    def gamma(self, mkt_dict_, engine_, unit_=None):
        """evaluate instrument GAMMA with market data and engine"""
        raise NotImplementedError("'gamma' method need to be defined in sub-classes")

    @property
    def type(self):
        """instrument type"""
        if self._type is None:
            raise ValueError("{} type not specified".format(self._name))
        return self._type

    @type.setter
    def type(self, type_):
        if type_ not in [_type.value for _type in InstType]:
            raise ValueError("invalid {} type given".format(self._name))
        self._type = type_

    @property
    def unit(self):
        """instrument unit - number of instrument"""
        if self._unit is None:
            raise ValueError("{} unit not specified".format(self._name))
        return self._unit

    @unit.setter
    def unit(self, unit_):
        if unit_ is not None:
            if not isinstance(unit_, (int, float)):
                raise ValueError("type <int> is required for unit, not {}".format(type(unit_)))
            self._unit = unit_

    @property
    def price(self):
        """instrument price"""
        if self._price is None:
            raise ValueError("{} price not specified".format(self._name))
        return self._price

    @price.setter
    def price(self, price_):
        if price_ is not None:
            if not isinstance(price_, (int, float)):
                raise ValueError("type <int> or <float> is required for price, not {}".format(type(price_)))
            self._price = price_

    @staticmethod
    def _load_market(mkt_dict_, load_param_):
        _res = []
        for _param in load_param_:
            _value = mkt_dict_.get(_param)
            if _param in [EnvParam.RiskFreeRate.value, EnvParam.UdVolatility.value, EnvParam.UdDivYieldRatio.value]:
                if not isinstance(_value, (int, float)):
                    raise ValueError("type <int> or <float> is required for {}, not {}".format(_param, type(_value)))
                _value /= 100
            if _param in [EnvParam.RiskFreeRate.value, EnvParam.UdDivYieldRatio.value]:
                _rate_format = mkt_dict_.get(EnvParam.RateFormat.value)
                if _rate_format not in [_r.value for _r in RateFormat]:
                    raise ValueError("invalid rate type given: {}".format(_rate_format))
                if _rate_format == RateFormat.Single.value:
                    _value = to_continuous_rate(_value)
            _res.append(_value)
        return _res
