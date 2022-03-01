
class Index():
    def __init__(self,wave_list,abso_list,mode):
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

    def calculate_index(self):
        """Returns index as int"""

