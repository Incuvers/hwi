# -*- coding: utf-8 -*-
"""
Event Types
===========
Modified: 2021-04

Namespace to store the system event types

Dependencies:
-------------
```
from typing import Any, Callable, Dict, Union
from hwi.events.event import Event
from hwi.events.pipeline import Pipeline
```
Copyright © 2021 Incuvers. All rights reserved.
"""

from typing import Any, Callable, Dict, Union
from hwi.events.event import Event


class Registry:
    """
    Interpreting Typing schema:
    Callable[[argtype], rtype]
    """
    # arduino commands
    aux_duty = Event[Callable[[str, Union[float, int]], None]]('AUX_DUTY')
    op_mode = Event[Callable[[str, Union[float, int]], None]]('OP_MODE')
    fan_duty = Event[Callable[[str, Union[float, int]], None]]('FAN_DUTY')
    co2_calibration = Event[Callable[[], None]]('CO2_CALIBRATION')
    # AMQP events
    amqp_publish = Event[Callable[[str, Dict[str, Any]], None]]('AMQP_PUBLISH')
