"""
Overwrites a specific white rectangular area with a pattern found elsewhere
in the grid. The white block serves as the target area. The pattern block
(source) is identified by having the exact same dimensions as the white block,
containing no white pixels, and being surrounded by the same single, non-white
background color that surrounds the white block.
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
    coords = np.argwhere(grid == color)

    if coords.shape[0] == 0:
        return None

    min_r, min_c = coords.min(axis=0)
    max_r, max_c = coords.max(axis=0)

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    if coords.shape[0] != height * width:
        return None # Not a solid rectangle (L-shape, holes, multiple blocks)

    # Double check the block defined by the bounding box is entirely the target color
    block = grid[min_r:min_r + height, min_c:min_c + width]
    if np.all(block == color):
        return min_r, min_c, height, width
    else:
        return None


def get_uniform_border_color(grid, r, c, h, w):
    """
    Checks the pixels immediately adjacent to the border of a block defined by
    (r, c, h, w).

    Args:
        grid (np.array): The input grid.
        r, c, h, w (int): Bounding box of the block.

    Returns:
        int: The uniform border color if it exists, is single, and is not white (0).
        None: Otherwise (mixed border, white border, block touches edge inconsistently).
    """
    rows, cols = grid.shape
    border_pixels = []

    # Top border (if r > 0)
    if r > 0:
        border_pixels.extend(grid[r - 1, c:c + w])
    # Bottom border (if r + h < rows)
    if r + h < rows:
        border_pixels.extend(grid[r + h, c:c + w])
    # Left border (if c > 0)
    if c > 0:
        border_pixels.extend(grid[r:r + h, c - 1])
    # Right border (if c + w < cols)
    if c + w < cols:
        border_pixels.extend(grid[r:r + h, c + w])

    # Add corners if they exist and haven't been implicitly added by sides
    # Top-left
    if r > 0 and c > 0:
        border_pixels.append(grid[r - 1, c - 1])
    # Top-right
    if r > 0 and c + w < cols:
        border_pixels.append(grid[r - 1, c + w])
    # Bottom-left
    if r + h < rows and c > 0:
        border_pixels.append(grid[r + h, c - 1])
    # Bottom-right
    if r + h < rows and c + w < cols:
        border_pixels.append(grid[r + h, c + w])

    if not border_pixels:
        # Block might occupy the entire grid or be ill-defined
        return None

    first_pixel_color = border_pixels[0]

    # Check if the border color is white
    if first_pixel_color == 0:
        return None

    # Check if all border pixels have the same color
    if all(p == first_pixel_color for p in border_pixels):
        return first_pixel_color
    else:
        # Border is not uniform
        return None


def transform(input_grid):
    """
    Transforms the input grid by finding a white block and a pattern block
    with matching dimensions and border color, then copying the pattern onto
    the white block's location.
    """
    # Convert input list of lists to a numpy array
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_array)
    rows, cols = input_array.shape

    # 1. Find the unique solid white rectangular block (target)
    white_bbox = find_solid_rect_block(input_array, 0)
    if white_bbox is None:
        # print("Warning: No solid white block found.")
        return input_grid # Return original if no white block

    wr, wc, h, w = white_bbox
    # print(f"Found white block at ({wr}, {wc}), size {h}x{w}")

    # 2. Determine the uniform border color around the white block
    border_color = get_uniform_border_color(input_array, wr, wc, h, w)
    if border_color is None:
        # print(f"Warning: Could not determine a valid uniform non-white border color around the white block.")
        return input_grid # Return original if border condition not met

    # print(f"Determined border color: {border_color}")

    # 3. Find the pattern block (source)
    pattern_bbox = None
    for pr in range(rows - h + 1):
        for pc in range(cols - w + 1):
            # a. Skip the white block's location
            if pr == wr and pc == wc:
                continue

            # Define the candidate block
            candidate_block = input_array[pr:pr + h, pc:pc + w]

            # b. Check if it contains any white pixels
            if np.any(candidate_block == 0):
                continue

            # c. Check if it's surrounded by the determined border_color
            candidate_border_color = get_uniform_border_color(input_array, pr, pc, h, w)

            if candidate_border_color == border_color:
                # Found the pattern block (assuming uniqueness as per hypothesis)
                pattern_bbox = (pr, pc, h, w)
                # print(f"Found pattern block at ({pr}, {pc}) matching border color {border_color}")
                break # Stop searching once found
        if pattern_bbox:
            break # Stop outer loop as well

    # 4. If a pattern block was found, perform the copy
    if pattern_bbox:
        pr, pc, _, _ = pattern_bbox
        # Extract the pattern data
        pattern_data = input_array[pr:pr + h, pc:pc + w]
        # Paste the pattern onto the output grid at the white block's location
        output_grid[wr:wr + h, wc:wc + w] = pattern_data
    else:
        # print("Warning: No matching pattern block found.")
        # If no pattern block found, return the original grid (as per fallback)
        return input_grid

    # 5. Convert the result back to list of lists and return
    return output_grid.tolist()