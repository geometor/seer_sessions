```python
"""
Identifies a rectangular block of white pixels (color 0) and another rectangular
block of the exact same dimensions containing a pattern (no white pixels).
Copies the pattern from the second block onto the location of the white block
in the output grid. The rest of the grid remains unchanged.
"""

import numpy as np

def find_solid_rect_block(grid, color):
    """
    Finds the first occurrence of a solid rectangular block of a given color.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the block to find.

    Returns:
        tuple: (row, col, height, width) of the block, or None if not found.
    """
    rows, cols = grid.shape
    coords = np.argwhere(grid == color)

    if coords.shape[0] == 0:
        return None

    min_r, min_c = coords.min(axis=0)
    max_r, max_c = coords.max(axis=0)

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Check if the number of pixels matches the bounding box area
    if coords.shape[0] != height * width:
        # This handles cases where the shape isn't rectangular or has holes
        # A more robust check might be needed for multiple separate blocks
        # but for this task's examples, this seems sufficient. Let's try
        # iterating through potential blocks if this fails.
        pass # Continue to the more rigorous check below

    # Verify that the bounding box area is solidly filled with the target color
    block = grid[min_r:min_r + height, min_c:min_c + width]
    if np.all(block == color):
        return min_r, min_c, height, width

    # Fallback: If the simple bounding box of all color pixels wasn't it,
    # iterate to find the first actual solid block. This handles cases where
    # there might be stray pixels of the target color elsewhere.
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                # Found a potential top-left corner
                # Determine max possible width from this point
                max_w = 0
                for w in range(1, cols - c + 1):
                    if grid[r, c + w - 1] == color:
                        max_w = w
                    else:
                        break
                if max_w == 0: continue # Should not happen based on initial check

                # Determine max possible height for this width
                max_h = 0
                for h in range(1, rows - r + 1):
                    if np.all(grid[r + h - 1, c:c + max_w] == color):
                        max_h = h
                    else:
                        break
                if max_h == 0: continue # Should not happen

                # Check if the found block is solid
                potential_block = grid[r:r + max_h, c:c + max_w]
                if np.all(potential_block == color):
                    # Check if this is the *minimal* bounding box for this specific block
                    # This ensures we don't just find a sub-part of a larger block
                    actual_coords = np.argwhere(potential_block == color)
                    if actual_coords.shape[0] == max_h * max_w:
                         return r, c, max_h, max_w # Found a solid block

    return None # No solid block found


def find_matching_pattern_block(grid, target_height, target_width, white_bbox):
    """
    Finds a block with target dimensions that does not contain white (0)
    and is not the white block itself.

    Args:
        grid (np.array): The input grid.
        target_height (int): The height of the block to find.
        target_width (int): The width of the block to find.
        white_bbox (tuple): The (row, col, height, width) of the white block
                             to avoid matching the same block.

    Returns:
        tuple: (row, col, height, width) of the pattern block, or None if not found.
    """
    rows, cols = grid.shape
    white_r, white_c, _, _ = white_bbox

    for r in range(rows - target_height + 1):
        for c in range(cols - target_width + 1):
            # Check if this is the same location as the white block
            if r == white_r and c == white_c:
                continue

            # Extract the candidate block
            candidate_block = grid[r:r + target_height, c:c + target_width]

            # Check if the block contains any white pixels
            if np.any(candidate_block == 0):
                continue

            # If we reach here, the block has the right dimensions,
            # is not the white block, and contains no white pixels.
            return r, c, target_height, target_width

    return None # No matching pattern block found

def transform(input_grid):
    """
    Identifies a white rectangular block and a matching-dimension pattern block.
    Copies the pattern onto the white block's location.
    """
    # Convert input to numpy array
    input_array = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_array)

    # 1. Find the white block
    white_bbox = find_solid_rect_block(output_grid, 0) # Use output_grid to search

    if white_bbox is None:
        # Handle error: No white block found (or not solid rectangle)
        # Based on examples, assume one always exists and is solid.
        # If the task allows no white block, return input copy.
        print("Warning: No solid white block found.")
        return output_grid.tolist() # Return copy in this case

    white_r, white_c, white_h, white_w = white_bbox
    # print(f"Found white block at ({white_r}, {white_c}), size {white_h}x{white_w}")

    # 2. Find the pattern block with matching dimensions
    pattern_bbox = find_matching_pattern_block(input_array, white_h, white_w, white_bbox)

    if pattern_bbox is None:
        # Handle error: No matching pattern block found.
        # Based on examples, assume one always exists.
        # If the task allows no pattern block, return input copy.
         print("Warning: No matching pattern block found.")
         return output_grid.tolist() # Return copy in this case

    pattern_r, pattern_c, pattern_h, pattern_w = pattern_bbox
    # print(f"Found pattern block at ({pattern_r}, {pattern_c}), size {pattern_h}x{pattern_w}")

    # 3. Extract the pattern from the input grid
    pattern_data = input_array[pattern_r : pattern_r + pattern_h,
                               pattern_c : pattern_c + pattern_w]

    # 4. Copy (paste) the pattern onto the white block's location in the output grid
    output_grid[white_r : white_r + white_h,
                white_c : white_c + white_w] = pattern_data

    # Convert the result back to a list of lists
    return output_grid.tolist()
```