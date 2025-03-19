"""
1.  **Identify Blue Objects:** Locate all contiguous blue (1) objects within the grid.

2.  **Check for Magenta:** If a magenta (6) pixel exists anywhere in the grid, find *any* blue object and change all pixels in *that* blue object to magenta (6). If there are multiple or zero magenta pixels, choose any one.

3.  **Check for Azure:** If an azure (8) pixel exists anywhere in the grid, find *any* blue object and change all pixels in *that* blue object to azure (8). If there are multiple or zero azure pixels, , choose any one.

4.  **Priority:** It's unclear from the current data which rule (magenta or azure) takes precedence if both apply.  We'll assume *any* blue object may be changed, but we will need more data to clarify a selection strategy if multiple blue objects are present. For now, if both 6 and 8, we choose any blue object, and update it with the appropriate value.

5.  **All other pixels remain unchanged.**
"""

import numpy as np

def get_all_blue_objects(grid):
    """Gets a list of all contiguous blue objects in the grid."""
    rows, cols = grid.shape
    visited = set()
    blue_objects = []

    def get_object(start_row, start_col):
        """Helper function to retrieve single object starting at cell"""
        if grid[start_row, start_col] != 1:
            return set()

        visited_inner = set()
        queue = [(start_row, start_col)]
        object_coords = set()

        while queue:
            row, col = queue.pop(0)
            if (row, col) in visited_inner:
                continue
            visited_inner.add((row, col))
            
            if grid[row, col] == 1:
                object_coords.add((row, col))
                if row > 0:
                    queue.append((row - 1, col))
                if row < rows - 1:
                    queue.append((row + 1, col))
                if col > 0:
                    queue.append((row, col - 1))
                if col < cols - 1:
                    queue.append((row, col + 1))
        return object_coords
        
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 1 and (r,c) not in visited:
                obj = get_object(r, c)
                blue_objects.append(obj)
                visited.update(obj) # mark all cells in object as visited
    return blue_objects

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify all blue objects
    blue_objects = get_all_blue_objects(output_grid)

    # Check for Magenta
    magenta_exists = np.any(output_grid == 6)
    if magenta_exists and blue_objects:
        # replace any blue object with magenta
        chosen_object = blue_objects.pop() # remove and get one
        for r, c in chosen_object:
            output_grid[r, c] = 6

    # Check for Azure
    azure_exists = np.any(output_grid == 8)
    if azure_exists and blue_objects:
        # replace any blue object with azure
        chosen_object = blue_objects.pop()  # remove and get one
        for r, c in chosen_object:
            output_grid[r, c] = 8

    return output_grid