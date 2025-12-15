"""
Shared Qt typing helpers used by BasedPyright.
These protocol definitions let us keep strict typing without importing Qt.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol, TypedDict


class QtSignalProtocol(Protocol):
    """Minimal interface used from Qt signal instances."""

    def connect(
        self, __slot: Callable[..., Any], *, type: int | None = None
    ) -> Any: ...

    def emit(self, *args: Any, **kwargs: Any) -> Any: ...


class QtSignalFactory(Protocol):
    """Callable used to declare Qt signals."""

    def __call__(self, *args: Any, **kwargs: Any) -> QtSignalProtocol: ...


class QObjectProtocol(Protocol):
    """Subset of QObject we depend on."""

    def __init__(self) -> None: ...


class QWidgetProtocol(QObjectProtocol, Protocol):
    """Subset of QWidget used in this project."""

    def setStyleSheet(self, stylesheet: str) -> None: ...


class QApplicationProtocol(Protocol):
    """Subset of QApplication used in this project."""

    @staticmethod
    def instance() -> QApplicationProtocol | None: ...

    def setStyleSheet(self, stylesheet: str) -> None: ...


QtObjectType = type[QObjectProtocol]
QtWidgetType = type[QWidgetProtocol]
QtApplicationType = type[QApplicationProtocol]


class QtModuleMap(TypedDict):
    """Structure returned by the Qt detector when a framework is available."""

    QObject: QtObjectType
    pyqtSignal: QtSignalFactory
    QApplication: QtApplicationType
    QWidget: QtWidgetType
    version: str
