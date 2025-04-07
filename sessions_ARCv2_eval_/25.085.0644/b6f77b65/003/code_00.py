"""
Transform the input grid based on the color C of the pixel at (0,0).
Determine a downward shift amount S based on C:
- If C is Maroon (9), S = 0.
- If C is Magenta (6), S = 2.
- Otherwise, S = 3.

If S = 0, return a copy of the input grid.

If S > 0:
1. Create a new output grid filled with white (0).
2. Copy the indicator pixel C to output grid at (0,0).
3. Find all distinct monochromatic objects (connected components of the same non-white color using 4-way adjacency), ignoring the pixel at (0,0).
4. For each monochromatic object found:
   - If the object's color is NOT equal to C, shift all its pixels down by S rows in the output grid. Discard pixels shifted off the grid.
   - If the object's color IS equal to C, discard the object.
5. Return the resulting output grid.
"""

import numpy as np
from collections import deque

def find_mono_objects(grid: np.ndarray) -> list:
    """
    Finds all connected monochromatic objects (pixels of the same color)
    in the grid, ignoring the pixel at (0,0) and white pixels (0).
    Uses 4-way adjacency.

    Args:
        grid: The input numpy array representing the grid.

    Returns:
        A list of objects, where each object is a dictionary containing:
        - 'pixels': a list of (row, col) tuples for the object.
        - 'color': the integer color of the object.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    # Mark (0,0) as visited to ignore the indicator pixel location,
    # regardless of its color.
    if rows > 0 and cols > 0:
        visited[0, 0] = True

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Find start of a new object: non-white, not visited
            if color != 0 and not visited[r, c]:
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                object_color = color # All pixels in this object must have this color

                while q:
                    row, col = q.popleft()
                    current_object_pixels.append((row, col)) # Store only coords

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, SAME color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == object_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    'pixels': current_object_pixels, # List of (r, c) tuples
                    'color': object_color
                })
    return objects

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    """
    rows, cols = input_grid.shape

    # 1. Examine the color C of the pixel at (0, 0)
    indicator_color = input_grid[0, 0]

    # 2. Determine the downward shift amount S
    if indicator_color == 9:  # Maroon
        shift_amount = 0
    elif indicator_color == 6: # Magenta
        shift_amount = 2
    else: # Any other color
        shift_amount = 3

    # 3. If S is 0, return a copy of the input grid
    if shift_amount == 0:
        return input_grid.copy()

    # 4. If S > 0:
    #    a. Create a new output grid filled with white (0)
    output_grid = np.zeros_like(input_grid)

    #    b. Copy the indicator pixel C to the output grid
    output_grid[0, 0] = indicator_color

    #    c. Identify all distinct monochromatic objects (ignoring (0,0))
    mono_objects = find_mono_objects(input_grid)

    #    d. Process each monochromatic object
    for obj in mono_objects:
        obj_color = obj['color']
        obj_pixels = obj['pixels']

        # ii. If the object's color is NOT the indicator color C
        if obj_color != indicator_color:
            # Shift its pixels downwards
            for r, c in obj_pixels:
                # Calculate the new row
                r_new = r + shift_amount
                # If the new row is within grid height
                if r_new < rows:
                    # Set the pixel in the output grid
                    output_grid[r_new, c] = obj_color
        # iii. If the object's color IS the indicator color C, do nothing (object removed)

    # e. Return the resulting output grid
    return output_grid