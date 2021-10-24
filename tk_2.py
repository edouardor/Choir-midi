import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from music21 import *



class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Select midi file, part and measures')    
        self.root.geometry("600x350+450+200")
        self.filename = tk.StringVar()
        self.part_list = []

        #declare control variables

        self.selected_part = tk.IntVar(value = 0)
        self.repeat = tk.BooleanVar()
        self.first_measure = tk.IntVar(value = 1)
        self.last_measure = tk.IntVar(value = 10)
        self.text_file = tk.StringVar()
        self.info_key = tk.StringVar()
        
        #declare window widgets

        self.btt1 = ttk.Button(self.root, text="Select Midi File", command=self.file_select)
        self.lbl1 = tk.Label(self.root, text="File selected:")
        self.lbl2 = tk.Label(self.root, textvariable = self.text_file)
        self.lbl3 = tk.Label(self.root, textvariable = self.info_key)
        self.separ1 = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.lbl4 = tk.Label(self.root,text='Select the part you want to sing: ' )
        self.combo = ttk.Combobox(self.root, values = self.part_list, state="readonly", textvariable = self.selected_part)
        self.chkbtt = tk.Checkbutton(self.root, text = 'Repeat', width = 15, variable = self.repeat)
        self.lbl5 = tk.Label(self.root, text='Select the measures you want to sing: ')
        self.lbl6 = tk.Label(self.root, text= 'First measure')
        self.lbl7 = tk.Label(self.root, text= 'Last measure')
        self.entry1 = tk.Entry(self.root, textvariable=self.first_measure, width = 3)
        self.entry2 = tk.Entry(self.root, textvariable = self.last_measure, width = 3)
        self.lbl8 = tk.Label(self.root, text = '')
        self.btt2 = ttk.Button(self.root, text="Play", command=self.play)
        self.combo.bind("<<ComboboxSelected>>", self.part_select)

        
        self.btt1.pack()
        self.lbl1.pack()
        self.lbl2.pack()
        self.lbl3.pack()
        self.separ1.pack(fill='x')
        self.lbl4.pack()
        self.combo.pack()
        self.chkbtt.pack(padx = 5, pady = 5)
        self.lbl5.pack()
        self.lbl6.pack(side = tk.LEFT, padx = 20, expand = True)
        self.entry1.pack(side = tk.LEFT, padx = 20, expand = True)
        self.lbl7.pack(side = tk.LEFT, padx = 20, expand = True)        
        self.entry2.pack(side = tk.LEFT, padx = 20, expand = True)
        self.lbl8.pack()
        self.btt2.pack(side = tk.BOTTOM, fill = tk.BOTH)

        self.root.mainloop()

    def file_select(self):
        self.filename = askopenfilename(initialdir = '/Users/eduardoratier/Downloads',
        title ='Select a midi file',filetypes = [('midi files','*.mid')])
        short_name_file = self.filename[self.filename.rfind('/')+1:]
        short_name_file = short_name_file[:short_name_file.find('.')]
        self.text_file.set(short_name_file)

        self.score = converter.parse(self.filename)
        self.combo['values'] = [part.partName for part in self.score.parts] 

        self.key = self.score.analyze('key')
        info = 'song guessed signature: ' + self.key.tonic.name + " " + self.key.mode
        self.info_key.set(info)

        self.score_with_measures = self.score.makeMeasures()
        self.last_measure.set(self.score_with_measures[-1].number)


    def part_select(self, event):
        w = event.widget
        self.selected_part.set(w.current())

    def play(self):
        print(f'filename: {self.filename}')
        print(f'selected part: {self.selected_part.get()}')
        print(f'repeat: {self.repeat.get()}')
        print(f'first measure: {self.first_measure.get()}')
        print(f'last measure: {self.last_measure.get()}')
        self.root.destroy()    
                 
def main():
    my_app = App()
    return 0

if __name__ == '__main__':
    main()




