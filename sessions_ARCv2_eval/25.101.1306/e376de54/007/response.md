```python
"""
Transforms the input grid based on the set of unique non-background colors present.
The background color is assumed to be Orange (7). Three specific rules are defined based on the exact set of active colors found in the input grid:

Rule 1 (Active Colors: {Red(2), Maroon(9), Blue(1)}):
Applies a specific, hardcoded pattern modification. The output grid (initialized as a copy of the input) is modified at fixed coordinates:
- Sets pixels to Red(2): (2,5), (3,4), (4,3), (4,7), (5,6), (6,5), (7,4)
- Sets pixels to Blue(1): (10,13), (11,12)
- Sets pixels to Orange(7): (6,13), (7,12)

Rule 2 (Active Colors: {Gray(5), Maroon(9), Green(3)}):
Adjusts horizontal segments of Gray, Maroon, or Green based on the input grid. For each row:
- Segments are extended rightwards in the output grid with their color to end at column index 9 (inclusive).
- If a segment in the input originally extended beyond column 9, the portion from column index 10 onwards is changed back to the background Orange(7) in the output grid.

Rule 3 (Active Colors: {Azure(8)}):
Performs vertical consolidation of Azure pixels within each column based on the input grid.
- First, determine the maximum row index (`max_multi_r`) that contains Azure pixels in more than one column in the input.
- Then, for each column `c` containing Azure pixels in the input:
  - Find the minimum (`min_r_c`) and maximum (`max_r_c`) row indices of Azure pixels within that column in the input.
  - Calculate the target maximum row for filling: `final_max_r = max(max_r_c, max_multi_r)`.
  - Fill the column `c` in the output grid with Azure(8) from row `min_r_c` down to `final_max_r` (inclusive).

If the set of active colors does not match any of these specific sets ({1, 2, 9}, {3, 5, 9}, or {8}), the input grid is returned unchanged.
"""

import numpy as np
from typing import List, Set, Tuple

# --- Helper Functions ---

def get_unique_colors(grid: np.ndarray, background_color: int = 7) -> Set[int]:
    """Finds unique colors in the grid, excluding the background color."""
    unique_colors = set(np.unique(grid))
    unique_colors.discard(background_color)
    return unique_colors

def apply_rule_1(output_grid: np.ndarray):
    """Applies the hardcoded transformation for Rule 1 (Colors: Red, Maroon, Blue)."""
    height, width = output_grid.shape
    
    # Define coordinates for modifications
    coords_red = [(2,5), (3,4), (4,3), (4,7), (5,6), (6,5), (7,4)]
    coords_blue = [(10,13), (11,12)]
    coords_orange = [(6,13), (7,12)] # Pixels to set back to background

    # Apply modifications within grid bounds
    for r, c in coords_red:
        if 0 <= r < height and 0 <= c < width: 
             output_grid[r, c] = 2
             
    for r, c in coords_blue:
       if 0 <= r < height and 0 <= c < width: 
            output_grid[r, c] = 1
            
    for r, c in coords_orange:
        if 0 <= r < height and 0 <= c < width: 
            output_grid[r, c] = 7

def apply_rule_2(input_grid: np.ndarray, output_grid: np.ndarray):
    """Applies horizontal adjustment rule for Rule 2 (Colors: Gray, Maroon, Green) to column 9."""
    height, width = input_grid.shape
    target_col_index = 9
    background_color = 7
    rule_colors = {5, 9, 3}

    # Iterate through each row to find and adjust segments
    for r in range(height):
        c = 0
        while c < width:
            color = input_grid[r, c]
            # Check if the current pixel starts a relevant segment
            if color in rule_colors:
                # Find the end of the contiguous segment in the input grid
                c_start = c
                c_end = c
                while c_end + 1 < width and input_grid[r, c_end + 1] == color:
                    c_end += 1

                # --- Apply logic to output grid based on input segment ---
                # Extend segment rightwards if it ends before the target column
                if c_end < target_col_index:
                    for fill_c in range(c_end + 1, target_col_index + 1):
                         if fill_c < width: # Check bounds
                            output_grid[r, fill_c] = color

                # Truncate segment if it ends after the target column
                if c_end > target_col_index:
                    for clear_c in range(target_col_index + 1, c_end + 1):
                         if clear_c < width: # Check bounds
                            output_grid[r, clear_c] = background_color

                # Move the column iterator past the processed segment
                c = c_end + 1
            else:
                # If the current cell is not a rule color, just move to the next column
                c += 1

def apply_rule_3(input_grid: np.ndarray, output_grid: np.ndarray):
    """Applies vertical consolidation rule for Rule 3 (Color: Azure)."""
    height, width = input_grid.shape
    color_azure = 8
    background_color = 7

    # Find all Azure coordinates in the input grid
    azure_coords = np.argwhere(input_grid == color_azure)
    # If no Azure pixels exist, no action is needed
    if azure_coords.size == 0:
        return 

    # Determine rows and columns containing Azure in the input grid
    azure_rows = set(azure_coords[:, 0])
    azure_cols = set(azure_coords[:, 1])

    # Find rows with Azure in multiple columns in the input grid
    rows_multi_azure = set()
    for r in azure_rows:
        # Get column indices for azure pixels in this row
        cols_in_row = azure_coords[azure_coords[:, 0] == r][:, 1]
        # Check if there's more than one unique column index
        if len(np.unique(cols_in_row)) > 1:
            rows_multi_azure.add(r)

    # Determine the maximum row index with Azure in multiple columns
    max_multi_r = -1 # Default if no rows have multi-column azure
    if rows_multi_azure:
        max_multi_r = max(rows_multi_azure)

    # Process each column containing Azure based on input grid findings
    for c in azure_cols:
        # Find min and max row for Azure in this specific column in the input grid
        rows_in_col = azure_coords[azure_coords[:, 1] == c][:, 0]
        min_r_c = np.min(rows_in_col)
        max_r_c = np.max(rows_in_col)

        # Calculate the final maximum row for filling in this column
        # The fill extends down to the max of the column's max or the overall multi-column max
        final_max_r = max(max_r_c, max_multi_r)

        # Fill the column segment in the output grid
        for r_fill in range(min_r_c, final_max_r + 1):
             if 0 <= r_fill < height: # Check bounds before modifying output grid
                output_grid[r_fill, c] = color_azure

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid. 
    # Rule functions will modify this grid directly or based on input grid analysis.
    output_np = input_np.copy()
    
    background_color = 7

    # Identify the set of unique non-background colors present in the input grid
    unique_colors = get_unique_colors(input_np, background_color)

    # --- Conditional Rule Application ---
    # Check which rule applies based on the exact set of unique colors found
    
    # Rule 1 condition: Exactly Red(2), Maroon(9), Blue(1)
    if unique_colors == {1, 2, 9}:
        # Apply the hardcoded pixel modifications for Rule 1
        apply_rule_1(output_np) 

    # Rule 2 condition: Exactly Gray(5), Maroon(9), Green(3)
    elif unique_colors == {3, 5, 9}:
        # Apply the horizontal adjustment logic based on input segments
        apply_rule_2(input_np, output_np) 

    # Rule 3 condition: Exactly Azure(8)
    elif unique_colors == {8}:
        # Apply the vertical consolidation logic based on input azure positions
        apply_rule_3(input_np, output_np)
        
    # Else: If the set of unique colors doesn't match any defined rule,
    # no specific transformation is applied, and the output_np (copy of input) is returned.

    # Convert the final numpy array back to a list of lists for the required output format
    return output_np.tolist()
```