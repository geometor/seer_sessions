import numpy as np

"""
Transforms an input grid based on direct pixel adjacency.

Rule:
1. Iterate through each pixel in the input grid.
2. If a pixel is green (3), check its orthogonal neighbors (up, down, left, right).
3. If any orthogonal neighbor of the green pixel is red (2) in the input grid, 
   change the corresponding pixel in the output grid to blue (1).
4. If a pixel is not green, or if it is green but has no red orthogonal neighbors, 
   it retains its original color from the input grid in the output grid.
"""

def transform(input_grid):
    """
    Applies the direct adjacency transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for efficient operations and indexing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize the output grid as a copy of the input grid.
    # We will modify this grid based on the rule.
    output_grid = np.copy(input_np)

    # Define orthogonal neighbor offsets.
    neighbor_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

    # Iterate through each pixel of the input grid.
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the *input* grid is green (3).
            if input_np[r, c] == 3:
                is_adjacent_to_red = False
                # Check each orthogonal neighbor.
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    
                    # Ensure the neighbor is within the grid boundaries.
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is red (2) in the *input* grid.
                        if input_np[nr, nc] == 2:
                            is_adjacent_to_red = True
                            # Found a red neighbor, no need to check others for this green pixel.
                            break 
                
                # If this green pixel was adjacent to a red one in the input:
                if is_adjacent_to_red:
                    # Change this pixel's color to blue (1) in the *output* grid.
                    output_grid[r, c] = 1
            
            # If the pixel was not green, or was green but not adjacent to red,
            # it keeps its original color because we started with a copy.

    # Convert the final numpy array back to a list of lists as required.
    return output_grid.tolist()