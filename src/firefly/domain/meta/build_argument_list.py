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

import inspect
import typing
import firefly.domain as ffd

# __pragma__('skip')
from dataclasses import is_dataclass, fields
from abc import ABC
# __pragma__('noskip')
# __pragma__ ('ecom')
"""?
from firefly.ui.web.polyfills import is_dataclass, fields
?"""
# __pragma__ ('noecom')


def build_argument_list(params: dict, obj: typing.Union[typing.Callable, type]):
    args = {}
    field_dict = {}
    is_dc = False

    if is_dataclass(obj):
        is_dc = True
        field_dict = {}
        # noinspection PyDataclass
        for field_ in fields(obj):
            field_dict[field_.name] = field_
        sig = inspect.signature(obj.__init__)
        types = typing.get_type_hints(obj)
    elif isinstance(obj, type):
        sig = inspect.signature(obj.__init__)
        types = typing.get_type_hints(obj.__init__)
    else:
        sig = inspect.signature(obj)
        try:
            types = typing.get_type_hints(obj)
        except NameError:
            types = obj.__annotations__

    for param in sig.parameters.values():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return params

    for name, param in sig.parameters.items():
        if name == 'self' or param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue

        required = False
        if is_dc:
            required = field_dict[name].metadata.get('required', False) is True
        elif param.default is not None:
            required = True

        type_ = types[name] if name in types else None
        if isinstance(type_, type) and issubclass(type_, ffd.Entity):
            entity_args = build_argument_list(params, type_)
            args[name] = type_(**entity_args)
            for key in entity_args.keys():
                if key != type_.id_name():
                    del params[key]
                    if key in args:
                        del args[key]
        elif name in params:
            args[name] = params[name]
        elif name.endswith('_') and name.rstrip('_') in params:
            args[name] = params[name.rstrip('_')]
        elif required is True:
            raise ffd.MissingArgument(f'Argument: {name} is required')

    return args
