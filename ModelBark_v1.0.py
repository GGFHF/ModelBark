#!/usr/bin/env python3

"""
    ModelBark: a toy model to study bark formation in Woody species

    Authors: Álvaro Gutiérrez Climent, Juan Carlos Nuño, Unai López de Heredia, Álvaro Soto

    UTF-8

"""


import tkinter as tk
import os
from PIL import ImageTk, Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use('agg')

working_directory = os.getcwd()

class Plant:
    def __init__(self):

        self.radius = [1]
        self.number_phellogen = 0
        self.xylem_storage = [0]
        self.phloem_storage = [0]
        self.inactive_phloem_storage = [0]
        self.phellem_storage = [0]
        self.phelloderm_storage = [0]
        self.equation_storage = [1]
        self.first_phellogen_storage = 0

    def sample(self, probability: float):

        sample = np.random.random_sample()

        if sample <= probability:
            return int(0)

        else:
            return int(1)

    def vascular_cambium_division(self, vcdr: float):

        radius_mod = self.radius

        sample = self.sample(vcdr)

        if sample == 0:
            radius_mod.insert(0, 0)

        if sample == 1:
            radius_mod.insert(radius_mod.index(1) + 1, 0)

        self.radius = radius_mod

    def first_phellogen(self, percentage: float):

        radius_mod = self.radius

        vascular_cambium_position = radius_mod.index(1)

        radius_length = len(radius_mod)

        insert_place = (
            radius_length - (round((radius_length - vascular_cambium_position) * percentage)))

        radius_mod.insert(insert_place, 3)

        self.radius = radius_mod

        self.first_phellogen_storage = len(radius_mod)

        self.number_phellogen = 1

    def phellem_production(self, pdr: float):

        radius_mod = self.radius

        number_phellogen_mod = self.number_phellogen

        phellogen_position = radius_mod.index(3)

        if self.sample(pdr) == 0:
            radius_mod.insert(phellogen_position + 1,
                              (number_phellogen_mod + 3))

        self.radius = radius_mod

    def phelloderm_production(self, pddr: float):

        radius_mod = self.radius

        phellogen_position = radius_mod.index(3)

        if self.sample(pddr) == 0:
            radius_mod.insert(phellogen_position,
                              (2))
        
        self.radius = radius_mod

        
    def new_phellogen(self, percentage: float):

        radius_mod = self.radius

        vascular_cambium_position = radius_mod.index(1)

        phellogen_position = radius_mod.index(3)

        insert_place = (phellogen_position - round((phellogen_position -
                        vascular_cambium_position) * percentage))

        radius_mod[phellogen_position] = (self.number_phellogen + 3)

        radius_mod.insert(insert_place, 3)

        self.number_phellogen += 1

        self.radius = radius_mod

    def radius_length(self):

        return len(self.radius)

    def num_last_phellogen_cells(self):

        radius_mod = self.radius

        number_phellogen = self.number_phellogen

        return int(radius_mod.count(number_phellogen + 3))

    def num_xylem_cells(self):

        radius_mod = self.radius

        return radius_mod.index(1)

    def num_phloem_cells(self):

        radius_mod = self.radius

        vascular_cambium_position = radius_mod.index(1)

        if radius_mod.count(3) == 1:

            phellogen_position = radius_mod.index(3)

            return radius_mod[vascular_cambium_position:phellogen_position].count(0)
            
        else:
            return radius_mod.count(0) - vascular_cambium_position

    def num_phellem_cells(self):

        radius_mod = self.radius

        if radius_mod.count(3) == 0:
            return 0

        else:

            num_xylem_or_phloem_cells = radius_mod.count(0)
            num_phelloderm_cells = radius_mod.count(2)
            radius_length = len(radius_mod)
            vascular_suber_cambium_cells = radius_mod.count(1) + radius_mod.count(3)
            return radius_length - num_xylem_or_phloem_cells - num_phelloderm_cells - vascular_suber_cambium_cells
    
    def num_phellogen_cells(self):

        radius_mod = self.radius

        return radius_mod.count(3)
        
        
    def num_phelloderm_cells(self):

        radius_mod = self.radius

        return radius_mod.count(2)


    def num_inactive_phloem_cells(self):

        radius_mod = self.radius

        num_xylem_or_phloem_cells = radius_mod.count(0)

        xylem_cells = self.num_xylem_cells()

        active_phloem_cells = self.num_phloem_cells()

        return num_xylem_or_phloem_cells - xylem_cells - active_phloem_cells

    def parameters(self):

        xylem = self.num_xylem_cells()

        phloem = self.num_phloem_cells()

        phellem = self.num_phellem_cells()

        inactive_phloem = self.num_inactive_phloem_cells()

        phelloderm = self.num_phelloderm_cells()

        phellogen = self.num_phellogen_cells()

        return [xylem, phloem, phellem, inactive_phloem, phelloderm, phellogen]

    def equation(self, a, b, c, d, e, f, g):

        radius_parameters = self.parameters()

        xylem_a = a * radius_parameters[0]

        phloem_b = b * radius_parameters[1]

        phellem_c = c * radius_parameters[2]

        inactive_phloem_d = d * radius_parameters[3]

        phelloderm_e = e * radius_parameters[4]

        phellogen_f = f * radius_parameters[5]

        vascular_cambium_g = g * 1

        return (1 + phellem_c + inactive_phloem_d + phelloderm_e + phellogen_f) / (xylem_a + phloem_b + vascular_cambium_g)

    def graphical_parameters_storage(self, a, b, c, d, e, f, g):

        self.xylem_storage.append(self.num_xylem_cells())

        self.phloem_storage.append(self.num_phloem_cells())

        self.phellem_storage.append(self.num_phellem_cells())

        self.inactive_phloem_storage.append(self.num_inactive_phloem_cells())

        self.phelloderm_storage.append(self.num_phelloderm_cells())

        self.equation_storage.append(self.equation(a, b, c, d, e, f, g))

    def result(self):

        output = self.parameters()

        output.append(self.number_phellogen)

        output.append(self.first_phellogen_storage)

        output.append(self.radius)

        return output

    def plotting(self, k):

        if not os.path.exists(os.path.join(working_directory, 'Figures')):
            os.mkdir(os.path.join(working_directory, 'Figures'))

        # Parameters through time plot

        plt.plot(self.xylem_storage, label='Xylem')

        plt.plot(self.phloem_storage, label='Phloem')

        plt.plot(self.phellem_storage, label='Phellem')

        plt.plot(self.inactive_phloem_storage, label='Inactive Phloem')

        plt.plot(self.phelloderm_storage, label= 'Phelloderm')

        plt.legend()

        plt.title('Parameters of the model through time')

        plt.savefig('Figures/Parameters_plot.jpg')

        plt.close()

        # Equation through time plot

        plt.plot(self.equation_storage, label='F(t)')

        plt.axhline(y=k, color='r', linestyle=':', label='K threshold')

        plt.legend()

        plt.title('F(t) through time')

        plt.savefig('Figures/Equation_plot.jpg')

        plt.close('all')


