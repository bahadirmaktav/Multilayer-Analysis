import numpy as np
from numpy.lib.index_tricks import IndexExpression
from layerAnalysis import Layer

# H -> High Index Layer Translational Matrix
# L -> Low Index Layer Translational Matrix
# M -> Medium Index Layer Translational Matrix
# D -> Defect Layer Translational Matrix
# A -> Air Layer Inverse Dynamical Matrix
# S -> Substrate Layer Inverse Dynamical Matrix
# T -> Metal Thin Layer Inverse Dynamical Matrix


class MultilayerAnalysis:
    def __init__(self, designWaveLength, thicknessDividerCoefficient, wavelength):
        self.designWaveLength = designWaveLength
        self.thicknessDividerCoefficient = thicknessDividerCoefficient
        self.wavelength = wavelength
        self.H_layer = Layer(designWaveLength=designWaveLength,
                             thicknessDividerCoefficient=thicknessDividerCoefficient,
                             wavelength=wavelength,
                             refrectiveIndex=4.234,
                             isThicknessPredefined=False,
                             matrixType=1)
        self.L_layer = Layer(designWaveLength=designWaveLength,
                             thicknessDividerCoefficient=thicknessDividerCoefficient,
                             wavelength=wavelength,
                             refrectiveIndex=1.14,
                             isThicknessPredefined=False,
                             matrixType=1)
        self.M_layer = Layer(designWaveLength=designWaveLength,
                             thicknessDividerCoefficient=thicknessDividerCoefficient,
                             wavelength=wavelength,
                             refrectiveIndex=1.45,
                             isThicknessPredefined=False,
                             matrixType=1)
        self.D_layer = Layer(designWaveLength=designWaveLength,
                             thicknessDividerCoefficient=thicknessDividerCoefficient,
                             wavelength=wavelength,
                             refrectiveIndex=1.45,
                             isThicknessPredefined=True,
                             matrixType=1,
                             thickness=241.379)
        self.A_layer = Layer(designWaveLength=designWaveLength,
                             thicknessDividerCoefficient=thicknessDividerCoefficient,
                             wavelength=wavelength,
                             refrectiveIndex=1.000273,
                             isThicknessPredefined=False,
                             matrixType=3)
        self.S_layer = Layer(designWaveLength=designWaveLength,
                             thicknessDividerCoefficient=thicknessDividerCoefficient,
                             wavelength=wavelength,
                             refrectiveIndex=1.458,
                             isThicknessPredefined=False,
                             matrixType=2)
        self.T_layer = Layer(designWaveLength=designWaveLength,
                             thicknessDividerCoefficient=thicknessDividerCoefficient,
                             wavelength=wavelength,
                             refrectiveIndex=complex(3.073, -3.383),
                             isThicknessPredefined=True,
                             matrixType=1,
                             thickness=5)
        self.H = self.H_layer.LayerMatrixReturnCal()
        self.L = self.L_layer.LayerMatrixReturnCal()
        self.M = self.M_layer.LayerMatrixReturnCal()
        self.D = self.D_layer.LayerMatrixReturnCal()
        self.A = self.A_layer.LayerMatrixReturnCal()
        self.S = self.S_layer.LayerMatrixReturnCal()
        self.T = self.T_layer.LayerMatrixReturnCal()

    def TotalSystemMatrixCal(self, multilayerSequence):
        totalSystemMatrix = self.CharToLayerMatrix(multilayerSequence[0])
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
        return totalSystemMatrix

    def CharToLayerMatrix(self, char):
        if(char == 'H'):
            return self.H
        elif(char == 'L'):
            return self.L
        elif(char == 'M'):
            return self.M
        elif(char == 'D'):
            return self.D
        elif(char == 'A'):
            return self.A
        elif(char == 'S'):
            return self.S
        elif(char == 'T'):
            return self.T
        else:
            return np.ones((2, 2), dtype=complex)

    # ------------------ Results Functions ------------------

    def ReflectanceCal(self, totalSystemMatrix):
        return (abs(totalSystemMatrix[1][0]) / abs(totalSystemMatrix[0][0]))**2

    def TransmittanceCal(self, totalSystemMatrix):
        subRefractiveIndex = self.S_layer.refrectiveIndex
        airRefractiveIndex = self.A_layer.refrectiveIndex
        return (subRefractiveIndex / airRefractiveIndex) * ((1 / abs(totalSystemMatrix[0][0]))**2)

    def AbsorptanceCal(self, totalSystemMatrix):
        reflectance = self.ReflectanceCal(totalSystemMatrix)
        transmittance = self.TransmittanceCal(totalSystemMatrix)
        return (1.0 - reflectance - transmittance)
    # -------------------------------------------------------
