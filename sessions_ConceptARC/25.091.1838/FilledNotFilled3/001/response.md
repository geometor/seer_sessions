```python
import numpy as np

"""
Identify all 3x3 'plus' shapes in the input grid. A 'plus' shape is defined as 
a 3x3 area where the 8 outer pixels share one non-white color (frame_color) 
and the single central pixel has a different non-white color (center_color).

If exactly one 'plus' shape is found, the output is a 1x1 grid containing the 
center_color of that 'plus' shape.

If no 'plus' shapes are found, the output is a 2x2 grid filled with the 
white color (0).

The case of multiple 'plus' shapes is assumed not to occur based on the 
provided examples.
"""

def find_plus_shapes(grid_np):
    """
    Scans the grid for 3x3 'plus' shapes.

    Args:
        grid_np: A numpy array representing the input grid.

    Returns:
        A list containing the center colors of all found 'plus' shapes.
    """
    plus_center_colors = []
    rows, cols = grid_np.shape

    # Iterate through all possible top-left corners of a 3x3 subgrid
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Extract the 3x3 subgrid
            subgrid = grid_np[r:r+3, c:c+3]

            # Get the center pixel color and the top-left pixel color (potential frame color)
            center_color = subgrid[1, 1]
            frame_color_candidate = subgrid[0, 0]

            # Basic checks: center and frame must be non-white and different
            if center_color == 0 or frame_color_candidate == 0 or center_color == frame_color_candidate:
                continue

            # Check if all 8 border pixels match the frame_color_candidate
            is_plus = True
            for i in range(3):
                for j in range(3):
                    if i == 1 and j == 1:  # Skip the center pixel
                        continue
                    if subgrid[i, j] != frame_color_candidate:
                        is_plus = False
                        break
                if not is_plus:
                    break
            
            # If it matches the plus pattern, store the center color
            if is_plus:
                plus_center_colors.append(center_color)

    return plus_center_colors


def transform(input_grid):
    """
    Transforms the input grid based on the presence of a 'plus' shape.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input list of lists to a numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)

    # Find all 'plus' shapes and their center colors
    center_colors = find_plus_shapes(input_np)

    # Determine the output based on the number of plus shapes found
    if len(center_colors) == 1:
        # If exactly one plus shape is found, output is 1x1 with its center color
        output_grid = np.array([[center_colors[0]]], dtype=int)
    elif len(center_colors) == 0:
        # If no plus shapes are found, output is 2x2 white grid
        output_grid = np.zeros((2, 2), dtype=int)
    else:
        # Handle unexpected case of multiple plus shapes (defaulting to 2x2 white for now, as per examples)
        # Or raise an error, or implement alternative logic if required by future examples.
        # Based on the provided training examples, this case doesn't occur.
        # We default to the "no plus shape found" case.
        print(f"Warning: Found {len(center_colors)} plus shapes, expected 0 or 1. Defaulting to white 2x2 output.")
        output_grid = np.zeros((2, 2), dtype=int)

    # Convert the numpy array back to a list of lists for the final output format
    return output_grid.tolist()
```