def simulation_generation(vascular_cambium_division_rate: float,
                          phellogen_division_rate: float,
                          phelloderm_division_rate: float,
                          phellogen_position: float,
                          a: float,
                          b: float,
                          c: float,
                          d: float,
                          e:float,
                          f:float,
                          g:float,
                          threshold: float,
                          max_length: int):
    
    simulation = Plant()
    simulation.vascular_cambium_division(vascular_cambium_division_rate)
    simulation.graphical_parameters_storage(a, b, c, d, e, f, g)

    while simulation.equation(a, b, c, d, e, f, g) >= threshold:
        simulation.vascular_cambium_division(vascular_cambium_division_rate)
        simulation.graphical_parameters_storage(a, b, c, d, e, f, g)

        if simulation.radius_length() >= max_length:
            break

    if simulation.radius_length() >= max_length:
        simulation.plotting(threshold)
        return simulation.result()

    else:

        simulation.first_phellogen(phellogen_position)
        while simulation.radius_length() <= max_length:

            while simulation.equation(a, b, c, d, e, f, g) >= threshold and simulation.radius_length() <= max_length:
                simulation.vascular_cambium_division(
                    vascular_cambium_division_rate)
                simulation.phellem_production(phellogen_division_rate)
                simulation.phelloderm_production(phelloderm_division_rate)
                simulation.graphical_parameters_storage(a, b, c, d, e, f, g)

            if simulation.radius_length() <= max_length:
                simulation.new_phellogen(phellogen_position)
                simulation.vascular_cambium_division(
                    vascular_cambium_division_rate)

            else:
                break

        simulation.plotting(threshold)
        return simulation.result()

