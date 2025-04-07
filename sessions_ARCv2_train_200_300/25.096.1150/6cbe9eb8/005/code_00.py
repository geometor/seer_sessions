import numpy as np

"""
Transformation Rule:
1.  Identify the set of background digits (heuristically {0, 1, 2, 3} if present in the input).
2.  Locate all cells in the input grid containing non-background digits.
3.  Determine the global bounding box (minimum and maximum row and column indices) that encloses *all* these non-background cells. If no non-background cells exist, return an empty grid.
4.  Identify the "framing cells" which are the non-background cells located exactly on the perimeter (min/max row or min/max col) of this global bounding box.
5.  Create the output grid with dimensions matching the global bounding box size.
6.  Iterate through each cell within the global bounding box area of the input grid, mapping input coordinates (r_in, c_in) to output coordinates (r_out, c_out).
7.  For each corresponding cell in the output grid:
    *   Get the original value `v` from `input_grid[r_in][c_in]`.
    *   Check if `v` is a background digit.
    *   Check if the input coordinate `(r_in, c_in)` corresponds to one of the identified framing cells.
    *   If `v` is a background digit AND `(r_in, c_in)` is *not* a framing cell, set the output cell value to 0.
    *   Otherwise (if `v` is non-background OR `(r_in, c_in)` is a framing cell), copy the original value `v` to the output cell.
8.  Return the resulting output grid.
"""

def find_bounding_box(points):
    """Calculates the bounding box for a set of points (tuples of row, col)."""
    if not points:
        return None
    min_row = min(r for r, c in points)
    max_row = max(r for r, c in points)
    min_col = min(c for r, c in points)
    max_col = max(c for r, c in points)
    return min_row, min_col, max_row, max_col

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Extracts a subgrid defined by the bounding box of all non-background elements,
    identifies the frame as non-background elements on the box perimeter,
    and replaces internal background elements with 0.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # --- 1. Identify potential background digits ---
    potential_bg = {0, 1, 2, 3}
    present_digits = set(input_array.flatten())
    background_digits = potential_bg.intersection(present_digits)
    # If no digits from {0,1,2,3} are present, treat this set as empty,
    # meaning no digit will be considered background by default.
    
    # --- 2. Locate non-background cells ---
    non_background_coords = []
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] not in background_digits:
                non_background_coords.append((r, c))

    # Handle case where no non-background elements are found
    if not non_background_coords:
        return [] 

    # --- 3. Determine global bounding box ---
    bbox = find_bounding_box(non_background_coords)
    # We already checked non_background_coords is not empty, so bbox will be valid
    min_row, min_col, max_row, max_col = bbox

    # --- 4. Identify framing cells ---
    # Framing cells are non-background cells on the perimeter of the global bounding box
    framing_cells = set()
    for r, c in non_background_coords:
        if r == min_row or r == max_row or c == min_col or c == max_col:
            framing_cells.add((r, c))

    # --- 5. Create output grid ---
    output_rows = max_row - min_row + 1
    output_cols = max_col - min_col + 1
    # Initialize with a placeholder, perhaps -1, to distinguish from intended 0s
    output_array = np.full((output_rows, output_cols), -1, dtype=int) 

    # --- 6 & 7. Populate output grid ---
    for r_out in range(output_rows):
        for c_out in range(output_cols):
            # Corresponding coordinates in the input grid
            r_in = min_row + r_out
            c_in = min_col + c_out
            
            # Ensure coords are within input bounds (should be guaranteed by bbox from existing points)
            if 0 <= r_in < rows and 0 <= c_in < cols:
                original_value = input_array[r_in, c_in]
                original_coord = (r_in, c_in)

                # Check if the cell contains a background digit
                is_background = original_value in background_digits
                # Check if the cell is part of the identified frame
                is_framing_cell = original_coord in framing_cells
                
                # Apply transformation rule
                if is_background and not is_framing_cell:
                    output_array[r_out, c_out] = 0
                else:
                    # Keep original value if it's non-background OR if it's part of the frame
                    output_array[r_out, c_out] = original_value
            # else: # This case should ideally not be reached if bbox logic is sound
            #     print(f"Warning: Input coordinates ({r_in}, {c_in}) out of bounds.")
            #     pass # Keep placeholder or handle error

    # Convert back to list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid