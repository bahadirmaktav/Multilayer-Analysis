import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
import numpy as np
from multilayerAnalysis import MultilayerAnalysis

# Layer Types
# 0 -> H -> High Index Layer Translational Matrix
# 1 -> L -> Low Index Layer Translational Matrix
# 2 -> M -> Medium Index Layer Translational Matrix
# 3 -> D -> Different Material 1 Layer Translational Matrix
# 4 -> T -> Different Material 2 Translational Matrix
# 5 -> V -> Different Material 2 Translational Matrix
# 6 -> A -> First Layer (Air) Inverse Dynamical Matrix
# 7 -> S -> Last Layer (Substrate) Dynamical Matrix

def IsThicknessAutoCalculatedEntriesChanged():
    for i in range(8):
        if(isThicknessAutoCalculatedVars[i].get()):
            thicknessEntries[i].config(state=DISABLED)
        else:
            thicknessEntries[i].config(state=NORMAL)

def Analyze():
    try:
        CalculateThicknessAuto()
        designWavelength = float(designWavelengthStr.get())
        thicknessDividerCoefficient = float(thicknessDividerCoefficientStr.get())
        refractiveIndexArr = []
        isThicknessAutoCalculatedArr= []
        thicknessArr = []
        for i in range(8):
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
                thicknessArr=thicknessArr, multilayerSequence=multilayerSequence).PlotTheResults(wavelengthRange)
    except Exception as e:
        print(e)

def InitializeValues():
    designWavelengthEntry.insert(0,"600")
    thicknessDividerCoefficientEntry.insert(0,"4")
    wavelengthRangeLowEntry.insert(0,"400")
    wavelengthRangeHighEntry.insert(0,"800")
    stepSizeEntry.insert(0,"0.1")
    refraciveIndexEntries[0].insert(0,"4.234")
    refraciveIndexEntries[1].insert(0,"1.14")
    refraciveIndexEntries[2].insert(0,"1.45")
    refraciveIndexEntries[3].insert(0,"1.45")
    refraciveIndexEntries[4].insert(0,"3.073-3.383j")
    refraciveIndexEntries[5].insert(0,"3.073-3.383j")
    refraciveIndexEntries[6].insert(0,"1.000273")
    refraciveIndexEntries[7].insert(0,"1.52")
    thicknessEntries[3].insert(0,"241.38")
    thicknessEntries[4].insert(0,"5")
    thicknessEntries[5].insert(0,"5")
    for i in range(8):
        if(i != 3 and i != 4 and i != 5):
            isThicknessAutoCalculatedEntries[i].select()
            thicknessEntries[i].config(state=DISABLED)
    CalculateThicknessAuto()

def CalculateThicknessAuto():
    thicknessDividerCoefficient = float(thicknessDividerCoefficientStr.get())
    designWavelength = float(designWavelengthStr.get())
    for i in range(8):
        if(isThicknessAutoCalculatedVars[i].get()):
            refractiveIndex = complex(refraciveIndexVars[i].get())
            thicknessEntries[i].config(state=NORMAL)
            thicknessEntries[i].delete(0,'end')
            thicknessEntries[i].insert(0,str(designWavelength/(thicknessDividerCoefficient*refractiveIndex).real))
            thicknessEntries[i].config(state=DISABLED)

ws = tk.Tk()
ws.title('Multilayer Analysis')
ws.geometry('750x400')
ws.iconbitmap("C:/Users/Bahadir/Desktop/BahadırUni/ELE401GraduationProject_I/Codes/MultilayerAnalysis_GraduationProject/MultilayerAnalysisCode_CurrentVersion/multilayerAnalysisIcon2.ico")


tk.Label(ws, text=' ').grid(row=0, sticky=tk.W)
tk.Label(ws, text='High Index Layer                  : H').grid(row=1, sticky=tk.W, padx=8)
tk.Label(ws, text='Low Index Layer                   : L').grid(row=2, sticky=tk.W, padx=8)
tk.Label(ws, text='Medium Index Layer           : M').grid(row=3, sticky=tk.W, padx=8)
tk.Label(ws, text='Different Material 1 Layer   : D').grid(row=4, sticky=tk.W, padx=8)
tk.Label(ws, text='Different Material 2 Layer   : T').grid(row=5, sticky=tk.W, padx=8)
tk.Label(ws, text='Different Material 3 Layer   : V').grid(row=6, sticky=tk.W, padx=8)
tk.Label(ws, text='First Layer                             : A').grid(row=7, sticky=tk.W, padx=8)
tk.Label(ws, text='Last Layer                             : S').grid(row=8, sticky=tk.W, padx=8)

