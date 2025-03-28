```python
import numpy as np

"""
Recolor each gray (5) pixel in the input grid. 
The replacement color is determined by scanning leftwards from the gray pixel's position within the same row.
The color of the first non-white (0) pixel encountered during this scan is used as the replacement color.
All other pixels retain their original color.
"""

def find_source_color_left(grid, r, c):
    """
    Scans leftward from position (r, c-1) in the grid to find the first non-white color.

    Args:
        grid (np.array): The input grid.
        r (int): The row index.
        c (int): The column index of the gray pixel.

    Returns:
        int: The color of the first non-white pixel found to the left,
             or potentially the original color at (r,c) if no non-white is found (though problem implies one exists).
             Returns -1 if scan goes out of bounds without finding a non-white pixel (edge case).
    """
    # Scan from the column immediately to the left towards the beginning of the row
    for scan_c in range(c - 1, -1, -1):
        color = grid[r, scan_c]
        # Check if the color is not white (0)
        if color != 0:
            return color
    # This case might occur if the gray pixel is in column 0 or only white is to its left.
    # Based on examples, a non-white source is always present.
    # If no non-white color is found, what should happen?
    # The examples imply a source always exists. Returning the original gray might be safest
    # if the assumption fails, but let's stick to the observed pattern for now.
    # Let's return an indicator like -1 if no source found, although the logic below assumes one is found.
    # Or, based on the examples, we could return grid[r,c] itself if no other source found.
    # Let's stick to the assumption derived from examples: a non-white color will be found.
    # If the loop finishes, it implies only white or out-of-bounds.
    # Based on problem constraints and examples, we assume a non-white source will be found.
    # If gray is in col 0, the loop won't even run. What happens then?
    # Example 1: azure/red are in col 0. Example 2: maroon/magenta/yellow are in col 0.
    # It seems the source can be in col 0 itself. Let's adjust the scan.
    # No, the rule says scan *leftward*. If gray is in col 1, we scan col 0. If gray is in col 0, scan left fails.
    # Re-evaluating: "Find the first cell encountered during this leftward scan whose color is *not* white (0)."
    # Let's assume the source color MUST be found. The examples support this.
    # If gray is in column 0, the loop range(c-1, -1, -1) is empty.
    # What if the non-white pixel *is* in column 0? The rule works if gray is in col > 0.
    # Let's trust the examples: gray pixels are never in column 0, and there's always a non-white pixel at or before the gray pixel's column.

    # If the loop completes without finding a non-white pixel (e.g., gray is in col 0 or only white is left)
    # This path *shouldn't* be reached based on observed examples.
    # If it were, returning the original gray color might be a fallback.
    # print(f"Warning: No non-white source found left of ({r}, {c}).")
    return grid[r, c] # Fallback to original color, though not expected.


def transform(input_grid):
    """
    Transforms the input grid by recoloring gray pixels based on the color
    of the nearest non-white pixel to their left in the same row.

    Args:
        input_grid (list or np.array): A 2D grid represented as a list of lists or numpy array.

    Returns:
        np.array: The transformed grid as a numpy array.
    """
    # Convert input to numpy array for easier handling
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(grid)
    height, width = grid.shape

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell is gray (5)
            if grid[r, c] == 5:
                # Find the source color by scanning leftward in the same row
                source_color = -1 # Initialize with a sentinel value
                for scan_c in range(c - 1, -1, -1):
                    color = grid[r, scan_c]
                    # Check if the color is not white (0)
                    if color != 0:
                        source_color = color
                        break # Found the first non-white color, stop scanning

                # Update the output grid cell with the found source color
                # Ensure a source color was actually found (as expected from examples)
                if source_color != -1:
                     output_grid[r, c] = source_color
                # else: # Handle unexpected case where no source color is found to the left
                     # Keep the original color (gray 5) in the output grid, as per the copy.
                     # print(f"Debug: No source color found for gray at ({r},{c}), keeping gray.")


    return output_grid.tolist() # Return as list of lists as per standard ARC format
```