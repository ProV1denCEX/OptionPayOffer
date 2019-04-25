# coding=utf-8
"""definition of stock for payoff estimation and pricing"""

from instrument import Instrument
from instrument.env_param import EnvParam
# from numpy.ma import exp


class Stock(Instrument):
    """stock class with basic parameters"""
    _name = "stock"

    def __init__(self, inst_dict_):
        super(Stock, self).__init__(inst_dict_)

    def payoff(self, mkt_dict_):
        """get stock payoff for given spot"""
        _spot = self._load_market(mkt_dict_, [EnvParam.UdSpotForPrice.value])[0]
        return _spot * self.unit

    def pv(self, mkt_dict_, engine_, unit_=None):
        """no pv calc needed for stock"""
        # _div, _t = tuple(self._load_market(mkt_dict_, [EnvParam.UdDivYieldRatio.value, EnvParam.PortMaturity.value]))
        _unit = unit_ or self.unit
        _spot = self._load_market(mkt_dict_, [EnvParam.UdSpotForPrice.value])[0]
        return _spot * _unit  # * exp(-_div * _t)

    def delta(self, mkt_dict_, engine_, unit_=None):
        """no delta calc needed for stock"""
        _unit = unit_ or self.unit
        return 1 * _unit

    def gamma(self, mkt_dict_, engine_, unit_=None):
        """no gamma calc needed for stock"""
        _unit = unit_ or self.unit
        return 0 * _unit
