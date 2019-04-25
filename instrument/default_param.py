# coding=utf-8
"""default value of all parameters"""

from gui.plot import PlotParam
from instrument import InstParam, InstType
from instrument.env_param import EnvParam, EngineMethod, EngineParam, RateFormat


default_param = {
    InstType.CallOption.value: {
        InstParam.InstUnit.value: 1,
        InstParam.InstCost.value: 0,
        InstParam.OptionStrike.value: EnvParam.UdSpotForPrice.value,
        PlotParam.Show.value: False,
    },
    InstType.PutOption.value: {
        InstParam.InstUnit.value: 1,
        InstParam.InstCost.value: 0,
        InstParam.OptionStrike.value: EnvParam.UdSpotForPrice.value,
        PlotParam.Show.value: False,
    },
    InstType.Stock.value: {
        InstParam.InstUnit.value: 1,
        InstParam.InstCost.value: EnvParam.UdSpotForPrice.value,
        PlotParam.Show.value: False,
    }
}

default_type = InstType.CallOption.value

env_default_param = {
    EnvParam.RiskFreeRate.value: 3,
    EnvParam.UdVolatility.value: 30,
    EnvParam.UdDivYieldRatio.value: 0,
    EnvParam.UdSpotForPrice.value: 100,
    EnvParam.PortMaturity.value: 1,
    EnvParam.CostRounding.value: 2,
    EnvParam.RateFormat.value: RateFormat.Single.value,
    EnvParam.PricingEngine.value: EngineMethod.BS.value,
    EngineParam.MCIteration.value: 1000000,
}
