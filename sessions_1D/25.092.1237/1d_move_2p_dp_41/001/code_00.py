"""
Scan the input grid (a 1D array) to identify three key components:
a. The 'main object': A contiguous sequence of identical pixels whose color is neither white (0) nor green (3).
b. The 'anchor pixel': The single pixel with the color green (3).
c. The 'separator pixels': The sequence of white (0) pixels located directly between the end of the 'main object' and the 'anchor pixel'.
Identify the pixels *before* the 'main object'.
Identify the pixels *from* the 'anchor pixel' to the end of the grid.
Construct the output grid by concatenating these components in the following order:
a. The pixels *before* the 'main object'.
b. The 'separator pixels'.
c. The 'main object'.
d. The pixels *from* the 'anchor pixel' to the end.
"""

import sys
import numpy as np # numpy might be useful for more complex grid operations, though not strictly needed here.

# We expect the input grid to be 1xN, so we primarily work with the first row.
def transform(input_grid):
    """
    Transforms the input grid based on the identified rules.
    """
    
    # Ensure input is not empty and has at least one row
    if not input_grid or not input_grid[0]:
        return [] # Return empty for invalid input

    grid_1d = input_grid[0]
    n = len(grid_1d)

    # --- Find the Main Object ---
    main_start = -1
    main_end = -1
    main_color = -1
    
    # Iterate to find the start of the main object
    for i in range(n):
        pixel = grid_1d[i]
        if pixel != 0 and pixel != 3: # Found a potential start
            main_start = i
            main_color = pixel
            break
            
    if main_start == -1:
        # If no main object is found (unexpected based on examples), return original grid
        print("Warning: Main object not found.", file=sys.stderr)
        return input_grid 

    # Iterate from the start to find the end of the main object
    for i in range(main_start, n):
        if grid_1d[i] != main_color:
            main_end = i # The end index is exclusive
            break
    else: # If the loop completed without breaking, the object goes to the end
        main_end = n
        
    # --- Find the Anchor Pixel (Green=3) ---
    anchor_index = -1
    # Search only *after* the main object
    for i in range(main_end, n):
        if grid_1d[i] == 3:
            anchor_index = i
            break

    if anchor_index == -1:
        # If no anchor pixel is found (unexpected based on examples), return original grid
        print("Warning: Anchor pixel (3) not found after main object.", file=sys.stderr)
        return input_grid

    # --- Extract Components ---
    
    # 1. Pixels before the main object
    pixels_before = grid_1d[:main_start]
    
    # 2. The main object itself
    main_object_pixels = grid_1d[main_start:main_end]
    
    # 3. Separator pixels (between main object end and anchor)
    separator_pixels = grid_1d[main_end:anchor_index]
    # Optional: Verify separator pixels are all white (0)
    # if not all(p == 0 for p in separator_pixels):
    #     print("Warning: Non-white pixels found in separator segment.", file=sys.stderr)

    # 4. Anchor pixel and all subsequent pixels
    anchor_and_after = grid_1d[anchor_index:]

    # --- Construct the Output Grid ---
    # Concatenate in the new order: before + separators + main_object + anchor_and_after
    output_1d = pixels_before + separator_pixels + main_object_pixels + anchor_and_after
    
    # Return the result in the expected format (list of lists)
    output_grid = [output_1d]
    
    return output_grid
