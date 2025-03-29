```python
import numpy as np

"""
Identifies non-white (0) and non-blue (1) contiguous objects ('pattern objects').
Identifies horizontal and vertical blue (1) lines ('boundary markers').
Creates an output grid initialized from the input.
For each pattern object:
  - Gets its color (C) and bounding box (min_row, min_col, max_row, max_col).
  - Fills all rows corresponding to horizontal blue lines with color C.
  - Fills all columns corresponding to vertical blue lines with color C.
  - Fills the rows min_row and max_row with color C.
  - Fills the columns min_col and max_col with color C.
Fills from later pattern objects overwrite earlier ones in case of overlap.
"""

def find_objects(grid, colors_to_exclude={0, 1}):
    """
    Finds contiguous objects of colors not in colors_to_exclude.

    Args:
        grid (np.array): The input grid.
        colors_to_exclude (set): Set of colors to ignore.

    Returns:
        list: A list of tuples, where each tuple represents an object
              (color, min_row, min_col, max_row, max_col).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color not in colors_to_exclude and not visited[r, c]:
                # Found the start of a potential new object
                obj_color = color
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == obj_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if obj_pixels: # Check if we actually found pixels (should always be true here)
                    objects.append((obj_color, min_r, min_c, max_r, max_c))
                    
    return objects

def find_blue_lines(grid):
    """
    Finds horizontal and vertical lines composed entirely of blue (1) pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: A tuple containing two lists:
               - List of row indices for horizontal blue lines.
               - List of column indices for vertical blue lines.
    """
    height, width = grid.shape
    h_lines = []
    v_lines = []

    # Find horizontal lines
    for r in range(height):
        if np.all(grid[r, :] == 1):
            h_lines.append(r)

    # Find vertical lines
    for c in range(width):
        if np.all(grid[:, c] == 1):
            v_lines.append(c)

    return h_lines, v_lines


def transform(input_grid):
    """
    Transforms the input grid based on pattern objects and blue lines.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = output_grid.shape

    # 1. Identify Pattern Objects (non-white, non-blue)
    pattern_objects = find_objects(input_np)

    # 2. Identify Blue Lines
    h_blue_lines, v_blue_lines = find_blue_lines(input_np)

    # 3. & 4. Initialize Output Grid (done above) & Iterate through Pattern Objects
    for obj_color, min_r, min_c, max_r, max_c in pattern_objects:
        # 5a. Get color and bounding box (already done)
        C = obj_color
        
        # Rows and Columns to fill for this object
        rows_to_fill = set(h_blue_lines) | {min_r, max_r}
        cols_to_fill = set(v_blue_lines) | {min_c, max_c}

        # 5c. Fill horizontal blue line rows
        # 5e. Fill min_row
        # 5f. Fill max_row
        for r in rows_to_fill:
             if 0 <= r < height: # Check bounds just in case
                 output_grid[r, :] = C

        # 5d. Fill vertical blue line columns
        # 5g. Fill min_col
        # 5h. Fill max_col
        for c in cols_to_fill:
             if 0 <= c < width: # Check bounds just in case
                output_grid[:, c] = C

    # 6. Return final grid as list of lists
    return output_grid.tolist()
```