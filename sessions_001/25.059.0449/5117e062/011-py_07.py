import numpy as np
from collections import Counter

def count_objects(grid, color):
    """Counts distinct objects of a given color."""
    visited = set()
    count = 0

    def dfs(row, col):
        """Depth-first search to find contiguous regions."""
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited and grid[row, col] == color:
                dfs(row, col)
                count += 1
    return count

def analyze_example(input_grid, output_grid, color=3):
    """Analyzes a single input-output pair."""
    input_objects = count_objects(input_grid, color)
    output_objects = count_objects(output_grid, color)

    green_coords = np.argwhere(input_grid == color)
    if len(green_coords) == 0:
        bbox_match = False
        size_match = False
        input_bbox = None
        output_size = None
        
    else:
      min_row, max_row, min_col, max_col = bounding_box(green_coords)
      input_bbox = (max_row - min_row + 1, max_col - min_col + 1)

      output_green_coords = np.argwhere(output_grid == 3)

      if(len(output_green_coords) == 0):
        bbox_match = False
        size_match = False
        input_bbox = None
        output_size = None
      else:
        min_row_out, max_row_out, min_col_out, max_col_out = bounding_box(output_green_coords)
        output_size = (max_row_out - min_row_out + 1, max_col_out - min_col_out + 1)

        bbox_match = (input_objects == output_objects) and np.array_equal(np.argwhere(input_grid[min_row:max_row+1, min_col:max_col+1] == 3), np.argwhere(output_grid[min_row_out:max_row_out+1, min_col_out:max_col_out+1] == 3))
        size_match = input_bbox == output_size


    return {
        "input_objects": input_objects,
        "output_objects": output_objects,
        "bbox_match": bbox_match,
        "size_match": size_match,
        "input_bbox": input_bbox,
        "output_size": output_size
    }

# Example Usage (replace with actual input/output grids)
# provided by the ARC task
task_data = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [3]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [3],
        [3],
        [3]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 3, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [3, 3, 3]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [3, 3],
        [3, 3]
      ]
    }
  ]
}

results = []
for example in task_data['train']:
  input_grid = np.array(example['input'])
  output_grid = np.array(example['output'])
  analysis = analyze_example(input_grid, output_grid)
  results.append(analysis)

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Objects: {result['input_objects']}")
    print(f"  Output Objects: {result['output_objects']}")
    print(f"  Bounding Box Match: {result['bbox_match']}")
    print(f"  Size Match: {result['size_match']}")
    print(f"  Input BBox size: {result['input_bbox']}")
    print(f"  Output size: {result['output_size']}")