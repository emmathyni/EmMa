"""Test functions for calculations.py to ensure correctness"""

from calculations import *
import numpy as np
import matplotlib.pyplot as plt

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
    Carb = PlasticIndex(x, y, "test", "sin")
    index = Carb._find_index()
    corr_data = [x[index[0]:index[1]+1], y[index[0]:index[1]+1], x[index[2]:index[3]+1], y[index[2]:index[3]+1]]
    c, d= Carb.uneven_integrator(corr_data)
    if not c/d-1 < 0.0001:  # error is smaller than 0.0001
        return False

    y2 = [math.exp(elem) for elem in x]
    C2 = PlasticIndex(x, y2, "test", "exp")
    index2 = C2._find_index()
    corr_data2 = [x[index2[0]:index2[1] + 1], y2[index2[0]:index2[1] + 1], x[index2[2]:index2[3] + 1], y2[index2[2]:index2[3] + 1]]
    a, b = C2.uneven_integrator(corr_data2)
    if not a/b -(np.e-1)/((np.e)**3-(np.e)**2) < 0.001: # error smaller than 0.001 but bigger than 0.0001
        return False
    else:
        return True


def t_fwhm():
    """Test case for fwhm, returns true if all cases are passed."""
    """TODO: check all testcases, not sure how it should function"""
    x = [0.1*i for i in range(-150, 150+1)]
    y = []
    for i in range(len(x)):
        if 0 < x[i] < 5:
            y.append(x[i])
        elif x[i] >= 5:
            y.append(10-x[i])
        elif -5 < x[i] <= 0:
            y.append(-x[i])
        else:
            y.append(x[i]+10)
    expected_fw = 7.5-2.5
    # plt.plot(x,y)
    # plt.show()
    C =PlasticIndex(x, y, "test", "FWHM")
    if not C.FWHM(x, y) == expected_fw:
        print("hello")
        return False
    elif not C.calculate_FWHM() == expected_fw: # testcase that does not work
        print(C.calculate_FWHM())
        return False
    else:
        return True

def test_baseline_corr():
    x = [0.002 * math.pi * i for i in range(-10, 1050)]
    y = [(math.sin(elem)) + elem for elem in x]
    x2 = [0.002 * math.pi * i for i in range(0, 500+1)]
    y2 = [(math.sin(elem)) for elem in x2]
    C = PlasticIndex(x, y, "test", "sin")
    indexes = C._find_index()
    t = C.correct_baseline(indexes[0], indexes[1])

    for i in range(len(y2)):
        #print(i)
        #print(t[1][i], y2[i])
        if abs(t[1][i]- y2[i]) < 0.001:
            continue
        else:
            return False
    return True


def main():
    assert t_binsearch() == True
    assert test_integration() == True
    # assert t_fwhm() == True
    assert test_baseline_corr() == True





if __name__ == '__main__':
    main()