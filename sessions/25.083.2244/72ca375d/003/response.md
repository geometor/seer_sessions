```python
"""
1.  **Identify Shapes:** Scan the input grid and identify all distinct, contiguous regions of non-zero pixels. Each region is a "shape", defined by its color, position, width, height, and constituent pixels.
2.  **Select Shape:**
      * If there's a yellow (color 4) shape: Select it (example 1)
      * If there is no yellow shape, but a magenta shape exists: Select the lower of the magenta shape(s) (Example 2)
      * If there is no yellow or magenta, select the gray (color 5) object (Example 3)
3. **Extract Shape**: Create a new grid containing *only* the selected shape, maintaining internal zeros within the shape.
4. **Preserve Internal Zeros (Conditional):** If the selected shape had internal zeros in the original input grid, those zero positions must be maintained in the output grid. Zeros surrounding the shape on all sides are removed.
"""

import numpy as np

def identify_shapes(grid):
    shapes = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, shape_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        shape_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, shape_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                shape_coords = []
                dfs(r, c, grid[r, c], shape_coords)
                if shape_coords:
                    min_r = min(coord[0] for coord in shape_coords)
                    max_r = max(coord[0] for coord in shape_coords)
                    min_c = min(coord[1] for coord in shape_coords)
                    max_c = max(coord[1] for coord in shape_coords)
                    shapes.append({
                        'color': grid[r, c],
                        'position': (min_r, min_c),
                        'width': max_c - min_c + 1,
                        'height': max_r - min_r + 1,
                        'coords': shape_coords,
                    })
    return shapes

def select_shape(shapes):
    yellow_shapes = [shape for shape in shapes if shape['color'] == 4]
    if yellow_shapes:
        return yellow_shapes[0]  # Return the first yellow shape (if multiple)

    magenta_shapes = [shape for shape in shapes if shape['color'] == 6]
    if magenta_shapes:
        # Select the lowest magenta shape (largest row value in position)
        return max(magenta_shapes, key=lambda shape: shape['position'][0])

    gray_shapes = [shape for shape in shapes if shape['color'] == 5]
    if gray_shapes:
        return gray_shapes[0]  # Return the first gray shape

    return None  # No matching shape found


def extract_shape(shape, grid):
    if shape is None:
        return np.array([])

    min_r, min_c = shape['position']
    max_r = min_r + shape['height']
    max_c = min_c + shape['width']
    extracted_grid = np.zeros_like(grid[min_r:max_r, min_c:max_c])

    for r_in, r_out in enumerate(range(min_r, max_r)):
        for c_in, c_out in enumerate(range(min_c, max_c)):
             if (r_out,c_out) in shape['coords']:
                extracted_grid[r_in, c_in] = grid[r_out,c_out]

    return extracted_grid

def remove_zeros(grid):
    if grid.size == 0:  # Handle empty grid case
        return grid

    # Remove zero rows from top
    while grid.size > 0 and np.all(grid[0] == 0):
        grid = grid[1:]

    # Remove zero rows from bottom
    while grid.size > 0 and np.all(grid[-1] == 0):
        grid = grid[:-1]

    if grid.size == 0: #check
        return grid

    # Remove zero columns from left
    while grid.size > 0 and np.all(grid[:, 0] == 0):
        grid = grid[:, 1:]

    # Remove zero columns from right
    while grid.size > 0 and np.all(grid[:, -1] == 0):
        grid = grid[:, :-1]

    return grid


def transform(input_grid):
    # Convert input grid to a NumPy array
    grid = np.array(input_grid)

    # Identify shapes in the input grid
    shapes = identify_shapes(grid)

    # Select a shape
    selected_shape = select_shape(shapes)
    
    # Extract shape with internal zeros
    extracted_grid = extract_shape(selected_shape, grid)
    
    # remove surrounding zeros
    output_grid = remove_zeros(extracted_grid)
    
    return output_grid.tolist()
```