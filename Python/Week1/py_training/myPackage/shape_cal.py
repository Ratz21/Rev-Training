"""   Area Circumference"""
from math import pi
#package vs module so math is a module
def area_of_square(side):
    """
    Area of Square
    :param side: side of square
    :return: Area
    """
    return side * side
def area_of_circle(rad):
    """
    Area of Square
    :param : Side of Circle
    :return:
    """
    return pi * rad * rad

def area_of_rect(leng,brd): # this is local variable
    return leng * brd

def cir_of_circle(rad):
    return 2 * pi * rad
