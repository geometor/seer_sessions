```python
import numpy as np
from scipy.ndimage import label, generate_binary_structure
import collections

"""
Transformation rule:
1. Initialize: Create the output grid as a copy of the input grid.
2. Identify Separator: Find the first row index (`sep_row`) where all pixels have the same non-white color. Let this color be the `separator_color` (S). If no such row exists, return the initial copy.
3. Define Sections: The 'control section' comprises rows 0 to `sep_row - 1`. The 'data section' comprises rows `sep_row` to the bottom.
4. Identify Key Colors: Create a set `key_colors` (K) containing all unique non-white colors found in the first column (`column 0`) of the input grid's control section.
5. Clean Data Section: Iterate through each pixel `(r, c)` in the output grid's data section (where `r >= sep_row`). Let the pixel's color be `C`. If `C` is not the `separator_color` (S) AND `C` is not in the set `key_colors` (K), change the color of the pixel `output_grid[r, c]` to `separator_color` (S).
6. Process Control Section: Iterate through each row `r` in the control section (where `r < sep_row`):
    a. Get the `key_color` from the input grid at `input_grid[r, 0]`.
    b. If `key_color` is not white (0):
        i. Count the number `N` of distinct connected objects (using 8-way adjacency) of `key_color` within the *modified* data section of the output grid.
        ii. If `N > 0`:
            1. Calculate the line length, ensuring it doesn't exceed the grid width: `line_length = min(N, grid_width)`.
            2. In the output grid, set the pixels in row `r` from column 0 up to (but not including) `line_length` to `key_color`.
            3. Set the remaining pixels in row `r` (from column `line_length` to the end) to white (0).
        iii. If `N == 0`:
            1. Set all pixels in row `r` of the output grid to white (0).
    c. If `key_color` is white (0), leave the row `r` in the output grid unchanged from the initial copy (it's already mostly white, or will be overwritten if its key pixel was non-white).
7. Return: Return the modified output grid.
"""

def find_objects_count(grid_section, color):
    """
    Counts the number of distinct connected objects of a given color
    in a grid section using 8-way connectivity.
    """
    # Create a binary mask where 1 represents the target color, 0 otherwise
    binary_mask = (grid_section == color)

    # Define the connectivity structure (8-way)
    structure = generate_binary_structure(2, 2) # 2 means connectivity includes diagonals

    # Label connected components
    labeled_array, num_features = label(binary_mask, structure=structure)

    return num_features

def transform(input_grid):
    """
    Applies the transformation rule based on object counts in the data section,
    after cleaning the data section based on control keys.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # 1. Initialize output grid
    output_grid = np.copy(input_np)

    # 2. Identify Separator row and color
    sep_row = -1
    separator_color = -1
    for r in range(height):
        row = input_np[r, :]
        # Check if all elements are the same and not white (0)
        first_val = row[0]
        if first_val != 0 and np.all(row == first_val):
            sep_row = r
            separator_color = first_val
            break

    # If no separator found
    if sep_row == -1:
        #print("Warning: Separator row not found. Returning input grid copy.")
        return output_grid.tolist() 

    # 3. Define Sections (implicit in loops below)
    control_section_rows = range(sep_row)
    data_section_rows = range(sep_row, height)

    # 4. Identify Key Colors (K) from control section column 0
    key_colors = set()
    for r in control_section_rows:
        key = input_np[r, 0]
        if key != 0: # Exclude white
            key_colors.add(key)

    # 5. Clean Data Section (in the output_grid)
    for r in data_section_rows:
        for c in range(width):
            pixel_color = output_grid[r, c]
            # Replace if color is not Separator (S) AND not a Key Color (K)
            if pixel_color != separator_color and pixel_color not in key_colors:
                output_grid[r, c] = separator_color

    # Define the cleaned data section for counting
    cleaned_data_section = output_grid[sep_row:, :]

    # 6. Process Control Section
    for r in control_section_rows:
        # a. Get the key color C from the *original* input
        key_color = input_np[r, 0]

        # b. If C is non-white
        if key_color != 0:
            # i. Count objects N of key_color in the *cleaned* data section
            object_count = find_objects_count(cleaned_data_section, key_color)

            # ii. If N > 0
            if object_count > 0:
                # 1. Calculate line length
                line_length = min(object_count, width) # Ensure not exceeding width
                # 2. Draw line
                output_grid[r, 0:line_length] = key_color
                # 3. Set remaining pixels in the row to white
                if line_length < width:
                    output_grid[r, line_length:] = 0
            # iii. If N == 0
            else:
                # 1. Set entire row to white
                output_grid[r, :] = 0
        
        # c. If key_color is white(0), do nothing - row remains as copied initially,
        #    unless a previous step modified it (which shouldn't happen for rows starting with white).
        #    Making sure rows starting with white are cleared just in case:
        # else: # key_color == 0
        #    This might clear potentially useful info if input rows start with 0 but have other colors.
        #    The examples show rows starting with 0 remain 0, so the original 'do nothing' is best.
        #    output_grid[r, :] = 0 # Reverted this potential change.

    # 7. Return the modified output grid
    return output_grid.tolist()
```