import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.index_tricks import IndexExpression
from layerAnalysisv2 import Layer

# Layer Types
# 0 -> H -> High Index Layer Translational Matrix
# 1 -> L -> Low Index Layer Translational Matrix
# 2 -> M -> Medium Index Layer Translational Matrix
# 3 -> D -> Different Material Layer Translational Matrix
# 4 -> A -> Air Layer Inverse Dynamical Matrix
# 5 -> S -> Substrate Layer Dynamical Matrix
# 6 -> T -> Thin Metal Layer Translational Matrix


class MultilayerAnalysis:
    def __init__(self, designWaveLength, thicknessDividerCoefficient, refractiveIndexArr, isThicknessAutoCalculatedArr, thicknessArr, wavelength=1):
        self.designWaveLength = designWaveLength
        self.thicknessDividerCoefficient = thicknessDividerCoefficient
        self.wavelength = wavelength
        self.refractiveIndexArr = refractiveIndexArr
        self.isThicknessAutoCalculatedArr = isThicknessAutoCalculatedArr
        self.thicknessArr = thicknessArr
        self.matrixTypeArr = np.array([1, 1, 1, 1, 3, 2, 1])
        self.layerTypes = []
        self.layerMatrixTypes = []
        self.firstLayerRefractiveIndex = 0
        self.lastLayerRefractiveIndex = 0
        for k in range(7):
            self.layerTypes.append(Layer(designWaveLength=designWaveLength,
                                         thicknessDividerCoefficient=thicknessDividerCoefficient,
                                         wavelength=wavelength,
                                         refractiveIndex=refractiveIndexArr[k],
                                         matrixType=self.matrixTypeArr[k],
                                         thickness=(designWaveLength / (thicknessDividerCoefficient * refractiveIndexArr[k])) if isThicknessAutoCalculatedArr[k] else thicknessArr[k]))
            self.layerMatrixTypes.append(self.layerTypes[k].LayerMatrixReturnCal())

    #TODO Parentheses inside parentheses mechanism can be add with recursive.
    def TotalSystemMatrixCal(self, multilayerSequence):
        totalSystemMatrix = self.CharToLayerMatrix(multilayerSequence[0])
        self.firstLayerRefractiveIndex = self.CharToLayer(
            multilayerSequence[0]).refractiveIndex
        index = 1
        while index < len(multilayerSequence):
            if(multilayerSequence[index] == '('):
                index += 1
                betweenBracketsMatrixHolder = self.CharToLayerMatrix(
                    multilayerSequence[index])
                index += 1
                while multilayerSequence[index] != ')':
                    betweenBracketsMatrixHolder = betweenBracketsMatrixHolder.dot(
                        self.CharToLayerMatrix(multilayerSequence[index]))
                    index += 1
                index += 1
                powerVal = 1
                if(multilayerSequence[index] == '^'):
                    index += 1
                    if(multilayerSequence[index] == '('):
                        index += 1
                        powerString = multilayerSequence[index]
                        index += 1
                        while multilayerSequence[index] != ')':
                            powerString += multilayerSequence[index]
                            index += 1
                        powerVal = int(powerString)
                        index += 1
                bracketsMatrixPowered = betweenBracketsMatrixHolder
                for i in range(0, powerVal-1):
                    bracketsMatrixPowered = bracketsMatrixPowered.dot(
                        betweenBracketsMatrixHolder)
                totalSystemMatrix = totalSystemMatrix.dot(
                    bracketsMatrixPowered)
            else:
                totalSystemMatrix = totalSystemMatrix.dot(
                    self.CharToLayerMatrix(multilayerSequence[index]))
                index += 1
        self.lastLayerRefractiveIndex = self.CharToLayer(
            multilayerSequence[index - 1]).refractiveIndex
        return totalSystemMatrix

    def CharToLayerMatrix(self, char):
        if(char == 'H'):
            return self.layerMatrixTypes[0]
        elif(char == 'L'):
            return self.layerMatrixTypes[1]
        elif(char == 'M'):
            return self.layerMatrixTypes[2]
        elif(char == 'D'):
            return self.layerMatrixTypes[3]
        elif(char == 'A'):
            return self.layerMatrixTypes[4]
        elif(char == 'S'):
            return self.layerMatrixTypes[5]
        elif(char == 'T'):
            return self.layerMatrixTypes[6]
        else:
            return np.ones((2, 2), dtype=complex)

    def CharToLayer(self, char):
        if(char == 'H'):
            return self.layerTypes[0]
        elif(char == 'L'):
            return self.layerTypes[1]
        elif(char == 'M'):
            return self.layerTypes[2]
        elif(char == 'D'):
            return self.layerTypes[3]
        elif(char == 'A'):
            return self.layerTypes[4]
        elif(char == 'S'):
            return self.layerTypes[5]
        elif(char == 'T'):
            return self.layerTypes[6]
        else:
            return np.ones((2, 2), dtype=complex)

    # ------------------ Results Functions ------------------

    def ReflectanceCal(self, totalSystemMatrix):
        return (abs(totalSystemMatrix[1][0]) / abs(totalSystemMatrix[0][0]))**2

    def TransmittanceCal(self, totalSystemMatrix):
        subRefractiveIndex = self.lastLayerRefractiveIndex
        airRefractiveIndex = self.firstLayerRefractiveIndex
        return (subRefractiveIndex / airRefractiveIndex) * ((1 / abs(totalSystemMatrix[0][0]))**2)

    def AbsorptanceCal(self, totalSystemMatrix):
        reflectance = self.ReflectanceCal(totalSystemMatrix)
        transmittance = self.TransmittanceCal(totalSystemMatrix)
        return (1.0 - reflectance - transmittance)
    # -------------------------------------------------------

    def PlotTheResults(self, multilayerSequence, wavelengthRange):
        absorptance = []
        reflectance = []
        transmittance = []
        for wavelengthCounter in wavelengthRange:
            instance = MultilayerAnalysis(designWaveLength=self.designWaveLength,
                                          thicknessDividerCoefficient=self.thicknessDividerCoefficient,
                                          wavelength=wavelengthCounter,
                                          refractiveIndexArr=self.refractiveIndexArr,
                                          isThicknessAutoCalculatedArr=self.isThicknessAutoCalculatedArr,
                                          thicknessArr=self.thicknessArr)
            totalSystemMatrix = instance.TotalSystemMatrixCal(multilayerSequence)
            reflectance.append(instance.ReflectanceCal(totalSystemMatrix))
            transmittance.append(instance.TransmittanceCal(totalSystemMatrix))
            absorptance.append(instance.AbsorptanceCal(totalSystemMatrix))
        fig, axs = plt.subplots(3, figsize=(18, 14))
        axs[0].plot(wavelengthRange, reflectance, 'tab:blue')
        axs[1].plot(wavelengthRange, transmittance, 'tab:green')
        axs[2].plot(wavelengthRange, absorptance, 'tab:orange')
        axs[0].title.set_text('Reflectance - Wavelength')
        axs[1].title.set_text('Transmittance - Wavelength')
        axs[2].title.set_text('Absorptance - Wavelength')
        axs[0].grid(True)
        axs[1].grid(True)
        axs[2].grid(True)
        fig.show()
