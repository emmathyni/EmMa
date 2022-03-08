
class Index():
    def __init__(self, wave_list, abso_list, mode):
        self.wave = wave_list
        self.abso = abso_list
        self.mode = mode
        self.step = self.wave[1]-self.wave[0]
        self.modedict = {1: [1650, 1850, 1420, 1500],
                         2: [2800, 3000, 1420, 1500]}
        areas = self.integrator(mode)
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
    """Binary search of number in list. Returns index of element """
    mid = (high + low) // 2
    if number < list[mid+1] and number > list[mid-1]:
        return mid

    elif number < list[mid]:
        return binsearch(number, list, mid-1, low)

    elif number > list[mid]:
        return binsearch(number, list, high, mid+1)


if __name__== "__main__":
    main()








