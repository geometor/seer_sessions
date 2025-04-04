import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the specified color.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == color and not visited[i, j]:
                obj = []
                stack = [(i, j)]
                while stack:
                    r, c = stack.pop()
                    if 0 <= r < rows and 0 <= c < cols and grid[r, c] == color and not visited[r, c]:
                        visited[r, c] = True
                        obj.append((r, c))
                        stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])
                objects.append(obj)
    return objects

def is_l_shape(obj):
    """
    Checks if a given object (list of coordinates) forms an L-shape.
    """
    if len(obj) != 3:
        return False

    obj.sort()  # Sort to make checking easier
    x, y = zip(*obj)

    # Check all 4 possible L-shape orientations
    if (x[0] == x[1] and x[1] + 1 == x[2] and y[0] + 1 == y[1] and y[1] == y[2]) or \
       (x[0] + 1 == x[1] and x[1] == x[2] and y[0] == y[1] and y[1] + 1 == y[2]) or \
       (x[0] == x[1] and x[1] + 1 == x[2] and y[0] == y[1] and y[1] - 1 == y[2]) or \
       (x[0] + 1 == x[1] and x[1] == x[2] and y[0] - 1 == y[1] and y[1] == y[2]):
        return True

    return False
    
def find_insertion_point(obj):
    """
    Finds the coordinates where the blue pixel should be inserted.
    """
    obj.sort()  # Sort for consistent checking
    x, y = zip(*obj)

    # Check the four possible L shapes and their corresponding insertion points
    if x[0] == x[1] and x[1] + 1 == x[2] and y[0] + 1 == y[1] and y[1] == y[2]:
        return (x[0], y[0])  # top left
    elif x[0] + 1 == x[1] and x[1] == x[2] and y[0] == y[1] and y[1] + 1 == y[2]:
        return (x[0], y[2]) # top right
    elif x[0] == x[1] and x[1] + 1 == x[2] and y[0] == y[1] and y[1] - 1 == y[2]:
        return (x[0],y[0]) # bottom left
    elif x[0] + 1 == x[1] and x[1] == x[2] and y[0] - 1 == y[1] and y[1] == y[2]:
        return (x[2],y[2]) # bottom right

    return None

def transform(input_grid):
    output_grid = np.copy(input_grid)
    azure_objects = find_objects(input_grid, 8)

    for obj in azure_objects:
        if is_l_shape(obj):
            insertion_point = find_insertion_point(obj)
            if insertion_point:
                x, y = insertion_point
                # Make sure we are inside the limits of the grid
                if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:
                   output_grid[x, y] = 1

    return output_grid