import numpy as np
from collections import deque

"""
Identify distinct green (3) shapes and magenta (6) markers in the input grid.
For each green shape, find associated magenta markers that align horizontally or vertically with the shape's bounding box.
Based on the relative position of the associated marker (left, right, above, below), determine a rectangular fill area extending from the shape's edge towards the marker.
Fill the calculated area(s) in the output grid with green (3), overwriting any existing colors except magenta (6).
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is represented by:
              - set: A set of (row, col) tuples representing the pixels of the object.
              - tuple: The bounding box (min_row, max_row, min_col, max_col).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                obj_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_pixels.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                if obj_pixels:
                    objects.append((obj_pixels, (min_r, max_r, min_c, max_c)))
    return objects

def find_pixels(grid, color):
    """
    Finds the coordinates of all pixels of a specific color.

    Args:
        grid (np.array): The input grid.
        color (int): The color to find.

    Returns:
        list: A list of (row, col) tuples for pixels of the specified color.
    """
    return list(zip(*np.where(grid == color)))


def transform(input_grid):
    """
    Transforms the input grid by extending green shapes towards associated magenta markers.

    1. Finds all distinct green shapes and magenta markers.
    2. For each green shape, determines associated markers based on alignment.
    3. Calculates the fill area between the shape and the marker.
    4. Fills the area with green, avoiding overwriting magenta markers.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Find green shapes (color 3) and their bounding boxes
    green_shapes = find_objects(output_grid, 3)
    
    # Find magenta markers (color 6)
    magenta_markers = find_pixels(output_grid, 6)

    # Process each green shape
    for _, (min_r, max_r, min_c, max_c) in green_shapes:
        # Check each marker for association
        for m_r, m_c in magenta_markers:
            fill_area_rows = None
            fill_area_cols = None

            # Check horizontal alignment (marker row within shape's row span)
            if min_r <= m_r <= max_r:
                # Marker is to the right
                if m_c > max_c:
                    fill_area_rows = range(min_r, max_r + 1)
                    fill_area_cols = range(max_c + 1, m_c)
                # Marker is to the left
                elif m_c < min_c:
                    fill_area_rows = range(min_r, max_r + 1)
                    fill_area_cols = range(m_c + 1, min_c)

            # Check vertical alignment (marker col within shape's col span)
            elif min_c <= m_c <= max_c:
                 # Marker is below
                if m_r > max_r:
                    fill_area_rows = range(max_r + 1, m_r)
                    fill_area_cols = range(min_c, max_c + 1)
                # Marker is above
                elif m_r < min_r:
                    fill_area_rows = range(m_r + 1, min_r)
                    fill_area_cols = range(min_c, max_c + 1)
            
            # Apply fill if an area was determined
            if fill_area_rows is not None and fill_area_cols is not None:
                for r in fill_area_rows:
                    for c in fill_area_cols:
                        # Ensure coordinates are within grid bounds
                        if 0 <= r < rows and 0 <= c < cols:
                           # Fill with green (3) only if not magenta (6)
                           if output_grid[r, c] != 6:
                               output_grid[r, c] = 3

    return output_grid