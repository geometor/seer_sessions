```python
"""
In a single-row grid (1xN), identify the first contiguous horizontal block of a single color (not white 0 or gray 5) and the first gray pixel (5) that appears after it. Fill all pixels in the gap between the end of the colored block and the gray pixel with the color of the block.
"""

import numpy as np

def find_colored_block_info(grid: np.ndarray) -> tuple[int | None, int | None, int | None]:
    """
    Finds the first contiguous block of a single color other than white (0) or gray (5) in a 1xN grid.

    Args:
        grid: A 1xN numpy array representing the input grid row.

    Returns:
        A tuple containing (block_color, start_col, end_col) of the block,
        or (None, None, None) if no such block is found.
    """
    rows, cols = grid.shape
    if rows != 1:
        # This function assumes a single row grid
        return None, None, None

    start_col = -1
    block_color = -1
    
    for c in range(cols):
        pixel = grid[0, c]
        
        # Start of a potential block
        if start_col == -1 and pixel != 0 and pixel != 5:
            start_col = c
            block_color = pixel
        # Continuation of the current block
        elif start_col != -1 and pixel == block_color:
            continue
        # End of the block (found white, gray, or different color)
        elif start_col != -1:
             return block_color, start_col, c - 1

    # If the block extends to the very end of the grid
    if start_col != -1:
        return block_color, start_col, cols - 1
        
    # No block found at all
    return None, None, None

def find_gray_pixel_col(grid: np.ndarray, start_search_col: int = 0) -> int | None:
    """
    Finds the column index of the first gray (5) pixel in a 1xN grid,
    starting the search from a specific column.

    Args:
        grid: A 1xN numpy array representing the input grid row.
        start_search_col: The column index to start searching from (inclusive).

    Returns:
        The column index of the gray pixel, or None if not found.
    """
    rows, cols = grid.shape
    if rows != 1:
        return None
        
    for c in range(start_search_col, cols):
        if grid[0, c] == 5:
            return c
    return None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid (1xN numpy array).

    Args:
        input_grid: A 1xN numpy array representing the input sequence.

    Returns:
        A 1xN numpy array representing the transformed output sequence.
    """
    # Check if the input is a 1xN grid, otherwise return a copy
    if len(input_grid.shape) != 2 or input_grid.shape[0] != 1:
        print("Warning: Input grid is not 1xN. Returning copy.")
        return input_grid.copy()
        
    # Initialize output_grid as a copy of the input
    output_grid = input_grid.copy()

    # Find the main colored block
    block_color, _, block_end_col = find_colored_block_info(output_grid)

    # If no colored block is found, return the original grid
    if block_color is None:
        return output_grid

    # Find the gray pixel, starting search after the block ends
    # (or from beginning if block doesn't exist, though handled above)
    search_start = block_end_col + 1 if block_end_col is not None else 0
    gray_col = find_gray_pixel_col(output_grid, start_search_col=search_start)

    # If no gray pixel is found *after* the block, return the original grid
    if gray_col is None:
        # We might need to search the whole grid if the gray pixel could be before the block
        # Re-search from the beginning if the first search failed
        gray_col_anywhere = find_gray_pixel_col(output_grid, start_search_col=0)
        if gray_col_anywhere is None or gray_col_anywhere <= block_end_col:
             return output_grid # No gray pixel at all, or it's not after the block
        else:
            gray_col = gray_col_anywhere # Found gray pixel, but it wasn't found initially starting after block_end_col (this case shouldn't happen based on logic but adding robustness)


    # Ensure the gray pixel is strictly after the block end (redundant check given search logic, but safe)
    if block_end_col is None or gray_col <= block_end_col:
        return output_grid # Invalid configuration or block not found

    # Iterate through the columns in the gap and change pixels to the block color
    # Gap is from block_end_col + 1 up to (but not including) gray_col
    for c in range(block_end_col + 1, gray_col):
        output_grid[0, c] = block_color

    return output_grid
```