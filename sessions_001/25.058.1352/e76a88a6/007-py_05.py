import numpy as np

# Provided example 3:
input_grid3 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
    [0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

output_grid3 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 4, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        """Depth-first search to find contiguous pixels of the same color."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append({'color': grid[row, col], 'pixels': obj_pixels})
    return objects

# Find objects in the third example input
objects3 = find_objects(input_grid3)
print(f"Objects in example 3 input: {objects3}")

# Analyze the gray object in example 3.
gray_objects3 = [obj for obj in objects3 if obj['color'] == 5]
for gray_object in gray_objects3:
    min_row = min(pixel[0] for pixel in gray_object['pixels'])
    max_row = max(pixel[0] for pixel in gray_object['pixels'])
    min_col = min(pixel[1] for pixel in gray_object['pixels'])
    max_col = max(pixel[1] for pixel in gray_object['pixels'])

    width = max_col - min_col + 1
    height = max_row - min_row + 1
    print(f"Gray object dimensions: width={width}, height={height}")


#check assumptions about other examples
input_grid1 = np.array([
    [0, 0, 0, 0, 0],
    [0, 5, 5, 5, 0],
    [0, 5, 5, 5, 0],
    [0, 5, 5, 5, 0],
    [0, 0, 0, 0, 0]
])
output_grid1 = np.array([
    [0, 0, 0, 0, 0],
    [0, 2, 2, 4, 0],
    [0, 2, 2, 4, 0],
    [0, 2, 2, 4, 0],
    [0, 0, 0, 0, 0]
])

input_grid2 = np.array([
    [5, 5],
    [5, 5]
])

output_grid2 = np.array([
    [2, 4],
    [2, 4]
])

# Find objects in the first example input
objects1 = find_objects(input_grid1)
print(f"Objects in example 1 input: {objects1}")
# Analyze the gray object
gray_objects1 = [obj for obj in objects1 if obj['color'] == 5]
for gray_object in gray_objects1:
    min_row = min(pixel[0] for pixel in gray_object['pixels'])
    max_row = max(pixel[0] for pixel in gray_object['pixels'])
    min_col = min(pixel[1] for pixel in gray_object['pixels'])
    max_col = max(pixel[1] for pixel in gray_object['pixels'])

    width = max_col - min_col + 1
    height = max_row - min_row + 1
    print(f"Gray object dimensions: width={width}, height={height}")
    
objects2 = find_objects(input_grid2)
print(f"Objects in example 2 input: {objects2}")
gray_objects2 = [obj for obj in objects2 if obj['color'] == 5]
for gray_object in gray_objects2:
    min_row = min(pixel[0] for pixel in gray_object['pixels'])
    max_row = max(pixel[0] for pixel in gray_object['pixels'])
    min_col = min(pixel[1] for pixel in gray_object['pixels'])
    max_col = max(pixel[1] for pixel in gray_object['pixels'])

    width = max_col - min_col + 1
    height = max_row - min_row + 1
    print(f"Gray object dimensions: width={width}, height={height}")