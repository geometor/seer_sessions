import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule:
Locates the unique pair of Red (2) and Yellow (4) pixels that are adjacent 
(including diagonals). If no such pair exists, the input is returned unchanged.
Identifies the columns containing the Red pixel (x_red) and the Yellow pixel 
(x_yellow).
Determines a 'stop row' by finding the first row below the lower of the two 
trigger pixels (max(y_red, y_yellow)) where a non-background (Azure 8) pixel 
exists in either the x_red or x_yellow column. If no such pixel exists, the 
stop row is the grid height.
If the Red and Yellow pixels are in the same column (x_red == x_yellow):
    - If the Red pixel is below the Yellow pixel (y_red > y_yellow), fill the 
      column from row 0 up to (but not including) the stop row with an 
      alternating pattern starting with Red (2) and then Yellow (4).
    - Otherwise (Red is above or same row as Yellow), fill the column with an 
      alternating pattern starting with Yellow (4) and then Red (2).
If the Red and Yellow pixels are in different columns (x_red != x_yellow):
    - Fill the x_red column from row 0 up to (but not including) the stop row 
      with solid Red (2).
    - Fill the x_yellow column from row 0 up to (but not including) the stop row 
      with solid Yellow (4).
All other pixels remain unchanged.
"""

def _find_adjacent_pair(grid: np.ndarray, color1: int, color2: int) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Finds the coordinates of the first adjacent pair of color1 and color2.
    Assumes a unique pair exists based on the task examples.

    Args:
        grid: The input grid as a numpy array.
        color1: The first color to search for.
        color2: The second color to search for.

    Returns:
        A tuple containing two tuples: ((r1, c1), (r2, c2)), or None if no
        adjacent pair is found.
    """
    locs1 = np.argwhere(grid == color1)
    locs2 = np.argwhere(grid == color2)

    for r1, c1 in locs1:
        for r2, c2 in locs2:
            # Check for 8-connectivity adjacency
            if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
                # Return the coordinates in a consistent order (color1, color2)
                return (int(r1), int(c1)), (int(r2), int(c2))
    return None

def _find_stop_row(grid: np.ndarray, y_red: int, x_red: int, y_yellow: int, x_yellow: int, background_color: int) -> int:
    """
    Finds the row index where the vertical pattern should stop.

    Args:
        grid: The input grid as a numpy array.
        y_red: Row index of the red pixel.
        x_red: Column index of the red pixel.
        y_yellow: Row index of the yellow pixel.
        x_yellow: Column index of the yellow pixel.
        background_color: The color considered as background (8).

    Returns:
        The row index (exclusive) where the pattern stops.
    """
    height = grid.shape[0]
    start_check_row = max(y_red, y_yellow) + 1
    stop_row = height # Default to grid height

    for r in range(start_check_row, height):
        stop_found = False
        # Check red column
        if grid[r, x_red] != background_color:
            stop_found = True
        # Check yellow column (if different)
        if x_red != x_yellow and grid[r, x_yellow] != background_color:
            stop_found = True

        if stop_found:
            stop_row = r
            break
    return stop_row

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on an adjacent Red(2) and Yellow(4) pair.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape
    background_color = 8
    red_color = 2
    yellow_color = 4

    # --- Find the adjacent Red and Yellow pair ---
    pair_coords = _find_adjacent_pair(grid, red_color, yellow_color)

    # --- If no adjacent pair found, return the original grid ---
    if pair_coords is None:
        return input_grid

    (y_red, x_red), (y_yellow, x_yellow) = pair_coords

    # --- Determine the stop row for the pattern ---
    stop_row = _find_stop_row(grid, y_red, x_red, y_yellow, x_yellow, background_color)

    # --- Apply the modification based on whether columns are the same ---
    if x_red == x_yellow:
        # Case 1: Same column - Apply alternating pattern
        target_col = x_red
        # Determine starting color based on vertical position
        if y_red > y_yellow:
            start_color = red_color
            alt_color = yellow_color
        else:
            start_color = yellow_color
            alt_color = red_color

        # Apply the alternating pattern
        for r in range(stop_row):
            if r % 2 == 0: # Even rows
                output_grid[r, target_col] = start_color
            else: # Odd rows
                output_grid[r, target_col] = alt_color
    else:
        # Case 2: Different columns - Apply solid colors
        # Fill red column
        for r in range(stop_row):
            output_grid[r, x_red] = red_color
        # Fill yellow column
        for r in range(stop_row):
            output_grid[r, x_yellow] = yellow_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()