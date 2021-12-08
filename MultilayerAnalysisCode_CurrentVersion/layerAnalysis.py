import numpy as np
import math

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
        dynamicalMatrix = np.ones((2, 2), dtype=complex)
        dynamicalMatrix[1][0] = refractiveIndex
        dynamicalMatrix[1][1] = -refractiveIndex
        return dynamicalMatrix

    def InverseDynamicalMatrixCal(self, dynamicalMatrix):
        return np.linalg.inv(dynamicalMatrix)

    def TranslationalMatrixCal(self, thickness, wavelength, refractiveIndex):
        translationalMatrix = np.zeros((2, 2), dtype=complex)
        phase = 2.0*math.pi*thickness*refractiveIndex/wavelength
        translationalMatrix[0][0] = complex(math.cos(phase.real)*math.exp(-1*phase.imag), math.sin(phase.real)*math.exp(-1*phase.imag))
        translationalMatrix[1][1] = complex(math.cos(phase.real)*math.exp(phase.imag), -1.0 * math.sin(phase.real)*math.exp(phase.imag))
        return translationalMatrix
    # -------------------------------------------------------------------------------------------------------------------
