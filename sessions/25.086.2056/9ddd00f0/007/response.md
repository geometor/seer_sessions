```python
import numpy as np

"""
Transforms the input grid based on the vertical position of its non-background (non-white) pixels.

1. Analyze the Input Grid: Check if the input grid contains any non-background pixels (pixels with value != 0).
   - If no non-background pixels exist, return the input grid unchanged.
2. Identify Pattern Position: Determine the minimum row index (`min_r`) containing any non-background pixel.
3. Apply Conditional Transformation:
   - Case 1: Pattern touches the top edge (`min_r == 0`): Return the input grid unchanged.
   - Case 2: Pattern does not touch the top edge (`min_r > 0`):
     a. Find the maximum row index (`max_r`) containing a non-background pixel.
     b. Calculate the height of the pattern's row span: `block_height = max_r - min_r + 1`.
     c. Extract the rectangular block of rows from the input grid spanning `min_r` to `max_r` (inclusive) across the full grid width.
     d. Create a new block by vertically flipping the extracted block.
     e. Create the output grid as a copy of the input grid.
     f. Determine the number of rows to overwrite at the top: `rows_to_overwrite = min(block_height, grid_height)`.
     g. Replace the content of the output grid from row 0 up to (but not including) `rows_to_overwrite` with the corresponding top rows of the flipped block.
4. Return the Output Grid: Return the resulting transformed grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    background_pixel = 0

    # 1. Analyze the Input Grid: Find indices of non-background pixels
    non_bg_coords = np.argwhere(grid != background_pixel)

    # Handle case where grid is all background
    if non_bg_coords.size == 0:
        return input_grid # Return original grid unchanged

    # 2. Identify Pattern Position (minimum row index)
    min_r = non_bg_coords[:, 0].min()

    # 3. Apply Conditional Transformation

    # Case 1: Pattern touches the top edge (min_r == 0)
    if min_r == 0:
        # Return the input grid unchanged
        output_grid = grid

    # Case 2: Pattern does not touch the top edge (min_r > 0)
    else:
        # a. Find maximum row index
        max_r = non_bg_coords[:, 0].max()

        # b. Calculate row span height
        block_height = max_r - min_r + 1

        # c. Extract the block of rows containing the pattern (full width)
        pattern_block = grid[min_r : max_r + 1, :]

        # d. Vertically flip the extracted block
        reversed_block = np.flipud(pattern_block)

        # e. Create output grid as a copy of the input
        output_grid = grid.copy()

        # f. Determine the number of rows to overwrite at the top
        rows_to_overwrite = min(block_height, height)

        # g. Replace the top 'rows_to_overwrite' rows with the flipped block
        # Ensure the source slice matches the destination slice size
        output_grid[0:rows_to_overwrite, :] = reversed_block[0:rows_to_overwrite, :]

    # 4. Return the Output Grid
    # Convert back to list of lists as required by the ARC format
    return output_grid.tolist()
```