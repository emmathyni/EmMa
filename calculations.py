
class Index():
    def __init__(self, wave_list, abso_list, mode):
        self.wave = wave_list
        self.abso = abso_list
        self.mode = mode
        self.step = 0

    def _find_stepsize(self):
        """Finds difference in wavenumber between to datapoints, sets self.step to this"""

    def integrator(self,mode):
        """Integrates two peaks using trapezoidal integration depending on mode, returns list with two areas"""

    def _integrator_step(self):
        """Integrates one step, called by integrator, returns one int"""

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








