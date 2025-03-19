import numpy as np
from collections import Counter

def get_objects(grid):
    """Identifies contiguous objects of the same color in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj_pixels):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                obj_pixels = []
                dfs(row, col, color, obj_pixels)
                if obj_pixels:
                    objects.append({
                        'color': color,
                        'pixels': obj_pixels,
                        'size': len(obj_pixels),
                        'bbox': (min(p[0] for p in obj_pixels), min(p[1] for p in obj_pixels),
                                 max(p[0] for p in obj_pixels), max(p[1] for p in obj_pixels))
                    })
    return objects

def analyze_example(input_grid, output_grid):
    """Analyzes an input-output pair and returns object-based metrics."""
    input_objects = get_objects(input_grid)
    output_objects = get_objects(output_grid)

    input_object_counts = Counter([(obj['color'], obj['size']) for obj in input_objects])
    output_object_counts = Counter([(obj['color'], obj['size']) for obj in output_objects])

    return {
        'input_objects': input_objects,
        'output_objects': output_objects,
        'input_object_counts': input_object_counts,
        'output_object_counts': output_object_counts,
        'diff_counts': input_object_counts - output_object_counts,
        'input_colors': set([o['color'] for o in input_objects]),
        'output_colors': set([o['color'] for o in output_objects]),
    }
# Example Usage and Test (assuming train_in, train_out are lists of input/output grids
train_in = [
    np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    np.array([[8, 8, 8, 0, 8, 8, 8],
              [8, 8, 8, 0, 8, 8, 8],
              [8, 8, 8, 0, 8, 8, 8],
              [0, 0, 0, 0, 0, 0, 0],
              [8, 8, 8, 0, 8, 8, 8],
              [8, 8, 8, 0, 8, 8, 8],
              [8, 8, 8, 0, 8, 8, 8]]),
    np.array([[5, 0, 5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0, 5, 0],
              [5, 0, 5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0, 5, 0],
              [5, 0, 5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0, 5, 0],
              [5, 0, 5, 0, 5, 0, 5]])
    ]
train_out = [
    np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    np.array([[8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8]]),
    np.array([[5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5]])
]

for i, (input_grid, output_grid) in enumerate(zip(train_in, train_out)):
    analysis = analyze_example(input_grid, output_grid)
    print(f"Example {i+1}:")
    #print(f"  Input Objects: {analysis['input_objects']}")
    #print(f"  Output Objects: {analysis['output_objects']}")
    print(f"  Input Object Counts (color, size): {analysis['input_object_counts']}")
    print(f"  Output Object Counts (color, size): {analysis['output_object_counts']}")
    print(f"  Difference in Counts: {analysis['diff_counts']}")
    print(f"Input Colors: {analysis['input_colors']}")
    print(f"Output Colors: {analysis['output_colors']}")
    print("-" * 20)