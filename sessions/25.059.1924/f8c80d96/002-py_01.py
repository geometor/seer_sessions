"""
1.  **Identify the primary object:** Find the contiguous region of non-zero pixels in the input grid. Note its color and initial location.

2.  **Expand the object:**
    *   Iterate through rows and columns.
    *   Wherever the object is found, attempt to expand to the orthogonal neighboring cells (above, below, left, and right).
    *   If the bordering cell contains zero (white), then fill it with the color of the primary object.
    *   Expansion is limited to the bounding box that fully surrounds the expanded object using only orthogonal neighbors.

3.  **Fill the remaining original zero-value cells within the bounding box:**
     * Fill remaining zero-value cells in the input, with the color `5`, that is bounded on all four sides using orthogonal directions.

4.  **Preserve Initial Object:** The original, contiguous object from the input should remain and maintain its relative location in the output.
"""

import numpy as np

def find_object(grid):
    """Finds the contiguous region of non-zero pixels and returns its color and coordinates."""
    rows, cols = len(grid), len(grid[0])
    non_zero_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0:
                non_zero_pixels.append((r, c))

    if not non_zero_pixels:
        return None, []

    # Assuming the first non-zero pixel belongs to the object
    first_pixel = non_zero_pixels[0]
    object_color = grid[first_pixel[0]][first_pixel[1]]
    object_pixels = set()
    
    # Breadth First Search for other object pixels
    queue = [first_pixel]
    while queue:
        r,c = queue.pop(0)
        if (r,c) in object_pixels:
            continue
        object_pixels.add((r, c))
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == object_color and (nr,nc) not in object_pixels:
                queue.append(nr,nc)

    return object_color, list(object_pixels)

def get_bounding_box(pixels):
    min_r = min(p[0] for p in pixels)
    max_r = max(p[0] for p in pixels)
    min_c = min(p[1] for p in pixels)
    max_c = max(p[1] for p in pixels)

    return (min_r, min_c), (max_r, max_c)
    
def get_orthogonal_neighbors(coord, rows, cols):
    r,c = coord
    neighbors = []
    if r>0:
      neighbors.append((r-1, c)) # above
    if r<rows-1:
      neighbors.append((r+1, c)) # below
    if c>0:
      neighbors.append((r, c-1)) # left
    if c<cols-1:
      neighbors.append((r, c+1)) # right
    return neighbors

def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = np.full((rows, cols), 5)  # Initialize with gray (5)

    # find object
    object_color, object_pixels = find_object(grid)

    if object_color is None:
      return output_grid.tolist()

    # Expand object by iterating its pixels and finding neighbors
    expanded_pixels = set(object_pixels)
    queue = object_pixels.copy()  # Use a copy to avoid modifying the original list during iteration
    for r, c in queue:
        neighbors = get_orthogonal_neighbors((r,c), rows, cols)
        for nr, nc in neighbors:
            if grid[nr][nc] == 0:
              expanded_pixels.add((nr,nc))


    # copy the expanded pixels to the output grid with the correct color
    for r, c in expanded_pixels:
      output_grid[r][c] = object_color

    return output_grid.tolist()