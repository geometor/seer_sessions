```python
"""
Identifies a solid white rectangular block (color 0) and another solid
rectangular block of the exact same dimensions containing no white pixels.
Copies the pattern from the second block onto the location of the white
block in the output grid. The rest of the grid remains unchanged.
"""

import numpy as np

def find_solid_rect_block(grid, color):
    """
    Finds the bounding box of a single solid rectangular block of a given color.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the block to find.

    Returns:
        tuple: (row, col, height, width) of the block, or None if not found
               or if the pixels of the specified color do not form a single
               solid rectangle.
    """
    rows, cols = grid.shape
    # Find all coordinates where the grid matches the specified color
    coords = np.argwhere(grid == color)

    if coords.shape[0] == 0:
        # No pixels of the target color found
        return None

    # Determine the bounding box of these pixels
    min_r, min_c = coords.min(axis=0)
    max_r, max_c = coords.max(axis=0)

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Check 1: Does the number of found pixels match the bounding box area?
    # This verifies that the shape is rectangular and has no holes.
    if coords.shape[0] != height * width:
        # If not, it's not a single solid rectangle (e.g., L-shape, hollow, multiple blocks)
        return None

    # Check 2: Is the block defined by the bounding box entirely the target color?
    # This confirms that the bounding box doesn't encompass other colors, which can
    # happen if the np.argwhere coordinates were misleading (though check 1 makes this less likely).
    block = grid[min_r:min_r + height, min_c:min_c + width]
    if np.all(block == color):
        # If all checks pass, return the location and dimensions
        return min_r, min_c, height, width
    else:
        # If the block within the bounding box isn't solid color, something is wrong.
        return None


def find_matching_pattern_block(grid, target_height, target_width, white_bbox):
    """
    Finds a solid block with target dimensions that does not contain white (0)
    and is not the white block itself. Assumes the pattern block is also solid.

    Args:
        grid (np.array): The input grid.
        target_height (int): The height of the block to find.
        target_width (int): The width of the block to find.
        white_bbox (tuple): The (row, col, height, width) of the white block
                             to avoid matching the same block location.

    Returns:
        tuple: (row, col, height, width) of the pattern block, or None if not found.
    """
    rows, cols = grid.shape
    white_r, white_c, _, _ = white_bbox # Unpack to check against white block location

    # Iterate through all possible top-left corners for a block of the target size
    for r in range(rows - target_height + 1):
        for c in range(cols - target_width + 1):
            # Check if this candidate block is at the same location as the white block
            if r == white_r and c == white_c:
                 continue # Skip the white block location

            # Extract the candidate block region
            candidate_block = grid[r:r + target_height, c:c + target_width]

            # Check if the candidate block contains any white pixels (color 0)
            if np.any(candidate_block == 0):
                continue # Skip if it contains white

            # If we reach here, the block has the right dimensions,
            # is not at the white block's location, and contains no white pixels.
            # We assume based on the problem description that this is the pattern block.
            return r, c, target_height, target_width # Return its location and dimensions

    return None # No matching pattern block found


def transform(input_grid):
    """
    Transforms the input grid by finding a white rectangular block and a
    pattern block of the same dimensions (without white pixels), then copying
    the pattern onto the location of the white block.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Create a copy of the input array to modify, preserving the original
    output_grid = np.copy(input_array)

    # 1. Find the solid white rectangular block (color 0) in the input grid
    white_bbox = find_solid_rect_block(input_array, 0)

    # Handle case where no suitable white block is found
    if white_bbox is None:
        # Based on ARC task structure, examples usually guarantee requirements are met.
        # If not found, it might indicate a misunderstanding of the task.
        # Returning the original grid is a safe fallback.
        # print("Warning: No solid white block found.")
        return input_grid # Return original list of lists

    # Extract dimensions and location of the white block
    white_r, white_c, white_h, white_w = white_bbox
    # print(f"Found white block at ({white_r}, {white_c}), size {white_h}x{white_w}")

    # 2. Find the corresponding pattern block in the input grid:
    #    - Same dimensions as the white block (white_h, white_w)
    #    - Does not contain any white pixels (color 0)
    #    - Is not the white block itself (using white_bbox for comparison)
    pattern_bbox = find_matching_pattern_block(input_array, white_h, white_w, white_bbox)

    # Handle case where no suitable pattern block is found
    if pattern_bbox is None:
        # print("Warning: No matching pattern block found.")
        return input_grid # Return original list of lists

    # Extract location and dimensions (h/w should match white block)
    pattern_r, pattern_c, pattern_h, pattern_w = pattern_bbox
    # print(f"Found pattern block at ({pattern_r}, {pattern_c}), size {pattern_h}x{pattern_w}")

    # 3. Extract the actual pattern data from the input grid using the pattern block's coordinates
    pattern_data = input_array[pattern_r : pattern_r + pattern_h,
                               pattern_c : pattern_c + pattern_w]

    # 4. Copy (paste) the extracted pattern data onto the location of the white block
    #    in the output grid.
    output_grid[white_r : white_r + white_h,
                white_c : white_c + white_w] = pattern_data

    # Convert the modified numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
```