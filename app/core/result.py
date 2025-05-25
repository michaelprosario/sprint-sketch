from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class Result(Generic[T]):
    """
    A class to represent the result of an operation which can either succeed with a value or fail with an error message.
    This is used throughout the application to handle errors in a consistent way.
    """

    def __init__(self, is_success: bool, value: Optional[T] = None, error_message: str = ""):
        self._is_success = is_success
        self._value = value
        self._error_message = error_message

    @property
    def is_success(self) -> bool:
        return self._is_success

    @property
    def is_failure(self) -> bool:
        return not self._is_success

    @property
    def value(self) -> T:
        if self.is_failure:
            raise ValueError("Cannot access value on a failure result")
        return self._value

    @property
    def error(self) -> str:
        if self.is_success:
            raise ValueError("Cannot access error on a success result")
        return self._error_message

    @staticmethod
    def success(value: T) -> 'Result[T]':
        return Result(True, value)

    @staticmethod
    def failure(error_message: str) -> 'Result[T]':
        return Result(False, None, error_message)
