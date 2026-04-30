import math
import tkinter as tk
from contextlib import nullcontext
from idlelib.browser import file_open
from tkinter import filedialog, ttk, messagebox, Label
from tkinter import ttk
import csv
from tokenize import String
import numpy as np
import cmath
import matplotlib.pyplot as plt
from fontTools.cffLib.specializer import commandsToProgram
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
from time import strftime
from tkinter import *
from tkinter.ttk import *
from time import strftime
import pandas as pd
from numpy import fft
from pandas import read_csv
import fft_alg

import time


class DataApp:
    def open_ins(self):
        self.insa_window = tk.Toplevel(self.root)
        self.insa_window.title("Navod na pouzivanie aplikacie")
        self.insa_win_width = 400
        self.insa_win_height = 400
        self.insa_window.geometry(str(self.insa_win_width) + "x" + str(self.insa_win_height))
        # frame
        insm_frame = tk.Frame(self.insa_window, width=self.insa_win_width, height=self.insa_win_height, padx=10, pady=10, bg="blue")
        insm_frame.place(x=0, y=0)
        in_lbl1 = Label(insm_frame, text="1. Importovat subor vo formate .csv")
        in_lbl1.place(x=10, y=80)
        in_lbl2 = Label(insm_frame, text="2. Vybrat algoritmus")
        in_lbl2.place(x=10, y=110)
        in_lbl3 = Label(insm_frame, text="3. Potvrdit vyber")
        in_lbl3.place(x=10, y=140)
        in_lbl4 = Label(insm_frame, text="4. Exportovat subor")
        in_lbl4.place(x=10, y=170)

    def open_alg_info(self):
        self.insb_window = tk.Toplevel(self.root)
        self.insb_window.title("Informacie o algoritmoch")
        self.insb_win_width = 400
        self.insb_win_height = 400
        self.insb_window.geometry(str(self.insb_win_width) + "x" + str(self.insb_win_height))
        # frame
        insb_frame = tk.Frame(self.insb_window, width=self.insb_win_width, height=self.insb_win_height, padx=10, pady=10, bg="blue")
        insb_frame.place(x=0, y=0)
        # rolovanie zoznamu
        scroll_bar = Scrollbar(insb_frame)
        scroll_bar.pack(side=RIGHT,fill=Y)
        # info
        mylist = Listbox(insb_frame, yscrollcommand=scroll_bar.set)
        #
        mylist.insert(END, "Cooley-Tukey")
        mylist.insert(END, "Pocet vzoriek: 2^n")
        mylist.insert(END, "Cooley-Tukey")
        mylist.insert(END, " ")
        mylist.insert(END, "Prime factor")
        mylist.insert(END, "Pocet vzoriek: N = N1 * N2; N1 a N2 su nesudelitelne")
        mylist.insert(END, "Prime factor")
        mylist.insert(END, " ")
        mylist.insert(END, "Split Radix")
        mylist.insert(END, "Pocet vzoriek: N = 4*n")
        mylist.insert(END, "Cooley-Tukey")
        mylist.pack(side=LEFT, fill=BOTH)
        scroll_bar.config(command=mylist.yview)

    def open_app_info(self):
        self.insc_window = tk.Toplevel(self.root)
        self.insc_window.title("Informacie o aplikacii")
        self.insc_win_width = 400
        self.insc_win_height = 400
        self.insc_window.geometry(str(self.insc_win_width) + "x" + str(self.insc_win_height))
        # frame
        insc_frame = tk.Frame(self.insc_window, width=self.insc_win_width, height=self.insc_win_height, padx=10, pady=10, bg="blue")
        insc_frame.place(x=0, y=0)
        #
        inf_label = tk.Label(insc_frame, text="Autori: Matus Banas a Ing.Dominik Cambal")
        inf_label.place(x=10, y=50)
        inf_label = tk.Label(insc_frame, text="Jazyk: Python 3.14.2")
        inf_label.place(x=10, y=80)
        inf_label = tk.Label(insc_frame, text="©2026")
        inf_label.place(x=10, y=110)

    # otvori navod na pouzivanie
    def open_instruction_window(self):
        #definicia okna
        self.insm_window = tk.Toplevel(self.root)
        self.insm_window.title("Pouzivatelska prirucka")
        self.insm_win_width = 400
        self.insm_win_height = 300
        self.insm_window.geometry(str(self.insm_win_width)+"x"+str(self.insm_win_height))
        # frame
        insm_frame = tk.Frame(self.insm_window,width=self.insm_win_width, height=self.insm_win_height, padx=10, pady=10, bg="blue")
        insm_frame.place(x=0, y=0)
        # rozlozenie
        nadpis = Label(insm_frame, text="Vitajte v kalkulacke")
        nadpis.config(font=("Times New Roman", 10))
        nadpis.place(x=50, y=50)
        btn1 = Button(insm_frame, text="Navod", command=self.open_ins)
        btn1.place(x=10, y=100)
        btn2 = Button(insm_frame, text="Algoritmy", command=self.open_alg_info)
        btn2.place(x=10, y=140)
        btn3 = Button(insm_frame, text="Informacie", command=self.open_app_info)
        btn3.place(x=10, y=180)

    def easter_egg(self):
        self.cal_window = tk.Toplevel(self.root)
        self.cal_window.title("Je cislo 2^n")
        self.cal_window.geometry("300x300")
        self.lbl = tk.Label(self.cal_window, text="Zadajte prirodzene cislo")
        self.lbl.config(font=("Times New Roman", 10))
        self.lbl.place(x=10, y=50)
        self.t = tk.Text(self.cal_window)
        self.t.config(font=("Times New Roman", 10), width=100, height=50)
        self.t.place(x=10, y=50)

    # importuje subor
    def import_file_dialogwindow(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        file = open(filepath, "r")
        #print(file.read())
        self.data = pd.read_csv(file, header=None)
        #self.data = self.data.values.flatten()
        self.update_plots()


    # ulozi subor ako .csv
    def save_file_dialogwindow(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv")
        if filepath and self.data is not None:
            self.data.to_csv(filepath, index=False)

    '''def select_algorithm(self, sel):
        try:
            if (sel == 0): # Cooley-Tukey
                if(math.log2())'''


    #konstruktor
    def __init__(self, root): #hlavne okno
        # vlastnosti okna
        self.insm_window = None
        self.cal_window = None
        self.window_width = 1500 #width = sirka
        self.window_height = 800 #height = vyska
        self.root = root
        self.root.title("Vypocet FFT")
        self.root.geometry(str(self.window_width)+"x"+str(self.window_height))
        self.root.resizable(False, False)

        #vlastnost, ulozi sa do tejto premennej data z csv
        self.data = None

        #definicia layoutu (rozlozenia)
        #menu
        menubar = Menu(root)
        navody = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Navody', menu=navody)
        navody.add_command(label = "Navod", command=self.open_instruction_window)
        navody.add_command(label = "2^n", command=self.easter_egg)
        self.root.config(menu=menubar)
        #

        #horny a dolny ramec
        self.frame_height = self.window_height/2
        top_frame = tk.Frame(self.root, width=self.window_width, height=self.frame_height, padx=10, pady=10, bg="lightblue")
        top_frame.place(x=0,y=0)
        bottom_frame = tk.Frame(self.root, width=self.window_width, height=self.frame_height, padx=10, pady=10, bg="red")
        bottom_frame.place(x=0,y=self.frame_height)
        #

        #Nadpis
        label_radio = tk.Label(top_frame, text="Vyberte FFT algoritmus")
        label_radio.place(x=20, y=20)
        label_radio.config(font=("Times New Roman", 10))

        # Vyber FFT algoritmu
        self.select = tk.StringVar()
        radio_btn = tk.Radiobutton(top_frame, variable = self.select, text="Cooley-Tukey", value=0, bg="lightblue")
        radio_btn.place(x=20, y=50)
        radio_btn.select()
        radio_btn = tk.Radiobutton(top_frame, variable = self.select, text="Prime Factor", value=1, bg="lightblue")
        radio_btn.place(x=20, y=80)
        radio_btn = tk.Radiobutton(top_frame, variable = self.select, text="Split Radix", value=2, bg="lightblue")
        radio_btn.place(x=20, y=110)
        sel = tk.IntVar(radio_btn)
        # zobrazenie metrik
        self.cas_popis = Label(top_frame, text="Cas programu:")
        self.cas_popis.place(x=10, y=200)
        self.cas_okno = Entry(top_frame)
        self.cas_okno.place(x=150, y=200)
        self.opakovania_popis = Label(top_frame, text="Pocet opakovani:")
        self.opakovania_popis.place(x=10, y=240)
        self.opakovania_okno = Entry(top_frame)
        self.opakovania_okno.place(x=150, y=240)

        # button spustenie vybraneho algoritmu
        btn_inst = tk.Button(top_frame, text="Spustit", command=self.update_plots)
        btn_inst.place(x=20, y=140)#, command=self.select_algorithm(sel))

        # ramec pre import/export buttony
        self.io_frame_width = 300
        self.io_frame_height = 150
        io_frame = tk.Frame(top_frame, width=self.io_frame_width, height=self.io_frame_height, padx=10, pady=10, bg="white")
        io_frame.place(x=self.window_width - self.io_frame_width - 20, y=20)

        #bottom frame
        #buttom_frame = tk.Frame(self.root, padx=10, pady=10, bg="darkblue")
        self.left_bottom_frame = tk.Frame(bottom_frame, width=self.window_width/2, height=self.window_height/2)
        self.left_bottom_frame.place(x=0,y=0)
        self.right_bottom_frame = tk.Frame(bottom_frame, width=self.window_width/2, height=self.window_height/2)
        self.right_bottom_frame.place(x=self.window_width/2,y=0)
        self.init_plots()
        #bottom frame

        # import a export button, udaje FFT
        self.btn_import = tk.Button(io_frame, text="Importovat z .csv", command=self.import_file_dialogwindow)
        self.btn_import.place(x=10, y=20)
        self.btn_import.config(font=("Times New Roman", 10))
        # self.btn_load.pack(side="top", padx=5, pady=10)
        self.btn_export = tk.Button(io_frame, text="Exportovat do .csv", command=self.save_file_dialogwindow)
        self.btn_export.place(x=10, y=80)
        self.btn_export.config(font=("Times New Roman", 10))
        #messagebox.showinfo(":)","Subor bol exportovany do .csv")
    # zobrazenie navodu


    #inicializacia grafov (metoda)
    def init_plots(self):
        px = 1 / plt.rcParams['figure.dpi'] # konvertuje palce na pixely
        fig_width = (self.window_width / 2 - 2*50)*px #sirka grafu
        fig_height = (self.window_height / 2 - 2*40)*px # vyska grafu

        self.fig_td = Figure(figsize=(fig_width,fig_height), dpi=100)
        self.ax_td = self.fig_td.add_subplot(111)
        self.ax_td.set_title("časová doména")
        self.fig_td.tight_layout()
        self.canvas_td = FigureCanvasTkAgg(self.fig_td, master=self.left_bottom_frame)
        self.canvas_td.get_tk_widget().pack(side="top", fill="both", expand=True)

        self.fig_fd = Figure(figsize=(fig_width,fig_height), dpi=100)
        self.ax_fd = self.fig_fd.add_subplot(111)
        self.ax_fd.set_title("frekvenčná doména")
        self.fig_fd.tight_layout()
        self.canvas_fd = FigureCanvasTkAgg(self.fig_fd, master=self.right_bottom_frame)
        self.canvas_fd.get_tk_widget().pack(side="top", fill="both", expand=True)
        # xbod = np.array([])
        # ybod = np.array([1,10])
        # plt.plot(xbod, ybod, 'i')
        # plt.show()

    #update grafov
    def update_plots(self):
        if self.data is None:
            messagebox.showwarning("Warning", "Najprv importujte CSV súbor!")
            return

        try:
            x_values = self.data.iloc[:, 0].values  # prvy riadok
            y_values = self.data.iloc[:, 1].values
            n = len(y_values)
            # 1. Aktualizacia grafu signalu
            self.ax_td.clear()
            self.ax_td.plot(x_values,y_values, color='blue')
            self.ax_td.set_title("Časová doména (Raw Signal)")
            self.canvas_td.draw()
            self.data = fft_alg.cooley_tukey(y_values)


            # 2. Calculate FFT (Frequency Domain)
            # Using numpy for the calculation logic

            fft_values = np.fft.fft(y_values)
            fft_freq = np.fft.fftfreq(y_values)

            # Get magnitudes (absolute values)
            magnitudes = np.abs(fft_values)[:n // 2]
            freqs = fft_freq[:n // 2]


            # 3. Update Frequency Domain Plot
            self.ax_fd.clear()
            self.ax_fd.plot(freqs, magnitudes, color='red')
            self.ax_fd.set_title("Frekvenčná doména (Magnitude)")

            self.canvas_fd.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Chyba pri spracovaní dát: {e}")

#symbolicky main
if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()
