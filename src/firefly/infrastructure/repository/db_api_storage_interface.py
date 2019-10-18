from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

import firefly.domain as ffd
import inflection


class DbApiStorageInterface(ABC):
    def __init__(self, name: str, config: dict):
        self.name = name
        self._config = config
        self._tables_checked = []

    def disconnect(self):
        self._disconnect()

    @abstractmethod
    def _disconnect(self):
        pass

    def add(self, entity: ffd.Entity):
        self._check_prerequisites(entity.__class__)
        self._add(entity)

    @abstractmethod
    def _add(self, entity: ffd.Entity):
        pass

    def all(self, entity_type: Type[ffd.Entity], criteria: ffd.BinaryOp = None, limit: int = None):
        self._check_prerequisites(entity_type)
        return self._all(entity_type, criteria, limit)

    @abstractmethod
    def _all(self, entity_type: Type[ffd.Entity], criteria: ffd.BinaryOp = None, limit: int = None):
        pass

    def find(self, uuid: str, entity_type: Type[ffd.Entity]):
        self._check_prerequisites(entity_type)
        return self._find(uuid, entity_type)

    @abstractmethod
    def _find(self, uuid: str, entity_type: Type[ffd.Entity]):
        pass

    def remove(self, entity: ffd.Entity):
        self._check_prerequisites(entity.__class__)
        self._remove(entity)

    @abstractmethod
    def _remove(self, entity: ffd.Entity):
        pass

    def update(self, entity: ffd.Entity):
        self._check_prerequisites(entity.__class__)
        self._update(entity)

    @abstractmethod
    def _update(self, entity: ffd.Entity):
        pass

    @abstractmethod
    def _ensure_connected(self):
        pass

    @abstractmethod
    def _ensure_table_created(self, entity: Type[ffd.Entity]):
        pass

    @staticmethod
    def _fqtn(entity: Type[ffd.Entity]):
        return f'{entity.get_class_context()}.{inflection.tableize(entity.__name__)}'

    def _check_prerequisites(self, entity: Type[ffd.Entity]):
        self._ensure_connected()
        if entity not in self._tables_checked:
            self._ensure_table_created(entity)
            self._tables_checked.append(entity)
