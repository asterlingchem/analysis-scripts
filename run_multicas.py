import os
import shutil
import sys

"""
Script to generate CAS-CI scan for orbital contraction project
First argument is template script to be modified
Second argument is first scan distance
Third argument is last scan distance
Fourth argument is number of scan steps
"""

if len(sys.argv) < 5:
    print("Args: [template] [first distance] [last distance] [scan steps]")
    exit(0)

# Get the current working directory as the source directory
source_directory = os.getcwd()

# Get the current working directory as the base directory
base_directory = os.getcwd()

# Get the script name from the command-line argument
script_name = sys.argv[1]
print(f"Template: {script_name}")

# Get the range of distances and number of steps to scan over

first_dist = float(sys.argv[2])
print(f"First distance: {first_dist}")
last_dist = float(sys.argv[3])
print(f"Last distance: {last_dist}")
scan_steps = int(sys.argv[4])
print(f"Scan steps: {scan_steps}")

print("=========================")

scan_range = float(last_dist) - float(first_dist)
interval = round((scan_range / scan_steps), 5)
scan_list = []

# Create directories and copy the script into each directory
for i in range(scan_steps+1):

    # Generate list of distances to scan over
    scan_list.append(first_dist + (i*interval))

    # Create the new directory
    subdir_name = str(round(scan_list[i], 2))
    new_directory = os.path.join(base_directory, subdir_name)
    os.makedirs(new_directory, exist_ok=True)

    # Copy the script into the new directory
    script_destination = os.path.join(new_directory, script_name)
    shutil.copy(os.path.join(source_directory, script_name), script_destination)

    # Replace the "SCAN_DISTANCE" string with the scan length
    with open(script_destination, "r") as file:
        script_content = file.read()
        modified_content = script_content.replace("SCAN_DISTANCE", str(scan_list[i]))

    with open(script_destination, "w") as file:
        file.write(modified_content)

    print(f"Created scan length {subdir_name}")

print("=========================")
print("Finished creating jobs")
