"""
Transforms an input grid based on the location of a single 'white' (0) pixel.
The output grid displays a modified checkerboard pattern originating from the 'white' pixel.
Pixels in the output grid are colored 'white' (0) if their Manhattan distance
from the original 'white' pixel is even, *unless* the pixel lies on the same row
or same column as the original 'white' pixel (excluding the original white pixel itself).
Pixels with odd Manhattan distance, or those with even distance lying on the
source row/column (but not the source pixel), retain the original background color.
"""

import numpy as np

def find_unique_colors(grid):
    """Finds unique colors in the grid."""
    return np.unique(grid)

def find_pixel_location(grid, color):
    """Finds the coordinates of the first pixel with the specified color."""
    locations = np.argwhere(grid == color)
    if len(locations) > 0:
        # Return the first location found (row, column)
        return tuple(locations[0])
    return None

def calculate_manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points (tuples)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Applies the modified checkerboard pattern transformation based on the
    Manhattan distance from the single white pixel in the input grid,
    excluding pixels on the same row/column as the source white pixel
    (except the source pixel itself) from turning white even if their
    distance is even.

    Args:
        input_grid (list): The input grid as a list of lists.

    Returns:
        list: The transformed output grid as a list of lists.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=np.int64) # Use explicit type for numpy ops
    height, width = grid.shape

    # 1. Identify the background color (the non-white color)
    unique_colors = find_unique_colors(grid)
    background_color = 0 # Default, should be overwritten
    for color in unique_colors:
        if color != 0:
            background_color = int(color) # Store as standard int
            break
    # Handle edge case if only white exists (unlikely per task description)
    if len(unique_colors) == 1 and unique_colors[0] == 0:
        # Decide behavior: maybe return all white or use a default like black (not in map)
        # For now, assume a background color always exists besides white.
        pass

    # 2. Locate the coordinates (r0, c0) of the single 'white' pixel
    white_pixel_loc = find_pixel_location(grid, 0)
    if white_pixel_loc is None:
        # Handle cases where no white pixel is found
        # Based on task description, one should always exist.
        # Raising an error might be appropriate, or returning input.
        # For now, let's assume it's found.
        print("Warning: No white pixel (0) found in the input grid.")
        return input_grid # Return original if no white pixel found
        
    # Convert numpy int types to standard python int for clarity if needed, though not strictly necessary for calculation
    r0, c0 = int(white_pixel_loc[0]), int(white_pixel_loc[1])

    # 3. Create a new output grid, initialized with the background color
    #    This simplifies the logic - we only need to change pixels to white.
    output_grid = np.full_like(grid, fill_value=background_color)

    # 4. For each pixel at coordinates (r, c) in the grid:
    for r in range(height):
        for c in range(width):
            current_pos = (r, c)
            
            # a. Calculate the Manhattan distance d
            distance = calculate_manhattan_distance(current_pos, (r0, c0))

            # b. Check if the distance d is an even number
            if distance % 2 == 0:
                # c. Further check: is the pixel the source pixel OR is it NOT on the source row/column?
                is_source_pixel = (r == r0 and c == c0)
                is_on_source_row_or_col = (r == r0 or c == c0)

                if is_source_pixel or not is_on_source_row_or_col:
                    # d. If d is even AND (it's the source OR not on source row/col), set color to 'white' (0)
                    output_grid[r, c] = 0
            # else:
                # Pixel has odd distance, or has even distance but is on the source row/column (and not the source itself)
                # It remains the background color (already initialized)

    # 5. Return the completed output grid as a list of lists
    return output_grid.tolist()