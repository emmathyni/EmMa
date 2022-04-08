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

def test_integration_error(p):
    """Test the error of the integration by integration of sin x from 0 to pi
    Returns True if it is a second order method"""
    inter = [0, math.pi]
    i = abs(inter[0]-inter[1])
    steps = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]

    x_dict = {z: [] for z in steps}
    index_dict = {z: [] for z in steps}
    int_res = []
    y_dict = {z: [] for z in steps}

    for j in steps:
        x_dict[j] = np.linspace(inter[0], inter[1], int(i/j))
        y_dict[j] = [math.sin(elem) for elem in x_dict[j]]
        index_dict[j] = PlasticIndex(x_dict[j], y_dict[j], "test", [0, 2*math.pi, 0, 2*math.pi])
        li = [x_dict[j], y_dict[j], [], []]
        res = index_dict[j].uneven_integrator(li)[0]
        int_res.append(abs(res-2))  # correct answer of integral of sinx from 0 to pi is 2

    if p:
        # print(int_res, 'int res')
        plt.loglog(steps, int_res, label='Error trapezoidal method')
        plt.loglog(steps, [h**2 for h in steps], label=r'$h^2$')
        #plt.loglog(steps, [10**(-7)*h for h in steps], label='h')
        plt.title(r'Integration error of sin(x) from 0 to $\pi$', fontsize=14)
        plt.ylabel('Error', fontsize=12)
        plt.xlabel(r'Step size $h$', fontsize=12)
        plt.legend()
        plt.show()

    res1 = int_res[2]
    res2 = int_res[3]
    # step size is 10 times smaller
    # => if it is a second order method log10(res1/res2) should be approx 2
    return abs(np.log10(res1/res2)-2) < 0.01


def error_known_func():
    """Test integration and baseline correction on known function to get error"""
    inter = [0, 8*math.pi]
    integration_int = [2*math.pi, 4*math.pi, 4*math.pi, 6*math.pi]
    i = abs(inter[0] - inter[1])
    steps = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]

    x_dict = {z: [] for z in steps}
    index_dict = {z: [] for z in steps}
    y_dict = {z: [] for z in steps}
    index_ans = []

    for j in steps:
        x_dict[j] = np.linspace(inter[0], inter[1], int(i / j))
        y_dict[j] = [math.sin(elem) + elem for elem in x_dict[j]]
        index_dict[j] = PlasticIndex(x_dict[j], y_dict[j], "test", integration_int)
        index_dict[j].calculate_index()
        index_ans.append(abs(index_dict[j].index-1))  # answer should be 1

    print(index_ans)
    plt.loglog(steps, index_ans, label='Error')
    plt.show()






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
    # assert t_binsearch() == True
    # assert t_fwhm() == True
    assert test_baseline_corr() == True

    # assert test_integration_error(False) == True

    # error_known_func()
    print('hello')





if __name__ == '__main__':
    main()