import math
import matplotlib.pyplot as plt
from dict import*
import numpy as np


class PlasticIndex():
    def __init__(self, wave_list, abso_list, interval):
        self.wave = wave_list
        self.abso = abso_list
        self.interval = interval
        self.index = 0
        self.num = 0
        self.mean = 0
        self.std = 0


    def calculate_index(self,d=5):
        """Calculates the index and sets self.index to this"""
        indexes = self._find_index(self.interval)
        corrected_data = self.correct_two_peaks(indexes)
        num, denom = self.uneven_integrator(corrected_data)
        self.num = num
        self.index = num/denom
        index_list = []
        d = 7.5
        vary_list = [(0, d), (0, -d), (d, 0), (-d, 0), (d, d), (-d, -d)]
        for elem in vary_list:
            index_list.append(self._vary_interval(elem))
        index_list.append(self.index)
        self.mean = np.mean(index_list)
        self.std = np.std(index_list)

    def _vary_interval(self, tup):
        """Estimate the standard deviation of the index when distance d from given interval"""
        d1, d2 = tup
        print(d1, d2)
        new_interval1 = [self.interval[0]+d1, self.interval[1] + d2, self.interval[2], self.interval[3]]
        indexes = self._find_index(new_interval1)
        corrected_data = self.correct_two_peaks(indexes)
        num, denom = self.uneven_integrator(corrected_data)
        return num/denom


    def uneven_integrator(self, corrected_data):
        """Integration using trapezoidal method with inconsistent step length"""
        new_wave1 = corrected_data[0]
        new_abso1 = corrected_data[1]
        new_wave2 = corrected_data[2]
        new_abso2 = corrected_data[3]

        num_result = 0
        for i in range(len(new_abso1)-1):
            num_result += 0.5 * (new_abso1[i] + new_abso1[i + 1]) * (new_wave1[i + 1] - new_wave1[i])

        denom_result = 0
        for i in range(len(new_abso2)-1):
            denom_result += 0.5 * (new_abso2[i] + new_abso2[i + 1]) * (new_wave2[i + 1] - new_wave2[i])

        return [num_result, denom_result]

    def calculate_FWHM(self):
        """Function to try FWHM"""
        indexes = self._find_index(self.interval)
        [new_wave1, new_abso1, new_wave2, new_abso2] = self.correct_two_peaks(indexes)
        fwhm1 = self.FWHM(new_wave1, new_abso1)
        fwhm2 = self.FWHM(new_wave2, new_abso2)
        return fwhm1, fwhm2

    def FWHM(self, corrected_x, corrected_y):
        """Returns full width at half maximum as float"""
        half_max = max(corrected_y)/2
        signs = np.sign(np.add(corrected_y, -half_max))
        intersect_x = []
        intersect_y = []
        for i in range(len(signs)-1):
            if signs[i] == 0:
                intersect_x.append(corrected_x[i])
                intersect_y.append(corrected_y[i])
            elif np.sign(signs[i-1]) != np.sign(signs[i]):
                if abs(corrected_y[i-1]-half_max) < abs(corrected_y[i]-half_max):
                    intersect_x.append(corrected_x[i-1])
                    intersect_y.append(corrected_y[i-1])
                else:
                    intersect_x.append(corrected_x[i])
                    intersect_y.append(corrected_y[i])
        # half_vect = [half_max for i in range(len(intersect_x))]
        # plt.plot(corrected_x, corrected_y)
        # plt.plot(intersect_x, half_vect, 'r*')
        # plt.plot(intersect_x, intersect_y, 'g*')
        # plt.show()
        FWHM = max(intersect_x)-min(intersect_x)
        return FWHM


    def correct_baseline(self, index1, index2):
        """Returns list with corrected baseline abso from index1 to index2"""
        #plt.figure()
        #plt.plot(self.wave, self.abso, label="whole")
        k1 = (self.abso[index1]-self.abso[index2])/(self.wave[index1]-self.wave[index2])
        m1 = self.abso[index1]-k1*self.wave[index1]
        new_abso = []
        for i in range(index1, index2+1):
            if self.abso[i]-k1*self.wave[i]-m1>0:
                new_abso.append(self.abso[i]-k1*self.wave[i]-m1)
            else:
                new_abso.append(0)
        # plt.plot(self.wave[index1:index2+1], new_abso)
        # plt.show()
        return self.wave[index1:index2+1], new_abso

    def correct_two_peaks(self, index):
        """Returns four lists with absorbance with corrected baseline (line), if negative sets it as zero"""
        new_wave1, new_abso1 = self.correct_baseline(index[0], index[1])
        new_wave2, new_abso2 = self.correct_baseline(index[2], index[3])

        return new_wave1, new_abso1, new_wave2, new_abso2


    def _find_index(self, interval):
        """Finds the index in the list of number using binary search. Returns the index of the n"""
        numbers = interval
        num_first = binsearch(numbers[0], self.wave, len(self.wave), 0)
        num_last = binsearch(numbers[1], self.wave, len(self.wave), 0)
        denom_first = binsearch(numbers[2], self.wave, len(self.wave), 0)
        denom_last = binsearch(numbers[3], self.wave, len(self.wave), 0)
        indexes = [num_first, num_last, denom_first, denom_last]
        return indexes




def binsearch(number, list, high, low):
    """Binary search of number in list. Returns index of element closest to number. Cannot find first
    and last element in list, returns None in that case"""
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





def main():
    pass

if __name__== "__main__":
    main()








