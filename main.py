import math
import tkinter as tk

from contextlib import nullcontext
from idlelib.browser import file_open
from tkinter import ttk, messagebox, Label
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
import fft_alg

import time


class DataApp:
    def open_ins(self):
        self.insa_window = tk.Toplevel(self.root)
        self.insa_window.title("Návod na používanie aplikácie")
        self.insa_win_width = 400
        self.insa_win_height = 400
        self.insa_window.geometry(str(self.insa_win_width) + "x" + str(self.insa_win_height))
        # frame
        insm_frame = tk.Frame(self.insa_window, width=self.insa_win_width, height=self.insa_win_height, padx=10, pady=10, bg="blue")
        insm_frame.place(x=0, y=0)
        in_lbl1 = Label(insm_frame, text="1. Importovať súbor vo formáte .csv")
        in_lbl1.place(x=10, y=80)
        in_lbl2 = Label(insm_frame, text="2. Vybrať algoritmus")
        in_lbl2.place(x=10, y=110)
        in_lbl3 = Label(insm_frame, text="3. Potvrdiť vyber")
        in_lbl3.place(x=10, y=140)
        in_lbl4 = Label(insm_frame, text="4. Exportovať súbor")
        in_lbl4.place(x=10, y=170)

    def open_alg_info(self):
        self.insb_window = tk.Toplevel(self.root)
        self.insb_window.title("Informácie o algoritmoch")
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
        mylist.insert(END, "Počet vzoriek: 2^n")
        mylist.insert(END, "Cooley-Tukey")
        mylist.insert(END, " ")
        mylist.insert(END, "Prime Factor")
        mylist.insert(END, "Počet vzoriek: N = N1 * N2; N1 a N2 sú nesúdeliteľné")
        mylist.insert(END, "Prime factor")
        mylist.insert(END, " ")
        mylist.insert(END, "Split Radix")
        mylist.insert(END, "Počet vzoriek: N = 4*n")
        mylist.insert(END, "Split-Radix")
        mylist.pack(side=LEFT, fill=BOTH)
        scroll_bar.config(command=mylist.yview)

    def open_app_info(self):
        messagebox.showinfo("Informácie o aplikácii", "Autori: Matúš Banáš a Ing. Dominik Čambál\nJazyk: Python 3.14.2\nPoužité externé balíky: Matplotlib, numpy, pandas\n©2026")

    # otvori navod na pouzivanie
    def open_instruction_window(self):
        #definicia okna
        self.insm_window = tk.Toplevel(self.root)
        self.insm_window.title("Používateľská príručka")
        self.insm_win_width = 400
        self.insm_win_height = 300
        self.insm_window.geometry(str(self.insm_win_width)+"x"+str(self.insm_win_height))
        # frame
        insm_frame = tk.Frame(self.insm_window,width=self.insm_win_width, height=self.insm_win_height, padx=10, pady=10, bg="blue")
        insm_frame.place(x=0, y=0)
        # rozlozenie
        nadpis = Label(insm_frame, text="Vitajte v kalkulačke")
        nadpis.config(font=("Times New Roman", 10))
        nadpis.place(x=50, y=50)
        btn1 = Button(insm_frame, text="Návod", command=self.open_ins)
        btn1.place(x=10, y=100)
        btn2 = Button(insm_frame, text="Algoritmy", command=self.open_alg_info)
        btn2.place(x=10, y=140)
        btn3 = Button(insm_frame, text="Informácie", command=self.open_app_info)
        btn3.place(x=10, y=180)

    def easter_egg(self):
        self.cal_window = tk.Toplevel(self.root)
        self.cal_window.title("Je číslo 2^n")
        self.cal_window.geometry("300x300")
        self.lbl = tk.Label(self.cal_window, text="Zadajte prirodzené číslo")
        self.lbl.config(font=("Times New Roman", 10))
        self.lbl.place(x=10, y=50)
        self.t = tk.Text(self.cal_window)
        self.t.config(font=("Times New Roman", 10), width=100, height=50)
        self.t.place(x=10, y=50)

    # importuje subor
    def import_file_dialogwindow(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        file = open(filepath, "r")
        self.data = pd.read_csv(file, header=None)
        #self.data = self.data.values.flatten()
        self.update_plots()


    # ulozi subor ako .csv
    def save_spectrum_dialogwindow(self):
        if not hasattr(self, 'spectrum_data') or self.spectrum_data is None:
            messagebox.showwarning("Varovanie", "Najprv musíte spustiť výpočet FFT!")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Uložiť frekvenčné spektrum"
        )

        if filepath:
            # Uložíme s hlavičkou, aby sme vedeli, čo je čo
            self.spectrum_data.to_csv(filepath, index=False)
            messagebox.showinfo("Info", "Frekvenčné spektrum bolo uložené.")

    #konstruktor
    def __init__(self, root): #hlavne okno
        # vlastnosti okna
        self.insm_window = None
        self.cal_window = None
        self.window_width = 1000 #width = sirka
        self.window_height = 600 #height = vyska
        self.root = root
        self.root.title("Výpočet FFT")
        self.root.geometry(str(self.window_width)+"x"+str(self.window_height))
        self.root.resizable(False, False)

        #vlastnost, ulozi sa do tejto premennej data z csv
        self.data = None

        #definicia layoutu (rozlozenia)
        #menu
        menubar = Menu(root)
        navody = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Návody', menu=navody)
        navody.add_command(label = "Návod", command=self.open_instruction_window)
        navody.add_command(label = "2^n", command=self.easter_egg)
        self.root.config(menu=menubar)
        #

        #horny a dolny ramec
        self.frame_height = self.window_height//2
        top_frame = tk.Frame(self.root, width=self.window_width, height=self.frame_height, padx=10, pady=10, bg="lightblue")
        top_frame.place(x=0,y=0)
        bottom_frame = tk.Frame(self.root, width=self.window_width, height=self.frame_height, padx=0, pady=0, bg="red")
        bottom_frame.place(x=0,y=self.frame_height)
        #

        #Nadpis
        label_radio = tk.Label(top_frame, text="Vyberte FFT algoritmus")
        label_radio.place(x=20, y=20)
        label_radio.config(font=("Times New Roman", 10))

        # Vyber FFT algoritmu
        self.sel = tk.IntVar(value=0)  # Jedna premenná pre Radiobuttony
        radio_btn1 = tk.Radiobutton(top_frame, variable=self.sel, text="Cooley-Tukey", value=0, bg="lightblue")
        radio_btn1.place(x=20, y=50)
        radio_btn2 = tk.Radiobutton(top_frame, variable=self.sel, text="Prime Factor", value=1, bg="lightblue")
        radio_btn2.place(x=20, y=80)
        radio_btn3 = tk.Radiobutton(top_frame, variable=self.sel, text="Split Radix", value=2, bg="lightblue")
        radio_btn3.place(x=20, y=110)
        # zobrazenie metrik
        self.cas_popis = Label(top_frame, text="Čas programu:")
        self.cas_popis.place(x=10, y=200)
        self.cas_okno = Entry(top_frame)
        self.cas_okno.place(x=150, y=200)
        self.cas_okno.config(state=tk.DISABLED)
        self.opakovania_popis = Label(top_frame, text="Počet opakovaní:")
        self.opakovania_popis.place(x=10, y=240)
        self.opakovania_okno = Entry(top_frame)
        self.opakovania_okno.place(x=150, y=240)
        self.opakovania_okno.config(state=tk.DISABLED)

        # button spustenie vybraneho algoritmu
        btn_inst = tk.Button(top_frame, text="Spustiť", command=self.update_plots)
        btn_inst.place(x=20, y=140)

        # ramec pre import/export buttony
        self.io_frame_width = 300
        self.io_frame_height = 150
        io_frame = tk.Frame(top_frame, width=self.io_frame_width, height=self.io_frame_height, padx=10, pady=10, bg="white")
        io_frame.place(x=self.window_width - self.io_frame_width - 20, y=20)

        #bottom frame
        #buttom_frame = tk.Frame(self.root, padx=10, pady=10, bg="darkblue")
        self.left_bottom_frame = tk.Frame(bottom_frame, width=self.window_width/2, height=self.window_height/2, padx=10, pady=10)
        self.left_bottom_frame.place(x=0,y=0)
        self.right_bottom_frame = tk.Frame(bottom_frame, width=self.window_width/2, height=self.window_height/2, padx=10, pady=10)
        self.right_bottom_frame.place(x=self.window_width//2,y=0)
        self.init_plots()
        #bottom frame

        # import a export button, udaje FFT
        self.btn_import = tk.Button(io_frame, text="Importovať z .csv", command=self.import_file_dialogwindow)
        self.btn_import.place(x=10, y=20)
        self.btn_import.config(font=("Times New Roman", 10))
        # self.btn_load.pack(side="top", padx=5, pady=10)
        self.btn_export = tk.Button(io_frame, text="Exportovať do .csv", command=self.save_spectrum_dialogwindow)
        self.btn_export.place(x=10, y=80)
        self.btn_export.config(font=("Times New Roman", 10))

    #inicializacia grafov (metoda)
    def init_plots(self):
        dpi = plt.rcParams['figure.dpi']
        px = 1 / dpi # konvertuje pixelov na palce
        available_w = (self.window_width // 2) - 2 * 10
        available_h = self.frame_height - 2 * 10
        fig_width = available_w * px #sirka grafu
        fig_height = available_h * px # vyska grafu

        # casova domena
        self.fig_td = Figure(figsize=(fig_width,fig_height), dpi=dpi, layout='constrained')
        self.ax_td = self.fig_td.add_subplot(111)
        self.ax_td.set_xlabel("Čas")
        self.ax_td.set_ylabel("Amplitúda")
        self.ax_td.set_title("Časová doména")
        self.fig_td.tight_layout()
        self.canvas_td = FigureCanvasTkAgg(self.fig_td, master=self.left_bottom_frame)
        self.canvas_td.get_tk_widget().pack(side="top", fill="both", expand=True)

        # frekvencna domena
        self.fig_fd = Figure(figsize=(fig_width,fig_height), dpi=dpi, layout='constrained')
        self.ax_fd = self.fig_fd.add_subplot(111)
        self.ax_fd.set_xlabel("Frekvencia")
        self.ax_fd.set_ylabel("Magnitúda")
        self.ax_fd.set_title("Frekvenčná doména")
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
            messagebox.showwarning("Varovanie", "Najprv importujte CSV súbor!")
            return

        try:
            # Extrakcia hodnôt (neprepisujeme self.data!)
            x_values = self.data.iloc[:, 0].values  # časová os
            y_values = self.data.iloc[:, 1].values  # amplitúda
            n = len(y_values)

            # Výpočet vzorkovacej frekvencie (predpokladáme rovnomerné vzorkovanie)
            dt = x_values[1] - x_values[0]
            fs = 1.0 / dt

            # Vykreslenie časovej domény
            self.ax_td.clear()
            self.ax_td.plot(x_values, y_values, color='blue')
            self.ax_td.set_title("Časová doména (Raw Signal)")
            self.ax_td.set_xlabel("Čas [s]")
            #self.fig_td.tight_layout()
            self.canvas_td.draw()

            # Výber algoritmu a meranie času
            start_val = self.sel.get()
            time_start = time.time()
            if start_val == 0:
                fft_res = fft_alg.cooley_tukey(y_values)
            elif start_val == 1:
                fft_res = fft_alg.prime_factor(y_values)
            else:
                fft_res = fft_alg.split_radix(y_values)

            time_end = time.time()
            duration = time_end - time_start

            # Aktualizácia políčka pre čas v UI
            self.cas_okno.delete(0, tk.END)
            self.cas_okno.insert(0, f"{duration:.6f} s")

            # 3. Spracovanie výsledkov FFT pre graf
            # Magnitúda (absolútna hodnota)
            magnitudes = np.abs(fft_res)[:n // 2]
            # Výpočet frekvenčnej osi (Hz)
            freq_axis = np.linspace(0, fs / 2, len(magnitudes))

            # Vykreslenie frekvenčnej domény
            self.ax_fd.clear()
            self.ax_fd.plot(freq_axis, magnitudes, color='red')
            self.ax_fd.set_title("Frekvenčná doména (Amplitúdové spektrum)")
            self.ax_fd.set_xlabel("Frekvencia [Hz]")
            #self.fig_fd.tight_layout()
            self.canvas_fd.draw()

            # extrahoanie dat z frekvencneho spektra
            self.spectrum_data = pd.DataFrame({
                'Frequency_Hz': freq_axis,
                'Magnitude': magnitudes
            })

        except Exception as e:
            messagebox.showerror("Error", f"Chyba pri spracovaní dát: {e}")

#symbolicky main
if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()
