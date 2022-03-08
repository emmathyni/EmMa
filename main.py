""""Main kör hela skiten"""
import re
import math
from calculations import*

def format(name):
    """Opens and turns csv-file into usable format, returns two numpyarrays (just use lists instead, is already included)"""
    file = open(name)
    wave = []
    values = []
    for line in file:
        line.strip()
        x = re.findall("^\d,.*?,", line)
        y = re.findall(",\d,.*?$", line)
        x = x[0][:-1]
        y = y[0][1:]
        x = re.sub(",", ".", x)
        y = re.sub(",", ".", y)
        x_n=int(x[-1])
        y_n=int(y[-1])
        resx=re.search("e",x)
        resy=re.search("e",y)
        x_e=resx.start()
        y_e=resy.start()
        x=float(x[:x_e])*10**x_n
        y=float(y[:y_e])*10**y_n
        wave.append(x)
        values.append(y)
    #Check for zeroes
    counter=0
    for i in range(len(values)):
        if values[i]==float(0):
            counter+=1
        else:
            break
    counter_high = len(values)
    for i in range(len(values)-1, 0, -1):
        if values[i] == float(0):
            counter_high -= 1
        else:
            break
    wave=wave[counter:counter_high]
    values=values[counter:counter_high]

    return wave, values




def absorbance_converter(values, transmittance, percentage):
    """Converts values to absorbance if needed. Takes three arguments, the list values to be converted,
    a boolean value for transmittance and percentage. Returns a list with absorbance values"""
    # relation between transmittance and absorbance is A = -log_10(T) when T is between 0 and 1
    # when T is percentage relation is A = log_10(100) - log_10(T)
    # taken from https://www.edinst.com/blog/the-beer-lambert-law/

    # check to determine type of data in values
    if transmittance and percentage:
        for i in range(len(values)):
            values[i] = 2 - math.log10(values[i])
        return values

    if transmittance and not percentage:
        for i in range(len(values)):
            values[i] = - math.log10(values[i])
        return values

    if not transmittance:
        return values


def find_carbonyl_index(wavenr_list, abso_list, mode):
    """Start calculation of indexes. Mode indicates which index wanted(?). Prints wanted indices"""
    pass

def user_interaction():
    """Takes in the arguments wanted from the user and returns these"""
    file = input("Please enter file name: ")
    pass

def main():
    [wave, transm] = format("PVCfiber.CSV")
    [wave2,transm2]=format("pvc-acc.CSV")
    [wave3,transm3]=format("pvc-t0-5th.CSV")
    transmittance = True
    percentage = True
    transm = absorbance_converter(transm, transmittance, percentage)
    transm2 = absorbance_converter(transm2, transmittance, percentage)
    transm3 = absorbance_converter(transm3, transmittance, percentage)

    Carbonyl_Index=Index(wave, transm, 2)
    Carbonyl_Index2 = Index(wave2, transm2, 2)
    Carbonyl_Index3 = Index(wave3, transm3, 2)
    print(Carbonyl_Index.CI)
    print(Carbonyl_Index2.CI)
    print(Carbonyl_Index3.CI)

if  __name__ == "__main__":
    main()