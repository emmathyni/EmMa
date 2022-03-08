""""Main kör hela skiten"""
import re

def format():
    """Opens and turns csv-file into usable format, returns two numpyarrays (just use lists instead, is already included)"""
    file=open("PVC-t0.CSV")
    list=[]
    list2=[]
    list3=[]
    for line in file:
        line.strip()
        x=re.findall("^\d,.*?,",line)
        y=re.findall(",\d,.*?$",line)
        x=x[0][:-1]
        y=y[0][1:]
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
    return wave, values


def absorbance_converter(wavenr_list,transm_list):
    """If data not already shown as absorbance, converts from transmittance to absorbance. Returns two numpyarrays"""
    pass

def find_index(wavenr_list,abso_list,mode):
    """Start calculation of indexes. Mode indicates which index wanted(?). Prints wanted indices"""
    pass

def main():
    [wave,transm]=format("PVC-t0.CSV")
    transmittance=True
    percentage=True
    transm=absorbance_converter(transm,transmittance,percentage)


if  __name__ == "__main__":
    main()