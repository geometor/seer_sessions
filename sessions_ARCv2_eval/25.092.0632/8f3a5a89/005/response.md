```python
import numpy as np

"""
Transforms an input grid based on the direct adjacency of gray pixels to blue pixels.

1. Creates an output grid initialized as a copy of the input grid. This ensures 
   non-gray pixels (blue=1, magenta=6) are preserved in their original positions.
2. Iterates through each pixel of the input grid.
3. If the input pixel at position (r, c) is gray (8):
    a. Checks its 8 adjacent neighbors (including diagonals) in the *input* grid.
    b. If any of these neighbors is blue (1), the corresponding pixel at (r, c) 
       in the *output* grid is set to orange (7).
    c. If none of the neighbors are blue, the pixel at (r, c) in the output 
       grid remains gray (8) (as it was initialized).
4. If the input pixel is not gray, its value in the output grid remains unchanged 
   from the initial copy.
5. Returns the transformed output grid.
"""

def transform(input_grid):
    """
    Applies the adjacency transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize the output grid as a copy of the input grid.
    # This handles the preservation of non-gray pixels (1 and 6).
    output_array = np.copy(input_array)

    # Define relative coordinates for the 8 neighbors (including diagonals)
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the *input* grid is gray (8)
            if input_array[r, c] == 8:
                found_blue_neighbor = False
                # Examine the 8 neighbors in the *input* grid
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the *input* grid is blue (1)
                        if input_array[nr, nc] == 1:
                            found_blue_neighbor = True
                            break # Stop checking neighbors once a blue one is found

                # If a blue neighbor was found in the input grid, 
                # change the corresponding pixel in the *output* grid to orange (7)
                if found_blue_neighbor:
                    output_array[r, c] = 7
                # Otherwise, the output pixel remains gray (8), which is already set by the initial copy.

    # Convert the result back to a list of lists for the standard ARC format
    return output_array.tolist()
```