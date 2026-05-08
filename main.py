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
        self.insa_win_width = int(400*self.scale)
        self.insa_win_height = int(400*self.scale)
        self.insa_window.geometry(str(self.insa_win_width) + "x" + str(self.insa_win_height))
        # frame
        insm_frame = tk.Frame(self.insa_window, width=self.insa_win_width, height=self.insa_win_height, padx=int(10*self.scale), pady=int(10*self.scale), bg="lightblue")
        insm_frame.place(x=0, y=0)

        in_lbl_m = Label(insm_frame, text="Návod na použitie")
        in_lbl_m.place(x=int(10*self.scale), y=int(30*self.scale))
        in_lbl1 = Label(insm_frame, text="1. Importovať súbor vo formáte .csv")
        in_lbl1.place(x=int(10*self.scale), y=int(80*self.scale))
        in_lbl2 = Label(insm_frame, text="2. Vybrať algoritmus")
        in_lbl2.place(x=int(10*self.scale), y=int(110*self.scale))
        in_lbl3 = Label(insm_frame, text="3. Exportovať frekvenčné spektrum")
        in_lbl3.place(x=int(10*self.scale), y=int(140*self.scale))

        in_lbl_file = Label(insm_frame, text="Usporiadanie signálu v súbore .csv")
        in_lbl_file.place(x=int(10*self.scale), y=int(230*self.scale))
        in_lbl_file1 = Label(insm_frame, text="Prvý stĺpec je pre čas odobrania danej vzorky")
        in_lbl_file1.place(x=int(10 * self.scale), y=int(270 * self.scale))
        in_lbl_file2 = Label(insm_frame, text="Druhý stĺpec je pre amplitúdu vzorky v čase")
        in_lbl_file2.place(x=int(10 * self.scale), y=int(300 * self.scale))

    def open_alg_info(self):
        self.insb_window = tk.Toplevel(self.root)
        self.insb_window.title("Informácie o algoritmoch")
        self.insb_win_width = int(400*self.scale)
        self.insb_win_height = int(400*self.scale)
        self.insb_window.geometry(str(self.insb_win_width) + "x" + str(self.insb_win_height))
        # frame
        insb_frame = tk.Frame(self.insb_window, width=self.insb_win_width, height=self.insb_win_height, padx=int(10*self.scale), pady=int(10*self.scale), bg="lightblue")
        insb_frame.place(x=0, y=0)
        # nadpis
        lbl_nadpis = Label(insb_frame, text="Kalkulačka slúži na výpočet frekvenčného spektra vzorkovaného signálu rýchlou Fourieroveou transformácoiu")
        lbl_nadpis.place(x=int(10*self.scale), y=int(30*self.scale))
        # rolovanie zoznamu
        scroll_bar = Scrollbar(insb_frame)
        scroll_bar.pack(side=RIGHT,fill=Y)
        # info
        mylist = Listbox(insb_frame, yscrollcommand=scroll_bar.set)
        mylist.place(x=int(10*self.scale), y=int(70*self.scale))
        #
        mylist.insert(END, "Cooley-Tukey")
        mylist.insert(END, "Počet vzoriek: N = 2^n")
        mylist.insert(END, "Náročnosť: O = n log(n)")
        mylist.insert(END, "Cooley-Tukey")
        mylist.insert(END, " ")
        mylist.insert(END, "Prime Factor")
        mylist.insert(END, "Počet vzoriek: N = N1 * N2; N1 a N2 sú nesúdeliteľné")
        mylist.insert(END, "Náročnosť: O = n log(n)")
        mylist.insert(END, "Prime factor")
        mylist.insert(END, " ")
        mylist.insert(END, "Split Radix")
        mylist.insert(END, "Počet vzoriek: N = 4*n")
        mylist.insert(END, "Náročnosť: O = n log(n)")
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
        self.insm_win_width = int(400*self.scale)
        self.insm_win_height = int(300*self.scale)
        self.insm_window.geometry(str(self.insm_win_width)+"x"+str(self.insm_win_height))
        # frame
        insm_frame = tk.Frame(self.insm_window,width=self.insm_win_width, height=self.insm_win_height, padx=int(10*self.scale), pady=int(10*self.scale), bg="lightblue")
        insm_frame.place(x=0, y=0)
        # rozlozenie
        nadpis = Label(insm_frame, text="Vitajte v kalkulačke")
        nadpis.config(font=("Times New Roman", int(10*self.scale)))
        nadpis.place(x=int(50*self.scale), y=int(50*self.scale))
        btn1 = Button(insm_frame, text="Návod", command=self.open_ins)
        btn1.place(x=int(10*self.scale), y=int(100*self.scale))
        btn2 = Button(insm_frame, text="Algoritmy", command=self.open_alg_info)
        btn2.place(x=int(10*self.scale), y=int(140*self.scale))
        btn3 = Button(insm_frame, text="Informácie", command=self.open_app_info)
        btn3.place(x=int(10*self.scale), y=int(180*self.scale))

    def easter_egg(self):
        self.cal_window = tk.Toplevel(self.root)
        self.cal_window.title("Je číslo 2^n")
        self.cal_window.geometry("300x300")
        self.lbl = tk.Label(self.cal_window, text="Zadajte prirodzené číslo")
        self.lbl.config(font=("Times New Roman", int(10*self.scale)))
        self.lbl.place(x=int(10*self.scale), y=int(50*self.scale))
        self.t = tk.Text(self.cal_window)
        self.t.config(font=("Times New Roman", int(10*self.scale)), width=int(100*self.scale), height=int(50*self.scale))
        self.t.place(x=int(10*self.scale), y=int(50*self.scale))

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
        self.root = root
        self.dpi = self.root.winfo_fpixels('1i')
        self.scale = self.dpi/96
        self.window_width = int(1000*self.scale) #width = sirka
        self.window_height = int(600*self.scale) #height = vyska
        self.root.tk.call('tk', 'scaling', 2.5)
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
        top_frame = tk.Frame(self.root, width=self.window_width, height=self.frame_height, padx=int(10*self.scale), pady=int(10*self.scale), bg="lightblue")
        top_frame.place(x=0,y=0)
        bottom_frame = tk.Frame(self.root, width=self.window_width, height=self.frame_height, padx=0, pady=0, bg="red")
        bottom_frame.place(x=0,y=self.frame_height)
        #

        #Nadpis
        label_radio = tk.Label(top_frame, text="Vyberte FFT algoritmus")
        label_radio.place(x=int(20*self.scale), y=int(20*self.scale))
        label_radio.config(font=("Times New Roman", int(10*self.scale)))

        # Vyber FFT algoritmu
        self.sel = tk.IntVar(value=0)  # Jedna premenná pre Radiobuttony
        radio_btn1 = tk.Radiobutton(top_frame, variable=self.sel, text="Cooley-Tukey", value=0, bg="lightblue", command=self.update_plots)
        radio_btn1.place(x=int(20*self.scale), y=int(50*self.scale))
        radio_btn2 = tk.Radiobutton(top_frame, variable=self.sel, text="Prime Factor", value=1, bg="lightblue", command=self.update_plots)
        radio_btn2.place(x=int(20*self.scale), y=int(80*self.scale))
        radio_btn3 = tk.Radiobutton(top_frame, variable=self.sel, text="Split Radix", value=2, bg="lightblue", command=self.update_plots)
        radio_btn3.place(x=int(20*self.scale), y=int(110*self.scale))
        # zobrazenie metrik
        self.cas_popis = Label(top_frame, text="Čas programu:")
        self.cas_popis.place(x=int(10*self.scale), y=int(200*self.scale))
        self.cas_okno = Entry(top_frame)
        self.cas_okno.place(x=int(150*self.scale), y=int(200*self.scale))
        self.cas_okno.config(state=tk.DISABLED)
        self.mse_popis = Label(top_frame, text="Chyba (MSE):")
        self.mse_popis.place(x=int(10 * self.scale), y=int(240 * self.scale))
        self.mse_okno = Entry(top_frame)
        self.mse_okno.place(x=int(150 * self.scale), y=int(240 * self.scale))
        self.mse_okno.config(state=tk.DISABLED)
        self.add_popis = Label(top_frame, text="Sčítania:")
        self.add_popis.place(x=int(380 * self.scale), y=int(200 * self.scale))
        self.add_okno = Entry(top_frame)
        self.add_okno.place(x=int(480 * self.scale), y=int(200 * self.scale))
        self.add_okno.config(state=tk.DISABLED)
        self.mult_popis = Label(top_frame, text="Násobenia:")
        self.mult_popis.place(x=int(380 * self.scale), y=int(240 * self.scale))
        self.mult_okno = Entry(top_frame)
        self.mult_okno.place(x=int(480 * self.scale), y=int(240 * self.scale))
        self.mult_okno.config(state=tk.DISABLED)

        # button spustenie vybraneho algoritmu
        btn_inst = tk.Button(top_frame, text="Spustiť", command=self.update_plots)
        btn_inst.place(x=int(20*self.scale), y=int(140*self.scale))

        # ramec pre import/export buttony
        self.io_frame_width = int(300*self.scale)
        self.io_frame_height = int(150*self.scale)
        io_frame = tk.Frame(top_frame, width=self.io_frame_width, height=self.io_frame_height, padx=int(10*self.scale), pady=int(10*self.scale), bg="white")
        io_frame.place(x=self.window_width - self.io_frame_width - int(20*self.scale), y=int(20*self.scale))

        #bottom frame
        self.left_bottom_frame = tk.Frame(bottom_frame, width=self.window_width//2, height=self.frame_height)
        self.left_bottom_frame.place(x=0, y=0)
        self.left_bottom_frame.pack_propagate(False)
        self.right_bottom_frame = tk.Frame(bottom_frame, width=self.window_width//2, height=self.frame_height)
        self.right_bottom_frame.place(x=self.window_width//2, y=0)
        self.right_bottom_frame.pack_propagate(False)
        self.init_plots()
        #bottom frame

        # import a export button, udaje FFT
        self.btn_import = tk.Button(io_frame, text="Importovať z .csv", command=self.import_file_dialogwindow)
        self.btn_import.place(x=int(10*self.scale), y=int(20*self.scale))
        self.btn_import.config(font=("Times New Roman", int(10*self.scale)))
        # self.btn_load.pack(side="top", padx=5, pady=10)
        self.btn_export = tk.Button(io_frame, text="Exportovať do .csv", command=self.save_spectrum_dialogwindow)
        self.btn_export.place(x=int(10*self.scale), y=int(80*self.scale))
        self.btn_export.config(font=("Times New Roman", int(10*self.scale)))

    def _fit_plots(self):
        """Runs once after the window is fully rendered. Queries actual frame
        pixel sizes from tkinter and resizes matplotlib figures to match exactly,
        so no manual DPI/scaling arithmetic is needed."""
        for frame, fig, canvas in [
            (self.left_bottom_frame, self.fig_td, self.canvas_td),
            (self.right_bottom_frame, self.fig_fd, self.canvas_fd),
        ]:
            frame.update_idletasks()
            w = frame.winfo_width()
            h = frame.winfo_height()
            if w > 10 and h > 10:
                scale = 1  # how much of the frame the plot fills (lower = smaller)
                fig.set_size_inches(w * scale / fig.get_dpi(), h * scale / fig.get_dpi())
                fig.tight_layout()
                canvas.draw()

    #inicializacia grafov (metoda)
    def init_plots(self):
        dpi = self.dpi

        # Smaller text so labels/ticks don't dominate the plot area
        plt.rcParams.update({
            'font.size':        5,
            'axes.titlesize':   5,
            'axes.labelsize':   5,
            'xtick.labelsize':  5,
            'ytick.labelsize':  5,
        })
        # pack(fill="both", expand=True) then gives it the full frame.
        # _fit_plots() is called via after() once layout is settled, and resizes
        # the figure to the actual allocated frame size — no scaling guesswork.

        # casova domena
        self.fig_td = Figure(figsize=(1, 1), dpi=dpi)
        self.ax_td = self.fig_td.add_subplot(111)
        self.ax_td.set_xlabel("Čas [s]")
        self.ax_td.set_ylabel("Amplitúda")
        self.ax_td.set_title("Časová doména")
        self.canvas_td = FigureCanvasTkAgg(self.fig_td, master=self.left_bottom_frame)
        self.canvas_td.get_tk_widget().pack(side="top", fill="both", expand=True)

        # frekvencna domena
        self.fig_fd = Figure(figsize=(1, 1), dpi=dpi)
        self.ax_fd = self.fig_fd.add_subplot(111)
        self.ax_fd.set_xlabel("Frekvencia [Hz]")
        self.ax_fd.set_ylabel("Magnitúda")
        self.ax_fd.set_title("Frekvenčná doména")
        self.canvas_fd = FigureCanvasTkAgg(self.fig_fd, master=self.right_bottom_frame)
        self.canvas_fd.get_tk_widget().pack(side="top", fill="both", expand=True)

        # Wait for the window to finish laying out, then fit figures to frames
        self.root.after(150, self._fit_plots)

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
            self.ax_td.plot(x_values, y_values, color='lightblue')
            self.ax_td.set_title("Časová doména")
            self.ax_td.set_xlabel("Čas [s]")
            self.ax_td.set_ylabel("Amplitúda")
            self.canvas_td.draw()

            # Výber algoritmu a meranie času
            start_val = self.sel.get()

            def next_pow2(m):
                # najbližšia mocnina 2 >= m
                return 1 << (m - 1).bit_length() if m > 1 else 1

            def next_multiple(m, k):
                # najbližší násobok k >= m
                return ((m + k - 1) // k) * k if m > 0 else k

            def next_prime_factor_len(m):
                """Najbližšie N >= m, ktoré má aspoň jeden rozklad N=a*b,
                kde a>1, b>1 a gcd(a,b)=1 (podmienka pre Prime Factor)."""
                N = max(2, m)
                while True:
                    root = int(math.isqrt(N))
                    for a in range(2, root + 1):
                        if N % a == 0:
                            b = N // a
                            if math.gcd(a, b) == 1:
                                return N
                    N += 1

            if start_val == 0:
                # Cooley–Tukey: 2^k
                n_fft = next_pow2(n)
            elif start_val == 1:
                # Prime Factor: N = N1*N2, gcd(N1, N2) = 1
                n_fft = next_prime_factor_len(n)
            else:
                # Split-Radix: N = 4*k
                n_fft = next_multiple(n, 4)



            y_fft = np.pad(y_values, (0, n_fft - n), mode='constant') if n_fft != n else y_values

            time_start = time.time()
            if start_val == 0:
                fft_res, adds, mults = fft_alg.cooley_tukey(y_fft)
            elif start_val == 1:
                fft_res, adds, mults = fft_alg.prime_factor(y_fft)
            else:
                fft_res, adds, mults = fft_alg.split_radix(y_fft)

            time_end = time.time()
            duration = time_end - time_start

            reconstructed_signal = np.fft.ifft(fft_res)
            mse = np.mean(np.abs(y_fft - reconstructed_signal) ** 2)

            def update_field(entry, value):
                entry.config(state=tk.NORMAL)
                entry.delete(0, tk.END)
                entry.insert(0, value)
                entry.config(state=tk.DISABLED)

            update_field(self.cas_okno, f"{duration:.6f} s")
            update_field(self.add_okno, str(adds))
            update_field(self.mult_okno, str(mults))
            update_field(self.mse_okno, f"{mse:.2e}")


            # 3. Spracovanie výsledkov FFT pre graf
            # Magnitúda (absolútna hodnota)
            magnitudes = np.abs(fft_res)[:n_fft // 2]
            # Výpočet frekvenčnej osi (Hz)
            freq_axis = np.linspace(0, fs / 2, len(magnitudes))

            # Vykreslenie frekvenčnej domény
            self.ax_fd.clear()
            self.ax_fd.plot(freq_axis, magnitudes, color='red')
            self.ax_fd.set_title("Frekvenčná doména")
            self.ax_fd.set_xlabel("Frekvencia [Hz]")
            self.ax_fd.set_ylabel("Magnitúda")
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