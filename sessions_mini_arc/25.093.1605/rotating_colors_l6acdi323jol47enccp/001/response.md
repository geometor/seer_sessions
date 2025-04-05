```python
import numpy as np

"""
Rotate non-zero digits clockwise within concentric layers of a 2D grid.
For each layer, identify the non-zero elements. The value for each non-zero
position in the output grid is taken from the next non-zero position clockwise
in the input grid within that same layer. Zeroes remain stationary unless
overwritten by a moving non-zero digit.
"""

def get_layer_coords(layer_index, grid_size):
    """
    Generates the coordinates of a specific concentric layer in clockwise order.

    Args:
        layer_index: The index of the layer (0 for outermost).
        grid_size: The dimension of the square grid (N).

    Returns:
        A list of (row, col) tuples representing the coordinates of the layer.
    """
    coords = []
    min_idx = layer_index
    max_idx = grid_size - 1 - layer_index

    # Handle the center element for odd-sized grids
    if min_idx == max_idx:
        return [(min_idx, min_idx)]

    # Top row (left to right, excluding last element)
    for c in range(min_idx, max_idx):
        coords.append((min_idx, c))
    # Right column (top to bottom, excluding last element)
    for r in range(min_idx, max_idx):
        coords.append((r, max_idx))
    # Bottom row (right to left, excluding last element)
    for c in range(max_idx, min_idx, -1):
        coords.append((max_idx, c))
    # Left column (bottom to top, excluding last element)
    for r in range(max_idx, min_idx, -1):
        coords.append((r, min_idx))

    return coords

def transform(input_grid):
    """
    Applies the clockwise rotation of non-zero digits within concentric layers.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid)
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)
    grid_size = input_np.shape[0]

    # Determine the number of layers
    num_layers = (grid_size + 1) // 2

    # Iterate through each layer
    for l in range(num_layers):
        # Get the coordinates for the current layer
        layer_coords = get_layer_coords(l, grid_size)

        # Extract non-zero elements (value and original coordinate) from this layer
        non_zero_elements = []
        for r, c in layer_coords:
            value = input_np[r, c]
            if value != 0:
                non_zero_elements.append(((r, c), value))

        # If there are 2 or more non-zero elements, perform the rotation
        num_non_zero = len(non_zero_elements)
        if num_non_zero > 1:
            # Iterate through the non-zero elements found
            for i in range(num_non_zero):
                # Get the coordinate where the rotated value should be placed (target)
                target_coord, _ = non_zero_elements[i]

                # Determine the index of the element whose value will move here (source)
                # This is the *next* non-zero element clockwise in the input
                source_index = (i + 1) % num_non_zero
                _, source_value = non_zero_elements[source_index]

                # Place the source value at the target coordinate in the output grid
                output_np[target_coord[0], target_coord[1]] = source_value

    # Convert the numpy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid
```