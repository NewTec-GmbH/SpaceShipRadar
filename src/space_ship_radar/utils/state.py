"""State and Context

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

from __future__ import annotations
from abc import ABC, abstractmethod

# Variables ********************************************************************

# Classes **********************************************************************

# example from: https://refactoring.guru/design-patterns/state/python/example


class Context:
    """Context"""

    _state = None

    def __init__(self, state: State) -> None:
        self.transition_to(state)
        self._name = "State"

    @property
    def name(self) -> str:
        """getter for the state name"""
        return self._name

    def transition_to(self, state: State):
        """
        The Context allows changing the State object at runtime.
        """
        self._state = state
        self._state.context = self
        print(state.name)

    def update(self, camera):
        """
        The Context delegates part of its behavior to the current State object.
        """
        self._state.run(camera)


class State(ABC):
    """State"""

    @property
    def context(self) -> Context:
        """getter for context property"""
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def run(self, camera) -> None:
        """run method of state"""

# Functions ********************************************************************

# Main *************************************************************************
