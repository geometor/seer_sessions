import numpy as np
from skimage.measure import label, regionprops

def get_bounding_box(grid):
    """
    Finds the smallest bounding box that encloses all non-white pixels.
    Returns (min_row, min_col, max_row, max_col)
    """
    rows, cols = len(grid), len(grid[0])
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0:  # Not white
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    return min_row, min_col, max_row, max_col

def get_largest_object_metrics(grid):
    """
    Finds the largest connected component (excluding white) and its metrics.
    """
    grid_np = np.array(grid)
    labeled_grid = label(grid_np != 0, connectivity=1)  # Consider only non-white pixels
    regions = regionprops(labeled_grid)

    if not regions:  # handle empty case (all white)
        return {
            'area': 0,
            'bbox': (0, 0, 0, 0),
            'coords': [],
            'label': 0,
        }
    
    largest_region = max(regions, key=lambda region: region.area)
    
    return {
            'area': largest_region.area,
            'bbox': largest_region.bbox, # (min_row, min_col, max_row, max_col)
            'coords': largest_region.coords,
            'label' : largest_region.label
            }

def analyze_example(input_grid, expected_output, actual_output):
    """Analyzes a single example."""
    
    input_metrics = get_largest_object_metrics(input_grid)
    expected_metrics = get_largest_object_metrics(expected_output)
    actual_metrics = get_largest_object_metrics(actual_output)
    input_bbox = get_bounding_box(input_grid)


    analysis = {
        'input': {
            'largest_object_area': input_metrics['area'],
            'largest_object_bbox': input_metrics['bbox'],
            'largest_object_label': input_metrics['label'],
            'bounding_box' : input_bbox,
            'shape': (len(input_grid), len(input_grid[0])),

        },
        'expected': {
            'largest_object_area': expected_metrics['area'],
            'largest_object_bbox': expected_metrics['bbox'],
            'shape': (len(expected_output), len(expected_output[0])),
        },
        'actual': {
            'largest_object_area': actual_metrics['area'],
            'largest_object_bbox': actual_metrics['bbox'],            
            'shape': (len(actual_output), len(actual_output[0])),
        },
    }
    return analysis


# Example usage (replace with actual example data)
task_data = {
  "train": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[2, 2, 2], [2, 2, 2], [2, 2, 2]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 4, 0, 0, 0], [0, 0, 0, 0, 4, 4, 0, 0, 0], [0, 0, 0, 0, 4, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[4, 4], [4, 4]]
    },
      {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 6, 6, 6, 6, 6, 0],
                [0, 0, 0, 6, 6, 6, 6, 6, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[6, 6, 6, 6, 6], [6, 6, 6, 6, 6]]
    }
  ]
}

results = []
for example in task_data['train']:
  input_grid = example['input']
  expected_output = example['output']
  actual_output = transform(input_grid)
  analysis = analyze_example(input_grid, expected_output, actual_output)
  results.append(analysis)

import json
print(json.dumps(results, indent=2))