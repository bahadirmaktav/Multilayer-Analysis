import numpy as np
import math

class Layer:
    def __init__(self, designWaveLength, thicknessDividerCoefficient, wavelength, refrectiveIndex, isThicknessPredefined, matrixType=1, thickness=1):
        self.designWaveLength = designWaveLength
        self.thicknessDividerCoefficient = thicknessDividerCoefficient
        self.refrectiveIndex = refrectiveIndex
        self.wavelength = wavelength
        self.isThicknessPredefined = isThicknessPredefined
        self.thickness = thickness if isThicknessPredefined else (designWaveLength / (thicknessDividerCoefficient * refrectiveIndex))
        self.matrixType = matrixType

    def LayerMatrixReturnCal(self):
        matrixType = self.matrixType
        if(matrixType == 1):
            return self.LayerMatrixCal(self.DynamicalMatrixCal(self.refrectiveIndex), self.InverseDynamicalMatrixCal(self.DynamicalMatrixCal(self.refrectiveIndex)), self.TranslationalMatrixCal(self.thickness, self.wavelength, self.refrectiveIndex))
        elif(matrixType == 2):
            return self.DynamicalMatrixCal(self.refrectiveIndex)
        else:
            return self.InverseDynamicalMatrixCal(self.DynamicalMatrixCal(self.refrectiveIndex))

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
        phase = 2*math.pi*thickness*refractiveIndex/wavelength
        translationalMatrix[0][0] = complex(math.cos(phase.real)*math.exp(-1*phase.imag), math.sin(phase.real)*math.exp(-1*phase.imag))
        translationalMatrix[1][1] = complex(math.cos(phase.real)*math.exp(phase.imag), -1.0 * math.sin(phase.real)*math.exp(phase.imag))
        return translationalMatrix
    # -------------------------------------------------------------------------------------------------------------------
