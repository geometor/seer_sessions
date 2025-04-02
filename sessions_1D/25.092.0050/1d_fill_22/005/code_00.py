import numpy as np

"""
Identifies the two non-white pixels (markers) in a 1xN input grid. 
If exactly two markers with the same color are found, it fills the 
segment of white pixels located strictly between these markers 
with the marker color. Otherwise, the original grid is returned.
"""

def find_markers_2d(grid_np):
    """
    Finds the column indices and color of the two non-white marker pixels in a 1xN grid.

    Args:
        grid_np (np.array): A 2D numpy array representing the input grid (expected shape 1xN).

    Returns:
        tuple: A tuple containing (min_col_index, max_col_index, color) if exactly two
               non-white pixels with the same color are found. 
               Otherwise, returns (None, None, None).
    """
    # Ensure the input is a 2D array with at least one row
    if grid_np.ndim != 2 or grid_np.shape[0] == 0:
        return None, None, None
        
    # Find row and column indices of all non-zero (non-white) pixels
    # Since we expect a 1xN grid, row_indices should all be 0.
    row_indices, col_indices = np.nonzero(grid_np)

    # Check if exactly two non-white pixels were found
    if len(col_indices) == 2:
        # Get the column indices
        c1 = col_indices[0]
        c2 = col_indices[1]
        
        # Determine the color from the first marker
        color1 = grid_np[0, c1]
        # Verify the color of the second marker
        color2 = grid_np[0, c2]

        # Check if colors are the same
        if color1 == color2:
            # Ensure min_c is the minimum and max_c is the maximum index
            min_c = min(c1, c2)
            max_c = max(c1, c2)
            return min_c, max_c, color1 # Return indices and the common color
        else:
            # Colors differ, rule doesn't apply
            return None, None, None
    else:
        # Handle cases with 0, 1, or more than 2 non-white pixels
        return None, None, None

def transform(input_grid):
    """
    Transforms the input 1xN grid by filling the gap between two marker pixels.

    Args:
        input_grid (list): A list of lists representing the 1xN input grid. 
                           Example: [[0, 0, 4, 0, 0, 4, 0]]

    Returns:
        list: A list of lists representing the transformed grid.
    """
    # Convert input list of lists to a numpy array
    grid_np = np.array(input_grid, dtype=int)

    # Check if input is valid (at least 1x1)
    if grid_np.size == 0 or grid_np.ndim != 2:
         return input_grid # Return original if invalid format

    # Find the marker pixels' column indices and color
    min_c, max_c, color = find_markers_2d(grid_np)

    # If markers weren't found according to the rule (exactly two non-white, same color),
    # return the original grid unchanged (as a list of lists).
    if min_c is None:
        return input_grid[:] # Return a copy of the original list

    # Create a copy of the grid to modify
    output_grid_np = grid_np.copy()

    # Fill the gap between the markers (exclusive of markers themselves)
    # The slice [0, min_c + 1 : max_c] selects row 0 and columns
    # from min_c + 1 up to (but not including) max_c.
    # Only fill if there is actually a gap (i.e., max_c > min_c + 1)
    if max_c > min_c + 1:
        output_grid_np[0, min_c + 1 : max_c] = color

    # Convert the modified numpy array back to a list of lists for the output
    return output_grid_np.tolist()