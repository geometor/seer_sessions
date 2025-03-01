import numpy as np

train = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 2, 0, 2, 0, 2, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2], [0, 2, 0, 2, 0, 2, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0]],
        "output": [[4, 0, 4, 0, 4, 0, 4, 0, 4]]
    },
    {
        "input": [[6, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5]],
        "output": [[6], [3], [5]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0]],
        "output": [[4]]
    }
]

def find_objects(grid):
    """Identifies distinct objects (contiguous regions of same color) in a grid."""
    grid = np.array(grid)
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color):
        """Depth-first search to find all pixels of a contiguous object."""
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return []
        visited[row, col] = True
        object_pixels = [(row, col)]
        object_pixels.extend(dfs(row + 1, col, color))
        object_pixels.extend(dfs(row - 1, col, color))
        object_pixels.extend(dfs(row, col + 1, color))
        object_pixels.extend(dfs(row, col - 1, color))
        return object_pixels

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col]:
                color = grid[row, col]
                object_pixels = dfs(row, col, color)
                if object_pixels:
                    objects.append((color, object_pixels))
    return objects

for i, example in enumerate(train):
    input_grid = example['input']
    output_grid = example['output']
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    print(f"Example {i+1}:")
    print(f"  Input objects: {input_objects}")    
    print(f" Output objects: {output_objects}")
    input_shapes = []
    for color, pixels in input_objects:
        rows = [p[0] for p in pixels]
        cols = [p[1] for p in pixels]
        height = max(rows) - min(rows) + 1
        width = max(cols) - min(cols) + 1
        input_shapes.append((color, height, width))    
    print(f"  Input object shapes (color, height, width): {input_shapes}")

    output_shapes = []
    for color, pixels in output_objects:
        rows = [p[0] for p in pixels]
        cols = [p[1] for p in pixels]
        height = max(rows) - min(rows) + 1
        width = max(cols) - min(cols) + 1
        output_shapes.append((color, height, width))
    print(f" Output object shapes (color, height, width): {output_shapes}")
    print("-" * 40)