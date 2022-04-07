from main import*
from calculations import*
import os

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
                Ind = PlasticIndex(wave, values, 'correctness', [1286, 1398, 940, 980])
                Ind.calculate_index()
                indexlist.append(Ind.index)
                steplist.append(wave[1]-wave[0])
                namelist.append(f)
    print(steplist)
    print(indexlist)
    print(namelist)
    for i in range(len(steplist)):
        if steplist[i] == 0.4820999999999458:
            res4.append(indexlist[i])
        elif steplist[i] == 0.9642999999999802:
            res8.append(indexlist[i])
        elif steplist[i] == 1.9284999999999854:
            res16.append(indexlist[i])

    print(res16)
    print(res8)
    print(res4)


error_analysis()