import re
from calculations import*
import matplotlib.pyplot as plt
import math
from dict import*
from tkinter import*
from tkinter import ttk, filedialog
from testcases_main import*
from main import*
import ntpath
from tkinter.ttk import Frame

class App(Tk):

    def __init__(self):
        super().__init__()
        self.title('EmMa')
        self.geometry("400x350")
        self.clickedtrans = StringVar()
        self.clickedperc = StringVar()
        self.clickedplastic = StringVar(self)
        self.clickedplastic.trace('w', self._set_plastic)
        #self.clickedplastic.set('test')
        self.clickedinterval = StringVar(self)
        self.clickedplastic.trace('w', self._set_plastic)
        self.transmittance = True
        self.percent = True
        self.wave = []
        self.values = []
        self.create_widgets()

    def create_widgets(self):
        frame1 = Frame(self)
        frame1.pack(fill=X)
        label = Label(frame1,text="Welcome to EmMa, choose a csv-file to calculate carbonyl-index", bg="#acf7f8", fg="black")
        label.pack()

        frame2 = Frame(self)
        frame2.pack(padx=5)
        label = Label(frame2, text="Click the Button to browse the Files", font='Georgia 13')
        label.pack(side=LEFT, padx=8, pady=4)
        browse = ttk.Button(frame2, text="Browse", command=self._get_lists).pack(side=LEFT, padx=8, pady=4)
        absopt = ["Absorbance", "Transmittance"]

        frame3 = Frame(self)
        frame3.pack(fill=BOTH)
        transmenu = OptionMenu(frame3, self.clickedtrans, "Absorbance", "Transmittance", command=self._set_transmittance)
        transmenu.pack(side=LEFT, fill=BOTH)
        percentmenu = OptionMenu(frame3, self.clickedperc, "Percent", "Not percent", command=self._set_percent)
        percentmenu.pack(side=LEFT, fill=BOTH)
        plasticmenu = OptionMenu(self, self.clickedplastic, *plastic_dict.keys(), command=self._set_plastic)
        plasticmenu.pack()
        self.intervalmenu = OptionMenu(self, self.clickedinterval, '')
        self.intervalmenu.pack()

    def _get_lists(self, *args):
        file = filedialog.askopenfile(filetypes=[('CSV files', '*.csv')])
        print(ntpath.basename(file.name))
        [wave, values] = self._user_format(file)
        self.wave = wave
        self.values = values


    def _set_transmittance(self, *args):
        if self.clickedtrans.get() == "Absorbance":
            self.transmittance = False
        elif self.clickedtrans.get() == "Transmittance":
            self.transmittance = True

    def _set_percent(self, *args):
        if self.clickedperc.get() == "Not percent":
            self.percent = False
        elif self.clickedperc.get() == "Percent":
            self.percent = True

    def _set_plastic(self, *args):
        self.plastic = self.clickedplastic.get()
        new_dict = plastic_dict.get(self.plastic)
        interval = []
        for key in new_dict:
            interval.append(key)
        #self.clickedinterval.set(interval[0])
        menu = self.intervalmenu['menu']
        menu.delete(0, 'end')
        for elem in interval:
            menu.add_command(label=elem, command=lambda intervals=elem: self.clickedinterval.set(intervals))
        print(self.clickedinterval.get())

    def _user_format(self, file):
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
        return [wave, values]

    def _absorbance_converter(self, values, transmittance, percentage):
        """Converts values to absorbance if needed. Takes three arguments, the list values to be converted,
        a boolean value for transmittance and percentage. Returns a list with absorbance values"""
        # relation between transmittance and absorbance is A = -log_10(T) when T is between 0 and 1
        # when T is percentage relation is A = log_10(100) - log_10(T)
        # taken from https://mmrc.caltech.edu/FTIR/Nicolet/Nicolet%20manuals/Omnic%20Users%20Manual%207.3.pdf page 253
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



