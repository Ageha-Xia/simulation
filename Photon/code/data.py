import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def compton_and_photoelectric():
    # Load the data
    file_path = 'Energy.xlsx'  # Replace with your file path
    data = pd.read_excel(file_path)

    # Remove duplicate energy values, keeping the first occurrence
    data_unique = data.drop_duplicates(subset=['能量/MeV'])

    # Extracting the columns for interpolation
    x = data_unique['能量/MeV']
    y_compton = data_unique['康普顿效应截面/cm^-1']
    y_photoelectric = data_unique['光电效应截面/cm^-1']

    # Creating cubic spline interpolation functions
    cubic_spline_compton = CubicSpline(x, y_compton)
    cubic_spline_photoelectric = CubicSpline(x, y_photoelectric)
    
    return cubic_spline_compton, cubic_spline_photoelectric

if __name__ == '__main__':
    # Load the data
    file_path = 'Energy.xlsx'  # Replace with your file path
    data = pd.read_excel(file_path)

    # Remove duplicate energy values, keeping the first occurrence
    data_unique = data.drop_duplicates(subset=['能量/MeV'])

    # Extracting the columns for interpolation
    x = data_unique['能量/MeV']
    y_compton = data_unique['康普顿效应截面/cm^-1']
    y_photoelectric = data_unique['光电效应截面/cm^-1']

    # Creating cubic spline interpolation functions
    cubic_spline_compton = CubicSpline(x, y_compton)
    cubic_spline_photoelectric = CubicSpline(x, y_photoelectric)
    
    # Generating a range of energy values for plotting the interpolation
    x_interp = np.linspace(min(x), max(x), 500)

    # Using the interpolation functions to predict values
    y_compton_interp = cubic_spline_compton(x_interp)
    y_photoelectric_interp = cubic_spline_photoelectric(x_interp)

    # Plotting the data and the interpolation functions
    plt.figure(figsize=(12, 6))

    # Plotting Compton Effect Cross-Section
    plt.subplot(1, 2, 1)
    plt.scatter(x, y_compton, color='blue', label='Original Data')
    plt.plot(x_interp, y_compton_interp, color='red', label='Interpolated Curve')
    plt.title('Compton Effect Cross-Section Interpolation')
    plt.xlabel('Energy/MeV')
    plt.ylabel('Compton Cross-Section/cm^-1')
    plt.legend()

    # Plotting Photoelectric Effect Cross-Section
    plt.subplot(1, 2, 2)
    plt.scatter(x, y_photoelectric, color='blue', label='Original Data')
    plt.plot(x_interp, y_photoelectric_interp, color='red', label='Interpolated Curve')
    plt.title('Photoelectric Effect Cross-Section Interpolation')
    plt.xlabel('Energy/MeV')
    plt.ylabel('Photoelectric Cross-Section/cm^-1')
    plt.legend()

    plt.tight_layout()
    plt.show()
