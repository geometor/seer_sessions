import numpy as np

"""
Transformation Rule:

1.  **Analyze Grid Structure:** The input is a 17x17 grid. Identify the solid horizontal lines at row 5 and row 11, and the solid vertical lines at column 5 and column 11. Determine the single color used for these divider lines (the `divider_color`). Note the background color is white (0).
2.  **Identify Object Color:** Scan the grid *excluding* the divider lines. Find the color present that is neither the background color (0) nor the `divider_color`. This is the `object_color`.
3.  **Define Sections:** Mentally (or actually) divide the grid into nine 5x5 sections based on the divider lines (rows 0-4, 6-10, 12-16 and columns 0-4, 6-10, 12-16).
4.  **Process Sections:** Iterate through each of the nine sections.
5.  **Check for Object:** For the current section, determine if any pixel within its boundaries has the `object_color`.
6.  **Apply Transformation:** Create the output grid as a copy of the input grid.
    *   If the current section *contains* the `object_color`: Find all pixels within this section in the output grid that are currently the background color (0) and change their color to the `divider_color`.
    *   If the current section *does not contain* the `object_color`: Make no changes to this section in the output grid.
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
    """
    # Determine divider color from a known divider pixel
    # Assuming the grid is at least 6x1, row 5 exists.
    divider_color = grid[5, 0]

    object_color = None
    rows, cols = grid.shape

    # Define section boundaries (excluding divider lines themselves)
    # Section row ranges: 0-4, 6-10, 12-(rows-1)
    # Section col ranges: 0-4, 6-10, 12-(cols-1)
    section_row_ranges = [(0, 5), (6, 11), (12, rows)]
    section_col_ranges = [(0, 5), (6, 11), (12, cols)]

    # Search within sections for the object color
    found_object_color = False
    for r_start, r_end in section_row_ranges:
        if found_object_color:
            break
        for c_start, c_end in section_col_ranges:
            if found_object_color:
                break
            # Extract the current section from the input grid
            section = grid[r_start:r_end, c_start:c_end]
            # Find unique colors in this section
            unique_in_section = np.unique(section)
            for color in unique_in_section:
                # Check if the color is neither background nor divider
                if color != 0 and color != divider_color:
                    object_color = color
                    found_object_color = True # Stop searching once found
                    break # Exit inner color loop

    # Basic check if object color was found (it should be based on examples)
    if object_color is None:
         print(f"Warning: Could not find a distinct object color (Divider: {divider_color}).")
         # Optionally, implement a fallback or raise an error if needed.
         # For this task, we expect an object color to exist.

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

    # 1. & 2. Identify divider and object colors
    divider_color, object_color = find_colors_and_dividers(input_grid_np)

    # If object_color wasn't found, return the original grid (or handle error)
    if object_color is None:
        print("Error: Object color not identified. Returning original grid.")
        return input_grid # Return original list of lists

    # 3. Define section boundaries
    section_row_ranges = [(0, 5), (6, 11), (12, rows)]
    section_col_ranges = [(0, 5), (6, 11), (12, cols)]

    # 4. Iterate through sections
    for r_start, r_end in section_row_ranges:
        for c_start, c_end in section_col_ranges:

            # Extract the current section view from the *input* grid
            input_section = input_grid_np[r_start:r_end, c_start:c_end]

            # 5. Check if the input section contains the object color
            contains_object = np.any(input_section == object_color)

            # 6. Apply conditional fill to the output grid
            if contains_object:
                # Iterate only through the pixels within this section's bounds
                for r in range(r_start, r_end):
                    for c in range(c_start, c_end):
                        # Check if the pixel in the output grid is background (0)
                        if output_grid_np[r, c] == 0:
                            # Change it to the divider color
                            output_grid_np[r, c] = divider_color
            # Else (contains_object is False): No changes needed for this section,
            # as output_grid_np started as a copy of input_grid_np.

    # 7. Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()