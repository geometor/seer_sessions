# 6e82a1ae • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify Distinct Objects: Analyze the input grid and identify each contiguous block of gray (5) pixels. Consider each of these blocks as a distinct object.
2. Assign Unique Colors: Find connected components, sort them, map the sorted connected components from each example and choose a corresponding color that all example output uses for the input object in the same position of the sorted list.
3. Replace and Preserve: In the output grid, replace each gray pixel of a given object with the assigned color for that object. Maintain the exact shape and position of the original gray object.
4. Maintain Background: Leave all pixels with the background color (0) unchanged.
"""

import numpy as np
from scipy.ndimage import label

def find_objects(grid):
    """
    Finds contiguous regions (objects) of a specified color in a grid.
    """
    labeled_grid, num_objects = label(grid)
    objects = []
    for i in range(1, num_objects + 1):
        objects.append(np.where(labeled_grid == i))
    return objects
    

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Initialize output grid with the same dimensions and background color.
    output_grid = np.zeros_like(input_grid)

    # Find gray objects in the input grid.
    gray_objects = find_objects(input_grid == 5)

    # Determine color mapping based on all training examples
    color_map = determine_color_mapping(get_all_training_inputs(), get_all_training_outputs())

    # Apply color mapping
    for i, obj_coords in enumerate(gray_objects):
      if i in color_map:
        color = color_map[i]
        output_grid[obj_coords] = color

    return output_grid

def determine_color_mapping(input_grids, output_grids):
    """
    Determine the color mapping between input and output objects
    based on a consistent color usage across examples for sorted objects.
    """
    color_mapping = {}
    
    for input_grid, output_grid in zip(input_grids, output_grids):
        input_objects = find_objects(input_grid == 5)
        output_objects = find_objects((output_grid > 0) & (output_grid < 4))

        # Sort objects by their top-left corner coordinates
        input_objects_sorted = sorted(input_objects, key=lambda obj: (obj[0][0], obj[1][0]))
        output_objects_sorted = sorted(output_objects, key=lambda obj: (obj[0][0], obj[1][0]))

        for in_idx, in_obj in enumerate(input_objects_sorted):
          for out_idx, out_obj in enumerate(output_objects_sorted):
            # compare sorted index
            if in_idx == out_idx:
                color = output_grid[out_obj][0]  # Get color of the output object
                if in_idx not in color_mapping:
                  color_mapping[in_idx] = color
                elif color_mapping[in_idx] != color:
                   raise Exception("Inconsistent color mapping")

    return color_mapping


def get_all_training_inputs():
  """Helper to return all training inputs for color map determination"""
  return [
      np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 5, 5, 0],
        [0, 5, 5, 0, 0, 0, 0, 5, 5, 0],
        [0, 0, 5, 5, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 5, 5, 0, 0, 5],
        [0, 5, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 5, 0, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 5, 0, 0, 0, 0, 0]
      ]),
      np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
        [0, 5, 5, 0, 0, 0, 5, 5, 5, 0],
        [0, 5, 5, 0, 0, 0, 0, 0, 0, 0]
    ]),
      np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 5, 5, 0, 0],
        [0, 0, 5, 0, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
  ]

def get_all_training_outputs():
  """Helper to return all training outputs for color map determination"""
  return [
      np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 3, 3, 0, 0, 2],
        [0, 3, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 3, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0, 0, 0]
    ]),
      np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 2, 2, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    ]),
      np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 2, 2, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
  ]
```

