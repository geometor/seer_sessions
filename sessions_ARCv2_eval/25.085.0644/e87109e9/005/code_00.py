import numpy as np
from collections import Counter
import sys

# Optional: Add path to utility functions if needed, e.g., for object detection
# if '../' not in sys.path:
#     sys.path.insert(0, '../')
# from util import find_objects 

# Color constants for clarity
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3
YELLOW = 4
GRAY = 5
MAGENTA = 6
ORANGE = 7
AZURE = 8
MAROON = 9

"""
The transformation identifies a 'key' section at the top of the input grid, 
bordered at the bottom by a horizontal gray line (color 5). The column indices 
containing unique non-white (0) and non-gray (5) colors within this key section 
(excluding its borders) are identified as 'target columns'. The portion of the 
grid *below* the gray divider line is the 'data section'. The most frequent color 
in the data section (excluding white) is determined ('color_to_change'). 
The output grid consists *only* of the transformed data section. The transformation 
rule is: for every pixel in the data section that falls within a 'target column' 
*and* originally had the 'color_to_change', its color is changed to azure (8). 
All other pixels in the data section retain their original color. The output grid's 
dimensions match the data section's dimensions.
"""

def find_divider_row(grid):
    """
    Finds the index of the horizontal gray line acting as the bottom border 
    of the 'key' section near the top of the grid.
    Searches from the top down, expecting non-gray content immediately above the divider.
    """
    height, width = grid.shape
    potential_divider = -1
    
    # Search the top half for a gray row preceded by a non-gray row.
    # Start search from row 1, as row 0 could be a border or part of the key.
    # Extend search slightly past halfway to be safe.
    for r in range(1, (height // 2) + 2): 
        if r >= height: # Avoid index out of bounds on smaller grids
            break 
            
        is_gray_row = np.all(grid[r] == GRAY)
        
        if is_gray_row:
            # Check if the row *above* this potential gray divider exists and is NOT gray
            if r > 0 and not np.all(grid[r - 1] == GRAY):
                 # Found a gray row preceded by a non-gray row. This is our divider.
                 potential_divider = r
                 # Assume only one such divider structure exists near the top and break.
                 break 
        # If the current row is not gray, or if it's gray but preceded by gray, continue search.
        
    # Fallback check specifically for row 5 if the main logic didn't find it.
    # This is based on the consistent pattern observed in the training examples.
    if potential_divider == -1 and height > 5 and np.all(grid[5] == GRAY):
         if 5 > 0 and not np.all(grid[4] == GRAY): # Ensure row 4 is not gray
              # print("Debug: Using fallback to identify divider at row 5.")
              return 5

    if potential_divider == -1:
         # This warning helps in debugging if the divider isn't found as expected.
         print(f"Warning: Could not reliably determine divider row based on expected pattern.")
         
    return potential_divider


def find_target_columns(grid, key_section_end_row):
    """
    Finds the column indices containing non-white/non-gray colors 
    within the key section.
    Assumes the key section is vertically between row 1 and key_section_end_row (exclusive).
    Assumes gray borders might exist horizontally at col 0 and col width-1, so excludes them.
    """
    height, width = grid.shape
    target_columns = set()
    
    # Define search boundaries for the internal part of the key section.
    start_row = 1 
    end_row = key_section_end_row # Search rows up to (but not including) the divider row.
    start_col = 1 # Assume border at column 0
    end_col = width - 1 # Assume border at last column

    # Check if the defined search area is valid.
    if start_row >= end_row or start_col >= end_col:
         # print("Debug: Invalid key section boundaries for searching target columns.")
         return [] # No valid internal area to search

    # Iterate through the internal key section.
    for r in range(start_row, end_row):
        for c in range(start_col, end_col): 
             pixel_color = grid[r, c]
             # Identify 'key' colors (not background white and not border/divider gray).
             if pixel_color != WHITE and pixel_color != GRAY:
                 target_columns.add(c)
                 
    return sorted(list(target_columns)) # Return sorted list for deterministic behavior.


def find_most_frequent_data_color(grid_section):
    """
    Finds the most frequent color in the given grid section, excluding white (0).
    If there's a tie, Counter.most_common(1) returns one of the tied elements.
    """
    # Ensure the input section is not empty.
    if grid_section.size == 0:
        return -1 # Indicate no data

    # Flatten the 2D section into a 1D array for easy counting.
    pixels = grid_section.flatten()
    
    # Count occurrences of each color, ignoring white pixels.
    color_counts = Counter(p for p in pixels if p != WHITE)
    
    # If no non-white colors are found (section is all white or empty).
    if not color_counts:
        return -1 # Indicate no dominant color found
        
    # Get the single most common non-white color.
    most_common_color, _ = color_counts.most_common(1)[0]
    return most_common_color


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list-of-lists to numpy array for easier manipulation.
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Step 1: Find the gray divider row that marks the end of the key section.
    divider_row_index = find_divider_row(input_np)
    
    # Validate the found divider index.
    if divider_row_index == -1:
        print(f"Error: Divider row not found.")
        return [] # Return empty list if essential structure is missing.
    if divider_row_index >= height - 1:
        print(f"Error: Divider row is at or past the bottom edge, no data section possible.")
        return [] # No data section exists below the divider.

    # Step 2: Extract target column indices from the key section (above the divider).
    target_columns = find_target_columns(input_np, divider_row_index)
    # print(f"Debug: Found target columns: {target_columns}")

    # Step 3: Identify and extract the data section (below the divider).
    data_section = input_np[divider_row_index + 1:, :]

    # Check if the extracted data section is empty.
    if data_section.size == 0:
        # print("Warning: Data section is empty.")
        return [] # Return empty grid if no data below divider.

    # Step 4: Determine the most frequent non-white color in the data section.
    color_to_change = find_most_frequent_data_color(data_section)
    # print(f"Debug: Found color to change: {color_to_change}")
    
    # Handle cases where the data section might be all white.
    if color_to_change == -1:
        # print("Info: Data section is all white or empty. No transformation needed.")
        # If no color needs changing, return the data section as is.
        return data_section.tolist() 

    # Step 5: Create the output grid as a copy of the data section.
    output_grid = data_section.copy()
    output_height, output_width = output_grid.shape

    # Step 6: Apply the transformation rule to the output grid.
    for r in range(output_height):
        for c in range(output_width):
            # Check if the current column is one of the target columns.
            if c in target_columns:
                # Check if the pixel's original color matches the color to be changed.
                # IMPORTANT: Check against the original `data_section`, not the `output_grid` being modified.
                if data_section[r, c] == color_to_change:
                    # Apply the color change to Azure (8).
                    output_grid[r, c] = AZURE
            # Pixels not meeting the criteria retain their original color due to the initial copy.

    # Step 7: Return the transformed data section.
    return output_grid.tolist() # Convert numpy array back to list of lists.
