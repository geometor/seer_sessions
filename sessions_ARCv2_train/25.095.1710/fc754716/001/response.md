```python
"""
Generates an output grid of the same dimensions as the input grid.
The output grid has a frame (outermost border) filled with the single non-zero 
value found in the input grid. All interior cells of the output grid are 0.
"""

import numpy as np

def find_frame_color(grid: list[list[int]]) -> int:
    """
    Finds the single non-zero value in the grid.
    Assumes there is exactly one non-zero value.
    """
    for row in grid:
        for cell in row:
            if cell != 0:
                return cell
    return 0 # Should not happen based on problem description, but good practice

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by creating a frame with the non-zero color.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Get grid dimensions
    height, width = input_array.shape

    # Find the non-zero color value from the input grid
    frame_color = find_frame_color(input_grid)

    # Initialize the output grid with zeros
    output_array = np.zeros_like(input_array)

    # Fill the top border
    output_array[0, :] = frame_color

    # Fill the bottom border
    output_array[height - 1, :] = frame_color

    # Fill the left border (excluding corners already filled)
    output_array[1:height - 1, 0] = frame_color

    # Fill the right border (excluding corners already filled)
    output_array[1:height - 1, width - 1] = frame_color

    # Convert the result back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```