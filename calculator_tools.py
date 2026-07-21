from agents import function_tool

import math


@function_tool
def add(a: float, b: float) -> float:
    print("add tool called")
    return a + b


@function_tool
def subtract(a: float, b: float) -> float:
    print("subtract tool called")
    return a - b


@function_tool
def multiply(a: float, b: float) -> float:
    print("multiply tool called")
    return a * b


@function_tool
def divide(a: float, b: float) -> float:
    print("divide tool called")
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


@function_tool
def mod(a: int, b: int) -> int:
    print("mod tool called")
    return a % b


@function_tool
def power(base: float, exponent: float) -> float:
    print("power tool called")
    return base ** exponent


@function_tool
def root(value: float, degree: float = 2) -> float:
    print("root tool called")
    if degree == 0:
        raise ValueError("Root degree cannot be zero.")
    return value ** (1 / degree)