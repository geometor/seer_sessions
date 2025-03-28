```python
import numpy as np

def find_bounding_box(grid):
    """
    Finds the coordinates of all non-background pixels and calculates their bounding box.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The color value representing the background (default is 0).

    Returns:
        tuple: (min_row, max_row, min_col, max_col) if non-background pixels exist,
               None otherwise.
    """
    non_background_pixels = np.argwhere(grid != 0)
    if non_background_pixels.size == 0:
        return None  # No non-background pixels found

    min_row = non_background_pixels[:, 0].min()
    max_row = non_background_pixels[:, 0].max()
    min_col = non_background_pixels[:, 1].min()
    max_col = non_background_pixels[:, 1].max()

    return min_row, max_row, min_col, max_col

def extract_subgrid(grid, min_row, max_row, min_col, max_col):
    """
    Extracts a subgrid defined by the bounding box coordinates.

    Args:
        grid (np.ndarray): The input grid.
        min_row (int): The minimum row index (inclusive).
        max_row (int): The maximum row index (inclusive).
        min_col (int): The minimum column index (inclusive).
        max_col (int): The maximum column index (inclusive).

    Returns:
        np.ndarray: The extracted subgrid.
    """
    # Numpy slicing is exclusive for the upper bound, so add 1
    return grid[min_row:max_row + 1, min_col:max_col + 1]

def transform(input_grid):
    """
    Extracts the smallest rectangular subgrid containing all non-white (0) pixels
    from the input grid.

    1. Scan the input grid to find all pixels that are not white (color value 0).
    2. Determine the minimum and maximum row indices among these non-white pixels.
    3. Determine the minimum and maximum column indices among these non-white pixels.
    4. These minimum/maximum row and column indices define the bounding box of the non-white object.
    5. Create a new grid (the output grid) by extracting the pixels from the input grid
       within the calculated bounding box (from min_row, min_col to max_row, max_col).
    """
    input_grid_np = np.array(input_grid)

    # Find the bounding box of the non-white object
    bounding_box = find_bounding_box(input_grid_np)

    # If no non-white pixels are found (edge case, though unlikely based on examples)
    if bounding_box is None:
        # Return an empty grid or handle as appropriate for the task specification
        # Based on examples, we expect an object, so extraction should work.
        # If this needs specific handling, adjust here. For now, assume it won't happen.
        return np.array([[]]) # Or perhaps return input_grid_np? Based on examples, we extract.

    min_row, max_row, min_col, max_col = bounding_box

    # Extract the subgrid corresponding to the bounding box
    output_grid = extract_subgrid(input_grid_np, min_row, max_row, min_col, max_col)

    return output_grid.tolist() # Convert back to list of lists if required by the environment
```