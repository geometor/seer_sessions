```python
"""
1.  **Global Color Mapping:**
    *   Examine all input/output pairs.
    *   Create a dictionary mapping each input color to its corresponding output color. If a color remains unchanged, that mapping does not need to be stored.

2.  **Apply Color Map:** Iterate through all cells of the input grid, replace the colors with their mapped values as determined in step 1

3.  **(Modified) Interior Object Identification:**
 *   Identify "interior objects," which are contiguous regions of the *same color*, not on the border of the grid.

4.  **(Modified) Interior object Processing:**
  * Check color change - check for change in color by comparing objects location in the input and output.
  * Apply the change to the object in the working grid.

5. **(Modified) Propagation:**
    *   For each changed pixel within each interior object do:
    *   Check adjacent cells (up, down, left, and right).
    *   If an adjacent cell has the *original* color of the changed pixel (before color mapping), change the adjacent cell's color to the *new* color (after color mapping).
    *   Continue this process recursively for all newly changed pixels, forming "chains" of color changes. This is similar to a flood-fill, but only triggered by interior object color changes and only propagating along connected components of the original color.
"""

import numpy as np

# Global variables to store training data.
train_inputs = []
train_outputs = []

def calculate_color_mapping(inputs, outputs):
    """Calculates the color mapping between input and output grids."""
    color_mapping = {}
    for input_grid, output_grid in zip(inputs, outputs):
        input_grid = np.array(input_grid)
        output_grid = np.array(output_grid)
        for i in range(input_grid.shape[0]):
            for j in range(input_grid.shape[1]):
                input_val = input_grid[i, j]
                output_val = output_grid[i, j]
                if input_val != output_val:
                    color_mapping[input_val] = output_val
    return color_mapping

def find_interior_objects(grid):
    """Finds contiguous blocks of same-colored pixels not on the border."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def is_interior(r, c):
        """Checks if a cell is within the interior of the grid."""
        return 0 < r < rows - 1 and 0 < c < cols - 1

    def dfs(r, c, color, obj_coords):
        """Depth-first search to find contiguous pixels."""
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or visited[r, c]
            or grid[r, c] != color
            or not is_interior(r, c)
        ):
            return

        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if not visited[r, c] and is_interior(r, c):
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                if obj_coords:
                    objects.append((grid[r, c], obj_coords))
    return objects

def propagate_changes(grid, changed_pixels, original_color_map):
    """
    Propagates color changes horizontally and vertically, recursively.
    Uses the original_color_map to check against pre-change colors.
    """
    rows, cols = grid.shape
    new_changes = set()
    
    while changed_pixels:
        next_changed_pixels = set()
        for r, c, old_color, new_color in changed_pixels:
            # Check neighbors (up, down, left, right)
            neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            for nr, nc in neighbors:
                if (0 <= nr < rows and 0 <= nc < cols and
                        (nr, nc) not in new_changes and
                        original_color_map.get(grid[nr,nc],grid[nr,nc]) == old_color
                    ):
                    grid[nr, nc] = new_color
                    next_changed_pixels.add((nr, nc, old_color, new_color))
                    new_changes.add( (nr,nc) ) # prevent infinite loops.
        changed_pixels = next_changed_pixels
    return

def transform(input_grid):
    # Make copies to avoid modifying the input directly.
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    
    # 1. Global Color Mapping
    color_mapping = calculate_color_mapping(train_inputs, train_outputs)

    # Create a reverse mapping for propagation
    original_color_map = {v:k for k,v in color_mapping.items()}

    # 2. Apply Color Map to entire grid
    rows, cols = output_grid.shape
    for r in range(rows):
      for c in range(cols):
        if output_grid[r,c] in color_mapping:
          output_grid[r,c] = color_mapping[output_grid[r,c]]
          
    # 3. Interior Object Identification (after color mapping)
    input_objects = find_interior_objects(output_grid)
    
    # 4. & 5. Interior object Processing and Propagation
    changed_pixels = set()

    for color, coords in input_objects:
      first_coord = coords[0]

      # check if interior object has color change
      new_color = None
      for train_input, train_output in zip(train_inputs, train_outputs):
        train_input_grid = np.array(train_input)
        train_output_grid = np.array(train_output)
        # apply global map to input
        for r in range(train_input_grid.shape[0]):
            for c in range(train_input_grid.shape[1]):
                if train_input_grid[r,c] in color_mapping:
                    train_input_grid[r,c] = color_mapping[train_input_grid[r,c]]
        # check if coord exists in this example
        if (first_coord[0] < train_input_grid.shape[0] and
              first_coord[1] < train_input_grid.shape[1] and
              train_input_grid[first_coord] == color
           ):
             new_color = train_output_grid[first_coord]
             break

      # Propagate if needed
      if new_color is not None and new_color != color:
        for r, c in coords:
            # find old color from the original input
            old_color = original_color_map.get(color, color)
            output_grid[r, c] = new_color  # Apply change to the object
            changed_pixels.add((r, c, old_color, new_color))

    propagate_changes(output_grid, changed_pixels, original_color_map)
    return output_grid
```