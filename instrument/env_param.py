# coding=utf-8
"""market and engine parameters"""

from enum import Enum


class EnvParam(Enum):
    """market parameter"""
    RiskFreeRate = 'RiskFreeRate'
    UdVolatility = 'UdVolatility'
    UdDivYieldRatio = 'UdDivYieldRatio'
    UdSpotForPrice = 'UdSpotForPrice'
    PortMaturity = 'PortMaturity'
    CostRounding = 'CostRounding'
    RateFormat = 'RateFormat'
    PricingEngine = 'PricingEngine'


class RateFormat(Enum):
    """Rate format - single or continuously compounded"""
    Single = 'Single'
    Compound = 'Compound'


class EngineMethod(Enum):
    """engine evaluation method"""
    BS = 'Black-Scholes'
    MC = 'Monte-Carlo'


class EngineParam(Enum):
    """engine parameter"""
    MCIteration = 'MCIteration'