def multiple_simulation(iterations, input_file, output_file_name):
            output_dataset = []

            for combination in range(len(input_file)):

                for iteration in range(iterations):
                    print(f'Running combination n: {combination + 1}, iteration:{iteration + 1}')
                    output_dataset.append(simulation_generation(input_file.iloc[combination, 0],
                                                                input_file.iloc[combination, 1],
                                                                input_file.iloc[combination, 2],
                                                                input_file.iloc[combination, 3],
                                                                input_file.iloc[combination, 4],
                                                                input_file.iloc[combination, 5],
                                                                input_file.iloc[combination, 6],
                                                                input_file.iloc[combination, 7],
                                                                input_file.iloc[combination, 8],
                                                                input_file.iloc[combination, 9],
                                                                input_file.iloc[combination, 10],
                                                                input_file.iloc[combination, 11],
                                                                input_file.iloc[combination, 12],)[8])
            export_df = pd.DataFrame(output_dataset)
            export_df.iloc[:,0:input_file.iloc[0, 12]].to_csv(output_file_name, index=False, header= False)
            print('Multiple Simulation Completed')

main_menu = tk.Tk()

screen_width = main_menu.winfo_screenwidth()
screen_height = main_menu.winfo_screenheight()

main_menu.configure(bg='white')
main_menu.title(
    'UPM - Universidad Politécnica de Madrid - Departamento de Sistemas y Recursos Naturales')

title_frame = tk.Frame(main_menu, bg='white')
title_frame.grid(row=0, column=0, padx=20, pady=10)
tk.Label(title_frame,
         text='ModelBark: a toy model to study bark formation in Woody species',
         bg='white',
         font=('Bahnschrift SemiBold Condensed', 18)).grid(row=0, column=0)
tk.Label(title_frame,
         text='Authors: Álvaro Gutiérrez Climent, Juan Carlos Nuño, Unai López de Heredia, Álvaro Soto',
         bg='white').grid(row=1, column=0, pady=10)

input_frame = tk.Frame(main_menu, bg='white')
input_frame.grid(row=1, column=0)

tk.Label(input_frame, text='r',
         bg='white').grid(row=0, column=0, padx=(30, 0))
tk.Label(input_frame, text='\u03B2',
         bg='white').grid(row=0, column=1)
tk.Label(input_frame, text='\u03B3',
         bg='white').grid(row=0, column=2)
tk.Label(input_frame, text='p',
          
         bg='white').grid(row=0, column=3)
tk.Label(input_frame, text='a', bg='white').grid(row=0, column=4)
tk.Label(input_frame, text='b', bg='white').grid(row=0, column=5)
tk.Label(input_frame, text='c', bg='white').grid(row=0, column=6)
tk.Label(input_frame, text='d', bg='white').grid(row=2, column=0)
tk.Label(input_frame, text='e', bg='white').grid(row=2, column=1)
tk.Label(input_frame, text='f', bg='white').grid(row=2, column=2)
tk.Label(input_frame, text='g', bg='white').grid(row=2, column=3)
tk.Label(input_frame, text='K', bg='white').grid(row=2, column=4)
tk.Label(input_frame, text='ML',
         bg='white').grid(row=2, column=5, pady=5)
tk.Label(input_frame, text="Input File Name",
         bg="white").grid(row=0, column=8, pady=5, padx=(60,20))
tk.Label(input_frame, text="Output File Name",
         bg="white").grid(row=0, column=9, pady=5)
tk.Label(input_frame, text="Iterations",
         bg="white").grid(row=0, column=10, pady=5)

