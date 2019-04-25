# coding=utf-8
"""common utility functions"""

from numpy.ma import log

PRECISION_ZERO = 10 ** -3


def float_int(string_):
    """convert string to int or float according to its real feature"""
    try:
        _number = float(string_)
        return _number if _number % 1 else int(_number)
    except ValueError:
        return None


def to_continuous_rate(rate_):
    """shift discrete rate to continuous rate"""
    return log(1 + rate_)


def parse_kwargs(kwargs_, parse_list_, alternative_=None):
    """parse kwargs with given parse keys"""
    return tuple([kwargs_.get(_key, alternative_) for _key in parse_list_])
