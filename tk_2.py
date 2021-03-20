import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from music21 import *

def onselect(evt):
    #global selected_part
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    #index = int(w.curselection()[0])
    value = w.get()
    print(f'You selected item {value} with index: {w.current()}')
    index = w.current()
    selected_part.set(value)
    

root = tk.Tk()
root.title('Select midi file, part and measures')
root.geometry("400x350+10+10")
#root.withdraw()
root.update()
lbl = tk.Label(root, text='Please select a Midi file')
lbl.pack()
filename = askopenfilename(initialdir = '/Users/eduardoratier/Downloads',title ='Select a midi file',filetypes = [('midi files','*.mid')]) # show an "Open" dialog box and return the path to the selected file
print(filename)
short_name_file = filename[filename.rfind('/')+1:]
short_name_file = short_name_file[:short_name_file.find('.')]
root.update()
#root.destroy()
lbl.destroy()
tk.Label(root, text='filename: ' + short_name_file).pack()


my_midi_file = filename
score = converter.parse(my_midi_file)

key = score.analyze('key')
tk.Label(root, text='song guessed signature: ' + key.tonic.name + " " + key.mode).pack()
tk.Label(root, text = '').pack()
tk.Label(root, text='Select the part you want to sing: ').pack()
part_list = [part.partName for part in score.parts]
selected_part=tk.StringVar()
comboExample = ttk.Combobox(root, values = part_list, state="readonly", textvariable = selected_part)
comboExample.current(0)
 

comboExample.bind("<<ComboboxSelected>>", onselect)
comboExample.pack()
print(selected_part.get())


Repeat1 = tk.IntVar()

ChkBttn = tk.Checkbutton(root, text = 'Repeat', width = 15, variable = Repeat1)
ChkBttn.pack(padx = 5, pady = 5)

tk.Label(root, text='Select the measures you want to sing: ').pack()
var = tk.StringVar()
var_entry = tk.Entry(root, textvariable=var)
var_entry.pack()
tk.Label(root, text='Example: 1,12 or nothing if whole song').pack()

tk.Button(root, text = 'Start', command = lambda : root.destroy()).pack()
root.mainloop()



