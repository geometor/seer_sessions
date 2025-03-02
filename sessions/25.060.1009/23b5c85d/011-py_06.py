import numpy as np

# Provided example data (replace with actual data from files)
train_task_examples = [
    {
        'input': np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1],
                           [0, 0, 0, 0, 1, 1]]),
        'output': np.array([[1, 1],
                            [1, 1]])
    },
     {
        'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 1, 0],
                           [0, 0, 0, 0, 1, 1, 1, 0]]),
        'output': np.array([[1, 1, 1],
                            [1, 1, 1]])
    },
    {
        'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 0, 0, 1, 0]]),
        'output': np.array([[1],
                            [1]])
    }

]


def find_objects(grid):
    """Finds rectangular objects in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c, color):
        return 0 <= r < rows and 0 <= c < cols and grid[r, c] == color and (r, c) not in visited

    def dfs(r, c, color, object_coords):
        visited.add((r, c))
        object_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc, color):
                dfs(nr, nc, color, object_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r,c] != 0:
                color = grid[r, c]
                object_coords = []
                dfs(r, c, color, object_coords)
                if object_coords:
                    min_r = min(coord[0] for coord in object_coords)
                    max_r = max(coord[0] for coord in object_coords)
                    min_c = min(coord[1] for coord in object_coords)
                    max_c = max(coord[1] for coord in object_coords)
                    objects.append({
                        "color": color,
                        "position": (min_r, min_c),
                        "dimensions": (max_r - min_r + 1, max_c - min_c + 1)
                    })
    return objects

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = example['input']
        expected_output = example['output']
        objects = find_objects(input_grid)

        blue_objects = [obj for obj in objects if obj['color'] == 1]
        largest_blue_object = None
        if blue_objects:
            largest_blue_object = max(blue_objects, key=lambda obj: obj['dimensions'][0] * obj['dimensions'][1])

        results.append({
            'example_index': i,
            'num_blue_objects': len(blue_objects),
            'largest_blue_object_dimensions': largest_blue_object['dimensions'] if largest_blue_object else None,
            'expected_output_shape': expected_output.shape,
            'output_equals_expected': (largest_blue_object['dimensions'] if largest_blue_object else (0,0)) == expected_output.shape[::-1] if len(expected_output.shape) ==2 else False
        })
    return results

analysis_results = analyze_examples(train_task_examples)
for result in analysis_results:
    print(result)