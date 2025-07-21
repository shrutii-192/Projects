
from langchain.tools import tool

@tool
def Addition(a:int,b:int)->int:
    """addition of two integer
    Args:
    a(int): The first integer
    b(int): the second integer
    return:
    int: the result of addition
    
    """
    return a+b

@tool
def Multiply(a:int,b:int)->int:
    """Multiplication of two integer
    Args:
    a(int): The first integer
    b(int): the second integer
    return:
    int: the result of Multiplication
    
    """
    return a*b

@tool
def Divide(a:int,b:int)->int:
    """Division of two integer
    Args:
    a(int): The first integer
    b(int): the second integer
    return:
    float: the result of Division
    
    """
    return a/b

@tool
def Percentage(a:int,b:int)->int:
    """percentage of two integer
    Args:
    a(int): The first integer
    b(int): the second integer
    return:
    float: the result of percentage (a% of b.)
    
    """
    return b*(a/100)



@tool
def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculates the discount amount given the original price and discount percent.

    Args:
        price (float): The original price of the item.
        discount_percent (float): The discount percentage to apply (e.g., 20 for 20%).

    Returns:
        float: The discount amount.
    """
    return price * (discount_percent / 100)

@tool
def final_price_after_discount(price: float, discount_percent: float) -> float:
    """
    Calculates the final price after applying the discount.

    Args:
        price (float): The original price of the item.
        discount_percent (float): The discount percentage.

    Returns:
        float: The final price after discount.
    """
    return price - (price * discount_percent / 100)