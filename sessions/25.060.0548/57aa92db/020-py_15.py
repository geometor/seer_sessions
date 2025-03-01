"""
1.  **Identify Objects:**
    *   Find the blue rectangle at the top of the grid. This rectangle contains a single yellow pixel. This is the "top anchor".
    *   Identify all disconnected azure and yellow shapes.

2.  **Preserve Top Anchor:** The blue rectangle (top anchor) and its inner yellow pixel remain unchanged in the output.

3.  **Combine and Expand within Columns:**
    *   Determine "columns" based on the horizontal extent of the top anchor.
    *   For each azure and yellow shape pair, check for horizontal overlap with each top_anchor column:
        *   If an azure and yellow shape have any horizontal overlap, they are considered to be in the same column.
        * If they are within the same column:
            a.  Combine their bounding boxes into a single bounding box.
            b.  Expand this combined bounding box by one pixel in all directions (up, down, left, right).
            c.  Fill the expanded bounding box with azure.
            d. Restore the original yellow pixels
            e.  Fill the area above the expanded shape with azure, up to the top of the grid, but only within the horizontal bounds of the expanded shape.

4.  **Output:** The final output grid consists of the unchanged top anchor and the newly combined and expanded shapes within their respective columns.
"""

import numpy as np

def find_objects(grid, color):
    """Finds all disconnected objects of a specified color."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                if current_object:
                    # Calculate bounding box
                    min_row = min(current_object, key=lambda p: p[0])[0]
                    max_row = max(current_object, key=lambda p: p[0])[0]
                    min_col = min(current_object, key=lambda p: p[1])[1]
                    max_col = max(current_object, key=lambda p: p[1])[1]
                    objects.append(((min_row, min_col), (max_row, max_col)))
    return objects

def check_horizontal_overlap(box1, box2):
    """Checks if two bounding boxes have horizontal overlap."""
    return not (box1[1][1] < box2[0][1] or box2[1][1] < box1[0][1])


def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the blue rectangle (top anchor)
    blue_objects = find_objects(input_grid, 1)
    if not blue_objects:
        return output_grid  # Return original if no blue object (shouldn't happen in these tasks)
    top_anchor = blue_objects[0]  # Expect only one

    # Find all azure and yellow shapes
    azure_objects = find_objects(input_grid, 8)
    yellow_objects = find_objects(input_grid, 4)

    # Combine and expand within columns
    for azure_box in azure_objects:
        for yellow_box in yellow_objects:
            # Check for horizontal overlap with the top anchor
            if check_horizontal_overlap(top_anchor, azure_box) and check_horizontal_overlap(top_anchor, yellow_box) and check_horizontal_overlap(azure_box, yellow_box):
                # Combine bounding boxes
                combined_top = (min(azure_box[0][0], yellow_box[0][0]), min(azure_box[0][1], yellow_box[0][1]))
                combined_bottom = (max(azure_box[1][0], yellow_box[1][0]), max(azure_box[1][1], yellow_box[1][1]))

                # Expand
                expanded_top = (max(0, combined_top[0] - 1), max(0, combined_top[1] - 1))
                expanded_bottom = (min(output_grid.shape[0] - 1, combined_bottom[0] + 1),
                                  min(output_grid.shape[1] - 1, combined_bottom[1] + 1))

                # Fill expanded area with azure
                for r in range(expanded_top[0], expanded_bottom[0] + 1):
                    for c in range(expanded_top[1], expanded_bottom[1] + 1):
                        output_grid[r, c] = 8

                #  restore original yellow pixels
                for r in range(yellow_box[0][0], yellow_box[1][0] + 1):
                    for c in range(yellow_box[0][1], yellow_box[1][1] + 1):
                        if input_grid[r,c] == 4:
                            output_grid[r, c] = 4

                # Fill above with azure, within bounds
                for r in range(0, expanded_top[0]):
                    for c in range(expanded_top[1], expanded_bottom[1] + 1):
                        output_grid[r, c] = 8

    return output_grid