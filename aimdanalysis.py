import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import argparse


def get_args():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('filename',
                           nargs='+',
                           type=str,
                           help="Input csv name, including '.csv' suffix")
    my_parser.add_argument("-a", "--atom_pair",
                           nargs='+',
                           action='store',
                           type=int,
                           help="Specify index of pair of atoms to calculate distance between them, 1-indexed")
    my_parser.add_argument("-m", "--multi",
                           action='store_true',
                           help="Process multiple files and overlay plots")
    return my_parser.parse_args()


def _get_relative_energies(energies):
    # Input numpy array, find minimum energy, normalize all energies to
    # lowest energy in kcal/mol
    min_energy = np.min(energies)
    rel_energies = (energies - min_energy) * 627.509

    return rel_energies


def extract_energy_from_sections(filename, debug=False):
    # Initialize variables to keep track of the current section
    in_section = False
    section_lines = []
    time_step_found = False
    energy_found = False
    inst_temp_found = False

    time_step = []
    energies = []
    inst_temp = []

    # Define the regular expression patterns
    section_start_pattern = r"TIME STEP #"
    section_end_pattern = r"Time for this dynamics step:"
    energy_pattern = r"Total energy in the final basis set =\s+(-?\d+\.\d+)"
    inst_temp_pattern = r"Instantaneous Temperature =\s+(-?\d+\.\d+)"

    with open(filename, 'r') as file:
        for line in file:
            # Check for the start of a new section
            if re.search(section_start_pattern, line):
                in_section = True
                section_lines = []
                time_step_value = line.strip().split()[8]
                if debug == True:
                    print(f"Time step value in this section: {time_step_value} fs")
                time_step.append(time_step_value)
                time_step_found = True

            if in_section:
                section_lines.append(line)

                # Check for the end of the section
                if re.search(section_end_pattern, line):
                    in_section = False

                    # Search for the energy line within the section
                    for section_line in section_lines:
                        energy_match = re.search(energy_pattern, section_line)
                        if energy_match:
                            energy_value = energy_match.group(1).strip().split()
                            if debug == True:
                                print(f"Energy in this section: {energy_value[0]} Ha")
                            energies.append(energy_value)
                            energy_found = True
                    # Search for the instantaneous temperature line within the section
                    for section_line in section_lines:
                        inst_temp_match = re.search(inst_temp_pattern, section_line)
                        if inst_temp_match:
                            inst_temp_value = str(inst_temp_match.group(1))
                            if debug == True:
                                print(f"Instantaneous temperature in this section: {inst_temp_value} K")
                                print("---------------------------------------------------")
                            inst_temp.append(inst_temp_value)
                            inst_temp_found = True

                    if not time_step_found:
                        print("Time step not found")
                        energies.append("NaN")
                    if not energy_found:
                        print("Energy not found")
                        energies.append("NaN")
                    if not inst_temp_found:
                        print("Instantaneous temperature not found")
                        inst_temp.append("NaN")

    time_step = np.array(time_step, dtype='float').T
    energies = np.array(energies, dtype='float').T[0]
    inst_temp = np.array(inst_temp, dtype='float').T

    rel_energies = _get_relative_energies(energies)

    # sim_data = np.column_stack((time_step, rel_energies, inst_temp))

    return time_step, rel_energies, inst_temp


def extract_energy_from_energy_file(filename):
    # Initialize an empty list to store the data
    data = []

    # Open the file and read its contents
    with open(filename, 'r') as file:
        # Skip the first line (header)
        next(file)
        for line in file:
            # Split the line into values and convert them to floats
            values = [float(val) for val in line.split()]
            data.append(values)

    # Create a numpy array from the extracted data
    arr = np.array(data)

    time_steps = arr[:, 0]
    diff_rel_energies = arr[:, 1]*627.509
    delta_rel_energies = arr[:, 2]*627.509

    return time_steps, diff_rel_energies, delta_rel_energies


def extract_data_from_tandv_file(filename):
    # Initialize an empty list to store the data
    data = []

    # Open the file and read its contents
    with open(filename, 'r') as file:
        # Skip the first line (header)
        next(file)
        for line in file:
            # Split the line into values and convert them to floats
            values = [float(val) for val in line.split()]
            data.append(values)

    # Create a numpy array from the extracted data
    arr = np.array(data)

    time_steps = arr[:, 0]
    pe_total = arr[:, 1]
    ke_total = arr[:, 2]
    pe_rel = arr[:, 3]*627.509
    ke_rel = arr[:, 4]*627.509

    return time_steps, pe_total, ke_total, pe_rel, ke_rel


