import numpy as np

"""
Transformation Rule:

1.  **Analyze Input Grid:** The input is a 17x17 grid. Identify the background color (white, 0). Confirm the presence of solid horizontal lines at row 5 and row 11, and solid vertical lines at column 5 and column 11. Determine the single color used for these divider lines (the `divider_color`).
2.  **Identify Object Color:** Scan the nine 5x5 areas defined by the divider lines (rows 0-4, 6-10, 12-16 and columns 0-4, 6-10, 12-16). Find the unique color present in these areas that is neither the background color (0) nor the `divider_color`. This is the `object_color`.
3.  **Prepare Output Grid:** Create a copy of the input grid to serve as the output grid.
4.  **Process Sections:** Iterate through each of the nine 5x5 section locations.
5.  **Check for Object Presence:** For the current section location, examine the corresponding 5x5 area in the *input* grid. Determine if any pixel within this area has the `object_color`.
6.  **Apply Conditional Transformation:**
    *   **If Object Present:** If the check in step 5 is true, locate the corresponding 5x5 section in the *output* grid. Within this output section, change the color of all pixels that are currently the background color (0) to the `divider_color`. Leave all other pixels within this output section (i.e., pixels that were originally `object_color` or `divider_color`) unchanged.
    *   **If Object Absent:** If the check in step 5 is false, make no changes to the corresponding section in the output grid.
7.  **Final Result:** The modified output grid, containing the original dividers, original object pixels, and filled backgrounds in affected sections, is the final output.
"""

def find_colors_and_dividers(grid_np):
    """
    Identifies the divider color and the object color in the grid.
    Assumes dividers are at fixed positions (row/col 5 and 11) and are consistent.
    Assumes a single object color exists besides white (0) and the divider color within sections.

    Args:
        grid_np (np.ndarray): The input grid as a NumPy array.

    Returns:
        tuple: (divider_color, object_color)
               Returns None for either color if it cannot be reliably determined.
    """
    rows, cols = grid_np.shape
    background_color = 0

    # Define expected divider locations (0-indexed)
    divider_rows = [5, 11]
    divider_cols = [5, 11]

    # Basic check for expected grid size and presence of dividers
    if not (rows > max(divider_rows) and cols > max(divider_cols)):
         # Grid is too small to contain the expected dividers
         # print("Error: Grid too small for expected dividers.")
         return None, None # Cannot determine colors

    # 1. Determine divider color and check consistency
    potential_divider_color = grid_np[divider_rows[0], 0] # Sample a point on a divider
    if potential_divider_color == background_color:
        # print("Error: Pixel at divider location is background color.")
        return None, None # Divider cannot be background

    # Verify all divider lines have the same, non-background color
    for r in divider_rows:
        if not np.all(grid_np[r, :] == potential_divider_color) or np.any(grid_np[r, :] == background_color):
            # print(f"Error: Inconsistent color or background found in divider row {r}.")
            return None, None
    for c in divider_cols:
         # Check the vertical column, excluding the intersections with horizontal dividers already checked
         col_segment1 = grid_np[0:divider_rows[0], c]
         col_segment2 = grid_np[divider_rows[0]+1:divider_rows[1], c]
         col_segment3 = grid_np[divider_rows[1]+1:rows, c]
         if not (np.all(col_segment1 == potential_divider_color) and \
                 np.all(col_segment2 == potential_divider_color) and \
                 np.all(col_segment3 == potential_divider_color)) or \
            np.any(col_segment1 == background_color) or \
            np.any(col_segment2 == background_color) or \
            np.any(col_segment3 == background_color):
            # print(f"Error: Inconsistent color or background found in divider col {c}.")
            return None, None

    divider_color = potential_divider_color

    # 2. Identify Object Color within sections
    object_color = None
    # Create a mask to select only pixels *within* the sections
    section_mask = np.ones(grid_np.shape, dtype=bool)
    section_mask[divider_rows, :] = False # Exclude divider rows
    section_mask[:, divider_cols] = False # Exclude divider columns

    # Find unique colors in the masked area (within sections)
    colors_in_sections = np.unique(grid_np[section_mask])

    # Find the color that is not background and not divider
    potential_object_colors = []
    for color in colors_in_sections:
        if color != background_color and color != divider_color:
            potential_object_colors.append(color)

    if len(potential_object_colors) == 1:
        object_color = potential_object_colors[0]
    #else:
        # Handle cases: 0 object colors or >1 potential object colors
        # Based on the problem description and examples, we expect exactly one.
        # If not exactly one, returning None signifies an issue.
        # print(f"Warning/Error: Expected 1 object color, found {len(potential_object_colors)}: {potential_object_colors}")
    #    pass # object_color remains None

    return divider_color, object_color


def transform(input_grid):
    """
    Applies the conditional background fill transformation based on object presence in sections.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify for the output
    output_grid_np = np.copy(input_grid_np)
    rows, cols = input_grid_np.shape
    background_color = 0

    # Step 1 & 2: Identify divider and object colors using the helper function
    divider_color, object_color = find_colors_and_dividers(input_grid_np)

    # Check if colors were successfully identified
    if divider_color is None or object_color is None:
        # print("Error: Divider or object color could not be reliably determined. Returning original grid.")
        # If the structure or colors don't match expectations, return the input unchanged.
        return input_grid # Return original list of lists

    # Step 4 & Define Sections: Define section boundaries (hardcoded for 17x17)
    # Row starts: 0, 6, 12. Col starts: 0, 6, 12. Size: 5x5
    section_starts = [(0, 0), (0, 6), (0, 12),
                      (6, 0), (6, 6), (6, 12),
                      (12, 0), (12, 6), (12, 12)]
    section_size = 5

    # Iterate through sections
    for r_start, c_start in section_starts:
        r_end = r_start + section_size
        c_end = c_start + section_size

        # Define slices for the current section
        section_slice = np.s_[r_start:r_end, c_start:c_end]

        # Step 5: Check if the input section contains the object color
        input_section = input_grid_np[section_slice]
        contains_object = np.any(input_section == object_color)

        # Step 6: Apply conditional fill to the output grid's section
        if contains_object:
            # Get the corresponding section view in the output grid
            output_section = output_grid_np[section_slice]
            # Find background pixels (color 0) within this output section
            background_mask = (output_section == background_color)
            # Change these background pixels to the divider color
            output_section[background_mask] = divider_color
            # Modification happens in place on output_grid_np due to view

        # Else (contains_object is False): No changes needed for this section,
        # as output_grid_np started as a copy of input_grid_np.

    # Step 7: Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()