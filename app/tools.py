from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers, 'a' and 'b'.

    Args:
        a (int): The first integer.
        b (int): The second integer.
    
    Returns:
        int: The product of 'a' and 'b'.
    """
    return a * b


@tool
def square(a: int) -> int:
    """
    Calculates the square of an integer 'a'.

    Args:
        a (int): The integer to square.
    
    Returns:
        int: The squared value of 'a'.
    """
    return a ** 2


# This list will be imported by your agent
all_tools = [multiply, square]