tk.Label(ws, text='Refractive Index').grid(row=0, column=1)
tk.Label(ws, text='Is Thickness Auto Calculated?').grid(row=0, column=3)
tk.Label(ws, text='Thickness (nm)').grid(row=0, column=2)

tk.Label(ws, text='Design Wavelength (nm)').grid(row=9, column=0, padx=8,pady=2, sticky=tk.W)
tk.Label(ws, text='Thickness Divider Coefficient').grid(row=10, column=0, padx=8,pady=2, sticky=tk.W)
tk.Label(ws, text='Wavelength Range (nm)').grid(row=11, column=0, padx=8,pady=2, sticky=tk.W)
tk.Label(ws, text='Step Size In 1nm Wavelength').grid(row=12, column=0, padx=8,pady=2, sticky=tk.W)
tk.Label(ws, text='Multilayer Sequence').grid(row=13, column=0, padx=8,pady=2, sticky=tk.W)

designWavelengthStr = tk.StringVar()
designWavelengthEntry = tk.Entry(ws, width=30, justify='center',textvariable=designWavelengthStr)
designWavelengthEntry.grid(column=1, row=9, sticky=tk.W)

thicknessDividerCoefficientStr = tk.StringVar()
thicknessDividerCoefficientEntry = tk.Entry(ws, width=30, justify='center',textvariable=thicknessDividerCoefficientStr)
thicknessDividerCoefficientEntry.grid(column=1, row=10, sticky=tk.W)

wavelengthRangeLowStr = tk.StringVar()
wavelengthRangeLowEntry = tk.Entry(ws, width=30, justify='center',textvariable=wavelengthRangeLowStr)
wavelengthRangeLowEntry.grid(column=1, row=11, sticky=tk.W)

wavelengthRangeHighStr = tk.StringVar()
wavelengthRangeHighEntry = tk.Entry(ws, width=30, justify='center',textvariable=wavelengthRangeHighStr)
wavelengthRangeHighEntry.grid(column=2, row=11, sticky=tk.W)

stepSizeStr = tk.StringVar()
stepSizeEntry = tk.Entry(ws, width=30, justify='center',textvariable=stepSizeStr)
stepSizeEntry.grid(column=1, row=12, sticky=tk.W)

multilayerSequenceStr = tk.StringVar()
multilayerSequenceEntry = tk.Entry(ws, width=91, justify='center',textvariable=multilayerSequenceStr)
multilayerSequenceEntry.grid(column=1, row=13, sticky=tk.W,columnspan=3)

refraciveIndexEntries = []
refraciveIndexVars = [tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]
isThicknessAutoCalculatedEntries = []
isThicknessAutoCalculatedVars = [tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar()]
thicknessEntries = []
thicknessVars = [tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]

analyzeButton = tk.Button(ws,width=15,text="Analyze",command=Analyze)
analyzeButton.grid(column=1,row=14,pady=5,columnspan=2)

for i in range(8):
    refraciveIndexEntries.append(tk.Entry(ws, width=30, justify='center',textvariable=refraciveIndexVars[i]))
    refraciveIndexEntries[i].grid(column=1, row=1+i, sticky=tk.W)

    isThicknessAutoCalculatedEntries.append(tk.Checkbutton(ws, width=30, justify='center',variable=isThicknessAutoCalculatedVars[i],command=IsThicknessAutoCalculatedEntriesChanged))
    isThicknessAutoCalculatedEntries[i].grid(column=3, row=1+i, sticky=tk.W)

    thicknessEntries.append(tk.Entry(ws, width=30, justify='center',textvariable=thicknessVars[i]))
    thicknessEntries[i].grid(column=2, row=1+i, sticky=tk.W)

InitializeValues()

ws.mainloop()
