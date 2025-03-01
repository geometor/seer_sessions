import numpy as np
from collections import Counter

def grid_metrics(grid):
    """Calculates and returns metrics for a given grid."""
    metrics = {}
    
    # Basic dimensions
    metrics['rows'] = grid.shape[0]
    metrics['cols'] = grid.shape[1]
    
    # Pixel counts
    pixel_counts = Counter(grid.flatten())
    metrics['pixel_counts'] = dict(pixel_counts)  # Convert Counter to a regular dict
    
    # Find contiguous objects (simplified version)
    objects = []
    visited = set()
    
    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if (r, c) not in visited:
                obj = []
                dfs(r, c, grid[r, c], obj)
                if obj:
                    objects.append({'color': grid[r, c], 'pixels': obj, 'count':len(obj)})

    metrics['objects'] = objects
    return metrics

def compare_metrics(input_grid, output_grid):
    """Compares metrics between input and output grids."""
    input_metrics = grid_metrics(input_grid)
    output_metrics = grid_metrics(output_grid)

    comparison = {
      'input': input_metrics,
      'output': output_metrics
    }

    return comparison

# Example Usage with example data (replace with your actual data)
# Example grids (replace with actual data loading)

example_grids = {
'example_0': {
        'input': np.array([[6, 5, 1, 2, 2, 6, 6, 5, 7, 7],
                           [6, 5, 5, 5, 5, 5, 6, 2, 2, 2],
                           [6, 5, 1, 2, 8, 5, 2, 2, 2, 5]]),
        'output': np.array([[6, 5, 1, 6, 6, 2, 6, 5, 7, 7],
                            [6, 5, 5, 5, 5, 5, 2, 2, 2, 2],
                            [6, 5, 1, 6, 8, 5, 2, 2, 2, 5]]),
    },
    'example_1': {
       'input':  np.array([[6, 5, 5, 5, 5, 5, 6, 2, 2, 2],
                    [6, 5, 1, 2, 2, 6, 6, 5, 7, 7],
                    [6, 5, 1, 2, 8, 5, 2, 2, 2, 5]]),
       'output': np.array([[6, 5, 5, 5, 5, 5, 2, 2, 2, 2],
                    [6, 5, 1, 6, 6, 2, 6, 5, 7, 7],
                    [6, 5, 1, 6, 8, 5, 2, 2, 2, 5]]),
    },
    'example_2': {
        'input': np.array([[0, 0, 0, 6, 2, 0, 0, 0, 0, 0],
                [0, 0, 6, 6, 2, 2, 0, 0, 0, 0],
                [0, 6, 5, 5, 2, 2, 2, 0, 0, 0],
                [6, 6, 0, 5, 5, 5, 2, 2, 0, 0],
                [6, 5, 0, 0, 0, 5, 5, 5, 5, 0],
                [5, 5, 5, 0, 0, 0, 0, 5, 5, 5],
                [5, 5, 5, 0, 0, 0, 0, 5, 5, 5],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        'output':np.array([[0, 0, 0, 2, 6, 0, 0, 0, 0, 0],
                    [0, 0, 6, 2, 6, 2, 0, 0, 0, 0],
                    [0, 6, 5, 5, 6, 2, 2, 0, 0, 0],
                    [6, 6, 0, 5, 5, 5, 2, 2, 0, 0],
                    [6, 5, 0, 0, 0, 5, 5, 5, 5, 0],
                    [5, 5, 5, 0, 0, 0, 0, 5, 5, 5],
                    [5, 5, 5, 0, 0, 0, 0, 5, 5, 5],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    }
}

results = {}
for example, grids in example_grids.items():
    results[example] = compare_metrics(grids['input'], grids['output'])

import json
print(json.dumps(results, indent=2))
