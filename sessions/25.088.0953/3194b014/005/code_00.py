import numpy as np
from collections import deque

"""
Identify all contiguous blocks of pixels that have the same, non-white color (color != 0).
For each block, determine if it forms a perfect, solid square. A solid square has equal height and width, and all pixels within its bounding box have the same color as the block, and the number of pixels in the block equals the area of the bounding box.
Find the maximum side length among all identified solid squares.
Identify all solid squares that have this maximum side length.
If there is only one such square, choose its color.
If there are multiple squares with the maximum side length, choose the color of the square that has the numerically smallest color value.
If no solid squares are found in the input grid, default to white (color 0).
Construct a 3x3 output grid and fill it entirely with the chosen color.
"""

def find_contiguous_blocks(grid):
    """
    Finds all contiguous blocks of the same non-background color (0).

    Uses Breadth-First Search (BFS) to find connected components for each color.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
              {'color': int, 'coords': set_of_tuples, 'size': int}
              representing a contiguous block. Returns an empty list if no
              non-background blocks are found.
    """
    height, width = grid.shape
    visited = set()
    blocks = []

    for r in range(height):
        for c in range(width):
            # Process pixel if it's non-background and not yet visited
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                component_coords = set()
                queue = deque([(r, c)])
                visited.add((r, c))

                # Start BFS from the current pixel
                while queue:
                    row, col = queue.popleft()
                    component_coords.add((row, col))

                    # Check cardinal neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor has the same color and hasn't been visited
                            if grid[nr, nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                queue.append((nr, nc))

                # Store the found block if it's not empty
                if component_coords:
                    blocks.append({
                        'color': color,
                        'coords': component_coords,
                        'size': len(component_coords)
                    })

    return blocks

def get_bounding_box(coords):
    """
    Calculates the bounding box dimensions and corners for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_r, min_c, max_r, max_c, height, width) or
               (None, None, None, None, 0, 0) if coords is empty.
    """
    if not coords:
        return None, None, None, None, 0, 0

    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    # Height and width are inclusive of the min/max row/col
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return min_r, min_c, max_r, max_c, height, width

def is_solid_square(block, grid):
    """
    Checks if a given contiguous block forms a solid square.

    A block is a solid square if:
    1. Its bounding box has equal height and width.
    2. The number of pixels in the block is equal to the area of the bounding box (height * width).
    3. All pixels within the bounding box in the original grid have the same color as the block.
       (Note: Check 3 is implicitly covered by Check 2 if the block was found correctly by
        `find_contiguous_blocks`, but we check explicitly for robustness).

    Args:
        block (dict): A dictionary representing the block {'color', 'coords', 'size'}.
        grid (np.array): The original input grid (needed for solidity check).

    Returns:
        tuple: (is_square, side_length, color)
               - is_square (bool): True if the block is a solid square.
               - side_length (int): The side length if it's a square, otherwise 0.
               - color (int or None): The block's color if it's a square, otherwise None.
    """
    coords = block['coords']
    color = block['color']
    pixel_count = block['size']

    if not coords:
        return False, 0, None

    # Calculate bounding box properties
    min_r, min_c, max_r, max_c, height, width = get_bounding_box(coords)

    # Check 1: Bounding box must be square (and have non-zero dimensions)
    if height != width or height == 0:
        return False, 0, None

    # Check 2: Pixel count must match the area of the bounding box
    if pixel_count != height * width:
        # This indicates the block is not solid (has holes) or is not rectangular
        return False, 0, None

    # Check 3: Verify all pixels within bounding box match the block's color
    # This check ensures the shape is indeed solid within its bounding box in the grid.
    grid_h, grid_w = grid.shape # Get grid dimensions for safe access
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Check bounds just in case (should be within grid if bbox is correct)
            if not (0 <= r < grid_h and 0 <= c < grid_w):
                 # Should not happen with correct bbox calculation on valid grid coords
                 return False, 0, None
            # Check if the pixel color in the grid matches the block's color
            if grid[r, c] != color:
                 # Found a pixel of a different color within the bounding box
                 return False, 0, None

    # If all checks pass, it is a solid square
    side_length = height # Since height == width
    return True, side_length, color

def transform(input_grid):
    """
    Transforms the input grid based on finding the largest solid square.

    The transformation logic is:
    1. Find all contiguous blocks of non-white pixels.
    2. Identify which of these blocks are solid squares.
    3. Find the size of the largest solid square(s).
    4. Among the largest solid squares, select the one with the smallest color index.
    5. If no solid squares are found, use white (0).
    6. Create a 3x3 output grid filled with the selected color.

    Args:
        input_grid (list of lists): The input grid representation.

    Returns:
        list of lists: A 3x3 grid filled with the determined color.
    """
    # Convert input to NumPy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)

    # Handle potential empty input
    if input_grid_np.size == 0:
        # Return a default 3x3 white grid if input is empty
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Step 1: Find all contiguous blocks
    blocks = find_contiguous_blocks(input_grid_np)

    # Step 2: Identify all solid squares from the blocks
    solid_squares = []
    for block in blocks:
        is_sq, size, sq_color = is_solid_square(block, input_grid_np)
        if is_sq:
            solid_squares.append({'color': sq_color, 'size': size})

    # Step 3-5: Determine the output color based on largest square(s) and tie-breaking
    output_color = 0 # Default to white (0)

    if solid_squares:
        # Find the maximum side length among the found solid squares
        max_square_size = 0
        # Check necessary as max() on empty sequence raises error
        if solid_squares:
             max_square_size = max(sq['size'] for sq in solid_squares)

        # Filter to get only the squares with the maximum size
        largest_squares = [sq for sq in solid_squares if sq['size'] == max_square_size]

        # Apply the tie-breaking rule: smallest color index wins
        if largest_squares:
            # Sort the list of largest squares based on color index (ascending)
            largest_squares.sort(key=lambda x: x['color'])
            # The first element after sorting has the minimum color index
            output_color = largest_squares[0]['color']

    # Step 6: Create the 3x3 output grid filled with the chosen color
    output_grid_np = np.full((3, 3), output_color, dtype=int)

    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_grid_np.tolist()

    return output_grid