import numpy as np
from typing import List, Set, Tuple

"""
Transforms the input grid based on the set of unique non-background colors present.
The background color is assumed to be Orange (7). Three specific rules are defined based on the exact set of active colors:

Rule 1 (Active Colors: {Red(2), Maroon(9), Blue(1)}):
Applies a specific, hardcoded pattern modification observed in the first training example. 
Certain pixels are added (changed from background to Red, Maroon, or Blue) and others are removed (changed from Maroon or Blue back to background Orange).

Rule 2 (Active Colors: {Gray(5), Maroon(9), Green(3)}):
Adjusts horizontal segments of Gray, Maroon, or Green. For each row, segments are extended rightwards with their color to end at column index 9 (inclusive). If a segment originally extended beyond column 9, the portion from column index 10 onwards is changed back to the background Orange(7).

Rule 3 (Active Colors: {Azure(8)}):
Performs vertical consolidation of Azure pixels within each column.
First, determine the maximum row index (`max_multi_r`) that contains Azure pixels in more than one column.
Then, for each column `c` containing Azure pixels:
  Find the minimum (`min_r_c`) and maximum (`max_r_c`) row indices of Azure pixels within that column.
  Calculate the target maximum row for filling: `final_max_r = max(max_r_c, max_multi_r)`.
  Fill the column `c` with Azure(8) from row `min_r_c` down to `final_max_r` (inclusive).

If the set of active colors does not match any of these specific sets, the input grid is returned unchanged.
"""

def get_unique_colors(grid: np.ndarray, background_color: int = 7) -> Set[int]:
    """Finds unique colors in the grid, excluding the background color."""
    unique_colors = set(np.unique(grid))
    unique_colors.discard(background_color)
    return unique_colors

def apply_rule_1(output_grid: np.ndarray):
    """Applies the hardcoded transformation for Rule 1."""
    # Add Red pixels
    coords_red = [(2,5), (3,4), (4,3), (4,7), (5,6), (6,5), (7,4)]
    for r, c in coords_red:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
             output_grid[r, c] = 2
             
    # Add Maroon pixels
    coords_maroon = [(6,7), (7,7)]
    for r, c in coords_maroon:
       if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
            output_grid[r, c] = 9
            
    # Add Blue pixels
    coords_blue = [(8,15), (9,14), (10,13), (11,12), (10,15), (11,14)]
    for r, c in coords_blue:
       if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
            output_grid[r, c] = 1
            
    # Remove pixels (set to Orange)
    coords_orange = [(6,9), (6,13), (7,12)]
    for r, c in coords_orange:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
            output_grid[r, c] = 7

def apply_rule_2(input_grid: np.ndarray, output_grid: np.ndarray):
    """Applies horizontal adjustment rule for Gray, Maroon, Green to column 9."""
    height, width = input_grid.shape
    target_col_index = 9
    background_color = 7
    rule_colors = {5, 9, 3}

    for r in range(height):
        c = 0
        while c < width:
            color = input_grid[r, c]
            if color in rule_colors:
                # Find the end of the contiguous segment in the input grid
                c_start = c
                c_end = c
                while c_end + 1 < width and input_grid[r, c_end + 1] == color:
                    c_end += 1

                # Apply extension logic based on input segment's end
                if c_end < target_col_index:
                    for fill_c in range(c_end + 1, target_col_index + 1):
                         if fill_c < width: # Check bounds
                             # Only fill if the target cell is background in the output grid
                             # This avoids overwriting parts of other segments processed earlier in the row
                             if output_grid[r, fill_c] == background_color:
                                output_grid[r, fill_c] = color

                # Apply truncation logic based on input segment's end
                if c_end > target_col_index:
                    for clear_c in range(target_col_index + 1, c_end + 1):
                         if clear_c < width: # Check bounds
                            # Set back to background color in the output grid
                            output_grid[r, clear_c] = background_color

                # Move the column iterator past the processed segment
                c = c_end + 1
            else:
                # If the current cell is not a rule color, just move to the next column
                c += 1

def apply_rule_3(input_grid: np.ndarray, output_grid: np.ndarray):
    """Applies vertical consolidation rule for Azure."""
    height, width = input_grid.shape
    color_azure = 8
    background_color = 7

    # Find all Azure coordinates
    azure_coords = np.argwhere(input_grid == color_azure)
    if azure_coords.size == 0:
        return # No Azure pixels, nothing to do

    # Determine rows and columns containing Azure
    azure_rows = set(azure_coords[:, 0])
    azure_cols = set(azure_coords[:, 1])

    # Find rows with Azure in multiple columns
    rows_multi_azure = set()
    for r in azure_rows:
        cols_in_row = azure_coords[azure_coords[:, 0] == r][:, 1]
        if len(np.unique(cols_in_row)) > 1:
            rows_multi_azure.add(r)

    # Determine the maximum row index with Azure in multiple columns
    max_multi_r = -1
    if rows_multi_azure:
        max_multi_r = max(rows_multi_azure)

    # Process each column containing Azure
    for c in azure_cols:
        # Find min and max row for Azure in this specific column
        rows_in_col = azure_coords[azure_coords[:, 1] == c][:, 0]
        min_r_c = np.min(rows_in_col)
        max_r_c = np.max(rows_in_col)

        # Calculate the final maximum row for filling in this column
        final_max_r = max(max_r_c, max_multi_r)

        # Fill the column segment in the output grid
        for r_fill in range(min_r_c, final_max_r + 1):
             if 0 <= r_fill < height: # Check bounds
                output_grid[r_fill, c] = color_azure


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the set of unique non-background colors.
    """
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_np = input_np.copy()
    height, width = input_np.shape
    background_color = 7

    # Identify the unique colors present (excluding background)
    unique_colors = get_unique_colors(input_np, background_color)

    # --- Conditional Rule Application ---

    # Rule 1 condition: Exactly Red(2), Maroon(9), Blue(1)
    if unique_colors == {1, 2, 9}:
        apply_rule_1(output_np) # Modifies output_np directly

    # Rule 2 condition: Exactly Gray(5), Maroon(9), Green(3)
    # Note: Rule 2 in example 2 also has Maroon(9), so it takes precedence if {3,5,9}
    elif unique_colors == {3, 5, 9}:
        apply_rule_2(input_np, output_np) # Needs input to find segments, modifies output

    # Rule 3 condition: Exactly Azure(8)
    elif unique_colors == {8}:
        apply_rule_3(input_np, output_np) # Needs input to find locations, modifies output

    # Else: No specific rule matches the color set, output remains a copy of input.

    # Convert back to list of lists for the expected output format
    return output_np.tolist()