vcdr_input = tk.Entry(input_frame, bg='pale green', width=7)
pdr_input = tk.Entry(input_frame, bg='pale green', width=7)
phdr_input = tk.Entry(input_frame, bg='pale green', width=7)
ppos_input = tk.Entry(input_frame, bg='pale green', width=7)
a_input = tk.Entry(input_frame, bg='pale green', width=7)
b_input = tk.Entry(input_frame, bg='pale green', width=7)
c_input = tk.Entry(input_frame, bg='pale green', width=7)
d_input = tk.Entry(input_frame, bg='pale green', width=7)
e_input = tk.Entry(input_frame, bg='pale green', width=7)
f_input = tk.Entry(input_frame, bg='pale green', width=7)
g_input = tk.Entry(input_frame, bg='pale green', width=7)
threshold_input = tk.Entry(input_frame, bg='pale green', width=7)
max_length_input = tk.Entry(input_frame, bg='pale green', width=7)
file_name_input = tk.Entry(input_frame, bg="pale green", width=13)
output_name_input = tk.Entry(input_frame, bg="pale green", width=13)
iterations_input = tk.Entry(input_frame, bg="pale green", width=13)

vcdr_input.grid(row=1, column=0, padx=(30, 0), pady=10)
pdr_input.grid(row=1, column=1, padx=20, pady=10)
phdr_input.grid(row=1, column=2, padx=20, pady=10)
ppos_input.grid(row=1, column=3, padx=20, pady=10)
a_input.grid(row=1, column=4, padx=20, pady=10)
b_input.grid(row=1, column=5, padx=20, pady=10)
c_input.grid(row=1, column=6, padx=20, pady=10)
d_input.grid(row=3, column=0, padx=(30, 0), pady=(0, 30))
e_input.grid(row=3, column=1, padx=20, pady=(0, 30))
f_input.grid(row=3, column=2, padx=20, pady=(0, 30))
g_input.grid(row=3, column=3, padx=20, pady=(0, 30))
threshold_input.grid(row=3, column=4, padx=20, pady=(0, 30))
max_length_input.grid(row=3, column=5, padx=20, pady=(0, 30))
file_name_input.grid(row=1, column=8, padx=(60,20), pady=10)
output_name_input.grid(row=1, column=9, padx=20, pady=10)
iterations_input.grid(row=1, column=10, padx=20, pady=10)


vcdr_input.insert(0, 0.9)
pdr_input.insert(0, 0.054)
ppos_input.insert(0,0.3)
phdr_input.insert(0,0.0025)
a_input.insert(0, 0.016)
b_input.insert(0, 0.008)
c_input.insert(0, 0.3)
d_input.insert(0, 0.002)
e_input.insert(0,0.001)
f_input.insert(0,0.0025)
g_input.insert(0,0.0025)
threshold_input.insert(0, 1)
max_length_input.insert(0, 1000)


