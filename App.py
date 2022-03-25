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
        self.chosenfilename_widget = 0
        self.px = 50
        self.py = 5
        self.wave = []
        self.values = []
        self.create_widgets()
        # self.widgets = tkinter.winfo_children()




    def create_widgets(self):
        px = 50
        py = 5

        #frame1 = Frame(self, relief =RAISED, borderwidth=1)
        #frame1.pack(fill=BOTH)
        label = Label(self, text="Welcome to EmMa, choose a csv-file to calculate carbonyl-index", bg="#acf7f8", fg="black", font='Georgia 13')
        label.pack(fill=X, side=TOP)

        #frame2 = Frame(self)
        #frame2.pack(pady=10)

        label2 = Label(self, text="Click the Button to browse the Files")
        label2.pack(anchor='w', padx=px, pady=py, side=TOP)

        frame3 = Frame(self, relief=RAISED, borderwidth=1)
        frame3.pack(fill=BOTH, expand=False, pady=py, side=TOP)
        browse = ttk.Button(frame3, text="Browse", command=self._get_lists).pack(side=LEFT, padx=px)
        label3 = Label(frame3, text="")
        self.chosenfilename_widget = label3

        frame4 = Frame(self, relief=RAISED, borderwidth=1)
        frame4.pack(fill=BOTH, pady=py)
        label4 = Label(frame4, text="Please choose the data types")
        label4.pack(padx=px, anchor='w', pady=5)
        transmenu = OptionMenu(frame4, self.clickedtrans, "Absorbance", "Transmittance", command=self._set_transmittance)
        transmenu.pack(anchor='w', expand=True, padx=px, pady=5)

        frame45 = Frame(self, relief=RAISED, borderwidth=1)
        frame45.pack(pady=5, fill=X)
        percentmenu = OptionMenu(frame45, self.clickedperc, "Percent", "Not percent", command=self._set_percent)
        percentmenu.pack(side=LEFT, padx=px)
        plotbutton = ttk.Button(frame45, text="Plot spectra")
        plotbutton.pack(side=RIGHT, padx=2*px)

        frame5 = Frame(self, relief=RAISED, borderwidth=1)
        frame5.pack(fill=BOTH, pady=py)
        label5 = Label(frame5, text="Please choose plastic type and desired peaks")
        label5.pack(anchor='w', padx=px)

        frame55 = Frame(self, relief=RAISED, borderwidth=1)
        frame55.pack(fill=BOTH, expand=True)
        plasticmenu = OptionMenu(frame55, self.clickedplastic, *plastic_dict.keys(), command=self._set_plastic)
        plasticmenu.pack(anchor='w', padx=px, pady=5, expand=True)
        self.intervalmenu = OptionMenu(frame55, self.clickedinterval, '')
        self.intervalmenu.pack(anchor='w', padx=px, expand=True)

        frame6 = Frame(self, relief=RAISED, borderwidth=1)
        frame6.pack(side=BOTTOM, fill=X, expand=False)
        okButton = ttk.Button(frame6, text="Calculate index")
        okButton.pack(side=LEFT, padx=px)
        label6 = Label(frame6, text="Calculated index")
        label6.pack(side=RIGHT, padx=2*px)

    def _get_lists(self, *args):
        file = filedialog.askopenfile(filetypes=[('CSV files', '*.csv')])
        [wave, values] = self._user_format(file)
        self.wave = wave
        self.values = values
        self.chosenfilename_widget['text'] = ntpath.basename(file.name)
        self.chosenfilename_widget.pack(side=RIGHT, padx=2*self.px)


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



