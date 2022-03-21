import re
from calculations import*
from main import*
import matplotlib.pyplot as plt
import math
from dict import*
from tkinter import*
from tkinter import ttk, filedialog

def test_integration():
    """Try to integrate sin(x)^2 from 0 to pi and then from pi to 2*pi and divide those areas.
    If result is close to one integration method works"""
    x = [0.002*math.pi*i for i in range(-10, 1050)]
    y = [(math.sin(elem))**2+2 for elem in x]
    Carb = Index(x, y, 5)
    print(Carb.CI, "carb")

def test_FWHM():
    x = [0.002 * math.pi * i for i in range(-10, 1050)]
    y = [(math.sin(elem))**2 for elem in x]
    test = Index(x, y, "sin", "test")
    test.try_FWHM()

    [wave, transm] = format("pvc-t0-5th.CSV")
    transmittance = True
    percentage = True
    transm = absorbance_converter(transm, transmittance, percentage)
    Carbonyl_Index = Index(wave, transm, "PVC_1718_1330", "PVC_carbonyl")
    Carbonyl_Index.try_FWHM()

def test_user_interface():
    # do not plot things using matplotlib in this function!
    file = filedialog.askopenfile(filetypes=[('CSV files', '*.csv')])
    if file:
        [wave, transm] = user_format(file)
        transmittance = True
        percentage = True
        transm = absorbance_converter(transm, transmittance, percentage)
        Carbonyl_Index = Index(wave, transm, "PVC_1718_1330", "PVC_carbonyl")
        print(Carbonyl_Index.CI)
        return wave, transm


def test_our_data(plastic, interval):
    [wave, transm] = format("PVCfiber.CSV")
    [wave2, transm2] = format("pvc-acc.CSV")
    [wave3, transm3] = format("pvc-t0-5th.CSV")
    transmittance = True
    percentage = True
    transm = absorbance_converter(transm, transmittance, percentage)
    transm2 = absorbance_converter(transm2, transmittance, percentage)
    transm3 = absorbance_converter(transm3, transmittance, percentage)
    CI = PlasticIndex(wave, transm, plastic, interval)
    CI2 = PlasticIndex(wave2, transm2, plastic, interval)
    CI3 = PlasticIndex(wave3, transm3, plastic, interval)
    CI.calculate_index()
    CI2.calculate_index()
    CI3.calculate_index()
    print(CI.index)
    print(CI2.index)
    print(CI3.index)
    plt.figure()
    plt.plot(wave, transm, label="fiber CI=" + str(round(CI.index, 5)))
    plt.plot(wave2, transm2, label="accumulated CI=" + str(round(CI2.index, 5)))
    plt.plot(wave3, transm3, label="as received CI=" + str(round(CI3.index, 5)))
    ax = plt.gca()
    ax.invert_xaxis()
    plt.legend()
    plt.show()

def test_data_from_article(plastic, mode):
    [wave, transm] = new_format("PVC-as-received-test(2).csv")
    transmittance = False
    percentage = True
    transm = absorbance_converter(transm, transmittance, percentage)
    Carbonyl_Index = Index(wave, transm, mode, plastic)
    print(str(Carbonyl_Index.CI) + " as received")
    [wave2, transm2] = new_format("PVC-16-days-test.csv")
    transmittance = False
    percentage = True
    transm2 = absorbance_converter(transm2, transmittance, percentage)
    Carbonyl_Index2 = Index(wave2, transm2, mode, plastic)
    print(str(Carbonyl_Index2.CI) + " 16 days")
    [wave3, transm3] = new_format("PVC-7-days-test.csv")
    transmittance = False
    percentage = True
    transm3 = absorbance_converter(transm3, transmittance, percentage)
    Carbonyl_Index3 = Index(wave3, transm3, mode, plastic)
    print(str(Carbonyl_Index3.CI) + " 7 days")
    print(round(Carbonyl_Index3.CI, 5))
    plt.figure()
    plt.plot(wave, transm, label="as received CI=" + str(round(Carbonyl_Index.CI, 5)))
    plt.plot(wave3, transm3, label="7 days CI=" + str(round(Carbonyl_Index3.CI, 5)))
    plt.plot(wave2, transm2, label="16 days CI=" + str(round(Carbonyl_Index2.CI, 5)))
    ax = plt.gca()
    ax.invert_xaxis()
    plt.legend()
    plt.title("Absorbance spectra for PVC from article")
    plt.show()

def main():
    #[wave, transm] = user_interaction()
    
    # finds carbonyl index using our data and intervals from GIVEN article
    test_our_data("test", "manual_peaks_CI")
    # test_data_from_article("PVC_carbonyl", "PVC_1718_1330")

    # finds carbonyl index using our data and intervals from FOUND article
    # test_our_data(4)

    # finds carbonyl index using data from article and intervals from GIVEN article
    # test_data_from_article(4)

    # finds carbonyl index using data from article and intervals from FOUND article
    # test_data_from_article(4)

if __name__ == "__main__":
    main()