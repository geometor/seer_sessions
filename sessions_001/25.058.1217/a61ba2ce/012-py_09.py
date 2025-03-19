import numpy as np

task_examples = [
    { # example 1: pass
        "input": np.array([[4, 4, 4, 0, 0, 0, 0, 0, 0],
                           [4, 4, 4, 0, 0, 6, 6, 6, 6],
                           [4, 4, 4, 0, 0, 6, 6, 6, 6],
                           [0, 0, 0, 0, 0, 6, 6, 6, 6],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 2, 2, 0, 0, 8],
                           [1, 1, 1, 0, 2, 2, 0, 8, 8],
                           [0, 1, 0, 0, 2, 2, 0, 8, 8],
                           [0, 0, 0, 0, 0, 0, 0, 8, 8]]),
        "output": np.array([[1, 0, 8, 0],
                            [1, 0, 8, 8],
                            [4, 4, 2, 0],
                            [4, 4, 2, 0]])

    },
        { # example 2: fail
        "input": np.array([[0, 0, 0, 5, 5, 5, 0, 0, 0],
                           [0, 8, 8, 5, 5, 5, 6, 6, 0],
                           [0, 8, 8, 5, 5, 5, 6, 6, 0],
                           [0, 8, 8, 0, 0, 0, 6, 6, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 4, 0, 0, 0, 0, 0, 0],
                           [0, 4, 4, 4, 0, 0, 0, 1, 0],
                           [0, 0, 4, 0, 0, 0, 1, 1, 1]]),
        "output": np.array([[1, 8],
                            [4, 0]])
    },
        { # example 3: fail
        "input": np.array([[7, 7, 7, 7, 7, 7, 7, 7, 7],
                           [7, 7, 7, 7, 7, 7, 7, 7, 7],
                           [7, 7, 7, 7, 7, 7, 7, 7, 7],
                           [7, 7, 7, 7, 7, 7, 7, 7, 7],
                           [7, 7, 7, 7, 7, 7, 7, 7, 7],
                           [7, 7, 7, 7, 7, 7, 7, 7, 7],
                           [7, 7, 7, 7, 7, 7, 7, 7, 7],
                           [7, 7, 7, 7, 7, 7, 7, 7, 7],
                           [7, 7, 7, 7, 7, 7, 7, 7, 7]]),
        "output": np.array([[7]])
    }
]

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
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
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                if obj_pixels:
                    objects.append({'color': grid[row, col], 'pixels': obj_pixels})
    return objects

def get_bounding_box(pixels):
    """Calculates the bounding box for a set of pixels."""
    if not pixels:
        return None
    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)
    return (min_row, min_col), (max_row, max_col)
    
for i, example in enumerate(task_examples):
    input_grid = example['input']
    output_grid = example['output']
    
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)
    
    
    print(f"Example {i+1}:")
    print(f"  Input Grid Size: {input_grid.shape}")
    print(f"  Output Grid Size: {output_grid.shape}")
    print(f"  Input Objects: {len(input_objects)}")
    for obj in input_objects:
        color = obj['color']
        pixels = obj['pixels']
        bounding_box = get_bounding_box(pixels)
        print(f"    Color: {color}, Bounding Box: {bounding_box}")
    print(f"  Output Objects: {len(output_objects)}")
    for obj in output_objects:
        color = obj['color']
        pixels = obj['pixels']
        bounding_box = get_bounding_box(pixels)
        print(f"    Color: {color}, Bounding Box: {bounding_box}")
