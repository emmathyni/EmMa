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
        self.geometry("500x500")
        self.clickedtrans = StringVar()
        self.clickedperc = StringVar()
        self.clickedplastic = StringVar(self)
        self.clickedplastic.trace('w', self._set_plastic)
        #self.clickedplastic.set('test')
        self.clickedinterval = StringVar(self)
        self.clickedinterval.trace('w', self._set_interval)
        self.manuallower = StringVar()
        self.manualupper = StringVar()
        self.transmittance = True
        self.percent = True
        self.wave = []
        self.values = []
        self.create_widgets()

    def create_widgets(self):
        #frame1 = Frame(self, relief =RAISED, borderwidth=1)
        #frame1.pack(fill=BOTH)
        label = Label(self, text="Welcome to EmMa, choose a csv-file to calculate carbonyl-index", bg="#acf7f8", fg="black", font='Georgia 13')
        label.pack(fill=X)

        frame2 = Frame(self)
        frame2.pack(pady=10)

        label2 = Label(frame2, text="Click the Button to browse the Files")
        label2.pack(side=RIGHT, anchor=S)

        frame3 = Frame(self, relief =RAISED, borderwidth=1)
        frame3.pack(fill=BOTH, expand=False)
        browse = ttk.Button(frame3, text="Browse", command=self._get_lists).pack(side=LEFT, padx=40, expand=True)
        label3 = Label(frame3, text="Chosen File")
        label3.pack(fill=X, padx=50, side=LEFT, expand=True)

        frame4 = Frame(self, relief=RAISED, borderwidth=1)
        frame4.pack(fill=BOTH)
        label4 = Label(frame4, text="Please choose the data types")
        label4.pack(padx=40)
        transmenu = OptionMenu(frame4, self.clickedtrans, "Absorbance", "Transmittance", command=self._set_transmittance)
        transmenu.pack(side=LEFT, expand=True, padx=40)

        frame45 = Frame(self)
        frame45.pack()
        percentmenu = OptionMenu(frame45, self.clickedperc, "Percent", "Not percent", command=self._set_percent)
        percentmenu.pack(side=LEFT, expand=True, padx=40)
        # comment to commit ?

        plotbutton = ttk.Button(frame45, text="Plot spectra")
        plotbutton.pack(side=RIGHT, expand=True, padx=30)

        frame5 = Frame(self, relief=RAISED, borderwidth=1)
        frame5.pack(fill=BOTH)
        label5 = Label(frame5, text="Please choose plastic type and desired peaks", font='Georgia 11')
        label5.pack(side=TOP)
        plasticmenu = OptionMenu(frame5, self.clickedplastic, *plastic_dict.keys(), command=self._set_plastic)
        plasticmenu.pack(side=LEFT, expand=True)
        self.intervalmenu = OptionMenu(frame5, self.clickedinterval, '')
        self.intervalmenu.pack(side=LEFT, expand=True)

        frame6 = Frame(self, relief=RAISED, borderwidth=1)
        frame6.pack(side=BOTTOM)
        okButton = ttk.Button(self, text="Calculate index")
        okButton.pack(side=LEFT, padx=50)
        label6 = Label(frame6, text="Calculated index")
        label6.pack()

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
        intervals = []
        for key in new_dict:
            intervals.append(key)
        intervals.append("Other")
        menu = self.intervalmenu['menu']
        menu.delete(0, 'end')
        for elem in intervals:
            menu.add_command(label=elem, command=lambda interval=elem: self.clickedinterval.set(interval))

    def _set_interval(self, *args):
        if self.clickedinterval.get() == "Other":
            self.lower = Entry(self, textvariable=self.manuallower)
            self.lower.pack()
            self.upper = Entry(self, textvariable=self.manualupper)
            self.upper.pack()
            ok_button = ttk.Button(self, text="OK", command=self._manual_interval)
            ok_button.pack()

    def _manual_interval(self):
        self.manuallower = self.lower.get()
        self.manualupper = self.upper.get()
        print(self.manuallower)
        print(self.manualupper)

    def _calculate_index(self):
        Ind = PlasticIndex(self.wave, self.values, self.plastic, self.interval, self.lowermanual, self.uppermanual)
        Ind.calculate_index()
        print(Ind.index)

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



