from abc import ABC, abstractmethod
from enum import Enum
from .tokens.token import Token

class FSAState(Enum):
  def __str__(self):
    return str(self.value)

  def __eq__(self, other):
    if isinstance(other, str):
      return self.value == other

    if isinstance(other, FSAState):
      return self is other

    return False

class FSA(ABC):
  @abstractmethod
  def get_state(self) -> FSAState: pass

  @abstractmethod
  def read_char(self, ch: str) -> None: pass

  @abstractmethod
  def read_eof(self) -> None: pass

  @abstractmethod
  def reset(self) -> None: pass

  @abstractmethod
  def get_token(self) -> Token: pass

