import numpy as np

"""
Transformation Rule:

1.  **Analyze Grid Structure:** The input is a 17x17 grid. Identify the solid horizontal lines at row 5 and row 11, and the solid vertical lines at column 5 and column 11. Determine the single color used for these divider lines (the `divider_color`). Note the background color is white (0).
2.  **Identify Object Color:** Scan the grid *excluding* the divider lines. Find the color present that is neither the background color (0) nor the `divider_color`. This is the `object_color`.
3.  **Define Sections:** Mentally (or actually) divide the grid into nine 5x5 sections based on the divider lines (rows 0-4, 6-10, 12-16 and columns 0-4, 6-10, 12-16).
4.  **Process Sections:** Iterate through each of the nine sections.
5.  **Check for Object:** For the current section, determine if any pixel within its boundaries in the *input* grid has the `object_color`.
6.  **Apply Transformation:** Create the output grid as a copy of the input grid.
    *   If the current section in the *input* grid *contains* the `object_color`: Find all pixels within this section in the *output* grid that are currently the background color (0) and change their color to the `divider_color`. Leave other pixels (object pixels, divider pixels already copied) unchanged within this section.
    *   If the current section in the *input* grid *does not contain* the `object_color`: Make no changes to this section in the output grid (it remains identical to the input section).
7.  **Final Output:** The resulting modified grid is the final output. The divider lines and the original object pixels remain unchanged throughout the process.
"""

def find_colors_and_dividers(grid):
    """
    Identifies the divider color and the object color in the grid.
    Assumes dividers are at fixed positions (row/col 5 and 11) and are consistent.
    Assumes a single object color exists besides white (0) and the divider color within sections.

    Args:
        grid (np.ndarray): The input grid as a NumPy array.

    Returns:
        tuple: (divider_color, object_color)
               Returns None for object_color if it cannot be determined.
               Returns None for divider_color if structure is not as expected.
    """
    rows, cols = grid.shape
    background_color = 0

    # Basic check for expected grid size
    if rows != 17 or cols != 17:
        print(f"Warning: Grid dimensions ({rows}x{cols}) are not the expected 17x17.")
        # Attempt to proceed if possible, but might fail later
        # For this specific task based on examples, we expect 17x17
        # If the structure is different, this logic won't work.
        # A more robust solution would dynamically find dividers.
        # Here, we'll assume fixed dividers based on the problem's pattern.
        # Set divider lines based on typical structure
        divider_rows = [5, 11]
        divider_cols = [5, 11]
        if not (rows > max(divider_rows) and cols > max(divider_cols)):
             print("Error: Grid too small for expected dividers.")
             return None, None # Cannot determine colors
    else:
        divider_rows = [5, 11]
        divider_cols = [5, 11]


    # 1. Determine divider color from a known divider pixel
    # Check consistency across all divider lines
    potential_divider_color = grid[divider_rows[0], 0]
    if potential_divider_color == background_color: # Divider cannot be background
        print("Error: Pixel at divider location is background color.")
        return None, None

    # Verify all divider lines have the same, non-background color
    for r in divider_rows:
        if not np.all(grid[r, :] == potential_divider_color):
            print(f"Error: Inconsistent color or background found in divider row {r}.")
            return None, None
    for c in divider_cols:
         if not np.all(grid[:, c] == potential_divider_color):
            print(f"Error: Inconsistent color or background found in divider col {c}.")
            return None, None

    divider_color = potential_divider_color


    # 2. Identify Object Color
    object_color = None
    # Define section boundaries (excluding divider lines themselves)
    # Create a mask to select only pixels *within* the sections
    section_mask = np.ones(grid.shape, dtype=bool)
    section_mask[divider_rows, :] = False # Exclude divider rows
    section_mask[:, divider_cols] = False # Exclude divider columns

    # Find unique colors in the masked area (within sections)
    colors_in_sections = np.unique(grid[section_mask])

    # Find the color that is not background and not divider
    found_object_color = None
    potential_object_colors = []
    for color in colors_in_sections:
        if color != background_color and color != divider_color:
            potential_object_colors.append(color)

    if len(potential_object_colors) == 1:
        object_color = potential_object_colors[0]
    elif len(potential_object_colors) == 0:
         print(f"Warning: Could not find a distinct object color within sections (Divider: {divider_color}).")
         # Fallback: Maybe check the entire grid? No, stick to sections per rule.
         return divider_color, None # Return divider, but no object found
    else:
         print(f"Warning: Found multiple potential object colors ({potential_object_colors}). Using the first one: {potential_object_colors[0]}.")
         # This case shouldn't happen based on examples, but handle it defensively.
         object_color = potential_object_colors[0]


    return divider_color, object_color


def transform(input_grid):
    """
    Applies the conditional background fill transformation based on object presence in sections.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify for the output
    output_grid_np = np.copy(input_grid_np)
    rows, cols = input_grid_np.shape
    background_color = 0

    # 1. & 2. Identify divider and object colors
    divider_color, object_color = find_colors_and_dividers(input_grid_np)

    # Check if colors were successfully identified
    if divider_color is None:
        print("Error: Divider color could not be reliably determined. Returning original grid.")
        return input_grid # Return original list of lists
    if object_color is None:
        print("Error: Object color not identified within sections. Returning original grid.")
        return input_grid # Return original list of lists

    # 3. Define section boundaries (hardcoded based on 17x17 structure)
    # Row starts: 0, 6, 12. Col starts: 0, 6, 12. Size: 5x5
    section_starts = [(0, 0), (0, 6), (0, 12),
                      (6, 0), (6, 6), (6, 12),
                      (12, 0), (12, 6), (12, 12)]
    section_size = 5

    # 4. Iterate through sections
    for r_start, c_start in section_starts:
        r_end = r_start + section_size
        c_end = c_start + section_size

        # Define slices for the current section
        section_slice = np.s_[r_start:r_end, c_start:c_end]

        # Extract the current section view from the *input* grid
        input_section = input_grid_np[section_slice]

        # 5. Check if the input section contains the object color
        contains_object = np.any(input_section == object_color)

        # 6. Apply conditional fill to the output grid's section
        if contains_object:
            # Get the corresponding section in the output grid
            output_section = output_grid_np[section_slice]
            # Find background pixels within this section
            background_mask = (output_section == background_color)
            # Change these background pixels to the divider color
            output_section[background_mask] = divider_color
            # Note: This modifies output_grid_np in place because output_section is a view

        # Else (contains_object is False): No changes needed for this section,
        # as output_grid_np started as a copy of input_grid_np.

    # 7. Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()