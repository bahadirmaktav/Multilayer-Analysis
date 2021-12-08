from numpy import ones,identity,array,arange,linalg,zeros
from math import pi
from math import exp
from math import sin
from math import cos

class Layer:
    def __init__(self, designWaveLength, thicknessDividerCoefficient, wavelength, refractiveIndex, thickness, matrixType=1):
        self.designWaveLength = designWaveLength
        self.thicknessDividerCoefficient = thicknessDividerCoefficient
        self.refractiveIndex = refractiveIndex
        self.wavelength = wavelength
        self.thickness = thickness
        self.matrixType = matrixType

    def LayerMatrixReturnCal(self):
        matrixType = self.matrixType
        if(matrixType == 1):
            return self.LayerMatrixCal(self.DynamicalMatrixCal(self.refractiveIndex), self.InverseDynamicalMatrixCal(self.DynamicalMatrixCal(self.refractiveIndex)), self.TranslationalMatrixCal(self.thickness, self.wavelength, self.refractiveIndex))
        elif(matrixType == 2):
            return self.DynamicalMatrixCal(self.refractiveIndex)
        else:
            return self.InverseDynamicalMatrixCal(self.DynamicalMatrixCal(self.refractiveIndex))

    # ------------------------------------------ Matrix Calculation Functions ------------------------------------------
    def LayerMatrixCal(self, dynamicalMatrix, inverseDynamicalMatrix, translationalMatrix):
        return dynamicalMatrix.dot(translationalMatrix).dot(inverseDynamicalMatrix)

    def DynamicalMatrixCal(self, refractiveIndex):
        dynamicalMatrix = ones((2, 2), dtype=complex)
        dynamicalMatrix[1][0] = refractiveIndex
        dynamicalMatrix[1][1] = -refractiveIndex
        return dynamicalMatrix

    def InverseDynamicalMatrixCal(self, dynamicalMatrix):
        return linalg.inv(dynamicalMatrix)

    def TranslationalMatrixCal(self, thickness, wavelength, refractiveIndex):
        translationalMatrix = zeros((2, 2), dtype=complex)
        phase = 2.0*pi*thickness*refractiveIndex/wavelength
        translationalMatrix[0][0] = complex(cos(phase.real)*exp(-1*phase.imag), sin(phase.real)*exp(-1*phase.imag))
        translationalMatrix[1][1] = complex(cos(phase.real)*exp(phase.imag), -1.0 * sin(phase.real)*exp(phase.imag))
        return translationalMatrix
    # -------------------------------------------------------------------------------------------------------------------
