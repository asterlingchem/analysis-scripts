import os
import fileinput
import sys
import shutil

def make_subdirectories(template_path):
    first_dist = float(sys.argv[2])
    print(f"First distance: {first_dist}")
    last_dist = float(sys.argv[3])
    print(f"Last distance: {last_dist}")
    scan_steps = int(sys.argv[4])
    print(f"Scan steps: {scan_steps}")

    scan_range = float(last_dist) - float(first_dist)
    interval = round((scan_range / scan_steps), 5)
    scan_list = []

    # Create directories and copy the script into each directory
    for i in range(scan_steps+1):

        # Generate list of distances to scan over
        scan_list.append(first_dist + (i*interval))

        # Create the new directory
        base_directory = os.getcwd()
        subdir_name = str(round(scan_list[i], 2))
        new_directory = os.path.join(base_directory, subdir_name)
        os.makedirs(new_directory, exist_ok=True)

        # Copy the input script and xyz file into the new directory
        input_destination = os.path.join(new_directory, template_path)
        shutil.copy(os.path.join(base_directory, template_path), input_destination)
        xyz_destination = os.path.join(new_directory, 'scan.xyz')
        shutil.copy(os.path.join(base_directory, 'scan.xyz'), xyz_destination)


# def copy_template_to_subdirectories(template_path):
    # for root, _, _ in os.walk('.'):
    #     subdirectory = os.path.join(root, 'scan.xyz')
    #     if os.path.isfile(subdirectory):
    #         target_file = os.path.join(root, os.path.basename(template_path))
    #         if not os.path.exists(target_file):
    #             shutil.copy(template_path, target_file)
    #             print("Copied template to ", root)
            # else:
            #     shutil.copy(template_path, target_file)
            #     print("Overwritten template in ", root)

    # Copy the input script and xyz file into the new directory
    # input_destination = os.path.join(new_directory, template_path)
    # shutil.copy(os.path.join(source_directory, template_path), input_destination)
    # xyz_destination = os.path.join(new_directory, 'scan.xyz')
    # shutil.copy(os.path.join(source_directory, 'scan.xyz'), xyz_destination)

def read_coordinates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove the first two lines (number of coordinates and blank line)
    lines = lines[2:]

    # Extract the coordinates
    coordinates = [line.strip().split() for line in lines]

    return coordinates

def update_scan_file(input_file_path, coordinates, first_frag_size, long_dist):
    scan_step = float(input_file_path.split('/')[1])
    with fileinput.FileInput(input_file_path, inplace=True) as file:
        for line in file:
            if "COORDS2" in line:
                # for coords in coordinates:
                #     print("\t".join(coords))
                for i, coords in enumerate(coordinates[:-first_frag_size]):
                    print("\t".join(coords))
                for i, coords in enumerate(coordinates[-first_frag_size:]):
                    updated_coords = [str(coords[0]), float(coords[1]), float(coords[2]), round(float(coords[3]) + scan_step, 5)]
                    print("\t".join(str(x) for x in updated_coords))
            elif "COORDS1" in line:
                for i, coords in enumerate(coordinates[:-first_frag_size]):
                    print("\t".join(coords))
                for i, coords in enumerate(coordinates[-first_frag_size:]):
                    updated_coords = [str(coords[0]), float(coords[1]), float(coords[2]), round(float(coords[3]) + long_dist, 5)]
                    print("\t".join(str(x) for x in updated_coords))
            else:
                print(line.strip())

if __name__ == "__main__":

    print("Frozen scan of molecule aligned along z axis")

    if len(sys.argv) < 7:
        print("Args: [inp name] [scan start] [scan end] [scan steps] [frag 1 size] [long dist]")
        exit(0)

    # Step 1: Copy template to all subdirectories
    template_path = sys.argv[1]
    print(f"Template: {template_path}")
    make_subdirectories(template_path)
    first_frag_size = int(sys.argv[5])
    long_dist = float(sys.argv[6])

    print("=========================")

    # Step 2: Read coordinates from scan.xyz and replace "COORDS1" and "COORDS2" in template
    for root, _, files in os.walk('.'):
        if root == '.':
            continue
        if 'scan.xyz' in files:
            xyz_file_path = os.path.join(root, 'scan.xyz')
            coordinates = read_coordinates(xyz_file_path)
            input_file_path = os.path.join(root, template_path)
            update_scan_file(input_file_path, coordinates, first_frag_size, long_dist)
            print("Written coordinates to input file: ", input_file_path)
        else:
            print("skipping", root)
