import tkinter as tk

ws = tk.Tk()
#frame = tk.Frame(ws)
#frame.pack()
ws.title('Multilayer Analysis')
ws.geometry('700x400')
tk.Label(ws, text=' ').grid(row=0, sticky=tk.W)
tk.Label(ws, text='High Index Layer').grid(row=1, sticky=tk.W, padx=8)
tk.Label(ws, text='Low Index Layer').grid(row=2, sticky=tk.W, padx=8)
tk.Label(ws, text='Medium Index Layer').grid(row=3, sticky=tk.W, padx=8)
tk.Label(ws, text='Different Material Layer').grid(row=4, sticky=tk.W, padx=8)
tk.Label(ws, text='Air Layer').grid(row=5, sticky=tk.W, padx=8)
tk.Label(ws, text='Substrate Layer').grid(row=6, sticky=tk.W, padx=8)
tk.Label(ws, text='Thin Metal Layer').grid(row=7, sticky=tk.W, padx=8)

tk.Label(ws, text='Refractive Index').grid(row=0, column=1, padx=5)
tk.Label(ws, text='Is Thickness Predefined?').grid(row=0, column=2, padx=5)
tk.Label(ws, text='Thickness').grid(row=0, column=3, padx=5)

tk.Label(ws, text='Design Wavelength').grid(row=8, column=0, padx=8, sticky=tk.W)
tk.Label(ws, text='Thickness Divider Coefficient').grid(row=9, column=0, padx=8, sticky=tk.W)
tk.Label(ws, text='Wavelength Range').grid(row=10, column=0, padx=8, sticky=tk.W)
tk.Label(ws, text='Multilayer Sequence').grid(row=11, column=0, padx=8, sticky=tk.W)

designWavelengthEntry = tk.Entry(ws, width=25, justify='center').grid(column=1, row=8, sticky=tk.W)
thicknessDividerCoefficientEntry = tk.Entry(ws, width=25, justify='center').grid(column=1, row=9, sticky=tk.W)
wavelengthRangeLowEntry = tk.Entry(ws, width=25, justify='center')
wavelengthRangeLowEntry.grid(column=1, row=10, sticky=tk.W)
wavelengthRangeLowEntry.insert(0, 'Low')
wavelengthRangeHighEntry = tk.Entry(ws, width=25, justify='center')
wavelengthRangeHighEntry.grid(column=2, row=10, sticky=tk.W)
wavelengthRangeHighEntry.insert(0, 'High')
multilayerSequenceEntry = tk.Entry(ws, width=76, justify='center').grid(column=1, row=11, sticky=tk.W,columnspan=3)
refraciveIndexEntries = []
isThicknessPredefinedEntries = []
thicknessEntries = []
for i in range(7):
    refraciveIndexEntries.append(
        tk.Entry(ws, width=25, justify='center').grid(column=1, row=1+i, sticky=tk.W))
    isThicknessPredefinedEntries.append(
        tk.Entry(ws, width=25, justify='center').grid(column=2, row=1+i, sticky=tk.W))
    thicknessEntries.append(
        tk.Entry(ws, width=25, justify='center').grid(column=3, row=1+i, sticky=tk.W))


ws.mainloop()
