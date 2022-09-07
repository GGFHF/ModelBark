# ModelBark

ModelBark is a software application to simulate outer bark growth of woody plant species using a simple mathematical
model based on the idea of cellular automata (Wolfram, 1983). The application simulates the evolution of cellular
components of a secondary stem radius taking into consideration the position of the cells of each type (Xylem, Vascular
cambium, Phloem, Phellogen and Phellem) and the mechanical stimuli produce by secondary growth.

ModelBark facilitates testing hypothesis related to bark development mediated by mechanical stimuli in woody plant
species and is able to produce different bark types (Thick/Thin or Rhytidome-like barks) by using different parameter 
combinations. 

The details of the mathematical model and a example of use of ModelBark are available at:

Gutiérrez Climent, Á. A mathematical-computational model to study the formation of barks of different types in woody species.


Installation:

ModelBark was programmed in Python3, and runs in any computer with an OS that allows
for Python 3: Linux/Unix, Microsoft Windows, Mac OS X and other platforms. If Linux is the OS
of your computer, Python will be already installed. In other cases, it can be downloaded from
https://www.python.org/.

To install ModelBark on Linux and macOS, simply decompress the ModelBark-main.zip into a
directory, typing the following command in a terminal window:

$ unzip ModelBark-main.zip

Then, the execution permissions of the programs must be set by using this command:

$ chmod u+x *.py *.sh

For Microsoft Windows, simply unzip ModelBark-main.zip in the usual way.

To work properly the directory that hosts ModelBark1_0.py requires an additional empty directory called Figuras (Already available in
the compressed file).

For Windows, you can download both Python versions from the official website
(https://www.python.org/), or use one of the several distributions that include Python along
with other software packages for standard bioinformatic analysis. We recommend installing
Anaconda (a version corresponding to Python 3.8.8 or higher). Anaconda is a free cross-platform
for Microsoft Windows, Linux and macOS (https://www.continuum.io/). The installation
instructions for Anaconda are available on its web site.

To work properly, ModelBark needs the following Python packages:

Tkinter: https://docs.python.org/3.8/library/tk.html

PIL: https://pypi.org/project/Pillow/

Numpy: https://numpy.org/

Matplotlib: https://matplotlib.org/

Pandas: https://pandas.pydata.org/

Disclaimer:

The software package ModelBark is available for free download from the GitHub software repository
(https://github.com/GGFHF/ModelBark) under GNU General Public License v3.0.
