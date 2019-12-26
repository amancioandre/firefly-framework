#  Copyright (c) 2019 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.

from __future__ import annotations

# __pragma__('skip')
from abc import ABCMeta

from dataclasses import dataclass

# __pragma__('noskip')
# __pragma__('ecom')
"""?
from firefly.ui.web.polyfills import ABCMeta, dataclass, optional
?"""
# __pragma__('noecom')

import firefly.domain as ffd


# __pragma__('kwargs')
class MessageMeta(ABCMeta):
    def __new__(mcs, name, bases, dct, **kwargs):
        if 'fields_' in kwargs and 'annotations_' in kwargs:
            for k, v in kwargs['fields_'].items():
                dct[k] = ffd.optional(default=v)
            if '__annotations__' in dct:
                dct['__annotations__'].update(kwargs['annotations_'])
            else:
                dct['__annotations__'] = kwargs['annotations_']

        ret = type.__new__(mcs, name, bases, dct)

        return dataclass(ret, eq=False, repr=False)
# __pragma__('nokwargs')
