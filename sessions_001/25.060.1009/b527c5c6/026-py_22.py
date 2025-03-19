"""
1.  **Object Identification:** Identify contiguous blocks of pixels of the same color as distinct objects. Classify objects as "single pixel" or "line" (horizontal or vertical).
2.  **Transformation Rules (Conditional):**

    *   **If there is one red pixel and one green pixel:** The red pixel becomes a vertical line occupying its original column. The green pixel moves to the row above where the original red pixel.

    *   **If there is one red pixel and NO green pixel**: The red pixel becomes a vertical line occupying its original column.

    *   **If there's a red horizontal line and a green pixel:** The red line remains unchanged, and the green pixel disappears.
    * **If there's any other combination:** Further examples needed.

3. **Priority**: Red transformations appear to take precedence.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous objects of a given color and classifies them."""
    visited = set()
    objects = []

    def dfs(row, col):
        """Depth-first search to find contiguous pixels and classify."""
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return None

        visited.add((row, col))
        object_pixels = [(row, col)]

        # Explore adjacent cells
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            result = dfs(new_row, new_col)
            if result:
                object_pixels.extend(result)
        return object_pixels

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                pixels = dfs(row, col)
                if pixels:
                    obj_type = "single_pixel"
                    if len(pixels) > 1:
                        # Check if it's a line
                        rows, cols = zip(*pixels)
                        if len(set(rows)) == 1:
                            obj_type = "horizontal_line"
                        elif len(set(cols)) == 1:
                            obj_type = "vertical_line"
                    objects.append({"type": obj_type, "pixels": pixels})
    return objects

def transform(input_grid):
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find green and red objects
    green_objects = find_objects(input_grid, 3)
    red_objects = find_objects(input_grid, 2)

    # Transformation rules
    if len(red_objects) == 1 and red_objects[0]['type'] == 'single_pixel':
        red_col = red_objects[0]['pixels'][0][1]
        output_grid[:, red_col] = 2  # Red to vertical line

        if len(green_objects) == 1 and green_objects[0]['type'] == 'single_pixel':
            green_row, green_col = green_objects[0]['pixels'][0]
            output_grid[green_row, green_col] = 0 # Remove original green
            new_green_row = red_objects[0]['pixels'][0][0] -1
            if new_green_row >= 0:
                output_grid[new_green_row, green_col] = 3  # Move green above red

    elif len(red_objects) == 1 and red_objects[0]['type'] == 'horizontal_line':
          if len(green_objects) == 1 and green_objects[0]['type'] == 'single_pixel':
            green_row, green_col = green_objects[0]['pixels'][0]
            output_grid[green_row, green_col] = 0   #remove green

    return output_grid