"""
CS 437 Lab 5: Wildlife Conservation Data Extraction Script
Author: Blake McBride (blakepm2@illinois.edu)

Purpose: To extract data from the READABLE simulation logs into a clean .json format and facilitate analysis 
"""

# import re for regex and json for saving the data
import json
import re

# method for parsing only the GPS data at each timestamp for each distinct animal using regex
def parse_gps_data(file_path : str) -> dict:
    """
    Parses GPS data at each timestamp for each distinct animal from a READABLE simulation log file and returns it as a dictionary
    
    This function reads a file from the World_win/StandalongWindows64/SavannaLogs/Simulation/simulation_2023_xx_xx_xx_xx_READABLE.txt format
    and extracts the timestamp and GPS coordinates recorded for each distinct animal; formatting the results into a dictionary which can then
    be processed into a clean .json file at the end of this script. 

    Args:
        file_path (str): The path to the *READABLE* .txt file containing the GPS data for your animals.

    Returns:
        dict: A dictionary containing all parsed GPS, timestamp, and animal data which can be saved as a clean .json and/or loaded
              into a pandas DataFrame for futher analysis.
    """
    
    # setup attributes for storing data and keeping track of the current (distinct) animal
    data = {}
    current_animal = None

    # define some regular expression patterns for grabbing the animal id, the timestamp, and the gps coordinates
    animal_pattern = re.compile(r'^=============== (.*?):(.*?) LOG ===============$')
    timestamp_pattern = re.compile(r'-- Timestamp: ([\d.]+)')
    location_pattern = re.compile(r'"location": \[([-?\d.]+),([-?\d.]+)\]')


    p = r'"oxygen_saturation": \[([-+]?[0-9]*\.?[0-9]+), "heart_rate": (^-?\d+)\]'
    oxygen_saturation_heart_rate_patter = re.compile(p)


    # open the *READABLE* simulation log file
    with open(file_path, 'r') as file:
        
        for line in file:
            
            # check for animal type and id and create new entries if (new) distinct animal
            animal_match = animal_pattern.match(line.strip())
            if animal_match:
                animal_type = animal_match.group(1)
                animal_id = animal_match.group(2)
                current_animal = f"{animal_type}:{animal_id}"
                
                # set up attributes reflecting the timestamps and gps coordinates for the distinct animal represented as lists
                data[current_animal] = {"timestamp": [], "gps coordinates": [], "oxygen_saturation": [], "heart_rate": []}
                continue

            # check for timestamp and location
            if current_animal:
                timestamp_match = timestamp_pattern.match(line.strip())
                location_match = location_pattern.match(line.strip())

                oxygen_saturation_heart_rate_match = oxygen_saturation_heart_rate_patter.match(line.strip())

                # if there is a new timestamp, we add it to the list of timestamps for the distinct animal
                if timestamp_match:
                    current_timestamp = timestamp_match.group(1)
                    data[current_animal]["timestamp"].append(current_timestamp)
                    
                # if there is a location match, we perform the same operation with the gps coordinates
                elif location_match:
                    location = (location_match.group(1), location_match.group(2))
                    data[current_animal]["gps coordinates"].append(location)

                elif oxygen_saturation_heart_rate_match:
                    print(oxygen_saturation_heart_rate_match)

                    data[current_animal]["oxygen_saturation"].append(oxygen_saturation_heart_rate_match.group(1))
                    data[current_animal]["heart_rate"].append(oxygen_saturation_heart_rate_match.group(2))

    return data

# example usage

#TODO fill in your infile and outfile paths
infile_path = "../Data/simulation_2024_12_2_0_19_46_READABLE.txt"
outfile_path = "../Data/path1"

# parse the READABLE simulation log
parsed_data = parse_gps_data(infile_path)

# save the loaded data into a clean .json file
with open(f"{outfile_path}.json", 'w') as outfile:
    json.dump(parsed_data, outfile, indent=4)
    outfile.close()
