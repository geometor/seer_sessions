```python
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    - Find all green pixels (value 3).
    - For each green pixel, check its 8 neighbors (orthogonal and diagonal).
    - If any neighbor is a red pixel (value 2), change the green pixel to blue (value 1) in the output grid.
    - All other pixels (including red pixels and green pixels not adjacent to red) retain their original color.
    The checks are performed on the original input grid, and modifications are made to a separate output grid.
    """
    # Convert input list of lists to a NumPy array for easier indexing and operations
    input_np = np.array(input_grid, dtype=int)
    # Create a copy of the input array to store the output. This ensures original values are preserved for checking neighbors.
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
            # Check if the current pixel in the *original* input is green (3)
            if input_np[r, c] == 3:
                # Assume initially that it's not adjacent to red
                is_adjacent_to_red = False
                # Check all 8 neighbors in the *original* input grid
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are within the grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the *original* input grid is red (2)
                        if input_np[nr, nc] == 2:
                            is_adjacent_to_red = True
                            # Found a red neighbor, no need to check further for this pixel
                            break 
                
                # If a red neighbor was found, change the corresponding pixel in the *output* grid to blue (1)
                if is_adjacent_to_red:
                    output_np[r, c] = 1
            
            # If the pixel is not green, or if it's green but not adjacent to red, 
            # it retains its original value in the output_np (because output_np started as a copy)

    # Convert the output NumPy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid
```