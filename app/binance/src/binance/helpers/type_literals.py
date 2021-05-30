"""
Collection of type literals.

Date: 2021-05-25
Author: Vitali Lupusor
"""

# Import standard modules
from typing import Literal

OrderBookLimit = Literal[5, 10, 20, 50, 100, 500, 1000, 5000]
KlineInterval = Literal[
    '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d',
    '3d', '1w', '1M'
]
TypeOptions = Literal[
    'LIMIT', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT',
    'TAKE_PROFIT_LIMIT', 'LIMIT_MAKER'
]
ResponseTypeOptions = Literal['ACK', 'RESULT', 'FULL']

del(Literal)
