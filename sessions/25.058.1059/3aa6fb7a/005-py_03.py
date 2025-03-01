import numpy as np

def describe_grid(grid):
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.count_nonzero(grid == color) for color in unique_colors}
    return {
        'rows': rows,
        'cols': cols,
        'unique_colors': unique_colors.tolist(),
        'color_counts': color_counts
    }

def find_objects(grid, color):
    # Find all objects of a specific color in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == color and not visited[i, j]:
                object_pixels = []
                stack = [(i, j)]
                visited[i, j] = True

                while stack:
                    x, y = stack.pop()
                    object_pixels.append((x, y))

                    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                    for nx, ny in neighbors:
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx, ny] == color and not visited[nx, ny]:
                            stack.append((nx, ny))
                            visited[nx, ny] = True
                objects.append(object_pixels)
    return objects

def object_metrics(obj):
    min_x = min(p[0] for p in obj)
    max_x = max(p[0] for p in obj)
    min_y = min(p[1] for p in obj)
    max_y = max(p[1] for p in obj)
    return {
        'min_row': min_x,
        'max_row': max_x,
        'min_col': min_y,
        'max_col': max_y,
        'height': max_x - min_x + 1,
        'width' : max_y - min_y + 1
    }


task_data = {
    'train': [
        {
            'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
            'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        },
        {
            'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 8, 8, 8, 8, 8, 8, 0, 0],
                               [0, 8, 8, 8, 8, 8, 8, 0, 0],
                               [0, 8, 8, 8, 8, 8, 8, 0, 0],
                               [0, 8, 8, 8, 8, 8, 8, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
            'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 8, 8, 8, 8, 8, 8, 0, 0],
                                [0, 8, 8, 8, 8, 8, 8, 0, 0],
                                [0, 8, 8, 8, 8, 8, 8, 0, 0],
                                [0, 0, 0, 0, 0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0]])
        },
        {
            'input': np.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 8, 8, 8, 8, 8, 0],
                               [0, 8, 8, 8, 8, 8, 0],
                               [0, 8, 8, 8, 8, 8, 0],
                               [0, 0, 0, 0, 0, 0, 0]]),
            'output': np.array([[0, 0, 0, 0, 0, 0, 0],
                                [0, 8, 8, 8, 8, 8, 0],
                                [0, 8, 8, 8, 8, 8, 0],
                                [0, 0, 0, 0, 0, 1, 0],
                                [0, 0, 0, 0, 0, 0, 0]])
        },
                {
            'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
            'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                                [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                                [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                                [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        },
        {
            'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
            'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                                [0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        }
    ]
}

for i, example in enumerate(task_data['train']):
    input_grid = example['input']
    output_grid = example['output']

    input_desc = describe_grid(input_grid)
    output_desc = describe_grid(output_grid)
    
    azure_objects_input = find_objects(input_grid, 8)
    azure_objects_output = find_objects(output_grid, 8)

    print(f"Example {i+1}:")
    print(f"  Input Grid: {input_desc}")
    print(f"  Output Grid: {output_desc}")
    print(f" Azure objects in input")
    for j, obj in enumerate(azure_objects_input):
      print(f"  Object {j}: {object_metrics(obj)}")    
    print(f" Azure objects in output")
    for j, obj in enumerate(azure_objects_output):
      print(f"  Object {j}: {object_metrics(obj)}")

    diff = output_grid - input_grid
    changed_pixels = np.where(diff != 0)
    print(f"  Changed Pixels: {list(zip(changed_pixels[0], changed_pixels[1]))}")
    print("---")