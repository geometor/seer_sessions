import numpy as np
from typing import List, Tuple, Dict, Any

"""
The transformation identifies all 3x3 subgrids within the input grid that contain pixels of exactly one non-white color (along with potentially white pixels). Among these valid monochromatic 3x3 subgrids, the one whose non-white color has the highest numerical value is selected as the output. If multiple subgrids share the same highest color value, any one of them is a valid output. The output is always a 3x3 grid.
"""

def _check_subgrid(subgrid: np.ndarray) -> Tuple[bool, int]:
    """
    Checks if a 3x3 subgrid contains exactly one non-white color.

    Args:
        subgrid: A 3x3 numpy array representing the subgrid.

    Returns:
        A tuple (is_valid, color).
        is_valid is True if the subgrid contains exactly one non-white color, False otherwise.
        color is the non-white color value if is_valid is True, otherwise -1.
    """
    # Find all unique pixel values in the subgrid
    unique_colors = np.unique(subgrid)
    
    # Filter out the white color (0) to get unique non-white colors
    non_white_colors = unique_colors[unique_colors != 0]

    # Check if there is exactly one unique non-white color
    if len(non_white_colors) == 1:
        # Exactly one non-white color found
        return True, int(non_white_colors[0]) # Return the color value
    else:
        # Either zero or more than one non-white color
        return False, -1


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Finds the 3x3 monochromatic subgrid with the highest color value in the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the 3x3 output grid. Returns a 3x3 white grid
        if the input is smaller than 3x3 or if no valid monochromatic subgrid is found.
    """
    # Convert input list of lists to a NumPy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Check if the grid is large enough to contain a 3x3 subgrid
    if height < 3 or width < 3:
        # Return a default 3x3 white grid if input is too small
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Store valid subgrids found and their associated color
    valid_subgrids: List[Dict[str, Any]] = []
    # Keep track of the highest color value encountered in valid subgrids
    max_color_found = -1

    # Iterate through all possible center coordinates (r, c) for 3x3 subgrids.
    # The center can range from (1, 1) to (height-2, width-2).
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Extract the 3x3 subgrid centered at (r, c)
            # NumPy slicing: [start_row:end_row+1, start_col:end_col+1]
            subgrid = input_np[r-1 : r+2, c-1 : c+2]

            # Check if the extracted subgrid contains exactly one non-white color
            is_valid, color = _check_subgrid(subgrid)

            if is_valid:
                # If valid, store the subgrid (as numpy array) and its color
                valid_subgrids.append({'grid': subgrid, 'color': color})
                # Update the maximum color found so far among valid subgrids
                if color > max_color_found:
                    max_color_found = color

    # After checking all possible subgrids, find one that corresponds to the max_color_found
    result_grid_np = None
    if max_color_found != -1:  # Check if at least one valid subgrid was found
        for candidate in valid_subgrids:
            if candidate['color'] == max_color_found:
                # Select the first candidate found with the highest color
                result_grid_np = candidate['grid']
                break 

    # Handle the case where no valid monochromatic subgrid was found
    if result_grid_np is None:
        # Return a default 3x3 white grid as a fallback
        result_grid_np = np.zeros((3, 3), dtype=int)

    # Convert the selected NumPy array grid back to a list of lists for the final output
    return result_grid_np.tolist()