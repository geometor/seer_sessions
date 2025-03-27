```python
import numpy as np

"""
Simulates gravity on non-white, non-azure objects in a grid.
Objects are defined implicitly by pixels of colors 1-7 and 9.
These mobile pixels fall downwards through white space (color 0) 
until they are directly above a non-white pixel (any color 1-9, including 
the static azure color 8) or until they reach the bottom boundary of the grid. 
The azure (color 8) pixels are considered static and do not move.
The simulation continues iteratively until no more pixels can move downwards 
in a full pass over the grid.
"""

def transform(input_grid):
    """
    Applies gravity simulation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid after gravity simulation.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Create a copy to modify, representing the grid state during simulation
    output_grid = input_np.copy()
    
    # Define background color and static colors
    background_color = 0
    static_colors = {8} # Azure (8) is static

    # Iteratively simulate pixel falling until the grid stabilizes
    while True:
        moved = False # Flag to track if any pixel moved in the current pass
        
        # Iterate through the grid cells, starting from the second-to-last row and moving upwards.
        # This ensures that pixels lower down move first, creating space for pixels above them.
        # We iterate row by row from bottom (height-2) to top (0).
        for r in range(height - 2, -1, -1): 
            # Iterate through columns left to right
            for c in range(width):
                current_color = output_grid[r, c]

                # Check if the current pixel is mobile 
                # (i.e., not background and not a static color)
                if current_color != background_color and current_color not in static_colors:
                    
                    # Check if the cell directly below is empty (background color)
                    if output_grid[r + 1, c] == background_color:
                        # If empty, move the current pixel down
                        output_grid[r + 1, c] = current_color
                        output_grid[r, c] = background_color
                        # Mark that a movement occurred in this pass
                        moved = True 

        # If no pixels moved during a full pass over the grid, the simulation is stable
        if not moved:
            break

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()

```