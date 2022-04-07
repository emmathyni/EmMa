import re
from calculations import*
import matplotlib.pyplot as plt
import math
from dict import*
from tkinter import*
from tkinter import ttk, filedialog, Frame
from testcases_main import*
#from main import*
import ntpath
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class App(Tk):

    def __init__(self):
        super().__init__()
        self.title('EmMa')
        #self.geometry("500x500")
        self.clickedtrans = StringVar()
        self.clickedperc = StringVar()
        self.clickedplastic = StringVar(self)
        self.clickedplastic.trace('w', self._set_plastic)
        #self.clickedplastic.set('test')
        self.clickedinterval = StringVar(self)
        self.clickedinterval.trace('w', self._set_interval)
        self.manuallowerref = StringVar()
        self.manualupperref = StringVar()
        self.manuallowerplast = StringVar()
        self.manualupperplast = StringVar()
        self.transmittance = True
        self.percent = True
        self.IntervalExists = False
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

        label2 = Label(self, text="Click the Button to browse the Files. Current data format accepted: (\d,\d*e(\+|-)\d*),(\d,\d*e(\+|-)\d*)")
        label2.pack(anchor='w', padx=px, pady=py, side=TOP)

        frame3 = Frame(self)
        frame3.pack(fill=BOTH, expand=False, pady=py, side=TOP)
        browse = ttk.Button(frame3, text="Browse", command=self._get_lists).pack(side=LEFT, padx=px)
        label3 = Label(frame3, text="")
        self.chosenfilename_widget = label3

        frame4 = Frame(self)
        frame4.pack(fill=X, pady=py)
        label4 = Label(frame4, text="Please choose the data types in your file")
        label4.pack(padx=px, anchor='w', pady=5)
        transmenu = OptionMenu(frame4, self.clickedtrans, "Absorbance", "Transmittance", command=self._set_transmittance)
        transmenu.pack(side=LEFT, padx=px)
        convert_button = ttk.Button(frame4, text="Convert spectrum to absorbance", command=self._convert_spectra)
        convert_button.pack(side=RIGHT, padx=2*px)

        frame45 = Frame(self)
        frame45.pack(pady=5, fill=X)
        percentmenu = OptionMenu(frame45, self.clickedperc, "Percent", "Arbitrary Units", command=self._set_percent)
        percentmenu.pack(side=LEFT, padx=px)
        plotbutton = ttk.Button(frame45, text="Plot spectrum", command=self._open_plot)
        plotbutton.pack(side=RIGHT, padx=2*px)

        frame5 = Frame(self)
        frame5.pack(fill=BOTH, pady=py)
        label5 = Label(frame5, text="Please choose plastic type and desired peaks")
        label5.pack(anchor='w', padx=px)

        frame55 = Frame(self)
        frame55.pack(fill=BOTH, expand=True)
        plasticelem=[]
        for key in plastic_dict:
            plasticelem.append(key)
        plasticelem.append("Create own interval")
        plasticmenu = OptionMenu(frame55, self.clickedplastic, *plasticelem)
        plasticmenu.pack(anchor='w', padx=px, pady=5, expand=True)
        self.intervalmenu = OptionMenu(frame55, self.clickedinterval, '')
        self.intervalmenu.pack(anchor='w', padx=px, expand=True)

        frame6 = Frame(self)
        frame6.pack(side=BOTTOM, fill=X, expand=False)
        okButton = ttk.Button(frame6, text="Calculate index", command=self._calculate_index)
        okButton.pack(side=LEFT, padx=px)
        self.label6 = Label(frame6, text="")
        frame7 = Frame(self)
        frame7.pack(fill=X, expand=False)
        self.label7 = Label(frame7, text="")
        frame8 = Frame(self)
        frame8.pack(fill=X, expand=False)
        self.label8 = Label(frame7, text="")
        #label6.pack(side=RIGHT, padx=2*px)


    def _open_plot(self):
        """Opens a new window with a plot of the spectrum"""
        newWindow = Toplevel(self)
        newWindow.title('Plot')
        #newWindow.geometry('300x200')

        if self.transmittance and self.percent:
            y_label = 'Transmittance %'
        elif self.transmittance and not self.percent:
            y_label = 'Transmittance [a.u.]'
        else:
            y_label = 'Absorbance [a.u.]'
        x_label = 'Wavenumbers [cm-1]'

        """TO ADD: reverse xaxis, add labels depending on datatype and perhaps show peaks used?"""
        f = Figure(figsize=(10, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot(self.wave, self.values)
        a.set_ylabel(y_label)
        a.set_xlabel(x_label)
        a.set_title('Spectrum')
        a.invert_xaxis()


        canvas = FigureCanvasTkAgg(f, newWindow)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, newWindow, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=BOTTOM, fill=X)
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)


    def _get_lists(self, *args):
        #self.transmittance = True
        #self.percent = True
        file = filedialog.askopenfile(filetypes=[('CSV files', '*.csv')])
        [wave, values] = self._user_format(file)
        self.wave = wave
        self.values = values
        self.chosenfilename_widget['text'] = 'Chosen file: ' + ntpath.basename(file.name)
        self.chosenfilename_widget.pack(side=RIGHT, padx=2*self.px)


    def _set_transmittance(self, *args):
        if self.clickedtrans.get() == "Absorbance":
            self.transmittance = False
        elif self.clickedtrans.get() == "Transmittance":
            self.transmittance = True

    def _set_percent(self, *args):
        if self.clickedperc.get() == "Arbitrary Units":
            self.percent = False
        elif self.clickedperc.get() == "Percent":
            self.percent = True

    def _set_plastic(self, *args):
        self.plastic = self.clickedplastic.get()
        if self.plastic == "Create own interval":
            self.clickedinterval.set("Create own interval")
        else:
            new_dict = plastic_dict.get(self.plastic)
            intervals = []
            for key in new_dict:
                intervals.append(key)
            menu = self.intervalmenu['menu']
            menu.delete(0, 'end')
            for elem in intervals:
                menu.add_command(label=elem, command=lambda interval=elem: self.clickedinterval.set(interval))

    def _set_interval(self, *args):
        if self.clickedinterval.get() == "Create own interval" and self.IntervalExists is False:
            frame_int = Frame(self, relief=RAISED, borderwidth=1)
            frame_int.pack(pady=self.py, fill=X)
            self.reference_label = Label(frame_int, text="Reference peak")
            self.reference_label.pack(side=LEFT, padx=self.px)
            ref_l = Label(frame_int, text="Lower")
            ref_l.pack(side=LEFT)
            self.reflower = Entry(frame_int, textvariable=self.manuallowerref)
            self.reflower.pack(side=LEFT)
            ref_u = Label(frame_int, text='Upper')
            ref_u.pack(side=LEFT)
            self.refupper = Entry(frame_int, textvariable=self.manualupperref)
            self.refupper.pack(side=LEFT, padx=5)

            frame_p = Frame(self, relief=RAISED, borderwidth=1)
            frame_p.pack(fill=X)

            self.peak_label = Label(frame_p, text="Plastic peak      ")
            self.peak_label.pack(side=LEFT, padx=self.px)
            plast_l =Label(frame_p, text='Lower')
            plast_l.pack(side=LEFT)
            self.plastlower = Entry(frame_p, textvariable=self.manuallowerplast)
            self.plastlower.pack(side=LEFT)
            plast_u = Label(frame_p, text='Upper')
            plast_u.pack(side=LEFT)
            self.plastupper = Entry(frame_p, textvariable=self.manualupperplast)
            self.plastupper.pack(side=LEFT, padx=5)

            ok_button = ttk.Button(frame_p, text="OK", command=self._manual_interval)
            ok_button.pack(side=RIGHT, padx=15)
            self.IntervalExists = True
        else:
            new_dict = plastic_dict.get(self.plastic)
            self.interval = new_dict.get(self.clickedinterval.get())

    def _manual_interval(self):
        self.manuallowerref = self.reflower.get()
        self.manualupperref = self.refupper.get()
        self.manuallowerplast = self.plastlower.get()
        self.manualupperplast = self.plastupper.get()
        self.interval = [float(self.manuallowerplast), float(self.manualupperplast), float(self.manuallowerref), float(self.manualupperref)]

    def _calculate_index(self):
        self._convert_spectra()
        Ind = PlasticIndex(self.wave, self.values, self.plastic, self.interval)
        #try:
        Ind.calculate_index()
        self.fwhmlist = Ind.calculate_FWHM()
        # except:
          #  self.label6['text'] = 'An error has occured somewhere. Please check your settings before continuing'
        self.index = round(Ind.index, 5)
        self.label6['text'] = 'Calculated index: '+ str(self.index)
        self.label6.pack()
        self.label7['text'] = 'FWHM for plastic peak: '+str(self.fwhmlist[0])
        self.label8['text'] = 'FWHM for reference peak: '+str(self.fwhmlist[1])
        self.label7.pack()
        self.label8.pack()
        self._plot_interesting_peaks()


    def _convert_spectra(self):
        self.values = self._absorbance_converter(self.values, self.transmittance, self.percent)
        self.transmittance = False
        self.percent = False

    def _plot_interesting_peaks(self):
        """Opens a new window with a plot of the spectrum"""
        newWindow2 = Toplevel(self)
        newWindow2.title('Calculated plot')
        # newWindow.geometry('300x200')


        y_label = 'Absorbance [a.u.]'
        x_label = 'Wavenumbers [cm-1]'
        textstr='\n'.join(('$FWHM plastic=%.2f$' % (self.fwhmlist[0], ),
    '$FWHM reference=%.2f$' % (self.fwhmlist[1], )))
        props = dict(boxstyle='round', facecolor='yellow', alpha=0.5)
        f = Figure(figsize=(10, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot(self.wave, self.values)
        m = max(self.values)
        mi = min(self.values)
        a.vlines(self.interval[0:2], mi, m, colors=['red', 'red'], label='Plastic Peak')
        a.vlines(self.interval[2:5], mi, m, colors=['purple', 'purple'], label='Reference Peak')
        a.set_ylabel(y_label)
        a.set_xlabel(x_label)
        a.set_title('Calculated index: ' + str(self.index))
        a.text(0.05, 0.95, textstr, transform=a.transAxes,
                verticalalignment='top', bbox=props)
        a.invert_xaxis()
        a.legend()

        canvas = FigureCanvasTkAgg(f, newWindow2)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, newWindow2, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=BOTTOM, fill=X)
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

    def _user_format(self, file):
        wave = []
        values = []
        for line in file:
            line.strip()
            #newline = re.sub("-","",line)
            x = re.findall("^\d*,.*?,", line)
            y = re.findall(",-?\d{1,2},.*?$", line)
            x = x[0][:-1]
            y = y[0][1:]
            x = re.sub(",", ".", x)
            y = re.sub(",", ".", y)
            y.lstrip("-")
            x_n = int(x[-1])
            y_n = int(y[-1])
            resx = re.search("e", x)
            resy = re.search("e", y)
            if resx is None and resy is None:
                wave.append(float(x))
                values.append(float(y))
            else:
                x_e = resx.start()
                y_e = resy.start()
                signy = y[y_e+1]
                if signy == "-":
                    y_n = -y_n
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
                values[i]
                values[i] = 2 - math.log10(values[i])
            return values

        if transmittance and not percentage:
            for i in range(len(values)):
                values[i] = - math.log10(values[i])
            return values

        if not transmittance:
            return values

#app = App()
#app.mainloop()

