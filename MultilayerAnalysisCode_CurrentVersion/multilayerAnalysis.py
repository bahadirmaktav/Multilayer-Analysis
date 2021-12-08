import numpy as np
import matplotlib.pyplot as plt
from layerAnalysis import Layer

# Layer Types
# 0 -> H -> High Index Layer Translational Matrix
# 1 -> L -> Low Index Layer Translational Matrix
# 2 -> M -> Medium Index Layer Translational Matrix
# 3 -> D -> Different Material 1 Layer Translational Matrix
# 4 -> T -> Different Material 2 Translational Matrix
# 5 -> V -> Different Material 2 Translational Matrix
# 6 -> A -> First Layer (Air) Inverse Dynamical Matrix
# 7 -> S -> Last Layer (Substrate) Dynamical Matrix


class MultilayerAnalysis:
    def __init__(self, designWaveLength, thicknessDividerCoefficient, refractiveIndexArr, isThicknessAutoCalculatedArr, thicknessArr, multilayerSequence, wavelength=1):
        self.designWaveLength = designWaveLength
        self.thicknessDividerCoefficient = thicknessDividerCoefficient
        self.wavelength = wavelength
        self.refractiveIndexArr = refractiveIndexArr
        self.isThicknessAutoCalculatedArr = isThicknessAutoCalculatedArr
        self.thicknessArr = thicknessArr
        self.matrixTypeArr = np.array([1,1,1,1,1,1,3,2])
        self.layerTypes = []
        self.layerMatrixTypes = []
        self.multilayerSequence = multilayerSequence,
        for k in range(8):
            if(self.IndexToChar(k) in multilayerSequence):
                self.layerTypes.append(Layer(designWaveLength=designWaveLength,
                                             thicknessDividerCoefficient=thicknessDividerCoefficient,
                                             wavelength=wavelength,
                                             refractiveIndex=refractiveIndexArr[k],
                                             matrixType=self.matrixTypeArr[k],
                                             thickness=(designWaveLength / (thicknessDividerCoefficient * refractiveIndexArr[k]).real) if isThicknessAutoCalculatedArr[k] else thicknessArr[k]))
                self.layerMatrixTypes.append(self.layerTypes[k].LayerMatrixReturnCal())
            else:
                self.layerTypes.append(Layer(1,1,1,1,1))
                self.layerMatrixTypes.append(np.ones((2,2),dtype=complex))
        self.firstLayerRefractiveIndex = self.CharToLayer(multilayerSequence[0]).refractiveIndex
        self.lastLayerRefractiveIndex = self.CharToLayer(multilayerSequence[len(multilayerSequence)-1]).refractiveIndex

    def TotalSystemMatrixCal(self, multilayerSequence):
        totalSystemMatrix = np.identity(2,dtype=complex)
        index = 0
        openParentheses = 0
        while index < len(multilayerSequence):
            if(multilayerSequence[index] == '['):
                openParentheses += 1
                index += 1
                newMultilayerSequence = ""
                while(openParentheses != 1 or multilayerSequence[index] != ']'):
                    if(multilayerSequence[index] == '['):
                        openParentheses += 1
                    elif(multilayerSequence[index] == ']'):
                        openParentheses -= 1
                    newMultilayerSequence += multilayerSequence[index]
                    index += 1
                betweenBracketsMatrixHolder = self.TotalSystemMatrixCal(newMultilayerSequence)
                openParentheses -= 1
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
                    bracketsMatrixPowered = bracketsMatrixPowered.dot(betweenBracketsMatrixHolder)
                totalSystemMatrix = totalSystemMatrix.dot(bracketsMatrixPowered)
            else:
                totalSystemMatrix = totalSystemMatrix.dot(self.CharToLayerMatrix(multilayerSequence[index]))
                index += 1
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
        elif(char == 'T'):
            return self.layerMatrixTypes[4]
        elif(char == 'V'):
            return self.layerMatrixTypes[5]
        elif(char == 'A'):
            return self.layerMatrixTypes[6]
        elif(char == 'S'):
            return self.layerMatrixTypes[7]
        else:
            return np.identity(2,dtype=complex)

    def CharToLayer(self, char):
        if(char == 'H'):
            return self.layerTypes[0]
        elif(char == 'L'):
            return self.layerTypes[1]
        elif(char == 'M'):
            return self.layerTypes[2]
        elif(char == 'D'):
            return self.layerTypes[3]
        elif(char == 'T'):
            return self.layerTypes[4]
        elif(char == 'V'):
            return self.layerTypes[5]
        elif(char == 'A'):
            return self.layerTypes[6]
        elif(char == 'S'):
            return self.layerTypes[7]
        else:
            return Layer(1,1,1,1,1)

    def IndexToChar(self, k):
        if(k == 0):
            return 'H'
        elif(k == 1):
            return 'L'
        elif(k == 2):
            return 'M'
        elif(k == 3):
            return 'D'
        elif(k == 4):
            return 'T'
        elif(k == 5):
            return 'V'
        elif(k == 6):
            return 'A'
        elif(k == 7):
            return 'S'
        else:
            return ' '
    # ------------------ Results Functions ------------------

    def ReflectanceCal(self, totalSystemMatrix):
        return (abs(totalSystemMatrix[1][0]) / abs(totalSystemMatrix[0][0]))**2

    def TransmittanceCal(self, totalSystemMatrix):
        lastLayerRefractiveIndex = self.lastLayerRefractiveIndex
        firstLayerRefractiveIndex = self.firstLayerRefractiveIndex
        return (lastLayerRefractiveIndex / firstLayerRefractiveIndex) * ((1 / abs(totalSystemMatrix[0][0]))**2)

    def AbsorptanceCal(self, totalSystemMatrix):
        reflectance = self.ReflectanceCal(totalSystemMatrix)
        transmittance = self.TransmittanceCal(totalSystemMatrix)
        return (1.0 - reflectance - transmittance)
    # -------------------------------------------------------

    def PlotTheResults(self, wavelengthRange):
        absorptance = []
        reflectance = []
        transmittance = []
        for wavelengthCounter in wavelengthRange:
            instance = MultilayerAnalysis(designWaveLength=self.designWaveLength,
                                          thicknessDividerCoefficient=self.thicknessDividerCoefficient,
                                          wavelength=wavelengthCounter,
                                          refractiveIndexArr=self.refractiveIndexArr,
                                          isThicknessAutoCalculatedArr=self.isThicknessAutoCalculatedArr,
                                          thicknessArr=self.thicknessArr,
                                          multilayerSequence=self.multilayerSequence[0])
            totalSystemMatrix = instance.TotalSystemMatrixCal(self.multilayerSequence[0])
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
