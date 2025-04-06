```python
"""
Creates a 15x15 output grid initialized with the background value 7.
Then, it places two copies of the input grid onto this output grid.
The first copy is placed starting at row 2, column 3 (0-based index) and overwrites 
the background unconditionally.
The second copy is placed starting at row 8, column 9 (0-based index). This second copy
only overwrites the existing values (background or first copy) if the corresponding 
pixel value in the input grid is NOT the background color (7).
Both copy operations are clipped to the 15x15 boundaries of the output grid.
"""

import numpy as np

def place_copy_unconditional(source_grid: np.ndarray, target_grid: np.ndarray, offset_row: int, offset_col: int):
    """
    Places a copy of the source_grid onto the target_grid unconditionally, clipping at boundaries.

    Args:
        source_grid: The numpy array to copy from.
        target_grid: The numpy array to copy to.
        offset_row: The starting row index in the target grid.
        offset_col: The starting column index in the target grid.
    """
    source_height, source_width = source_grid.shape
    target_height, target_width = target_grid.shape

    # Calculate the boundaries for placing the copy, ensuring clipping
    start_row = offset_row
    start_col = offset_col
    end_row = min(offset_row + source_height, target_height)
    end_col = min(offset_col + source_width, target_width)

    # Calculate the corresponding slice dimensions from the source grid
    source_slice_height = end_row - start_row
    source_slice_width = end_col - start_col

    # Perform the copy if the slice dimensions are valid
    if source_slice_height > 0 and source_slice_width > 0:
        target_grid[start_row:end_row, start_col:end_col] = source_grid[:source_slice_height, :source_slice_width]

def place_copy_conditional(source_grid: np.ndarray, target_grid: np.ndarray, offset_row: int, offset_col: int, background_color: int):
    """
    Places a copy of the source_grid onto the target_grid conditionally.
    A pixel is copied only if its value is not the background_color.
    Clipping at boundaries is applied.

    Args:
        source_grid: The numpy array to copy from.
        target_grid: The numpy array to copy to.
        offset_row: The starting row index in the target grid.
        offset_col: The starting column index in the target grid.
        background_color: The value to ignore during copying.
    """
    source_height, source_width = source_grid.shape
    target_height, target_width = target_grid.shape

    # Iterate through each pixel of the source grid
    for r in range(source_height):
        for c in range(source_width):
            source_value = source_grid[r, c]

            # Check if the source value is not the background color
            if source_value != background_color:
                # Calculate target coordinates
                target_r = offset_row + r
                target_c = offset_col + c

                # Check if the target coordinates are within the bounds of the target grid
                if 0 <= target_r < target_height and 0 <= target_c < target_width:
                    # Update the target grid pixel
                    target_grid[target_r, target_c] = source_value


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the specified rules.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the 15x15 transformed output grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)

    # Define output grid parameters
    output_height = 15
    output_width = 15
    background_color = 7

    # Initialize the 15x15 output grid with the background color
    output_grid = np.full((output_height, output_width), background_color, dtype=int)

    # Define offsets for the two copies
    offset1_row, offset1_col = 2, 3
    offset2_row, offset2_col = 8, 9

    # Place the first copy (unconditional)
    place_copy_unconditional(input_np, output_grid, offset1_row, offset1_col)

    # Place the second copy (conditional on source value not being background_color)
    place_copy_conditional(input_np, output_grid, offset2_row, offset2_col, background_color)

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```