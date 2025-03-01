"""
1. Identify the Largest Yellow Shape: Find the largest contiguous region of yellow (4) pixels in the input grid. Contiguous means pixels that are connected horizontally or vertically.

2. Identify Enclosed Shapes: Within the bounding box of the largest yellow shape, identify any shapes that are completely enclosed by the yellow shape. A shape is considered enclosed if all of its pixels are surrounded by yellow pixels of the largest yellow shape, either directly or through a chain of adjacent yellow pixels.

3. Fill Enclosed Shapes: Any shapes enclosed in the largest yellow shape are entirely filled with the color of the enclosing shape (yellow).

4. Extract Combined Shape: Create a new output grid. Copy the largest yellow shape and any enclosed, filled shapes from the input grid to the output grid. The output should be tightly bounded: create the smallest possible rectangle including the largest yellow object and any enclosed objects.
"""

import numpy as np

def find_shapes(grid):
    # Find all contiguous shapes in a grid
    shapes = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, shape_color, current_shape):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != shape_color:
            return
        visited.add((r, c))
        current_shape.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, shape_color, current_shape)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                shape_color = grid[r, c]
                if shape_color != 0: # don't care about blank
                   current_shape = []
                   dfs(r, c, shape_color, current_shape)
                   shapes.append((shape_color, current_shape))
    return shapes

def find_largest_shape(shapes):
    # Find the largest shape in a list of shapes
    largest_shape = []
    max_size = 0
    for color, shape in shapes:
        size = len(shape)
        if size > max_size:
            max_size = size
            largest_shape = shape
    return largest_shape

def flood_fill(grid, start_r, start_c, fill_color):
    """Fills a region in the grid with the given color."""
    rows, cols = grid.shape
    original_color = grid[start_r, start_c]
    if original_color == fill_color:
        return

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    queue = [(start_r, start_c)]
    visited = set()
    visited.add((start_r,start_c))

    while queue:
        r, c = queue.pop(0)
        grid[r, c] = fill_color

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and grid[nr, nc] == original_color and (nr, nc) not in visited:
                queue.append((nr, nc))
                visited.add((nr,nc))



def extract_shape_and_enclosed(input_grid, shape_pixels):
    """Extracts a shape and any enclosed shapes, filling enclosed regions."""
    if not shape_pixels:
        return np.zeros((1, 1), dtype=int)

    min_r = min(r for r, c in shape_pixels)
    max_r = max(r for r, c in shape_pixels)
    min_c = min(c for r, c in shape_pixels)
    max_c = max(c for r, c in shape_pixels)

    # Create a new grid for the bounding box
    rows = max_r - min_r + 1
    cols = max_c - min_c + 1
    extracted_grid = np.zeros((rows, cols), dtype=int)

    # Copy the main shape pixels
    for r, c in shape_pixels:
        extracted_grid[r - min_r, c - min_c] = input_grid[r, c]

    # Find enclosed regions and flood fill
    for r in range(rows):
        for c in range(cols):
            if extracted_grid[r, c] == 0:  # Check for potential enclosed regions
                is_enclosed = True
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < rows and 0 <= nc < cols and extracted_grid[nr,nc] != 0):
                        is_enclosed = False
                        break

                if is_enclosed:
                    # determine color to use
                    fill_color = 4
                    flood_fill(extracted_grid, r, c, fill_color)

    return extracted_grid


def transform(input_grid):
    # Find all shapes in the input grid
    shapes = find_shapes(input_grid)

    # Find yellow shapes
    yellow_shapes = [shape for color, shape in shapes if color == 4]

    # Find the largest yellow shape
    largest_yellow_shape = find_largest_shape(yellow_shapes)

    # Extract the largest yellow shape and fill enclosed regions
    output_grid = extract_shape_and_enclosed(input_grid, largest_yellow_shape)

    return output_grid