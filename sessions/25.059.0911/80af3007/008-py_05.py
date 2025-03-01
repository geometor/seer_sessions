"""
The transformation rule is context-dependent and involves different operations based on the structure of the input grid.

1. **Identify Objects:** The input grid contains colored objects, potentially interspersed with background color (0).

2. **Example Specific Rules:**
    *   **Example 1:** If there is a single repeated color (other than 0), subsample the input grid, taking every other row and every other column, *starting from the first row and column containing that color*. Reconstruct a grid using the subsampled elements.
    *   **Example 2:** If there is a pattern with single pixels of the same color (other than black) repeating every other element in every other row/column. Subsample the grid at those locations *starting from the first row and column containing that color* and add padding as needed.
    *   **Examples 3 & 4:** If there is a single solid, rectangular object. Extract the *first row of the object* and discard the rest. Add padding as needed to the final output.

3. **Output:** The output grid is based on the actions above.
"""

import numpy as np

def find_objects(grid):
    """Identifies distinct objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if not visited[i, j] and grid[i, j] != 0:
                color = grid[i, j]
                object_pixels = []
                stack = [(i, j)]
                visited[i,j] = True

                while stack:
                    x, y = stack.pop()
                    object_pixels.append((x, y))

                    # Check adjacent cells (up, down, left, right)
                    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                    for nx, ny in neighbors:
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx, ny] and grid[nx, ny] == color:
                            stack.append((nx, ny))
                            visited[nx, ny] = True
                objects.append({"color": color, "pixels": object_pixels})

    return objects

def get_object_bounds(pixels):
    """calculate the bounding box"""
    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """Transforms the input grid based on identified objects and rules."""
    objects = find_objects(input_grid)

    if len(objects) == 1:
        obj = objects[0]
        color = obj["color"]
        pixels = obj["pixels"]
        min_row, max_row, min_col, max_col = get_object_bounds(pixels)
        obj_height = max_row - min_row + 1
        obj_width = max_col - min_col + 1

        if obj_height > 1 and obj_width > 1 and all(input_grid[p[0],p[1]] == color for p in pixels):
           # Rule for Examples 3 & 4: Extract first row of the object.
           output_height = (input_grid.shape[0] + 1) // 2
           output_width = (input_grid.shape[1] + 1) //2
           output_grid = np.zeros((output_height, output_width), dtype=int)
           
           row_to_copy = input_grid[min_row, min_col:max_col+1]
           resized_row = np.zeros(output_width, dtype=int)

           for i in range(min(output_width, len(row_to_copy))):
               resized_row[i] = row_to_copy[i]

           output_grid[1,:] = resized_row # place it at the correct place.

        else:
            # Start from the assumption of rule 1
            output_rows = (input_grid.shape[0] + 1) // 2
            output_cols = (input_grid.shape[1] + 1) // 2
            output_grid = np.zeros((output_rows, output_cols), dtype=int)

            for i in range(min_row, input_grid.shape[0], 2):
                for j in range(min_col, input_grid.shape[1], 2):
                    if input_grid[i, j] == color:
                        output_i = i // 2
                        output_j = j // 2

                        # Check output bounds in case we started from different min_row/col
                        if output_i < output_rows and output_j < output_cols:
                            output_grid[output_i, output_j] = color
    
    elif len(objects) > 1:
        # more than one object, try to extract based on position
        
        first_obj = objects[0]
        first_color = first_obj["color"]
        first_pixels = first_obj["pixels"]
        first_min_row, _, first_min_col, _ = get_object_bounds(first_pixels)


        output_rows = (input_grid.shape[0] + 1) // 2
        output_cols = (input_grid.shape[1] + 1) // 2

        output_grid = np.zeros((output_rows, output_cols),dtype=int)

        for i in range(first_min_row, input_grid.shape[0], 2):
            for j in range(first_min_col, input_grid.shape[1], 2):
                if input_grid[i,j] != 0:
                    out_i = i//2
                    out_j = j//2
                    if out_i < output_rows and out_j < output_cols:
                        output_grid[out_i, out_j] = input_grid[i,j]

    else:
        # No objects found, return an empty grid of appropriate size
        output_rows = (input_grid.shape[0] + 1) // 2
        output_cols = (input_grid.shape[1] + 1) // 2
        output_grid = np.zeros((output_rows, output_cols), dtype=int)

    return output_grid