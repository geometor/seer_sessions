```python
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing green pixels (3) to blue (1) if they are adjacent 
    (orthogonally or diagonally) to any red pixel (2). All other pixels retain their original color.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Define the relative coordinates for 8 neighbors (orthogonal and diagonal)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each pixel in the grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is green (3)
            if input_np[r, c] == 3:
                is_adjacent_to_red = False
                # Check all 8 neighbors
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are within the grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the *original* input grid is red (2)
                        if input_np[nr, nc] == 2:
                            is_adjacent_to_red = True
                            break  # Found a red neighbor, no need to check others

                # If an adjacent red pixel was found, change the current pixel to blue (1) in the output grid
                if is_adjacent_to_red:
                    output_np[r, c] = 1

    # Convert the output NumPy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid

```