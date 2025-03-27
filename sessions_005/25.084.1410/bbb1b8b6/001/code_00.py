import numpy as np
from collections import Counter

"""
Transformation Rule Natural Language Description:

1.  Identify the vertical column consisting entirely of gray (5) pixels. This acts as a separator.
2.  Split the input grid into two subgrids based on this separator: the "left grid" (left of the separator) and the "right grid" (right of the separator).
3.  Find the single primary non-white color in the left grid (Color_L) and the single primary non-white color in the right grid (Color_R). Assume white (0) is the background and there's only one other significant color on each side for the core logic.
4.  Check for spatial overlap: Determine if there exists any coordinate (row, col) such that the pixel at `left_grid[row, col]` is Color_L AND the pixel at `right_grid[row, col]` is Color_R.
5.  Conditional Output Generation:
    a.  If an overlap is found (step 4 is true), the output grid is an exact copy of the left grid.
    b.  If no overlap is found (step 4 is false), create the output grid by starting with a copy of the left grid. Then, for every pixel position (row, col), if the pixel in the output grid is currently white (0) AND the corresponding pixel `right_grid[row, col]` is Color_R, update the output grid pixel at (row, col) to Color_R.
"""

def find_separator_column(grid):
    """Finds the index of the first column composed entirely of gray (5) pixels."""
    height, width = grid.shape
    for c in range(width):
        is_separator = True
        for r in range(height):
            if grid[r, c] != 5:
                is_separator = False
                break
        if is_separator:
            return c
    return -1 # Return -1 if no separator column is found

def find_primary_non_white_color(grid):
    """Finds the most frequent non-white color in the grid.
       Returns None if only white (0) is present or grid is empty."""
    if grid.size == 0:
        return None
        
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    # Remove white color (0) if present
    if 0 in color_counts:
        del color_counts[0]

    if not color_counts: # No non-white colors
        return None
    
    # Return the most frequent non-white color
    # If ties, it returns one of the most frequent ones. This matches the examples.
    primary_color = max(color_counts, key=color_counts.get)
    return primary_color


def transform(input_grid):
    """
    Transforms the input grid based on the presence or absence of overlap
    between non-white elements on either side of a gray separator column.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Find the separator column
    separator_col = find_separator_column(input_np)

    if separator_col == -1:
        # Handle error: No separator found. Based on task description,
        # this shouldn't happen for valid inputs. We might return input or raise error.
        # For now, let's assume valid inputs and return the input grid if separator not found.
        # Or perhaps return an empty grid of same shape? Let's try returning input.
        print("Warning: Separator column (color 5) not found.")
        return input_grid # Or raise ValueError("Separator column not found")

    # 2. Split the grid
    left_grid = input_np[:, :separator_col]
    # Ensure right_grid exists even if separator is the last column
    if separator_col + 1 < width:
        right_grid = input_np[:, separator_col + 1:]
    else:
        # Create an empty grid with same height if separator is last column
        right_grid = np.empty((height, 0), dtype=int) 

    # Check if left and right grids have compatible dimensions for comparison
    if left_grid.shape != right_grid.shape:
         # This case seems unlikely given the examples, but good to consider.
         # If dimensions mismatch, maybe default to copying left grid?
         # Let's assume dimensions will match based on the provided examples.
         # If they didn't match, the overlap check and fill logic would fail.
         # A robust solution might need padding or specific error handling.
         # For now, proceed assuming they match based on observed pattern.
         pass # Assume dimensions match for core logic


    # 3. Find primary non-white colors
    color_l = find_primary_non_white_color(left_grid)
    color_r = find_primary_non_white_color(right_grid)

    # Handle cases where one side might lack a non-white color (though not seen in examples)
    if color_l is None or color_r is None:
        # If either side lacks a primary non-white color, overlap is impossible by definition.
        # Follow the 'no overlap' rule, but filling might not happen if color_r is None.
        # If color_r is None, the fill step does nothing, effectively just copying left_grid.
        overlap_found = False
    else:
        # 4. Check for overlap
        overlap_found = False
        # Ensure grids are not empty before iterating
        if left_grid.size > 0 and right_grid.size > 0:
            rows, cols = left_grid.shape
            for r in range(rows):
                for c in range(cols):
                    if left_grid[r, c] == color_l and right_grid[r, c] == color_r:
                        overlap_found = True
                        break # Found overlap, no need to check further
                if overlap_found:
                    break

    # 5. Generate output based on overlap
    if overlap_found:
        # 5a. If overlap, output is the left grid
        output_grid = left_grid.copy()
    else:
        # 5b. If no overlap, copy left grid and conditionally fill with Color_R
        output_grid = left_grid.copy()
        # Only fill if color_r was found and grids aren't empty
        if color_r is not None and output_grid.size > 0 and right_grid.size > 0:
            rows, cols = output_grid.shape
            for r in range(rows):
                for c in range(cols):
                    # Check bounds for right_grid just in case of dimension mismatch, although assumed not to happen
                    if c < right_grid.shape[1]: 
                         if output_grid[r, c] == 0 and right_grid[r, c] == color_r:
                             output_grid[r, c] = color_r

    # Convert back to list of lists if necessary, though numpy array is often fine
    return output_grid.tolist()
