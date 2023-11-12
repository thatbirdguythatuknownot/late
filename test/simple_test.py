import inspect
from typing import Any

from late import latebinding, __, _LateBound


def test_with_list():

    @latebinding
    def f(x: list[Any] = __([])) -> list[Any]:
        x.append(1)
        return x

    assert f() == [1]
    assert f() == [1]
    assert f() == [1]

    @latebinding
    def f(x: list[list[Any]] = __([[]])) -> list[list[Any]]:
        x[0].append(1)
        return x

    assert f() == [[1]]
    assert f() == [[1]]
    assert f() == [[1]]


def test_immutable():
    @latebinding
    def f(x: frozenset[Any] = __(frozenset()), y: set = __(set())):
        return

    param = inspect.signature(f).parameters['x']
    assert type(param.default) is frozenset
    param = inspect.signature(f).parameters['y']
    assert type(param.default) is _LateBound


def test_count():
    t = 0

    def a() -> int:
        nonlocal t
        t += 1
        return t

    @latebinding
    def f(x: int = __(a())) -> int:
        return 2 * x

    assert f() == 2
    assert f() == 4
