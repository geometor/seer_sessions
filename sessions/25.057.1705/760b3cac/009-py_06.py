import numpy as np

def analyze_grid(grid):
    dims = grid.shape
    azure_count = np.count_nonzero(grid == 8)
    yellow_count = np.count_nonzero(grid == 4)
    white_count = np.count_nonzero(grid == 0)
    return dims, azure_count, yellow_count, white_count

def compare_grids(grid1, grid2):
    if grid1.shape != grid2.shape:
        return False, -1
    diff_count = np.count_nonzero(grid1 != grid2)
    return diff_count == 0, diff_count

train_data = [
    {
        "input": np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                           [0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                           [0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0]]),
        "output": np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
    },
    {
        "input": np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                           [0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                           [0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                           [0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0]]),
        "output": np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
    },
    {
        "input": np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                           [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
                           [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
                           [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0]]),
        "output": np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
    }
]

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Check if azure (8) exists in the objects
    if 8 not in objects:
        return output_grid

    # Iterate through each azure object
    for azure_object in objects[8]:
        # Create a set for quick pixel lookup
        azure_pixels = set(azure_object)
        
        # Iterate through the azure pixels to find pairs and apply fill rule
        for row, col in azure_pixels:
            #check for pairs
            if (row, col + 1) in azure_pixels:
                #check for white to the right
                if col + 2 < output_grid.shape[1] and output_grid[row, col + 2] == 0:
                    output_grid[row, col + 2] = 8
            

    return output_grid


def find_objects(grid):
    """
    Finds contiguous blocks of pixels with the same color.
    Returns a dictionary of objects, keyed by color.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
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
            if not visited[row, col]:
                color = grid[row, col]
                obj_pixels = []
                dfs(row, col, color, obj_pixels)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_pixels)
    return objects

results = []
for i, example in enumerate(train_data):
    input_grid = example["input"]
    expected_output = example["output"]
    transformed_grid = transform(input_grid)

    input_analysis = analyze_grid(input_grid)
    output_analysis = analyze_grid(expected_output)
    transformed_analysis = analyze_grid(transformed_grid)

    success, diff_count = compare_grids(expected_output, transformed_grid)

    results.append({
        "example": i + 1,
        "input_dims": input_analysis[0],
        "input_azure": input_analysis[1],
        "input_yellow": input_analysis[2],
        "input_white": input_analysis[3],
        "output_dims": output_analysis[0],
        "output_azure": output_analysis[1],
        "output_yellow": output_analysis[2],
        "output_white": output_analysis[3],
        "transformed_dims": transformed_analysis[0],
        "transformed_azure": transformed_analysis[1],
        "transformed_yellow": transformed_analysis[2],
        "transformed_white": transformed_analysis[3],
        "success": success,
        "diff_count": diff_count
    })

for result in results:
    print(result)