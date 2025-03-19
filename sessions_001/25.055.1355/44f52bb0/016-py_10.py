import numpy as np

train_examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 4, 4, 4, 4, 0],
                           [0, 4, 4, 4, 4, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[1]])
    },
      {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 8, 8, 8, 0, 0],
                          [0, 0, 0, 0, 8, 8, 8, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[8, 8, 8],
                           [8, 8, 8],
                           [8, 8, 8]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output" : np.array([[1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1]])
    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 6, 0, 0, 0],
                           [0, 0, 0, 0, 6, 6, 0, 0, 0],
                           [0, 0, 0, 6, 6, 6, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[5]])

    }

]

def get_object_details(grid):
    """Finds contiguous regions of non-zero pixels and returns their details."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                object_pixels = []
                color = grid[row, col]
                dfs(row, col, color, object_pixels)
                if object_pixels:  # Ensure the object isn't empty
                    min_row = min(p[0] for p in object_pixels)
                    max_row = max(p[0] for p in object_pixels)
                    min_col = min(p[1] for p in object_pixels)
                    max_col = max(p[1] for p in object_pixels)
                    objects.append({
                        'color': color,
                        'size': len(object_pixels),
                        'height': max_row - min_row + 1,
                        'width': max_col - min_col + 1,
                        'bounding_box': (min_row, min_col, max_row, max_col)
                    })
    return objects


for i, example in enumerate(train_examples):
    input_grid = example['input']
    output_grid = example['output']
    input_objects = get_object_details(input_grid)
    output_objects = get_object_details(output_grid) #in case output is meaningful
    print(f"Example {i+1}:")
    print(f"  Input shape: {input_grid.shape}")
    print(f"  Output shape: {output_grid.shape}")
    print(f"  Input unique colors: {np.unique(input_grid)}")
    print(f"  Output unique colors: {np.unique(output_grid)}")
    print(f"  Input objects: {input_objects}")
    print(f" Output objects: {output_objects}")
    print("-" * 20)