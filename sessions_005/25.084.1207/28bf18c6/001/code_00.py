import numpy as np
from collections import deque

"""
Identify the single contiguous non-white object in the input grid.
Determine its minimal bounding box.
Create an output grid whose height is the bounding box height and width is twice the bounding box width plus one.
Place the content of the bounding box (the object pattern) at the left side of the output grid.
Place the content of the bounding box again at the right side of the output grid, separated by a single column of white pixels.
"""

def find_colored_object(grid):
    """
    Finds the first contiguous non-white object in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: A tuple containing:
            - set: Coordinates of the object's pixels.
            - int: The color of the object.
            - tuple: The coordinates (row, col) of the first found pixel of the object.
        Returns (None, -1, None) if no non-white object is found.
    """
    rows, cols = grid.shape
    visited = set()
    q = deque()

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                object_pixels = set()
                q.append((r, c))
                visited.add((r, c))
                first_pixel = (r, c) # Store the first pixel found

                while q:
                    row, col = q.popleft()
                    object_pixels.add((row, col))

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                # Since we expect only one object, return after finding the first one
                return object_pixels, color, first_pixel

    return None, -1, None


def get_bounding_box(pixels):
    """
    Calculates the minimal bounding box for a set of pixel coordinates.

    Args:
        pixels (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, height, width)
               Returns (0, 0, 0, 0) if pixels set is empty.
    """
    if not pixels:
        return 0, 0, 0, 0

    min_row = min(r for r, c in pixels)
    max_row = max(r for r, c in pixels)
    min_col = min(c for r, c in pixels)
    max_col = max(c for r, c in pixels)

    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return min_row, min_col, height, width

def extract_subgrid(grid, min_row, min_col, height, width):
    """
    Extracts a subgrid based on bounding box parameters.

    Args:
        grid (np.array): The input grid.
        min_row (int): Top row index of the bounding box.
        min_col (int): Left column index of the bounding box.
        height (int): Height of the bounding box.
        width (int): Width of the bounding box.

    Returns:
        np.array: The extracted subgrid (object pattern).
    """
    return grid[min_row : min_row + height, min_col : min_col + width]


def transform(input_grid):
    """
    Transforms the input grid by duplicating the found object with a white spacer column.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)

    # 1. Identify the contiguous group of non-white pixels (the object).
    object_pixels, color, _ = find_colored_object(input_np)

    if object_pixels is None:
        # Handle cases where no object is found (though not expected based on examples)
        # Returning an empty grid or original might be options, let's return empty for now.
        return [[]] 

    # 2. Determine the minimal bounding box.
    min_row, min_col, height, width = get_bounding_box(object_pixels)

    # 3. Extract the subgrid defined by the bounding box (ObjectPattern).
    # We need to create the pattern relative to the bounding box origin.
    object_pattern = np.zeros((height, width), dtype=int)
    for r, c in object_pixels:
        relative_r = r - min_row
        relative_c = c - min_col
        object_pattern[relative_r, relative_c] = color

    # 4. Create the new output grid with calculated dimensions, filled with white (0).
    output_height = height
    output_width = (2 * width) + 1
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # 5. Place the ObjectPattern into the output grid at the top-left.
    output_grid_np[0:height, 0:width] = object_pattern

    # 6. Place the ObjectPattern again, offset by width + 1 columns.
    output_grid_np[0:height, width + 1 : output_width] = object_pattern

    # Convert the output numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    # 7. Return the resulting grid.
    return output_grid