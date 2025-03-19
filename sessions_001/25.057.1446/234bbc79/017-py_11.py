import numpy as np

# The find_objects function from the provided code (copied here for completeness)
def find_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.
    Returns a list of objects, where each object is a list of (row, col) tuples.
    """
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

# Input grids from Train Example 1
input_grid1 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# Input grids from Train Example 2
input_grid2 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 5, 5, 0, 0, 0, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
# run transform from above on the inputs
def transform(input_grid):
    """
    Transforms the input grid according to the refined rule:
    - Gray (5) objects become Azure (8).
    - Azure (8) objects immediately to the right of Gray (5) objects become Magenta (6).
    - No other objects move or change color.
    """
    output_grid = np.copy(input_grid) # Initialize with input
    objects = find_objects(input_grid)

    for obj in objects:
        first_pixel_r, first_pixel_c = obj[0]
        color = input_grid[first_pixel_r, first_pixel_c]

        if color == 5:  # Gray
            for r, c in obj:
                output_grid[r, c] = 8  # Change to Azure
        elif color == 8:  # Azure
            # Check for Gray to the left
            for r,c in obj:
                is_next_to_gray = False
                if any((r, c - 1) == (r_gray, c_gray)
                        for gray_obj in objects
                        for r_gray, c_gray in gray_obj
                        if input_grid[r_gray,c_gray] == 5):
                    is_next_to_gray=True
                    break;
            if is_next_to_gray:
              for r, c in obj:
                output_grid[r,c] = 6

    return output_grid

output_grid1 = transform(input_grid1)
output_grid2 = transform(input_grid2)


objects1 = find_objects(input_grid1)
objects2 = find_objects(input_grid2)

print("Objects in Input Grid 1:")
print(objects1)
print("Objects in Input Grid 2:")
print(objects2)
print("Predicted output 1")
print(output_grid1)
print("Predicted output 2")
print(output_grid2)