def single_run():

    vcdr_get = vcdr_input.get()
    pdr_get = pdr_input.get()
    ppos_get = ppos_input.get()
    phdr_get = phdr_input.get()
    a_get = a_input.get()
    b_get = b_input.get()
    c_get = c_input.get()
    d_get = d_input.get()
    e_get = e_input.get()
    f_get = f_input.get()
    g_get = g_input.get()
    threshold_get = threshold_input.get()
    max_length_get = max_length_input.get()
    tester = bool()

    try:
        vcdr_get = float(vcdr_get)
        pdr_get = float(pdr_get)
        ppos_get = float(ppos_get)
        phdr_get = float(phdr_get)
        a_get = float(a_get)
        b_get = float(b_get)
        c_get = float(c_get)
        d_get = float(d_get)
        e_get = float(e_get)
        f_get = float(f_get)
        g_get = float(g_get)
        threshold_get = float(threshold_get)
        max_length_get = int(max_length_get)
        tester = True

    except ValueError:

        error = tk.Toplevel()
        error.configure(bg='white')
        error.geometry('330x50')
        tk.Label(error, text="Error when entering the data into the equation",
                 bg="white").place(x=10, y=15)
        error.mainloop()

    if tester:
        input_data = [vcdr_get, pdr_get, phdr_get, ppos_get, a_get, b_get,
                      c_get, d_get, e_get, f_get, g_get, threshold_get, max_length_get]
        run = simulation_generation(input_data[0],
                                    input_data[1],
                                    input_data[2],
                                    input_data[3],
                                    input_data[4],
                                    input_data[5],
                                    input_data[6],
                                    input_data[7],
                                    input_data[8],
                                    input_data[9],
                                    input_data[10],
                                    input_data[11],
                                    input_data[12],)
        
        print(run)

        radius_list = run[8]
        res = [(max(run[8]) + 1) if item ==
               1 else item for item in radius_list]
        heatmap = np.array(res)
        heatmap = np.expand_dims(heatmap, axis=0)

        plt.figure(figsize=(14, 1.8))
        # YlOrBr tab20
        plt.imshow(heatmap, aspect='auto', cmap='YlOrBr')
        plt.axis('on')
        plt.title('Radius heatmap plot')
        plt.savefig('Figures/heatmap_plot.jpg')
        plt.close()

        results_menu = tk.Toplevel()
        results_menu.configure(bg="white")
        results_menu.title(
            'UPM - Universidad Politécnica de Madrid - Departamento de Sistemas y Recursos Naturales')

        header_frame = tk.Frame(results_menu, bg='white')
        header_frame.grid(row=0, column=0, )
        tk.Label(header_frame,
                 text='ModelBark: a toy model to study bark formation in Woody species',
                 bg='white',
                 font=('Bahnschrift SemiBold Condensed', 18)).grid(row=0, column=0)
        tk.Label(header_frame,
                 text='Authors: Álvaro Gutiérrez Climent, Juan Carlos Nuño, Unai López de Heredia, Álvaro Soto',
                 bg='white').grid(row=1, column=0, pady=10)

        main_frame = tk.Frame(results_menu, bg='white')
        main_frame.grid(row=1, column=0, padx=20, pady=10)

        statistics_frame = tk.Frame(main_frame, bg='white')
        statistics_frame.grid(row=0, column=0)
        tk.Label(statistics_frame,
                 text='Simulation Statistics',
                 bg='white',
                 font=('*font', 12, 'bold')).grid(row=0)
        tk.Label(statistics_frame,
                 text='Input parameters:',
                 bg='white',
                 font=('*font', 10, 'bold')).grid(row=1, sticky="W")
        tk.Label(statistics_frame,
                 text=f'r: {input_data[0]}',
                 bg='white').grid(row=2, sticky="W")
        tk.Label(statistics_frame,
                 text=f'\u03B2: {input_data[1]}',
                 bg='white').grid(row=3, sticky="W")
        tk.Label(statistics_frame,
                 text=f'\u03B3: {input_data[2]}',
                 bg='white').grid(row=4, sticky="W")
        tk.Label(statistics_frame,
                 text=f'p: {input_data[3]}',
                 bg='white').grid(row=5, sticky="W")
        tk.Label(statistics_frame,
                 text=f'a: {input_data[4]}',
                 bg='white').grid(row=6, sticky="W")
        tk.Label(statistics_frame,
                 text=f'b: {input_data[5]}',
                 bg='white').grid(row=7, sticky="W")
        tk.Label(statistics_frame,
                 text=f'c: {input_data[6]}',
                 bg='white').grid(row=8, sticky="W")
        tk.Label(statistics_frame,
                 text=f'd: {input_data[7]}',
                 bg='white').grid(row=9, sticky="W")
        tk.Label(statistics_frame,
                 text=f'e: {input_data[8]}',
                 bg='white').grid(row=10, sticky="W")
        tk.Label(statistics_frame,
                 text=f'f: {input_data[9]}',
                 bg='white').grid(row=11, sticky="W")
        tk.Label(statistics_frame,
                 text=f'g: {input_data[10]}',
                 bg='white').grid(row=12, sticky="W")
        tk.Label(statistics_frame,
                 text=f'K: {input_data[11]}',
                 bg='white').grid(row=13, sticky="W")
        tk.Label(statistics_frame,
                 text=f'Length of the radius: {input_data[12]}',
                 bg='white').grid(row=14, sticky="W")
        tk.Label(statistics_frame,
                 text='Output Statistics:',
                 bg='white',
                 font=('*font', 10, 'bold')).grid(row=15, sticky="W")
        tk.Label(statistics_frame,
                 text=f'Xylem cells number: {run[0]}',
                 bg='white').grid(row=16, sticky="W")
        tk.Label(statistics_frame,
                 text=f'Phloem cells number: {run[1]}',
                 bg='white').grid(row=17, sticky="W")
        tk.Label(statistics_frame,
                 text=f'Phellem cells number: {run[2]}',
                 bg='white').grid(row=18, sticky="W")
        tk.Label(statistics_frame,
                 text=f'Inactive phloem cells number: {run[3]}',
                 bg='white').grid(row=19, sticky="W")
        tk.Label(statistics_frame,
                 text=f'Phelloderm cells number: {run[4]}',
                 bg='white').grid(row=20, sticky="W")
        tk.Label(statistics_frame,
                 text=f'Phellogens created: {run[6]}',
                 bg='white').grid(row=21, sticky="W")
        tk.Label(statistics_frame,
                 text=f'Moment when the first phellogen was created: {run[7]}',
                 bg='white').grid(row=22, sticky="W")

        img_frame = tk.Frame(main_frame, bg='white')
        img_frame.grid(row=0, column=1)

        heatmap_frame = tk.Frame(img_frame, bg='white')
        heatmap_frame.grid(row=0, column=0)

        heatmap_img = Image.open('Figures/heatmap_plot.jpg')
        heatmap_width = round(screen_width / 2.13)
        heatmap_height = round(heatmap_width / 7.7)
        heatmap_resize = heatmap_img.resize((heatmap_width, heatmap_height))
        heatmap_photoimag = ImageTk.PhotoImage(heatmap_resize)
        tk.Label(heatmap_frame, image=heatmap_photoimag,
                 bg='white').grid(row=0, column=0, pady=15)

        graphs_frame = tk.Frame(img_frame, bg='white')
        graphs_frame.grid(row=1, column=0)

        parameter_img = Image.open("Figures/Parameters_plot.jpg")
        parameter_img_width = round(screen_width / 4.51)
        parameter_img_height = round(parameter_img_width / 1.41)
        parameter_img_resize = parameter_img.resize(
            (parameter_img_width, parameter_img_height))
        parameter_photoimag = ImageTk.PhotoImage(parameter_img_resize)
        tk.Label(graphs_frame, image=parameter_photoimag,
                 bg="white").grid(row=0, column=0)

        equation_img = Image.open("Figures/Equation_plot.jpg")
        equation_img_width = round(screen_width / 4.51)
        equation_img_height = round(equation_img_width / 1.41)
        equation_img_resize = equation_img.resize(
            (equation_img_width, equation_img_height))
        equation_photoimag = ImageTk.PhotoImage(equation_img_resize)
        tk.Label(graphs_frame, image=equation_photoimag,
                 bg="white").grid(row=0, column=1)

        footer_frame = tk.Frame(results_menu, bg='white')
        footer_frame.grid(row=2, column=0)
        tk.Label(footer_frame, text="Radius", bg="white",
                 font=('*font', 10, 'bold')).grid(row=0, column=0)
        radius_text = tk.Text(footer_frame, height=5, width=120, wrap="word")
        radius_text.insert('end', run[8])
        radius_text.grid(row=1, column=0, padx=10, pady=10)

        results_menu.mainloop()


def multiple_run():

    iterations_get = iterations_input.get()
    file_name_get = file_name_input.get()
    output_name_get = output_name_input.get()

    try:
        iterations_get = int(iterations_get)
        file_name_get = str(file_name_get)
        output_name_get = str(output_name_get)
        tester = True

    except ValueError:

        error = tk.Toplevel()
        error.configure(bg='white')
        error.geometry('330x50')
        tk.Label(error, text="Error when entering the data into the equation",
                 bg="white").place(x=10, y=15)
        error.mainloop()

    if tester:
        
        input_file_name = f'{file_name_get}.csv'
        output_name = f'{output_name_get}.csv'
        input_file_csv = pd.read_csv(input_file_name, header=None)
        multiple_simulation( iterations_get, input_file_csv,output_name)


run_b = tk.Button(input_frame, text='Run', width=7, command=single_run)
run_b.grid(row=3, column=6,pady=(0, 30))

multiple_run_b = tk.Button(
    input_frame, text='Multiple Run', width=13, command=multiple_run)
multiple_run_b.grid(row=3, column=10, pady=(0, 30),padx=20)

main_menu.mainloop()
