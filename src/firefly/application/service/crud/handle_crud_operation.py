from __future__ import annotations

from dataclasses import asdict
from typing import Callable

import firefly.domain as ffd
import firefly.application.service.crud as crud
import inflection


@ffd.query_handler()
@ffd.command_handler()
class HandleCrudOperation(ffd.Middleware):
    _registry: ffd.Registry = None

    def __call__(self, message: ffd.Message, next_: Callable) -> ffd.Message:
        if isinstance(message, (ffd.CrudCommand, ffd.CrudQuery)):
            entity_type = ffd.load_class(message.headers['entity_fqn'])

            class CrudOperation(self._generic_operation(message.headers['operation'])[entity_type]):
                pass
            handle = CrudOperation()
            handle._registry = self._registry

            return next_(handle(_message=message, **asdict(message)))

        return next_(message)

    @staticmethod
    def _generic_operation(operation: str):
        return getattr(crud, '{}Entity'.format(inflection.camelize(operation, uppercase_first_letter=True)))