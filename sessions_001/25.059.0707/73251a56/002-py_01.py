"""
The input is a 21x21 grid. The transformation removes specific white (0) colored pixels, primarily those forming internal rectangular or diagonal shapes within a larger magenta (6) region, while preserving the overall structure.
"""

import numpy as np

def get_objects(grid, color):
    """
    Finds contiguous regions (objects) of a specific color in the grid.
    Returns a list of sets, where each set contains the (row, col) coordinates of an object's pixels.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.add((r, c))
        # Explore adjacent cells
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = set()
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects
def transform(input_grid):
    """
    Transforms the input grid by removing specific white pixels.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find white objects
    white_objects = get_objects(output_grid, 0)

    # Iterate through white objects and remove based on conditions
    for obj in white_objects:

        #convert set of tuples to a numpy array of coordinates
        obj_array = np.array(list(obj))

        # Calculate the bounding box of the object.
        min_row = np.min(obj_array[:, 0])
        max_row = np.max(obj_array[:, 0])
        min_col = np.min(obj_array[:, 1])
        max_col = np.max(obj_array[:, 1])
        
        # calculate the height and width of the boundry box
        height = max_row - min_row + 1
        width = max_col - min_col + 1

        # if the object forms a rectangle or diagonal that cover most pixels in
        # the box, replace the white pixel with the underlying color, which is 6 in most cases.
        if len(obj) > (height * width)*.7:
            for r, c in obj:
               output_grid[r,c] = 6

    return output_grid