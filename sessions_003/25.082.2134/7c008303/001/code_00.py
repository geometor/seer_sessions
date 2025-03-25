"""
Identify a horizontal line of '8' (azure) in the input grid. 
Compress sections above and below this line by taking the number by pairs.
If the numbers in the pair are different, put them into the output.
If the numbers in the pair are the same, put zero.
"""

import numpy as np

def find_azure_line(grid):
    # Iterate through rows to find a row filled with '8'
    for i, row in enumerate(grid):
        if all(pixel == 8 for pixel in row):
            return i
    return -1  # Return -1 if no azure line is found

def compress_section(section):
    # Initialize an empty list to hold the compressed rows
    compressed_section = []

    # Check if the section has even or odd number of rows. Make it even.
    num_rows = len(section)
    if num_rows %2 != 0:
        section = section[:-1]

    # Iterate through the section, taking rows in pairs
    for i in range(0, len(section), 2):
        row1 = section[i]
        row2 = section[i+1]
        compressed_row = []

        # Iterate through columns
        for j in range(len(row1)):
          if row1[j] == row2[j]:
            compressed_row.append(0)
          else:
            compressed_row.append(row1[j])
            compressed_row.append(row2[j])
        
        compressed_row = compressed_row[:len(row1)//2*2] # make sure that it is even
        compressed_section.append(compressed_row)

    return compressed_section

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the azure line
    azure_line_index = find_azure_line(input_grid)

    # Split the grid into top and bottom sections
    top_section = input_grid[:azure_line_index]
    bottom_section = input_grid[azure_line_index + 1:]
    
    # Compress each section
    compressed_top = compress_section(top_section)
    compressed_bottom = compress_section(bottom_section)

    # Concatenate compressed sections to form output grid
    if (len(compressed_top) > 0) and (len(compressed_bottom) > 0):
      output_grid = np.concatenate((compressed_top, compressed_bottom), axis=0)
    elif (len(compressed_top) > 0):
      output_grid = np.array(compressed_top)
    elif (len(compressed_bottom) > 0):
      output_grid = np.array(compressed_bottom)
    else:
       output_grid = np.array([]) #empty

    return output_grid.tolist()