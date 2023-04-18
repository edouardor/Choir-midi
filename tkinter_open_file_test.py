import tkinter as tk
from tkinter import filedialog 
 
file_name = filedialog.askopenfilenames(initialdir="/", initialfile="ejemplo.txt",title="Select file",
                    filetypes=(("txt files", "*.txt"),("all files", "*.*")))
print(file_name)