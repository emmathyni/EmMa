from main import*
from calculations import*
import os
import math
import matplotlib.pyplot as plt

def error_analysis():
    indexlist = []
    steplist = []
    namelist = []
    directory = 'Error analysis'
    res4 = []
    res8 = []
    res16 = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            iscsv=re.search('CSV', filename)
            if iscsv is not None:
                [wave, values] = format(f)
                transmittance = True
                percent = True
                values = absorbance_converter(values, transmittance, percent)
                Ind = PlasticIndex(wave, values, [1700, 1770, 1400, 1480])
                Ind.calculate_index()
                indexlist.append(Ind.index)
                steplist.append(wave[1]-wave[0])
                namelist.append(f)
    for i in range(len(steplist)):
        if steplist[i] == 0.4820999999999458:
            res4.append(indexlist[i])
        elif steplist[i] == 0.9642999999999802:
            res8.append(indexlist[i])
        elif steplist[i] == 1.9284999999999854:
            res16.append(indexlist[i])

    mean16 = sum(res16)/len(res16)
    mean8 = sum(res8)/len(res8)
    mean4 = sum(res4)/len(res4)
    std16 = 0
    for elem in res16:
        std16 += (elem-mean16)**2
    std16 = math.sqrt(std16/len(res16))
    std8 = 0
    for elem in res8:
        std8 += (elem-mean8)**2
    std8 = math.sqrt(std8/len(res8))
    std4 = 0
    for elem in res4:
        std4 += (elem - mean4) ** 2
    std4 = math.sqrt(std4 / len(res4))
    stdlist = [std4, std8, std16]
    newstep = [0.4820999999999458, 0.9642999999999802, 1.9284999999999854]
    newstep3 = [0.4820999999999458, 0.4820999999999458, 0.4820999999999458, 0.9642999999999802, 0.9642999999999802,
                0.9642999999999802, 1.9284999999999854, 1.9284999999999854, 1.9284999999999854]
    plt.plot(newstep, stdlist, '*')
    plt.title("Standard deviation of reference index for different resolutions", fontsize=14)
    plt.xlabel("Step size [cm\u207B\u00b9]", fontsize=12)
    plt.ylabel("Standard deviation [a.u]", fontsize=12)
    plt.figure()
    plt.title("Calculated reference index for different resolutions", fontsize=14)
    plt.xlabel("Step size [cm\u207B\u00b9]", fontsize=12)
    plt.ylabel("Reference index [a.u]", fontsize=12)
    plt.plot(newstep3[0:3], res4, '*', label="resolution 4")
    plt.plot(newstep3[3:6], res8, '*', label="resolution 8")
    plt.plot(newstep3[6:], res16, '*', label="resolution 16")
    plt.legend()
    plt.show()



error_analysis()