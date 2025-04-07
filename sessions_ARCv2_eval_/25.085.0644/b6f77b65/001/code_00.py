import numpy as np
from collections import deque

"""
Transform the input grid based on the color C of the pixel at (0,0).
This color determines the downward shift amount S:
- If C is 9 (Maroon), S = 0 (no change).
- If C is 6 (Magenta), S = 2.
- Otherwise, S = 3.
If S > 0, identify all distinct connected non-white objects (excluding the pixel at (0,0)).
Remove objects containing the color C.
Shift the remaining objects downwards by S rows.
Copy the original indicator pixel C to (0,0) in the output.
"""

def find_objects(grid, indicator_color):
    """
    Finds all connected objects of non-white pixels in the grid,
    ignoring the pixel at (0,0).
    Returns a list of objects, where each object is a dictionary containing:
    - 'pixels': a list of (row, col, color) tuples for the object.
    - 'has_indicator_color': a boolean indicating if the object contains the indicator_color.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []
    
    # Mark (0,0) as visited to ignore the indicator pixel
    if rows > 0 and cols > 0:
        visited[0, 0] = True

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                # Start BFS for a new object
                current_object_pixels = []
                has_indicator = False
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    color = grid[row, col]
                    current_object_pixels.append((row, col, color))
                    if color == indicator_color:
                        has_indicator = True

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({
                    'pixels': current_object_pixels,
                    'has_indicator_color': has_indicator
                })
    return objects

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on the color C at (0,0).
    Determines shift amount S based on C.
    Removes objects containing C.
    Shifts remaining objects down by S rows.
    """
    rows, cols = input_grid.shape
    
    # 1. Examine the color C of the pixel at (0, 0)
    indicator_color = input_grid[0, 0]

    # 2. Determine the downward shift amount S
    if indicator_color == 9:  # Maroon
        shift_amount = 0
    elif indicator_color == 6: # Magenta
        shift_amount = 2
    else: # Yellow (4), Orange (7), or others
        shift_amount = 3

    # 3. If S is 0, return a copy of the input grid
    if shift_amount == 0:
        return input_grid.copy()

    # 4. If S > 0:
    #    a. Create a new output grid filled with white (0)
    output_grid = np.zeros_like(input_grid)
    
    #    b. Copy the indicator pixel to the output grid
    output_grid[0, 0] = indicator_color

    #    c. Identify all distinct connected objects (ignoring (0,0))
    objects = find_objects(input_grid, indicator_color)

    #    d. Process each object
    for obj in objects:
        # ii. If the object does NOT contain the indicator color C
        if not obj['has_indicator_color']:
            # Shift its pixels downwards
            for r, c, col in obj['pixels']:
                # Calculate the new row
                r_new = r + shift_amount
                # If the new row is within grid height
                if r_new < rows:
                    # Set the pixel in the output grid
                    output_grid[r_new, c] = col

    # e. Return the resulting output grid
    return output_grid
