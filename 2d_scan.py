"""
Python3 script that generates a 2D grid of scan points and energies, then
creates a 2D contour plot of the PES

TODO: Scan range reading from input file

Written by AJS
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.interpolate import griddata
from scipy.interpolate import Rbf
from pandas import read_csv
import argparse


def get_args():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('filename',
                           help="Input csv name, including '.csv' suffix")
    my_parser.add_argument("-c", "--column",
                           action='store',
                           type=int,
                           help="Specify column of csv file to extract energies from")
    my_parser.add_argument("-p", "--plot",
                           action='store_true',
                           help='Do plt.show()')
    my_parser.add_argument("-s", "--save",
                           action='store_true',
                           help='Save plot to current working directory')
    my_parser.add_argument("-n", "--plotname",
                           action='store',
                           default='plot',
                           type=str,
                           help='Specify name of plot')
    my_parser.add_argument("-x", "--n_x_vals",
                           action='store',
                           default=10,
                           type=int,
                           help="Specify number of x values for interpolation")
    my_parser.add_argument("-y", "--n_y_vals",
                           action='store',
                           default=10,
                           type=int,
                           help="Specify number of y values for interpolation")
    my_parser.add_argument("-l", "--levels",
                           action='store',
                           default=10,
                           type=int,
                           help="Specify number of levels for contour plot")
    return my_parser.parse_args()


def get_scan_params():
    return None


def get_energies(filename, column):
    csv_file_path = str(os.getcwd() + '/' + filename)
    df = np.genfromtxt(csv_file_path, delimiter=',', skip_header=1, dtype=float)
    energies = df[:, [column]]
    return energies


def _energies_ha_to_kcal(energies):
    energy_min = np.min(energies)
    energies -= energy_min
    energies *= 627.509
    return energies


def _get_scan_length(scan_input):
    if scan_input[2] > 0:
        scan_length = int(((scan_input[1] - scan_input[0]) / scan_input[2]) + 1)
    else:
        scan_length = int(((scan_input[1] - scan_input[0]) / scan_input[2]) + 2)
    return scan_length


def _generate_2d_grid(x_input, y_input):
    x_scan_len = _get_scan_length(x_input)
    print("Number of x values to scan over: ", x_scan_len)

    y_scan_len = _get_scan_length(y_input)
    print("Number of y values to scan over: ", y_scan_len)

    arr = np.zeros((x_scan_len*y_scan_len, 2))

    k = 0  # counter
    for i in range(x_scan_len):
        for j in range(y_scan_len):
            arr[k, 0] = x_input[0] + i * x_input[2]
            arr[k, 1] = y_input[0] + j * y_input[2]
            k += 1

    return arr, x_scan_len, y_scan_len


def _clean_data(arr, energies):

    # Stack (x, y) coords with energies, and remove any nan rows
    z = np.array(energies)
    data = np.column_stack((arr, z))
    data = data[~np.isnan(data).any(axis=1)]

    # Extract the x, y, and z values from the array
    clean_x = data[:, 0]
    clean_y = data[:, 1]
    clean_z = _energies_ha_to_kcal(data[:, 2])

    return clean_x, clean_y, clean_z


def _set_interpolation_vals(n_x_vals, n_y_vals, x_scan_len, y_scan_len):

    # Set number of x and y values for interpolation
    if n_x_vals is None:
        n_x_vals = x_scan_len
    if n_y_vals is None:
        n_y_vals = y_scan_len

    print(f"Using n_x_vals = {n_x_vals} and n_y_vals = {n_y_vals} to interpolate data")

    return n_x_vals, n_y_vals


def _interpolate_data(x, y, z, n_x_vals, n_y_vals, interpolator="Rbf"):

    # Create a grid of x and y values
    X, Y = np.meshgrid(np.linspace(min(x), max(x), n_x_vals), np.linspace(min(y), max(y), n_y_vals))

    # Interpolate the z values onto the grid using numpy
    if interpolator == "numpy":
        Z = np.interp(X.flatten(), x, z).reshape(X.shape) + np.interp(Y.flatten(), y, z).reshape(Y.shape)

    # Interpolate the z values onto the grid using scipy griddata interpolation, deals with NaN values
    elif interpolator == "griddata":
        Z = griddata((x, y), z, (X, Y), method='linear')

    # Interpolate the z values onto the grid using scipy Rbf interpolation, deals with NaN values
    elif interpolator == "Rbf":
        rbf = Rbf(x, y, z, function='multiquadric')
        Z = rbf(X, Y)

    print(f"Using interpolator: {interpolator}")

    return X, Y, Z


def generate_contour(x_input, y_input, energies, n_x_vals=None, n_y_vals=None,
                     levels=10, interp="Rbf", x_label=None, y_label=None, z_label=None,
                     plt_title=None, plt_save=False, plt_show=True, plt_name="2D_plot.pdf"):

    # Generate 2D array of scan points
    arr, x_scan_len, y_scan_len = _generate_2d_grid(x_input, y_input)
    clean_x, clean_y, clean_z = _clean_data(arr, energies)
    n_x_vals, n_y_vals = _set_interpolation_vals(n_x_vals, n_y_vals, x_scan_len, y_scan_len)
    X, Y, Z = _interpolate_data(clean_x, clean_y, clean_z, n_x_vals, n_y_vals, interp)

    # Create the contour plot
    cmap = mpl.cm.bwr
    plt.contourf(X, Y, Z, levels=levels, cmap=cmap, alpha=0.9)
    print(f"Using {levels} levels in contourf")

    # Add labels and title
    print(f"Setting x axis label as {x_label}")
    plt.xlabel(x_label)
    print(f"Setting y axis label as {y_label}")
    plt.ylabel(y_label)
    print(f"Setting plot title as {plt_title}")
    plt.title(plt_title + f"\n n_x_vals = {n_x_vals}, n_y_vals = {n_y_vals}, levels = {levels}")

    # Add a colorbar
    print(f"Setting z axis (colorbar) label as {z_label}")
    plt.colorbar(extend='both', label=z_label)

    # Set tight layout for plot
    plt.tight_layout()

    # Save the plot
    if plt_save == True:
        cwd = os.getcwd()
        print(f"Saving plot as {cwd}/{plt_name}")
        plt.savefig(plt_name, format="pdf")

    # Show the plot
    if plt_show == True:
        plt.show()


if __name__ == '__main__':

    args = get_args()
    filename = args.filename
    column = args.column
    energies = get_energies(filename, column)
    plotname = args.plotname
    n_x_vals = args.n_x_vals
    n_y_vals = args.n_y_vals
    levels = args.levels

    x_input = [1.5, 2.1, 0.1]
    y_input = [2.3, 1.1, -0.1]

    generate_contour(x_input, y_input, energies,
                     n_x_vals=n_x_vals, n_y_vals=n_y_vals,
                     levels=levels, interp="Rbf",
                     x_label="C–O / $\AA$",
                     y_label="C-H / $\AA$",
                     z_label = "$\Delta$E / kcal mol$^{-1}$",
                     plt_title="Concerted singlet O$_2$ insertion (UPBE0-D3BJ/def2-SVPD)",
                     plt_save=args.save, plt_show=args.plot,
                     plt_name=plotname+".pdf")
