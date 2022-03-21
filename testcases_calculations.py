"""Test functions for calculations.py to ensure correctness"""

from calculations import *
import numpy as np

def t_binsearch():
    """Test cases for binary search algorithm. Returns False if any testcases fail and True otherwise"""
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    b = [1.12, 2.13, 3.14, 4.25, 5.65, 6.98, 7.01, 8.67, 9.82, 10.0]
    if not binsearch(5, a, len(a)-1, 0) == 4:
        return False

    elif binsearch(1, a, len(a)-1, 0) is not None:
        return False

    elif not binsearch(4, b, len(b)-1, 0) == b.index(4.25):
        return False
    elif not binsearch(6, b, len(b)-1, 0) == b.index(5.65):
        return False
    else:
        return True

def test_integration():
    """Try to integrate sin(x)^2 from 0 to pi and then from pi to 2*pi and divide those areas.
    If result is close to one integration method works"""
    x = [0.002*math.pi*i for i in range(-10, 1050)]
    y = [(math.sin(elem))**2 for elem in x]
    Carb = Index(x, y, "test", "sin")
    if not Carb.CI-1 < 0.0001:  # error is smaller than 0.0001
        return False

    y2 = [math.exp(elem) for elem in x]
    C2 = Index(x, y2, "test", "exp")
    if not C2.CI-(np.e-1)/((np.e)**3-(np.e)**2) < 0.0001:
        return False









def main():
    assert t_binsearch() == True
    assert test_integration() == True





if __name__ == '__main__':
    main()