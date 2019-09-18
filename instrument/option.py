# coding=utf-8
"""definition of option for payoff estimation and pricing"""

from instrument import InstParam, InstType, Instrument, option_type
from instrument.env_param import EngineMethod, EngineParam, EnvParam
from numpy import average, pi
from numpy.ma import exp, log, sqrt
from scipy.stats import norm


class Option(Instrument):
    """
    option class with basic parameters
    only vanilla option is available (barrier is not supported)
    can estimate option payoff under different level of spot
    can evaluate option price under different market using different evaluation engine
    """
    _name = "option"
    _strike = None
    _maturity = None

    def __init__(self, inst_dict_):
        super(Option, self).__init__(inst_dict_)
        self.strike = inst_dict_[InstParam.OptionStrike.value]
        self.maturity = inst_dict_[InstParam.OptionMaturity.value]

    def __str__(self):
        return "{} * {} {}, Maturity {}".format(self.unit, self.strike, self.type, self.maturity)

    def payoff(self, mkt_dict_):
        """get option payoff for given spot"""
        _spot = self._load_market(mkt_dict_, [EnvParam.UdSpotForPrice.value])[0]
        _reference = _spot - self.strike if self.type == InstType.CallOption.value else self.strike - _spot
        return max([_reference, 0]) * self.unit

    def pv(self, mkt_dict_, engine_, unit_=None):
        """calculate option PV with market data and engine"""
        _rate, _spot, _vol, _div, _method, _param, _sign, _strike, _t = self._prepare_risk_data(mkt_dict_, engine_)
        _unit = unit_ or self.unit

        if _method == EngineMethod.BS.value:
            _d1 = (log(_spot / _strike) + (_rate - _div + _vol ** 2 / 2) * _t) / _vol / sqrt(_t)
            _d2 = _d1 - _vol * sqrt(_t)
            return _sign * (_spot * exp(-_div * _t) * norm.cdf(_sign * _d1) -
                            _strike * exp(-_rate * _t) * norm.cdf(_sign * _d2)) * _unit

        elif _method == EngineMethod.MC.value:
            from utils.monte_carlo import MonteCarlo
            _iteration = self._check_iter(_param[EngineParam.MCIteration.value])
            _spot = MonteCarlo.stock_price(_iteration, isp=_spot, rate=_rate, div=_div, vol=_vol, t=_t)
            _price = [max(_sign * (_s - _strike), 0) for _s in _spot]
            return average(_price) * exp(-_rate * _t) * _unit

    def delta(self, mkt_dict_, engine_, unit_=None):
        """calculate option DELTA with market data and engine"""
        _rate, _spot, _vol, _div, _method, _param, _sign, _strike, _t = self._prepare_risk_data(mkt_dict_, engine_)
        _unit = unit_ or self.unit

        if _method == EngineMethod.BS.value:
            _d1 = (log(_spot / _strike) + (_rate + _vol ** 2 / 2) * _t) / _vol / sqrt(_t)
            return _sign * norm.cdf(_sign * _d1) * exp(-_div * _t) * _unit

        elif _method == EngineMethod.MC.value:
            from utils.monte_carlo import MonteCarlo
            _iteration = self._check_iter(_param[EngineParam.MCIteration.value])
            _spot = MonteCarlo.stock_price(_iteration, isp=_spot, rate=_rate, div=_div, vol=_vol, t=_t)
            _step = 0.01
            _delta = [(max(_sign * (_s + _step - _strike), 0) - max(_sign * (_s - _step - _strike), 0)) /
                      (_step * 2) for _s in _spot]
            return average(_delta) * exp(-_rate * _t) * _unit

    def gamma(self, mkt_dict_, engine_, unit_=None):
        """calculate option GAMMA with market data and engine"""
        _rate, _spot, _vol, _div, _method, _param, _sign, _strike, _t = self._prepare_risk_data(mkt_dict_, engine_)
        _unit = unit_ or self.unit

        if _method == EngineMethod.BS.value:
            _d1 = (log(_spot / _strike) + (_rate + _vol ** 2 / 2) * _t) / _vol / sqrt(_t)
            return exp(-_d1 ** 2 / 2) / sqrt(2 * pi) / _spot / _vol / sqrt(_t) * exp(-_div * _t) * _unit

        elif _method == EngineMethod.MC.value:
            from utils.monte_carlo import MonteCarlo
            _iteration = self._check_iter(_param[EngineParam.MCIteration.value])
            _spot = MonteCarlo.stock_price(_iteration, isp=_spot, rate=_rate, div=_div, vol=_vol, t=_t)
            _step = 0.01
            _gamma = [((max(_sign * (_s + 2 * _step - _strike), 0) - max(_sign * (_s - _strike), 0)) -
                      (max(_sign * (_s - _strike), 0) - max(_sign * (_s - 2 * _step - _strike), 0))) /
                      (4 * _step ** 2)
                      for _s in _spot]
            return average(_gamma) * exp(-_rate * _t) * _unit

    @property
    def type(self):
        """option type - CALL or PUT"""
        if self._type is None:
            raise ValueError("{} type not specified".format(self._name))
        return self._type

    @type.setter
    def type(self, type_):
        if type_ not in option_type:
            raise ValueError("invalid {} type given".format(self._name))
        self._type = type_

    @property
    def strike(self):
        """strike level - percentage of ISP"""
        if self._strike is None:
            raise ValueError("strike level not specified")
        return self._strike

    @strike.setter
    def strike(self, strike_):
        if not isinstance(strike_, float) and not isinstance(strike_, int):
            raise ValueError("type <int> or <float> is required for strike level, not {}".format(type(strike_)))
        self._strike = strike_

    @property
    def maturity(self):
        """option maturity - year"""
        if self._maturity is None:
            raise ValueError("maturity not specified")
        return self._maturity

    @maturity.setter
    def maturity(self, maturity_):
        if maturity_ is not None:
            if not isinstance(maturity_, (int, float)):
                raise ValueError("type <int> or <float> is required for maturity, not {}".format(type(maturity_)))
            if maturity_ < 0:
                raise ValueError("non-negative value is required for maturity, not {}".format(maturity_))
            self._maturity = maturity_

    @staticmethod
    def _load_engine(engine_):
        _method = engine_.get('engine')
        if _method not in [_m.value for _m in EngineMethod]:
            raise ValueError("invalid evaluation engine given: {}".format(_method))
        _param = engine_.get('param', {})
        return _method, _param

    @staticmethod
    def _check_iter(iter_num):
        if not iter_num:
            raise ValueError("iteration not specified")
        if not isinstance(iter_num, int):
            raise ValueError("type <int> is required for iteration, not {}".format(type(iter_num)))

        return iter_num

    def _prepare_risk_data(self, mkt_dict_, engine_):
        _load_param = [EnvParam.RiskFreeRate.value, EnvParam.UdSpotForPrice.value, EnvParam.UdVolatility.value,
                       EnvParam.UdDivYieldRatio.value]
        _rate, _spot, _vol, _div = tuple(self._load_market(mkt_dict_, _load_param))
        _method, _param = self._load_engine(engine_)
        _sign = 1 if self.type == InstType.CallOption.value else -1
        return _rate, _spot, _vol, _div, _method, _param, _sign, self.strike, self.maturity


