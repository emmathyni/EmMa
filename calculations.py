import math
import matplotlib.pyplot as plt
from dict import*
import numpy as np
class Index():
    def __init__(self, wave_list, abso_list, mode, plastic):
        self.wave = wave_list
        self.abso = abso_list
        self.mode = mode
        self.plastic = plastic
        self.step = self.wave[1]-self.wave[0]
        #areas = self.uneven_integrator()
        #self.CI = areas[0]/areas[1]

    def integrator(self):
        """Integrates two peaks using trapezoidal integration depending on mode, returns list with two areas"""
        indexes = self._find_index()
        num_result = 0
        for i in range(indexes[0], indexes[1]+1):
            if i == indexes[0] or i == indexes[1]:
                num_result += self.abso[i]
            else:
                num_result += 2 * self.abso[i]
        num_result = 0.5*self.step*num_result

        denom_result = 0
        for i in range(indexes[2], indexes[3]+1):
            if i == indexes[2] or i == indexes[3]:
                denom_result += self.abso[i]
            else:
                denom_result += 2*self.abso[i]
        denom_result = 0.5*self.step*denom_result

        return [num_result, denom_result]

    def uneven_integrator(self):
        """Integration using trapezoidal method with inconsistent step length"""
        indexes = self._find_index()
        [new_wave1, new_abso1, new_wave2, new_abso2] = self._correct_baseline(indexes)
        num_result = 0
        for i in range(len(new_abso1)-1):
            num_result += 0.5 * (new_abso1[i] + new_abso1[i + 1]) * (new_wave1[i + 1] - new_wave1[i])
        denom_result = 0
        for i in range(len(new_abso2)-1):
            denom_result += 0.5 * (new_abso2[i] + new_abso2[i + 1]) * (new_wave2[i + 1] - new_wave2[i])
        return [num_result, denom_result]

    def try_FWHM(self):
        """Function to try FWHM"""
        self.FWHM(self.wave, self.abso)

    def FWHM(self, corrected_x, corrected_y):
        """Returns full width at half maximum as float"""

        half_max = max(corrected_y)/2
        print(half_max)
        #print(np.add(corrected_y, -half_max))
        signs = np.sign(np.add(corrected_y, -half_max))
        intersect = []
        for i in range(len(signs)-1):
            if signs[i] == 0:
                intersect.append(corrected_x[i])
            elif np.sign(signs[i-1]) != np.sign(signs[i]):
                intersect.append(corrected_x[i])
        print(intersect)
        kommafem = [0.5 for i in range(len(intersect))]
        plt.plot(corrected_x, corrected_y)
        plt.plot(intersect, kommafem, '*')
        plt.show()
        FWHM = max(intersect)-min(intersect)
        print(FWHM)


    def _correct_baseline(self, index):
        """Returns four lists with absorbance with corrected baseline (line), if negative sets it as zero"""
        plt.figure()
        plt.plot(self.wave, self.abso, label="whole")
        k1 = (self.abso[index[1]]-self.abso[index[0]])/(self.wave[index[1]]-self.wave[index[0]])
        m1 = self.abso[index[0]]-k1*self.wave[index[0]]
        new_abso1 = []
        new_wave1 = []
        for i in range(index[0], index[1]+1):
            if self.abso[i]-k1*self.wave[i]-m1>0:
                new_abso1.append(self.abso[i]-k1*self.wave[i]-m1)
            else:
                new_abso1.append(0)
            new_wave1.append(self.wave[i])
        plt.plot(new_wave1, new_abso1, label="num")
        k2 = (self.abso[index[3]] - self.abso[index[2]]) / (self.wave[index[3]] - self.wave[index[2]])
        m2 = self.abso[index[2]] - k2 * self.wave[index[2]]
        new_abso2 = []
        list = []
        new_wave2 = []
        for i in range(index[2], index[3]+1):
            if self.abso[i] - k2 * self.wave[i] - m2 > 0:
                new_abso2.append(self.abso[i] - k2 * self.wave[i] - m2)
            else:
                new_abso2.append(0)
            new_wave2.append(self.wave[i])
            list.append(self.abso[i])
        plt.plot(new_wave2, new_abso2, label="denom")
        plt.title("ref")
        plt.legend()
        return new_wave1, new_abso1, new_wave2, new_abso2


    def _find_index(self):
        """Finds the index in the list of number using binary search. Returns the index of the n"""
        dictionary = plastic_dict[self.plastic]
        numbers = dictionary[self.mode]
        num_first = binsearch(numbers[0], self.wave, len(self.wave), 0)
        num_last = binsearch(numbers[1], self.wave, len(self.wave), 0)
        denom_first = binsearch(numbers[2], self.wave, len(self.wave), 0)
        denom_last = binsearch(numbers[3], self.wave, len(self.wave), 0)
        indexes = [num_first, num_last, denom_first, denom_last]
        return indexes


def binsearch(number, list, high, low):
    """Binary search of number in list. Returns index of element closest to number"""
    mid = (high + low) // 2
    if number < list[mid+1] and number > list[mid-1]:
        minimum_dist = min(abs(list[mid-1]-number), abs(list[mid]-number), abs(list[mid+1]-number))
        if abs(list[mid]-number) == minimum_dist:
            return mid
        elif minimum_dist == abs(list[mid-1]-number):
            return mid-1
        else:
            return mid+1

    elif number < list[mid]:
        return binsearch(number, list, mid-1, low)

    elif number > list[mid]:
        return binsearch(number, list, high, mid+1)


#if __name__== "__main__":
    #main()