def extract_data_from_xyz_file(filename, atom1, atom2):
    coords = read_coordinates(filename)
    distances_array = calculate_distance(coords, atom1, atom2)

    return distances_array


def read_coordinates(filename, atom1, atom2):
    distances = []
    atom1_type = []
    atom2_type = []

    with open(filename, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        if lines[i].strip().isdigit():
            num_atoms = int(lines[i])
            time_step = float(lines[i + 1].strip())
            i += 2
            current_coords = []
            current_atom_types = []

            for j in range(num_atoms):
                atom_types = [str(coord) for coord in lines[i].split()[0]]
                coords = [float(coord) for coord in lines[i].split()[1:]]
                current_atom_types.append(atom_types)
                current_coords.append(coords)
                i += 1

            # switched atom numbering from 1-index to 0-index
            if len(current_coords) == num_atoms:
                atom1_type = current_atom_types[atom1-1]
                atom2_type = current_atom_types[atom2-1]
                atom1_coords = current_coords[atom1-1]
                atom2_coords = current_coords[atom2-1]
                distance = np.linalg.norm(np.array(atom1_coords) - np.array(atom2_coords))
                distances.append((time_step, distance))
        else:
            i += 1

    return np.array(distances), str(atom1_type[0]), str(atom2_type[0])


def calc_diffs(rel_energies, inst_temp):
    diff_rel_energies = np.diff(rel_energies)
    diff_rel_energies = np.insert(diff_rel_energies, 0, 0)
    diff_inst_temp = np.diff(inst_temp)
    diff_inst_temp = np.insert(diff_inst_temp, 0, 0)

    return diff_rel_energies, diff_inst_temp


def plot_data_from_out(time_steps, relative_energies, temperatures, delta_relative_energies, delta_temperatures, filename):

    # Create a figure with subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Plot Time step vs relative energy in the first subplot
    axs[0, 0].plot(time_steps, relative_energies, label='Rel. Energy')
    axs[0, 0].set_xlabel("Time Step (fs)")
    axs[0, 0].set_ylabel("Rel. Energy (kcal/mol)")
    axs[0, 0].set_title("Time Step vs Rel. Electronic Energy")

    # Plot Time step vs instantaneous temperature in the second subplot
    axs[0, 1].plot(time_steps, temperatures, label='Inst. Temperature')
    axs[0, 1].set_xlabel("Time Step (fs)")
    axs[0, 1].set_ylabel("Inst. Temperature (K)")
    axs[0, 1].set_title("Time Step vs Instantaneous Temperature")

    # Plot Time step vs delta relative energy in the third subplot
    axs[1, 0].plot(time_steps, delta_relative_energies, label='Diff Rel. Energy')
    axs[1, 0].set_xlabel("Time Step (fs)")
    axs[1, 0].set_ylabel("Seq. Diff. Rel. Energy (kcal/mol)")
    axs[1, 0].set_title("Time Step vs Diff Relative Electronic Energy")

    # Plot Time step vs delta instantaneous temperature in the fourth subplot
    axs[1, 1].plot(time_steps, delta_temperatures, label='Diff Inst. Temp.')
    axs[1, 1].set_xlabel("Time Step (fs)")
    axs[1, 1].set_ylabel("Seq. Diff. Inst. Temp. (K)")
    axs[1, 1].set_title("Time Step vs Diff Instantaneous Temperature")

    # Add legends to each subplot
    axs[0, 0].legend()
    axs[0, 1].legend()
    axs[1, 0].legend()
    axs[1, 1].legend()

    plt.tight_layout()
    plt.savefig(f"{filename}.pdf", format="pdf")
    plt.show()


def plot_data_from_energy(time_steps, diff_relative_energies, delta_relative_energies, filename):

    # Create a figure with subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Plot Time step vs diff relative energy in the first subplot
    axs[0].plot(time_steps, diff_relative_energies, label='Diff Rel. Energy')
    axs[0].set_xlabel("Time Step (fs)")
    axs[0].set_ylabel("Diff. Rel. Energy (kcal/mol)")
    axs[0].set_title("Time Step vs Seq. Diff. Rel. Energy")

    # Plot Time step vs delta relative energy in the second subplot
    axs[1].plot(time_steps, delta_relative_energies, label='Delta Rel. Energy')
    axs[1].set_xlabel("Time Step (fs)")
    axs[1].set_ylabel("Delta Rel. Energy (kcal/mol)")
    axs[1].set_title("Time Step vs Delta Relative Energy")

    # Add legends to each subplot
    axs[0].legend()
    axs[1].legend()

    plt.tight_layout()
    plt.savefig(f"{filename}.pdf", format="pdf")
    plt.show()


def plot_data_from_tandv(time_steps, abs_ke_kcal, abs_pe_kcal, rel_ke_kcal, rel_pe_kcal, filename):

    # Create a figure with subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Plot Time step vs diff relative energy in the first subplot
    axs[0].plot(time_steps, abs_ke_kcal, label='Abs KE Ha')
    axs[0].plot(time_steps, abs_pe_kcal, label='Abs PE Ha')
    axs[0].set_xlabel("Time Step (fs)")
    axs[0].set_ylabel("Energy component (Ha)")
    axs[0].set_title("Time Step vs Energy Component")

    # Plot Time step vs delta relative energy in the second subplot
    axs[1].plot(time_steps, rel_ke_kcal, label='Rel KE kcal')
    axs[1].plot(time_steps, rel_pe_kcal, label='Rel PE kcal')
    axs[1].set_xlabel("Time Step (fs)")
    axs[1].set_ylabel("Delta Energy (kcal/mol)")
    axs[1].set_title("Time Step vs Delta Energy Component")

    # Add legends to each subplot
    axs[0].legend()
    axs[1].legend()

    plt.tight_layout()
    plt.savefig(f"{filename}.pdf", format="pdf")
    plt.show()


def plot_data_from_xyz(time_distances_array, atom1, atom2, atom1_type, atom2_type, filename):

    time_steps = time_distances_array[:, 0]
    distances = time_distances_array[:, 1]

    # Create a figure with a single subplot
    fig, ax = plt.subplots(figsize=(5, 5))

    # Plot Time step vs distance
    ax.plot(time_steps, distances, label=f'r({atom1_type}{atom1}-{atom2_type}{atom2})')
    ax.set_xlabel("Time Step (fs)")
    ax.set_ylabel(f'r({atom1_type}{atom1}-{atom2_type}{atom2}) ($\AA$)')
    ax.set_title("Time Step vs Distance")

    # Add a legend to the subplot
    ax.legend()

    plt.tight_layout()
    plt.savefig(f"{filename}_distance_{atom1_type}{atom1}-{atom2_type}{atom2}.pdf", format="pdf")
    plt.show()


if __name__ == "__main__":

    args = get_args()
    filename = args.filename
    do_multi = args.multi
    print(do_multi)

    for i in range(len(filename)):

        if filename[i].endswith(".pdf"):
            continue

        elif filename[i].endswith(".out"):
            time_step, rel_energies, inst_temp = extract_energy_from_sections(filename[i], debug=False)
            diff_rel_energies, diff_inst_temp = calc_diffs(rel_energies, inst_temp)
            plot_data_from_out(time_step, rel_energies, inst_temp, diff_rel_energies, diff_inst_temp, filename[i].strip(".out"))

        elif filename[i].startswith("Energy"):
            time_step, diff_rel_energies, delta_rel_energies = extract_energy_from_energy_file(filename[i])
            plot_data_from_energy(time_step, diff_rel_energies, delta_rel_energies, filename[i])

        elif filename[i].startswith("TandV"):
            time_steps, pe_total, ke_total, pe_rel, ke_rel = extract_data_from_tandv_file(filename[i])
            plot_data_from_tandv(time_steps, pe_total, ke_total, pe_rel, ke_rel, filename[i])

        elif filename[i].endswith(".xyz"):
            atom1 = args.atom_pair[0]
            atom2 = args.atom_pair[1]
            time_distances_array, atom1_type, atom2_type = read_coordinates(filename[i], atom1, atom2)
            plot_data_from_xyz(time_distances_array, atom1, atom2, atom1_type, atom2_type, filename[i].strip(".xyz"))

        else:
            continue
