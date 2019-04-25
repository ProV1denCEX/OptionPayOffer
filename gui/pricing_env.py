# coding=utf-8
"""pricing env dialog"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QButtonGroup, QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit
from copy import deepcopy
from enum import Enum
from gui.custom import CustomRadioButton
from instrument.default_param import env_default_param
from instrument.env_param import EngineMethod, EngineParam, EnvParam, RateFormat
from utils import float_int


class FieldType(Enum):
    """Field type"""
    String = 0
    Number = 1
    Radio = 2


fixed_width = 180

env_param = [
    (FieldType.Number.value, EnvParam.RiskFreeRate.value, "Annual Risk Free Rate (%):", fixed_width,
     None, None, None),
    (FieldType.Number.value, EnvParam.UdVolatility.value, "Ud Volatility (%):", fixed_width,
     None, None, None),
    (FieldType.Number.value, EnvParam.UdDivYieldRatio.value, "Ud Dividend Yield (%):", fixed_width,
     None, None, None),
    (FieldType.Number.value, EnvParam.UdSpotForPrice.value, "Ud Spot for Pricing:", fixed_width,
     None, None, None),
    (FieldType.Number.value, EnvParam.PortMaturity.value, "Time to Maturity (Y):", fixed_width,
     None, None, None),
    (FieldType.Number.value, EnvParam.CostRounding.value, "Instrument Cost Rounding:", fixed_width,
     None, None, None),
    (FieldType.Radio.value, EnvParam.RateFormat.value, "Input Rate Format:", fixed_width,
     [_r.value for _r in RateFormat], None, None),
    (FieldType.Radio.value, EnvParam.PricingEngine.value, "Pricing Engine:", fixed_width,
     [_e.value for _e in EngineMethod], None, None),
    (FieldType.Number.value, EngineParam.MCIteration.value, "Monte-Carlo Iterations:", fixed_width,
     None, EnvParam.PricingEngine.value, EngineMethod.MC.value),
]


class PricingEnv(QDialog):
    """
    dialog for editing pricing environment parameters
    included paramters should be all defined above - env_param
    """
    def __init__(self, parent_, *args, **kwargs):
        super(PricingEnv, self).__init__(*args, **kwargs)
        self._parent = parent_
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Pricing Env")
        # initialize basic widgets
        self._main_layout = QVBoxLayout(self)
        # setup and show
        self.setup_ui()
        self.setLayout(self._main_layout)
        self.show()

    def setup_ui(self):
        """setup all parameter input widget and buttons"""
        for _param in env_param:
            self._add_param(_param)
        _btn = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Reset)
        _btn.button(QDialogButtonBox.Ok).autoDefault()
        _btn.button(QDialogButtonBox.Reset).clicked.connect(self._on_reset)
        _btn.accepted.connect(self._on_ok)
        _btn.rejected.connect(self.reject)
        self._main_layout.addWidget(_btn)

    def _add_param(self, param_):
        if param_[0] in [FieldType.String.value, FieldType.Number.value]:
            _hbox = QHBoxLayout()
            _label = QLabel(param_[2])
            _label.setFixedWidth(param_[3])
            _hbox.addWidget(_label)
            _wgt = QLineEdit(self)
            _wgt.setAlignment(Qt.AlignRight)
            _default = self._parent.env_data.get(param_[1])
            if _default is not None:
                _wgt.setText(str(_default))
            self.__setattr__(param_[1], _wgt)
            _hbox.addWidget(_wgt)
            self._main_layout.addLayout(_hbox)

            if param_[5] is not None:
                try:
                    _grand_parent = self.__getattribute__(param_[5])
                    for _btn in _grand_parent.buttons():
                        _btn.changed.connect(self._radio_connection)
                        if not hasattr(_btn, 'param'):
                            _btn.__setattr__('param', [])

                    _parent = self.__getattribute__(param_[6])
                    _parent.param.append(param_[1])
                    _parent.__setattr__(param_[1], _wgt)
                    _wgt.setEnabled(_parent.isChecked())

                except AttributeError as e:
                    raise Exception(str(e))

        elif param_[0] == FieldType.Radio.value:
            _vbox = QVBoxLayout()
            _label = QLabel(param_[2])
            _label.setFixedWidth(param_[3])
            _vbox.addWidget(_label)
            _hbox = QHBoxLayout()
            _btn_group = QButtonGroup()
            self.__setattr__(param_[1], _btn_group)
            _range = param_[4]
            for _idx, _item in enumerate(_range):
                _wgt = CustomRadioButton(_item, _item, self)
                self.__setattr__(_item, _wgt)
                _hbox.addWidget(_wgt)
                _btn_group.addButton(_wgt, _idx)
            _vbox.addLayout(_hbox)
            self._main_layout.addLayout(_vbox)
            _default = self._parent.env_data.get(param_[1])
            self.__getattribute__(_default).setChecked(True)

    def _radio_connection(self, wgt_name_):
        _wgt = self.__getattribute__(wgt_name_)
        for _param in _wgt.param:
            _child = _wgt.__getattribute__(_param)
            _child.setEnabled(_wgt.isChecked())

    def _on_ok(self):
        _env = dict()
        for _param in env_param:
            _env[_param[1]] = self._get_wgt_value(_param[1], _param[0], _param[4])

        self._parent.env_data = _env
        self.accept()

    def _on_reset(self):
        for _param in env_param:
            self._set_wgt_value(_param[1], _param[0], env_default_param[_param[1]])

    def _set_wgt_value(self, wgt_name_, wgt_type_, value_):
        _wgt = self.__getattribute__(wgt_name_)
        if wgt_type_ in [FieldType.String.value, FieldType.Number.value]:
            _wgt.setText(str(value_))
        elif wgt_type_ == FieldType.Radio.value:
            for _btn in _wgt.buttons():
                if _btn.name() == value_:
                    _btn.setChecked(True)
        else:
            raise ValueError("invalid widget type {}".format(wgt_type_))

    def _get_wgt_value(self, wgt_name_, wgt_type_, *args):
        _wgt = self.__getattribute__(wgt_name_)
        if wgt_type_ == FieldType.String.value:
            return _wgt.text()
        elif wgt_type_ == FieldType.Number.value:
            return float_int(_wgt.text())
        elif wgt_type_ == FieldType.Radio.value:
            _range = args[0]
            return _range[_wgt.checkedId()]
        else:
            return None


def parse_env(env_param_):
    """parse environment data into market, engine, and rounding"""
    _mkt = deepcopy(env_param_)
    _engine = dict(engine=_mkt.pop(EnvParam.PricingEngine.value), param={})
    for _engine_param in [_param for _param in env_param if _param[5] == EnvParam.PricingEngine.value]:
        _engine['param'][_engine_param[1]] = _mkt.pop(_engine_param[1])
    _rounding = _mkt.pop(EnvParam.CostRounding.value)
    return _mkt, _engine, _rounding
