# coding=utf-8
"""help doc"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPlainTextEdit, QTabWidget, QVBoxLayout

help_content = [
    ("Inst Params", """1. Strike - strike price of an OPTION

2. Qty - unit of each instrument
    * could be a FLOAT number
    * could be NEGATIVE indicating SHORT position

3. Premium - unit cost / premium of an OPTION"""),

    ("Curve Types", """From portfolio view:
1. Payoff Curve
    * portfolio payoff at maturity
2. PV Curve
    * portfolio current PV
3. Delta Curve
    * portfolio current Delta
4. Gamma Curve
    * portfolio current Gamma
    * Monte-Carlo is not recommended

From investment view:
1. Net Payoff Curve
    * portfolio payoff at maturity minus portfolio cost
2. PnL Curve
    * portfolio current PnL
    * portfolio PV minus portfolio cost"""),

    ("Pricing Tips", """1. Right click an OPTION for auto pricing
    * right click on the target line

2. Edit pricing env in Menu - Config - Pricing Env

3. Plotting for portfolios with STOCK may become confusing 
    when dividend yield is not zero.
    Because of the difference between STOCK and FORWARD, 
    STOCK cannot be used to hedge OPTION directly according 
    to the DELTA curve."""),

    ("Pricing Params", """1. Annual Risk Free Rate (%, default 3)
2. Underlying Volatility (%, default 30)
3. Dividend Yield Ratio (%, default 0)
4. Portfolio Maturity (y)
5. Cost Rounding (default 2)
6. Rate Format (default Single)
    * Single or Compound (continuous)
    * if Single is chosen, 1 & 3 will shifted via:
    * r_c = (ln(1 + r / 100) - 1) * 100
7. Pricing Engine (default Black-Scholes)
    * Black-Scholes or Monte-Carlo""")
]


class HelpDialog(QDialog):
    """help doc dialog"""
    def __init__(self, parent_, *args, **kwargs):
        self._parent = parent_
        super(HelpDialog, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Help")
        # initialize basic widgets
        self._main_layout = QVBoxLayout(self)
        # setup and show
        self.setup_ui()
        self.setLayout(self._main_layout)
        self.show()

    def setup_ui(self):
        """setup all ui components"""
        _tab = QTabWidget()
        for _content in help_content:
            _wgt = QPlainTextEdit(_content[1])
            _wgt.setFocusPolicy(Qt.NoFocus)
            _tab.addTab(_wgt, _content[0])
        self._main_layout.addWidget(_tab)
        _btn = QDialogButtonBox(QDialogButtonBox.Ok)
        _btn.button(QDialogButtonBox.Ok).setDefault(True)
        _btn.accepted.connect(self.accept)
        self._main_layout.addWidget(_btn)
