```python
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing cells with value 0 to 1 if they are
    horizontally or vertically adjacent to a cell with value 5. Cells with value
    5 remain unchanged. Cells with value 0 that are not adjacent to a 5 also
    remain unchanged.

    Args:
      input_grid (list of lists or numpy array): The input 2D grid containing 0s and 5s.

    Returns:
      numpy array: The transformed 2D grid containing 0s, 1s, and 5s.
    """

    # Convert input to numpy array for easier handling
    input_arr = np.array(input_grid)
    rows, cols = input_arr.shape

    # Initialize output_grid as a copy of the input grid
    # Use a copy to avoid modifying the input while iterating
    output_arr = np.copy(input_arr)

    # Define the relative coordinates for neighbors (up, down, left, right)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the input grid is 0
            if input_arr[r, c] == 0:
                # Check its neighbors
                is_neighbor_5 = False
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor is within grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor in the *input* grid is 5
                        if input_arr[nr, nc] == 5:
                            is_neighbor_5 = True
                            break # Found a neighbor 5, no need to check others

                # If any neighbor was 5, change the corresponding cell in the output grid to 1
                if is_neighbor_5:
                    output_arr[r, c] = 1
            # Cells with value 5 remain 5 (already handled by the initial copy)
            # Cells with value 0 not adjacent to 5 remain 0 (also handled by the initial copy)

    # Return the modified output grid
    return output_arr.tolist() # Convert back to list of lists if required by the environment

```