"""
Module for Interest calculation
"""


def simple_interest_calc(prin, ny , roi):# principle number of yrs rate of interest
    """
     calculating SI
    :param prin :
    :param ny :
    :param roi :
    :return:
    """
    si = prin * ny * roi/100
    amount = prin + si
    return si , amount

def comp_interest_calc(prin , ny , roi):
    """
    Calculating comp interest
    :param prin: Principal amt
    :param ny: no of yrs
    :param roi: rate of interest
    :return: total amt
    """
    amount = prin *  (1+ (roi/ 100)) ** (1*ny) # float div
    return amount
