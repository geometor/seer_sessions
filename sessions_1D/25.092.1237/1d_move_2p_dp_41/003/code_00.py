"""
Transforms a 1D input grid by rearranging specific segments.
1. Identify the 'Main Object': A contiguous sequence of identical pixels whose color is neither white (0) nor green (3).
2. Identify the 'Anchor Pixel': The single pixel with the color green (3) that appears after the Main Object.
3. Identify the 'Separator Pixels': The sequence of white (0) pixels located directly between the end of the 'Main Object' and the 'Anchor Pixel'.
4. Identify the 'Prefix Pixels': Any pixels before the 'Main Object'.
5. Identify the 'Suffix Pixels': Any pixels after the 'Anchor Pixel'.
6. Construct the output grid by concatenating these components in the order: Prefix + Separators + Main Object + Anchor + Suffix.
"""

import sys 
# numpy is not strictly required for this implementation using list slicing

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list containing a single list representing the 1D grid. 
                           Example: [[0, 2, 2, 0, 0, 3, 0]]

    Returns:
        list: A list containing the transformed 1D grid, or the original grid if
              the pattern is not found.
    """

    # Ensure input is valid and is a 1xN grid
    if not input_grid or not isinstance(input_grid, list) or len(input_grid) == 0 or not isinstance(input_grid[0], list):
        print("Warning: Invalid input grid format.", file=sys.stderr)
        return input_grid # Return original or empty based on context? Returning original for safety.

    # Extract the 1D row (convert to list just in case it's a numpy array row)
    try:
        grid_1d = list(input_grid[0])
    except TypeError:
         print("Warning: Could not convert input grid row to list.", file=sys.stderr)
         return input_grid # Return original grid if conversion fails

    n = len(grid_1d)
    if n == 0:
        return [[]] # Handle empty row case

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
        # If no main object is found, return the original grid
        # This might happen if the grid only contains 0s and 3s or is empty.
        # print("Warning: Main object not found.", file=sys.stderr) 
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
        # If no anchor pixel is found after the main object, return the original grid
        # print("Warning: Anchor pixel (3) not found after main object.", file=sys.stderr)
        return input_grid

    # --- Extract Components using list slicing ---
    
    # 1. Prefix Pixels: Pixels before the main object
    prefix_pixels = grid_1d[:main_start]
    
    # 2. Main Object Pixels: The main object itself
    main_object_pixels = grid_1d[main_start:main_end]
    
    # 3. Separator Pixels: Pixels between main object end and anchor
    separator_pixels = grid_1d[main_end:anchor_index]
    # Optional check: Verify separator pixels are all white (0) - not strictly needed for the reordering logic
    # if not all(p == 0 for p in separator_pixels):
    #     print("Warning: Non-white pixels found in separator segment.", file=sys.stderr)

    # 4. Anchor and Suffix Pixels: Anchor pixel and all subsequent pixels
    anchor_and_suffix_pixels = grid_1d[anchor_index:]

    # --- Construct the Output Grid ---
    # Concatenate in the new order: Prefix + Separators + Main Object + Anchor/Suffix
    output_1d = prefix_pixels + separator_pixels + main_object_pixels + anchor_and_suffix_pixels
    
    # Return the result in the expected format (list of lists)
    output_grid = [output_1d]
    
    return output_grid