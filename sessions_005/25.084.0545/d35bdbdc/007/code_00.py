"""
1.  **Object Definition:** An object is a contiguous group of pixels of the same color. Contiguous means adjacent horizontally, vertically, or diagonally.

2.  **Object Preservation:** If an object is completely surrounded by background color (0), the entire object is preserved without changes.

3.  **Interior Pixel Removal**:
    *   The "interior" of an object consists of pixels that have all eight neighbors (horizontal, vertical, and diagonal) being pixels of the *same* color as the object.
    *    If any interior pixel of an object is color 2, 4, or 6, then all *interior* pixels of that object become 0.

4.  **Complete Object Removal (Specific Colors):**
    *    If an object consists of color 1 ONLY, the entire object becomes 0
    *    If an object consists of color 2 ONLY, the entire object becomes 0

5.  **Color 9 Transformation (Special Case):**
    *   If a single-pixel object of color 9 exists, and it is adjacent (horizontally, vertically, or diagonally) to *both* a pixel of color 1 and a pixel of color 2, then the color 9 pixel becomes color 3. Otherwise, the color 9 pixel is unchanged.

6.  **Edge Cases**:
    * If part of object is touching the edge of the input, it is not considered surrounded.
"""

import numpy as np

def get_neighbors(grid, i, j, include_self=False):
    """Gets the colors of neighboring pixels (including diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for x in range(max(0, i - 1), min(rows, i + 2)):
        for y in range(max(0, j - 1), min(cols, j + 2)):
            if include_self or (x, y) != (i, j):
                neighbors.append(grid[x, y])
    return neighbors

def get_object(grid, i, j):
    """Extracts the object containing the given pixel."""
    rows, cols = grid.shape
    color = grid[i, j]
    if color == 0:
        return []

    object_pixels = []
    visited = set()
    queue = [(i, j)]

    while queue:
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if 0 <= x < rows and 0 <= y < cols and grid[x, y] == color:
            object_pixels.append((x, y))
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (dx, dy) != (0, 0):
                        queue.append((x + dx, y + dy))
    return object_pixels

def is_surrounded_by_0(grid, object_pixels):
    """Checks if an object is completely surrounded by color 0."""
    for x, y in object_pixels:
        neighbors = get_neighbors(grid, x, y)
        if not all(neighbor == 0 for neighbor in neighbors):
            return False
    return True

def get_interior_pixels(grid, object_pixels):
    """Identifies the interior pixels of an object."""
    interior_pixels = []
    for x, y in object_pixels:
        neighbors = get_neighbors(grid, x, y)
        # Check if all neighbors have same color.
        if all(neighbor == grid[x,y] for neighbor in neighbors):
            interior_pixels.append((x,y))
    return interior_pixels


def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    processed_pixels = set()

    for i in range(rows):
        for j in range(cols):
            if (i, j) not in processed_pixels:
                object_pixels = get_object(input_grid, i, j)

                if not object_pixels:  # background
                    continue

                processed_pixels.update(object_pixels)

                # Object Preservation
                if is_surrounded_by_0(input_grid, object_pixels):
                    continue  # Preserve object

                # Complete Object Removal (Specific Colors)
                object_colors = [input_grid[x, y] for x, y in object_pixels]
                if all(c == 1 for c in object_colors):
                    for x, y in object_pixels:
                        output_grid[x, y] = 0
                    continue
                if all(c == 2 for c in object_colors):
                    for x, y in object_pixels:
                        output_grid[x, y] = 0
                    continue

                # Interior Pixel Removal
                interior_pixels = get_interior_pixels(input_grid, object_pixels)
                if any(input_grid[x, y] in [2, 4, 6] for x, y in interior_pixels):
                    for x, y in interior_pixels:
                        output_grid[x, y] = 0

                # Color 9 Transformation (Special Case)
                if len(object_pixels) == 1:
                    x, y = object_pixels[0]
                    if input_grid[x, y] == 9:
                        neighbors = get_neighbors(input_grid, x, y)
                        if 1 in neighbors and 2 in neighbors:
                            output_grid[x, y] = 3

    return output_grid.tolist()