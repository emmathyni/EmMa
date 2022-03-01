""""Main kör hela skiten"""
import re

def format():
    """Opens and turns csv-file into usable format, returns two numpyarrays (just use lists instead, is already included)"""
    file=open("PVC-t0.CSV")
    list=[]
    list2=[]
    for line in file:
        line.strip()
        x=re.findall("^\d,.*?,",line)
        list.append(line)
        list2.append(x)
    print(list)
    print(list2)


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