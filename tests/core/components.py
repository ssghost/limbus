"""Components used in the tests."""
from typing import Any, List
import asyncio

import torch

from limbus.core import Params, Component, ComponentState
from limbus.widgets import BaseWidgetComponent
from limbus import widgets


class Stack(Component):
    """Stacks a list of tensors."""
    def __init__(self, name: str):
        super().__init__(name)

    @staticmethod
    def register_inputs(inputs: Params) -> None:  # noqa: D102
        inputs.declare("dim", int, value=0)
        inputs.declare("tensors", List[torch.Tensor])

    @staticmethod
    def register_outputs(outputs: Params) -> None:  # noqa: D102
        outputs.declare("out", torch.Tensor)

    async def forward(self) -> ComponentState:  # noqa: D102
        dim, inp = await asyncio.gather(self._inputs.dim.receive(), self._inputs.tensors.receive())
        out = torch.stack(inp, dim=dim)
        await self._outputs.out.send(out)
        return ComponentState.OK


class Unbind(Component):
    """Stacks a list of tensors."""
    def __init__(self, name: str):
        super().__init__(name)

    @staticmethod
    def register_inputs(inputs: Params) -> None:  # noqa: D102
        inputs.declare("dim", int, value=0)
        inputs.declare("input", torch.Tensor)

    @staticmethod
    def register_outputs(outputs: Params) -> None:  # noqa: D102
        outputs.declare("out", List[torch.Tensor])

    async def forward(self) -> ComponentState:  # noqa: D102
        dim, inp = await asyncio.gather(self._inputs.dim.receive(), self._inputs.input.receive())
        out = list(torch.unbind(inp, dim=dim))
        await self._outputs.out.send(out)
        return ComponentState.OK


class Constant(Component):
    """Constant component."""
    def __init__(self, name: str, value: Any):
        super().__init__(name)
        self._value = value

    @staticmethod
    def register_outputs(outputs: Params) -> None:  # noqa: D102
        outputs.declare("out", Any, arg="value")

    async def forward(self) -> ComponentState:  # noqa: D102
        # TODO: next line could be autogenerated since in register_inputs() we are already linking both.
        await self._outputs.out.send(self._value)
        return ComponentState.OK


class Printer(BaseWidgetComponent):
    """Prints the input to the console."""
    @staticmethod
    def register_properties(properties: Params) -> None:  # noqa: D102
        # this line is like super() but for static methods.
        BaseWidgetComponent.register_properties(properties)  # adds the title param
        properties.declare("append", bool, value=False)

    @staticmethod
    def register_inputs(inputs: Params) -> None:  # noqa: D102
        inputs.declare("inp", Any)

    async def _show(self, title: str) -> None:  # noqa: D102
        widgets.get().show_text(self, title,
                                str(await self._inputs.inp.receive()),
                                append=self._properties.get_param("append"))


class Adder(Component):
    """Add two numbers."""
    def __init__(self, name: str):
        super().__init__(name)

    @staticmethod
    def register_inputs(inputs: Params) -> None:  # noqa: D102
        inputs.declare("a", torch.Tensor)
        inputs.declare("b", torch.Tensor)

    @staticmethod
    def register_outputs(outputs: Params) -> None:  # noqa: D102
        outputs.declare("out", torch.Tensor)

    async def forward(self) -> ComponentState:  # noqa: D102
        a, b = await asyncio.gather(self._inputs.a.receive(), self._inputs.b.receive())
        await self._outputs.out.send(a + b)
        return ComponentState.OK
