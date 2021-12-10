# -*- coding: utf-8 -*-
"""
State Model Abstract
====================
Modified: 2021-11

Dependencies:
-------------
```
```
Copyright © 2021 Incuvers. All rights reserved.
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

import logging
from typing import Any, Dict, Union
from abc import ABC, abstractmethod

_PKey = Union[int, str]


class StateModel(ABC):

    def __init__(self, _id: _PKey) -> None:
        self._logger = logging.getLogger(__name__)
        self.id = _id

    def __eq__(self, o: object) -> bool:
        if hasattr(o, 'id') and hasattr(self, 'id'):
            return o.id == self.id  # type: ignore
        return False

    @property
    def id(self) -> _PKey:
        """
        Get state model id
        :return: state model id
        :rtype: _PKey
        """
        return self.__id

    @id.setter
    def id(self, _id: _PKey) -> None:
        """
        Set state model id
        :param _id: state model id 
        :type _id: _PKey
        """
        self.__id = _id

    @abstractmethod
    def serialize(self) -> Dict[str, Any]: ...

    @abstractmethod
    def deserialize(self, **kwargs) -> None: ...
