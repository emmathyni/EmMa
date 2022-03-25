""""Main kör hela skiten"""
import re
from calculations import*
import matplotlib.pyplot as plt
import math
from dict import*
from tkinter import*
from tkinter import ttk, filedialog
from testcases_main import*
from App import*

def user_format(file):
    """Used for GUI, takes a csv file as argument. Returns wave and value list"""
    wave = []
    values = []
    for line in file:
        #print(line)
        line.strip()
        x = re.findall("^\d,.*?,", line)
        y = re.findall(",\d,.*?$", line)
        x = x[0][:-1]
        y = y[0][1:]
        x = re.sub(",", ".", x)
        y = re.sub(",", ".", y)
        x_n = int(x[-1])
        y_n = int(y[-1])
        resx = re.search("e", x)
        resy = re.search("e", y)
        x_e = resx.start()
        y_e = resy.start()
        x = float(x[:x_e]) * 10 ** x_n
        y = float(y[:y_e]) * 10 ** y_n
        wave.append(x)
        values.append(y)
    # Check for zeroes
    file.close()
    counter = 0
    for i in range(len(values)):
        if values[i] == float(0):
            counter += 1
        else:
            break
    counter_high = len(values)
    for i in range(len(values) - 1, 0, -1):
        if values[i] == float(0):
            counter_high -= 1
        else:
            break
    wave = wave[counter:counter_high]
    values = values[counter:counter_high]

    return wave, values


def new_format(name):
    """Converts from format given by automeris.io, used for data taken from article. Use if not given
    data with scientific notation. Takes a name as argument, returns wave and value lists"""
    file = open(name)
    wave = []
    values = []
    for line in file:
        line.strip()
        x = re.findall("^\d*?,.*?,", line)
        y = re.findall(",\d*?,\d*?$", line)
        x = x[0][:-1]
        y = y[0][1:]
        x = re.sub(",", ".", x)
        y = re.sub(",", ".", y)
        wave.append(float(x))
        values.append(float(y))
    return wave, values

def format(name):
    """Converts data from csv file from nicolet iS10. Returns wave and value lists"""
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
    # taken from https://mmrc.caltech.edu/FTIR/Nicolet/Nicolet%20manuals/Omnic%20Users%20Manual%207.3.pdf page 253
    # check to determine type of data in values
    print(values, "hej")
    if transmittance and percentage:
        print("hej")
        for i in range(len(values)):
            values[i] = 2-math.log10(values[i])
        return values

    if transmittance and not percentage:
        for i in range(len(values)):
            values[i] = - math.log10(values[i])
        return values

    if not transmittance:
        return values


def get_file(trans, perc):
    file = filedialog.askopenfile(filetypes=[('CSV files', '*.csv')])
    [wave, values] = user_format(file)
    values = absorbance_converter(values, trans, perc)
    CI = PlasticIndex(wave, values, "correctness", "correct_960")
    CI.calculate_index()
    print(CI.index)

def user_interaction():
    """Takes in the arguments wanted from the user and returns these"""
    window = Tk()
    window.geometry("400x350")
    label = Label(text="Welcome to EmMa, choose a csv-file to calculate carbonyl-index", bg="#acf7f8", fg="black")
    label.pack()
    label = Label(window, text="Click the Button to browse the Files", font='Georgia 13')
    label.pack(pady=10)
    clickedtrans = StringVar()
    clickedperc = StringVar()
    #browse = ttk.Button(window, text="Browse", command=get_file).pack()
    transmenu = OptionMenu(window, clickedtrans, "Absorbance", "Transmittance", command=change_transmittance)
    transmenu.pack()
    percentmenu = OptionMenu(window, clickedperc, "Percent", "Not percent")
    percentmenu.pack()
    transmittance = True
    percent = True
    print(clickedtrans.get())
    if clickedtrans.get() == "Absorbance":
        print("Jag ändrar transmittance")
        transmittance = False
    if clickedperc.get() == "Not percent":
        percent = False
    print(transmittance)
    browse = ttk.Button(window, text="Browse", command=lambda: get_file(transmittance,percent)).pack(side= LEFT)
    #absorbance_converter(lists, True, True)
    window.mainloop()


def main():
    #user_interaction()
    # try to integrate sin(x) from
    # test_integration()
    #app = App()
    #app.mainloop()

    #test_FWHM()

    # finds carbonyl index using our data and intervals from GIVEN article
    test_our_data("PVC_carbonyl", "PVC_1718_1330")

    # finds carbonyl index using our data and intervals from FOUND article
    # test_our_data(4)

    # finds carbonyl index using data from article and intervals from GIVEN article
    # test_data_from_article(4)

    # finds carbonyl index using data from article and intervals from FOUND article
    #test_data_from_article(4)
if  __name__ == "__main__":
    main()