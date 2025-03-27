"""
Iterate through each pixel of the input grid. If a pixel is white (0) and has 
at least one yellow (4) neighbor (including diagonals), change its color to 
green (3) in the corresponding position in the output grid. Otherwise, the 
pixel retains its original color in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the rule: white pixels adjacent to yellow 
    pixels become green.
    
    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize the output grid as a copy of the input grid
    # We will modify this grid based on the rules
    output_array = np.copy(input_array)

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is white (0)
            if input_array[r, c] == 0:
                # Check its neighbors (Moore neighborhood: 8 surrounding cells)
                has_yellow_neighbor = False
                # Define the neighborhood boundaries, ensuring they stay within the grid
                for dr in range(max(0, r - 1), min(rows, r + 2)):
                    for dc in range(max(0, c - 1), min(cols, c + 2)):
                        # Skip the cell itself
                        if dr == r and dc == c:
                            continue
                        
                        # Check if the neighbor is yellow (4)
                        if input_array[dr, dc] == 4:
                            has_yellow_neighbor = True
                            break  # Found a yellow neighbor, no need to check further
                    if has_yellow_neighbor:
                        break # Break outer loop as well
                
                # If a yellow neighbor was found, change the output cell to green (3)
                if has_yellow_neighbor:
                    output_array[r, c] = 3
            # If the cell is not white, it retains its original color (already copied)

    # Convert the output NumPy array back to a list of lists before returning
    return output_array.tolist()
