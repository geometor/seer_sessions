"""
The transformation summarizes a 5x7 input grid into a 3x3 output grid.
It identifies the single non-white foreground color (C) in the input.
The 5x7 input grid is conceptually divided into 9 spatial zones, corresponding to the 9 cells of the 3x3 output grid.
These zones cover the corners, edges (excluding corners), and the central area of the input.
For each zone, the transformation checks if any pixel within that zone in the input grid has the foreground color C.
If the foreground color C is present in a zone, the corresponding cell in the 3x3 output grid is set to C.
Otherwise, the corresponding output cell remains white (0).
"""

import numpy as np

def find_foreground_color(grid: np.ndarray) -> int:
    """Finds the first non-zero color value in the grid."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                return grid[r, c]
    return 0 # Should not happen based on task description, but default to white

def check_zone_for_color(grid: np.ndarray, zone_slice: tuple, color: int) -> bool:
    """Checks if the specified color exists within the given zone slice of the grid."""
    return np.any(grid[zone_slice] == color)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 5x7 input grid to a 3x3 output grid by checking for the 
    presence of the foreground color in 9 defined spatial zones.
    """
    # Convert input list of lists to a NumPy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    
    # Verify input dimensions (optional but good practice for fixed size)
    if input_np.shape != (5, 7):
        raise ValueError("Input grid must be 5x7")

    # Initialize the 3x3 output grid with white (0)
    output_np = np.zeros((3, 3), dtype=int)

    # Identify the non-white foreground color (C)
    foreground_color = find_foreground_color(input_np)
    
    # If no foreground color is found (all white input), return the all-white output
    if foreground_color == 0:
         return output_np.tolist()

    # Define the zones as slices and map them to output coordinates
    # Each tuple contains: (output_row, output_col, input_zone_slice)
    zone_definitions = [
        (0, 0, np.s_[0, 0]),        # Top-Left Corner -> Output[0,0]
        (0, 1, np.s_[0, 1:6]),      # Top Edge -> Output[0,1]
        (0, 2, np.s_[0, 6]),        # Top-Right Corner -> Output[0,2]
        (1, 0, np.s_[1:4, 0]),      # Left Edge -> Output[1,0]
        (1, 1, np.s_[1:4, 1:6]),    # Center -> Output[1,1]
        (1, 2, np.s_[1:4, 6]),      # Right Edge -> Output[1,2]
        (2, 0, np.s_[4, 0]),        # Bottom-Left Corner -> Output[2,0]
        (2, 1, np.s_[4, 1:6]),      # Bottom Edge -> Output[2,1]
        (2, 2, np.s_[4, 6]),        # Bottom-Right Corner -> Output[2,2]
    ]

    # Iterate through each zone definition
    for r_out, c_out, zone_slice in zone_definitions:
        # Check if the foreground color exists in the current input zone
        if check_zone_for_color(input_np, zone_slice, foreground_color):
            # If yes, set the corresponding output cell to the foreground color
            output_np[r_out, c_out] = foreground_color
            
    # Convert the output NumPy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid