import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
import numpy as np
from multilayerAnalysis import MultilayerAnalysis

ws = tk.Tk()
ws.title('Multilayer Analysis')
ws.geometry('750x400')

tk.Label(ws, text=' ').grid(row=0, sticky=tk.W)
tk.Label(ws, text='High Index Layer                  : H').grid(row=1, sticky=tk.W, padx=8)
tk.Label(ws, text='Low Index Layer               : L').grid(row=2, sticky=tk.W, padx=8)
tk.Label(ws, text='Medium Index Layer           : M').grid(row=3, sticky=tk.W, padx=8)
tk.Label(ws, text='Different Material Layer    : D').grid(row=4, sticky=tk.W, padx=8)
tk.Label(ws, text='First Layer (Air)             : A').grid(row=5, sticky=tk.W, padx=8)
tk.Label(ws, text='Last Layer (Substrate)       : S').grid(row=6, sticky=tk.W, padx=8)
tk.Label(ws, text='Thin Metal Layer              : T').grid(row=7, sticky=tk.W, padx=8)

tk.Label(ws, text='Refractive Index').grid(row=0, column=1)
tk.Label(ws, text='Is Thickness Auto Calculated?').grid(row=0, column=3)
tk.Label(ws, text='Thickness').grid(row=0, column=2)

tk.Label(ws, text='Design Wavelength').grid(row=8, column=0, padx=8,pady=2, sticky=tk.W)
tk.Label(ws, text='Thickness Divider Coefficient').grid(row=9, column=0, padx=8,pady=2, sticky=tk.W)
tk.Label(ws, text='Wavelength Range').grid(row=10, column=0, padx=8,pady=2, sticky=tk.W)
tk.Label(ws, text='Step Size In 1nm Wavelength').grid(row=11, column=0, padx=8,pady=2, sticky=tk.W)
tk.Label(ws, text='Multilayer Sequence').grid(row=12, column=0, padx=8,pady=2, sticky=tk.W)

def IsThicknessAutoCalculatedEntriesChanged():
    for i in range(7):
        if(isThicknessAutoCalculatedVars[i].get()):
            thicknessEntries[i].config(state=DISABLED)
        else:
            thicknessEntries[i].config(state=NORMAL)

def Analyze():
    try:
        designWavelength = float(designWavelengthStr.get())
        thicknessDividerCoefficient = float(thicknessDividerCoefficientStr.get())
        refractiveIndexArr = []
        isThicknessAutoCalculatedArr= []
        thicknessArr = []
        for i in range(7):
            refractiveIndexArr.append(complex(refraciveIndexVars[i].get()))
            isThicknessAutoCalculatedArr.append(isThicknessAutoCalculatedVars[i].get())
            thicknessArr.append(float(thicknessVars[i].get()))
        multilayerSequence = multilayerSequenceStr.get()
        stepSize = float(stepSizeStr.get())
        wavelengthRange = np.arange(float(wavelengthRangeLowStr.get()),float(wavelengthRangeHighStr.get()),stepSize)
        MultilayerAnalysis(designWaveLength=designWavelength,
                thicknessDividerCoefficient=thicknessDividerCoefficient,
                refractiveIndexArr=refractiveIndexArr,
                isThicknessAutoCalculatedArr=isThicknessAutoCalculatedArr,
                thicknessArr=thicknessArr).PlotTheResults(multilayerSequence, wavelengthRange)
    except Exception as e:
        print(e)

designWavelengthStr = tk.StringVar()
designWavelengthEntry = tk.Entry(ws, width=30, justify='center',textvariable=designWavelengthStr)
designWavelengthEntry.grid(column=1, row=8, sticky=tk.W)

thicknessDividerCoefficientStr = tk.StringVar()
thicknessDividerCoefficientEntry = tk.Entry(ws, width=30, justify='center',textvariable=thicknessDividerCoefficientStr)
thicknessDividerCoefficientEntry.grid(column=1, row=9, sticky=tk.W)

wavelengthRangeLowStr = tk.StringVar()
wavelengthRangeLowEntry = tk.Entry(ws, width=30, justify='center',textvariable=wavelengthRangeLowStr)
wavelengthRangeLowEntry.grid(column=1, row=10, sticky=tk.W)
wavelengthRangeLowEntry.insert(0, "Low")

wavelengthRangeHighStr = tk.StringVar()
wavelengthRangeHighEntry = tk.Entry(ws, width=30, justify='center',textvariable=wavelengthRangeHighStr)
wavelengthRangeHighEntry.grid(column=2, row=10, sticky=tk.W)
wavelengthRangeHighEntry.insert(0, "High")

stepSizeStr = tk.StringVar()
stepSizeEntry = tk.Entry(ws, width=30, justify='center',textvariable=stepSizeStr)
stepSizeEntry.grid(column=1, row=11, sticky=tk.W)

multilayerSequenceStr = tk.StringVar()
multilayerSequenceEntry = tk.Entry(ws, width=91, justify='center',textvariable=multilayerSequenceStr)
multilayerSequenceEntry.grid(column=1, row=12, sticky=tk.W,columnspan=3)

refraciveIndexEntries = []
refraciveIndexVars = [tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]
isThicknessAutoCalculatedEntries = []
isThicknessAutoCalculatedVars = [tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar()]
thicknessEntries = []
thicknessVars = [tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]

for i in range(7):
    refraciveIndexEntries.append(tk.Entry(ws, width=30, justify='center',textvariable=refraciveIndexVars[i]))
    refraciveIndexEntries[i].grid(column=1, row=1+i, sticky=tk.W)

    isThicknessAutoCalculatedEntries.append(tk.Checkbutton(ws, width=30, justify='center',variable=isThicknessAutoCalculatedVars[i],command=IsThicknessAutoCalculatedEntriesChanged))
    isThicknessAutoCalculatedEntries[i].grid(column=3, row=1+i, sticky=tk.W)
    isThicknessAutoCalculatedEntries[i].select()

    thicknessEntries.append(tk.Entry(ws, width=30, justify='center',textvariable=thicknessVars[i]))
    thicknessEntries[i].grid(column=2, row=1+i, sticky=tk.W)
    thicknessEntries[i].config(state=DISABLED)

analyzeButton = tk.Button(ws,width=15,text="Analyze",command=Analyze)
analyzeButton.grid(column=1,row=13,pady=5,columnspan=2)


ws.mainloop()