if __name__ == '__main__':
    pass

    # import sys
    #
    # from personal_utils.logger_utils import get_default_logger
    # from personal_utils.time_utils import Timer
    #
    # logger = get_default_logger("option pricing test")
    #
    # callput = InstType.CallOption.value
    # strike = 80
    # spot = 100
    # maturity = 1
    # rate = 2
    # vol = 5
    # iteration = 1000000
    #
    # inst_1 = {
    #     InstParam.InstType.value: callput,
    #     InstParam.OptionStrike.value: strike,
    #     InstParam.OptionMaturity.value: maturity
    # }
    #
    # mkt = {
    #     EnvParam.RiskFreeRate.value: rate,
    #     EnvParam.UdVolatility.value: vol
    # }
    #
    # engine_1 = dict(engine=EngineMethod.BS.value)
    # engine_2 = dict(engine=EngineMethod.MC.value, param={EngineParam.MCIteration.value: iteration})
    #
    # option_1 = Instrument.get_inst(inst_1)
    #
    # _timer = Timer("option pricing: {} {}, {} years, rate {}%, vol {}%".format(
    #     strike, "call" if callput == InstType.CallOption.value else "put", maturity, rate, vol), logger, rounding_=6)
    # price_bs = round(option_1.pv(mkt, engine_1), 6)
    # logger.info("price = {} (Black-Scholes)".format(price_bs))
    # _timer.mark("pricing using Black-Scholes")
    # price_mc = round(option_1.pv(mkt, engine_2), 6)
    # logger.info("price = {} (Monte-Carlo, {} iteration)".format(price_mc, iteration))
    # _timer.mark("pricing using Monte-Carlo with {} iteration".format(iteration))
    # _timer.close()
    #
    # option_1.price = price_bs
    # option_1.unit = 1
    # logger.info("option payoff at spot {}: {}".format(spot, round(option_1.payoff(spot), 6)))
