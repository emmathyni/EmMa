import math
class Index():
    def __init__(self, wave_list, abso_list, mode):
        self.wave = wave_list
        self.abso = abso_list
        self.mode = mode
        self.step = self.wave[1]-self.wave[0]
        self.modedict = {1: [1550, 1850, 2700, 2750],
                         2: [1510, 1746, 1286, 1398],
                         3: [1650, 1850, 1420, 1500],
                         4: [0, math.pi, math.pi, 2 * math.pi]}
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
        num_result = 0
        for i in range(indexes[0], indexes[1]):
            num_result += 0.5 * (self.abso[i] + self.abso[i + 1]) * (self.wave[i + 1] - self.wave[i])
        denom_result = 0
        for i in range(indexes[2], indexes[3]):
            denom_result += 0.5 * (self.abso[i] + self.abso[i + 1]) * (self.wave[i + 1] - self.wave[i])

        return [num_result, denom_result]

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


if __name__== "__main__":
    main()








