```python
import numpy as np

"""
Transforms an input grid based on the following rule:
1. Create a copy of the input grid to serve as the output grid.
2. Iterate through each cell of the input grid.
3. If a cell contains a red pixel (color 2):
   a. Examine its 8 neighboring cells (Moore neighborhood) in the input grid.
   b. If a neighbor cell contains a green pixel (color 3), change the color 
      of the corresponding cell in the output grid to blue (color 1).
4. All other pixels (including red pixels and non-green neighbors of red pixels) 
   retain their original color in the output grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input_grid
    output_array = np.copy(input_array)
    
    rows, cols = input_array.shape

    # Define the 8 neighboring offsets (Moore neighborhood)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell contains a red pixel (color 2)
            if input_array[r, c] == 2:
                # Examine the 8 neighbors of the red pixel
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    
                    # Check if the neighbor coordinates are within the grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor cell in the *input* grid is green (color 3)
                        if input_array[nr, nc] == 3:
                            # Change the corresponding cell in the *output* grid to blue (color 1)
                            output_array[nr, nc] = 1

    # Convert the output NumPy array back to a list of lists before returning
    return output_array.tolist()
```