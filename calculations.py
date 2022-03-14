import math
import matplotlib.pyplot as plt
class Index():
    # mode 1 reference, should be constant
    # mode 2 index from GIVEN article
    # mode 3 index from Dr. Fei's peaks
    # mode 4 index from FOUND article
    # mode 5 for checking accuracy of integration
    def __init__(self, wave_list, abso_list, mode):
        self.wave = wave_list
        self.abso = abso_list
        self.mode = mode
        self.step = self.wave[1]-self.wave[0]
        self.modedict = {1: [1286, 1398, 2700, 2750],
                         2: [1510, 1746, 1286, 1398],
                         3: [1680, 1820, 1280, 1398],
                         4: [1650, 1850, 2700, 2750],
                         5: [0, math.pi, math.pi, 2 * math.pi],
                         6: [1286, 1398, 900, 1000]}
        areas = self.uneven_integrator(mode)
        self.CI = areas[0]/areas[1]

    def integrator(self, mode):
        """Integrates two peaks using trapezoidal integration depending on mode, returns list with two areas"""
        indexes = self._find_index(mode)
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

    def uneven_integrator(self, mode):
        """Integration using trapezoidal method with inconsistent step length"""
        indexes = self._find_index(mode)
        [new_wave1, new_abso1, new_wave2, new_abso2] = self._correct_baseline(indexes)
        num_result = 0
        for i in range(len(new_abso1)-1):
            num_result += 0.5 * (new_abso1[i] + new_abso1[i + 1]) * (new_wave1[i + 1] - new_wave1[i])
        denom_result = 0
        for i in range(len(new_abso2)-1):
            denom_result += 0.5 * (new_abso2[i] + new_abso2[i + 1]) * (new_wave2[i + 1] - new_wave2[i])
        print(num_result, "num", denom_result, "denom")
        return [num_result, denom_result]

    def _correct_baseline(self, index):
        """Returns four lists with absorbance with corrected baseline (line), if negative sets it as zero"""
        plt.figure()
        plt.plot(self.wave, self.abso, label="whole")
        print(self.wave[index[0]], self.wave[index[1]])
        k1 = (self.abso[index[1]]-self.abso[index[0]])/(self.wave[index[1]]-self.wave[index[0]])
        m1 = self.abso[index[0]]-k1*self.wave[index[0]]
        new_abso1 = []
        new_wave1 = []
        for i in range(index[0], index[1]+1):
            # print(self.abso[i]-k1*self.wave[i]-m1)
            if self.abso[i]-k1*self.wave[i]-m1>0:
                new_abso1.append(self.abso[i]-k1*self.wave[i]-m1)
            else:
                new_abso1.append(0)
            new_wave1.append(self.wave[i])
        plt.plot(new_wave1, new_abso1, label="num")
        print(self.wave[index[2]], self.wave[index[3]], self.abso[index[2]], self.abso[index[3]])
        k2 = (self.abso[index[3]] - self.abso[index[2]]) / (self.wave[index[3]] - self.wave[index[2]])
        m2 = self.abso[index[2]] - k2 * self.wave[index[2]]
        print(k2, "k2", m2, "m2")
        new_abso2 = []
        list = []
        new_wave2 = []
        for i in range(index[2], index[3]+1):
            # print(self.abso[i])
            # print(self.abso[i] - k2 * self.wave[i] - m2)
            if self.abso[i] - k2 * self.wave[i] - m2 > 0:
                new_abso2.append(self.abso[i] - k2 * self.wave[i] - m2)
            else:
                new_abso2.append(0)
            new_wave2.append(self.wave[i])
            list.append(self.abso[i])
        # print(new_abso2)
        plt.plot(new_wave2, new_abso2, label="denom")
        plt.title("ref")
        plt.legend()
        return new_wave1, new_abso1, new_wave2, new_abso2


    def _find_index(self, mode):
        """Finds the index in the list of number using binary search. Returns the index of the n"""
        numbers = self.modedict[mode]
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








