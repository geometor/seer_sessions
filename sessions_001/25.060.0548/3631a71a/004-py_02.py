"""
1.  **Identify:** Locate the large, contiguous block of maroon (9) pixels in the input grid.
2.  **Remove:** Delete all pixels belonging to this maroon block.
3. **Shift:** Blocks and partial blocks of the same color above the removed area are maintained at their relative locations, shifting downwards the correct number of spaces to recompact the space, only pixels that are above other pixels that are removed are shifted. All other pixels remain in their original locations.
"""

import numpy as np

def find_maroon_block(grid):
    # Find all maroon (9) pixels
    maroon_pixels = np.argwhere(grid == 9)
    if maroon_pixels.size == 0:
        return []

    # Start with the first maroon pixel
    start_pixel = tuple(maroon_pixels[0])
    block = set()
    queue = [start_pixel]

    while queue:
        current_pixel = queue.pop(0)
        if current_pixel in block:
            continue
        block.add(current_pixel)
        row, col = current_pixel

        # Check adjacent pixels (up, down, left, right)
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for r, c in neighbors:
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == 9 and (r, c) not in block:
                queue.append((r, c))

    return list(block)

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = input_grid.copy()

    # Find the maroon block
    maroon_block = find_maroon_block(output_grid)

    # Convert the block to a NumPy array for easier manipulation
    maroon_block_arr = np.array(maroon_block)
    
    # if there is no maroon block skip this step
    if len(maroon_block_arr) != 0:

        # Find the minimum and maximum row indices of the maroon block
        min_row = np.min(maroon_block_arr[:, 0])
        max_row = np.max(maroon_block_arr[:, 0])


        # Remove the maroon block
        for row, col in maroon_block:
            output_grid[row, col] = -1  # Mark as removed temporarily

        # Shift down pixels above the removed block
        for col in range(output_grid.shape[1]):
          empty_rows = []
          for row in range(output_grid.shape[0]):
            if output_grid[row, col] == -1:
              empty_rows.append(row)
            elif len(empty_rows) > 0:
              output_grid[empty_rows[0],col] = output_grid[row,col]
              output_grid[row,col] = -1
              empty_rows.pop(0)
              empty_rows.append(row)
    
    # remove the -1 markers
    output_grid[output_grid == -1] = 0

    return output_grid