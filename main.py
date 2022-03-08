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
        y=re.sub(",",".",y)
        list.append(line)
        list2.append(x)
        list3.append(y)
    print(list[0])
    print(list2[0])
    print(list3[0])


def absorbance_converter(wavenr_list,transm_list):
    """If data not already shown as absorbance, converts from transmittance to absorbance. Returns two numpyarrays"""
    pass

def find_index(wavenr_list,abso_list,mode):
    """Start calculation of indexes. Mode indicates which index wanted(?). Prints wanted indices"""
    pass

def main():
    [wave,transm]=format()
    [wave,transm]=absorbance_converter(wave,transm)
    find_index(wave,transm,1)

if  __name__ == "__main__":
    main()