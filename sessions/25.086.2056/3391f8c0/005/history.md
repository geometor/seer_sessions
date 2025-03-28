
Previous Code:
```python
import numpy as np

"""
Transformation Rule:
1. Identify the two unique non-white pixel values (colors) present in the input grid. Let these be color1 and color2.
2. Create an output grid of the same dimensions as the input grid, initialized entirely with the background color (white, 0).
3. Find all coordinates (row, column) in the input grid where the pixel value is color1.
4. Find all coordinates (row, column) in the input grid where the pixel value is color2.
5. For each coordinate originally containing color1 in the input grid, set the corresponding pixel in the output grid to color2.
6. For each coordinate originally containing color2 in the input grid, set the corresponding pixel in the output grid to color1.
7. Return the completed output grid. White pixels remain unchanged because they are the initial state of the output grid and are not targeted by the color-swapping steps.
"""


def find_non_white_colors(grid_np):
    """
    Finds the unique non-white (non-zero) colors in a numpy grid.

    Args:
        grid_np: A numpy array representing the grid.

    Returns:
        A list of unique non-white colors found in the grid.
        Returns an empty list if no non-white colors are found.
    """
    unique_values = np.unique(grid_np)
    non_white_colors = unique_values[unique_values != 0]
    return non_white_colors.tolist()

def transform(input_grid):
    """
    Swaps the colors associated with the locations of the two non-white colors
    found in the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid with the colors swapped
        based on their original locations. White pixels remain unchanged.
        If fewer or more than two non-white colors are present, the original
        grid is returned.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)

    # Find the unique non-white colors in the input grid
    non_white_colors = find_non_white_colors(input_np)

    # Check if exactly two non-white colors were found
    if len(non_white_colors) != 2:
        # If not exactly two, return the original grid as a list of lists
        # This aligns with the observation that all valid examples have two colors.
        return input_np.tolist()

    color1, color2 = non_white_colors[0], non_white_colors[1]

    # Create the output grid, initialized with white (0) pixels
    output_np = np.zeros_like(input_np)

    # Find the coordinates (indices) where color1 is present in the input
    # np.where returns a tuple of arrays (one for row indices, one for col indices)
    coords_color1 = np.where(input_np == color1)

    # Find the coordinates (indices) where color2 is present in the input
    coords_color2 = np.where(input_np == color2)

    # Apply the swap in the output grid:
    # At the locations where the input had color1, set the output to color2
    output_np[coords_color1] = color2

    # At the locations where the input had color2, set the output to color1
    output_np[coords_color2] = color1

    # White pixels (0) remain unchanged as they were the initial value of output_np
    # and were not overwritten by the steps above.

    # Convert the resulting numpy array back to a list of lists for the final output
    return output_np.tolist()

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 3 0 3 0 0
0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 8 0 0 0
0 8 8 8 0 8 8 8 0 0
0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 8 0 8 0 8 0 8 0 0
0 0 8 0 0 0 8 0 0 0
0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 15
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 33.333333333333314

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 2 2 0 2 2 0 0 0
0 2 0 0 2 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 3 0 0 0
0 0 0 0 2 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 3 0 0 3 0 0 0
0 3 3 0 3 3 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 2 2 0 0 0
0 0 0 0 3 3 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 3 3 0 3 3 0 0 0
0 3 0 0 3 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 2 0 0 0
0 0 0 0 3 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 9.259259259259252

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 1 0 0 1 0 0 0 7 0
0 0 1 0 0 1 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 7 0 1 0 0
0 7 0 0 7 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 7 0 0 7 0 0 0 1 0
0 0 7 0 0 7 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 18.181818181818173

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 8 8 8 0 0 0 0
0 0 8 0 0 0 0 1 1 1 0 0 0 0 8 0 0
0 8 8 8 0 0 0 0 1 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0
0 1 1 1 0 0 0 0 8 0 0 0 0 1 1 1 0
0 0 1 0 0 0 0 8 8 8 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 0
0 0 1 0 0 0 0 8 8 8 0 0 0 0 1 0 0
0 1 1 1 0 0 0 0 8 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 15.686274509803923
## General Assessment

The previous code implemented a simple color swap: pixels of color A became color B, and pixels of color B became color A, *at their original coordinates*. The results clearly show this is incorrect. The transformation does not happen pixel-wise in place but involves the concept of "objects" or "shapes".

The core misunderstanding was treating the transformation as a simple color value replacement rather than an operation on geometric objects. The provided examples demonstrate that shapes associated with one color move to the locations previously occupied by the shapes of the other color.

The strategy to resolve the errors involves:
1.  Identifying the distinct contiguous shapes (objects) formed by each of the two non-background colors in the input grid.
2.  Determining the unique shape pattern associated with each color.
3.  Identifying the anchor points (e.g., top-left corner of the bounding box) for each instance of these shapes in the input grid.
4.  Constructing the output grid by drawing the shape associated with the *first* color (using its color) at the anchor points originally occupied by the *second* color's shapes, and vice-versa.

## Metrics and Object Analysis

Based on visual inspection and confirmed by code execution, here's an analysis focusing on objects:



*code_execution:*
```python
import numpy as np
from scipy.ndimage import label, find_objects
import json

def analyze_example(input_grid):
    input_np = np.array(input_grid)
    unique_colors = np.unique(input_np)
    non_bg_colors = unique_colors[unique_colors != 0]

    if len(non_bg_colors) != 2:
        return {"error": "Requires exactly two non-background colors."}

    # Ensure consistent color order if needed, e.g., sort numerically
    non_bg_colors.sort()
    color1, color2 = non_bg_colors[0], non_bg_colors[1]

    results = {"color1": int(color1), "color2": int(color2), "objects": []}

    # Process color1
    labeled_grid1, num_labels1 = label(input_np == color1)
    objects1_slices = find_objects(labeled_grid1)
    shape1_pattern = None
    for i, slc in enumerate(objects1_slices):
        obj_grid = (input_np[slc] == color1) # Extract boolean pattern
        if shape1_pattern is None:
             # Store relative coordinates of the first object found
             coords = np.argwhere(obj_grid)
             shape1_pattern = coords.tolist()

        results["objects"].append({
            "original_color": int(color1),
            "top_left": (slc[0].start, slc[1].start),
            "shape_dims": obj_grid.shape
        })
    results["shape1_pattern_relative_coords"] = shape1_pattern

    # Process color2
    labeled_grid2, num_labels2 = label(input_np == color2)
    objects2_slices = find_objects(labeled_grid2)
    shape2_pattern = None
    for i, slc in enumerate(objects2_slices):
        obj_grid = (input_np[slc] == color2) # Extract boolean pattern
        if shape2_pattern is None:
             # Store relative coordinates of the first object found
             coords = np.argwhere(obj_grid)
             shape2_pattern = coords.tolist()

        results["objects"].append({
            "original_color": int(color2),
            "top_left": (slc[0].start, slc[1].start),
            "shape_dims": obj_grid.shape
        })
    results["shape2_pattern_relative_coords"] = shape2_pattern

    return results

# --- Inputs ---
input1 = [[0,0,0,0,0,0,0,0,0,0],[0,3,0,3,0,3,0,3,0,0],[0,0,3,0,0,0,3,0,0,0],[0,0,3,0,0,0,3,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,8,0,0,0,0,0,0,0],[0,8,8,8,0,0,0,0,0,0],[0,0,8,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
input2 = [[0,0,0,0,0,0,0,0,0,0,0,0],[0,2,2,0,2,2,0,2,2,0,0,0],[0,2,0,0,2,0,0,2,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,3,0,0,0],[0,0,0,0,2,0,0,3,3,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]]
input3 = [[0,0,0,0,0,0,0,0,0,0],[0,1,0,0,1,0,0,0,7,0],[0,0,1,0,0,1,0,7,0,0],[0,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
input4 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,8,8,8,0,0,0,0,0,0,0],[0,0,0,0,0,8,0,0,0,0,0,8,0,0,0,0,0],[0,0,0,0,8,8,8,0,0,0,8,8,8,0,0,0,0],[0,0,8,0,0,0,0,1,1,1,0,0,0,0,8,0,0],[0,8,8,8,0,0,0,0,1,0,0,0,0,8,8,8,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

# --- Analysis ---
analysis = {
    "example1": analyze_example(input1),
    "example2": analyze_example(input2),
    "example3": analyze_example(input3),
    "example4": analyze_example(input4)
}

# Use json for potentially complex nested structures in output
print(json.dumps(analysis, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
{
  "example1": {
    "color1": 3,
    "color2": 8,
    "objects": [
      {
        "original_color": 3,
        "top_left": [
          1,
          1
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 3,
        "top_left": [
          1,
          3
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 3,
        "top_left": [
          1,
          5
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 3,
        "top_left": [
          1,
          7
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 3,
        "top_left": [
          2,
          2
        ],
        "shape_dims": [
          2,
          1
        ]
      },
      {
        "original_color": 3,
        "top_left": [
          2,
          6
        ],
        "shape_dims": [
          2,
          1
        ]
      },
      {
        "original_color": 8,
        "top_left": [
          5,
          1
        ],
        "shape_dims": [
          3,
          3
        ]
      }
    ],
    "shape1_pattern_relative_coords": [
      [
        0,
        0
      ]
    ],
    "shape2_pattern_relative_coords": [
      [
        0,
        1
      ],
      [
        1,
        0
      ],
      [
        1,
        1
      ],
      [
        1,
        2
      ],
      [
        2,
        1
      ]
    ]
  },
  "example2": {
    "color1": 2,
    "color2": 3,
    "objects": [
      {
        "original_color": 2,
        "top_left": [
          1,
          1
        ],
        "shape_dims": [
          2,
          2
        ]
      },
      {
        "original_color": 2,
        "top_left": [
          1,
          4
        ],
        "shape_dims": [
          2,
          2
        ]
      },
      {
        "original_color": 2,
        "top_left": [
          1,
          7
        ],
        "shape_dims": [
          2,
          2
        ]
      },
      {
        "original_color": 2,
        "top_left": [
          4,
          4
        ],
        "shape_dims": [
          2,
          2
        ]
      },
      {
        "original_color": 3,
        "top_left": [
          4,
          7
        ],
        "shape_dims": [
          2,
          2
        ]
      }
    ],
    "shape1_pattern_relative_coords": [
      [
        0,
        0
      ],
      [
        0,
        1
      ],
      [
        1,
        0
      ]
    ],
    "shape2_pattern_relative_coords": [
      [
        0,
        1
      ],
      [
        1,
        0
      ],
      [
        1,
        1
      ]
    ]
  },
  "example3": {
    "color1": 1,
    "color2": 7,
    "objects": [
      {
        "original_color": 1,
        "top_left": [
          1,
          1
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 1,
        "top_left": [
          1,
          4
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 1,
        "top_left": [
          2,
          2
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 1,
        "top_left": [
          2,
          5
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 1,
        "top_left": [
          4,
          1
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 1,
        "top_left": [
          5,
          2
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 1,
        "top_left": [
          7,
          1
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 1,
        "top_left": [
          8,
          2
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 7,
        "top_left": [
          1,
          8
        ],
        "shape_dims": [
          1,
          1
        ]
      },
      {
        "original_color": 7,
        "top_left": [
          2,
          7
        ],
        "shape_dims": [
          1,
          1
        ]
      }
    ],
    "shape1_pattern_relative_coords": [
      [
        0,
        0
      ]
    ],
    "shape2_pattern_relative_coords": [
      [
        0,
        0
      ]
    ]
  },
  "example4": {
    "color1": 1,
    "color2": 8,
    "objects": [
      {
        "original_color": 1,
        "top_left": [
          5,
          7
        ],
        "shape_dims": [
          2,
          3
        ]
      },
      {
        "original_color": 8,
        "top_left": [
          1,
          7
        ],
        "shape_dims": [
          2,
          3
        ]
      },
      {
        "original_color": 8,
        "top_left": [
          3,
          4
        ],
        "shape_dims": [
          2,
          3
        ]
      },
      {
        "original_color": 8,
        "top_left": [
          3,
          10
        ],
        "shape_dims": [
          2,
          3
        ]
      },
      {
        "original_color": 8,
        "top_left": [
          5,
          1
        ],
        "shape_dims": [
          2,
          3
        ]
      },
      {
        "original_color": 8,
        "top_left": [
          5,
          13
        ],
        "shape_dims": [
          2,
          3
        ]
      }
    ],
    "shape1_pattern_relative_coords": [
      [
        0,
        0
      ],
      [
        0,
        1
      ],
      [
        0,
        2
      ],
      [
        1,
        1
      ]
    ],
    "shape2_pattern_relative_coords": [
      [
        0,
        1
      ],
      [
        1,
        0
      ],
      [
        1,
        1
      ],
      [
        1,
        2
      ]
    ]
  }
}

```
**Analysis Summary:**

*   **Consistency:** All examples contain exactly two non-background colors. Let's call them Color A and Color B.
*   **Objects:** Each color forms one or more distinct, contiguous objects.
*   **Unique Shapes:** Within a single example grid, all objects of Color A have the same shape pattern (relative pixel coordinates). Similarly, all objects of Color B have their own unique shape pattern.
*   **Locations:** Each object can be located by an anchor point, such as the top-left corner of its bounding box.
*   **Transformation:** The core transformation involves swapping the shapes associated with the colors. The *shape* of Color A is drawn (using Color A) at the original anchor points of Color B's objects. The *shape* of Color B is drawn (using Color B) at the original anchor points of Color A's objects.
*   **Output Construction:** The output grid is initially empty (all background color). The shapes are then "stamped" onto this grid at the calculated positions. Overlapping pixels are overwritten (although no overlaps seem to occur in these examples).

**Discrepancy with Previous Code:** The previous code swapped colors pixel by pixel (`output_np[coords_color1] = color2`). The correct approach requires identifying object shapes and locations, then redrawing the *other* color's shape at those locations. The code output above provides the necessary object locations (`top_left`) and shape patterns (`shape1_pattern_relative_coords`, `shape2_pattern_relative_coords`) to implement the correct logic. *Note: The object detection logic in the tool code needs refinement to correctly capture the full shapes as seen in the visual examples, rather than just the components found by default `scipy.ndimage.label`. Example 1 shows multiple small objects for color 3 instead of two '+' shapes. Example 3 shows single pixels for color 1 and 7 instead of 'L' and 'dot' shapes. This indicates the default connectivity might be wrong or the shape extraction logic needs adjusting. However, the *principle* of swapping shapes based on location remains the core observation.* Assuming we can correctly extract the canonical shape for each color and the top-left anchor points for each instance.

## YAML Fact Block


```yaml
task_description: Swap the shapes associated with two colors based on their locations.

definitions:
  - background_color: white (0)
  - object: A contiguous block of pixels of the same non-background color.
  - shape: The pattern of relative pixel coordinates that define an object, relative to an anchor point.
  - anchor_point: A reference coordinate for an object, typically the top-left corner of its bounding box.

observations:
  - grid_properties:
      - Input and output grids have the same dimensions.
      - All grids contain exactly two unique non-background colors (Color A, Color B).
      - Background pixels (white) remain unchanged unless overwritten by a drawn shape.
  - object_properties:
      - All objects composed of Color A within a single input grid have the same shape (Shape A).
      - All objects composed of Color B within a single input grid have the same shape (Shape B).
      - Shape A and Shape B may be different or the same.
      - Objects of the same color can appear multiple times at different locations.
  - transformation:
      - Identify the two non-background colors: Color A and Color B.
      - Determine the canonical shape for Color A (Shape A) and Color B (Shape B). This can be done by extracting the pattern from any one instance of an object of that color.
      - Find the anchor points for all instances of objects made of Color A (Locations A).
      - Find the anchor points for all instances of objects made of Color B (Locations B).
      - The output grid is generated by:
          - Placing Shape B, drawn using Color B, at each location in Locations A.
          - Placing Shape A, drawn using Color A, at each location in Locations B.
      - Placement is done relative to the anchor point (e.g., the top-left pixel of the shape aligns with the anchor point).

assumptions:
  - Contiguity for object definition likely includes diagonal adjacency based on visual inspection of shapes like '+'.
  - The anchor point is consistently the top-left corner of the object's bounding box.
  - All instances of a shape of a given color are identical within one input grid.
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Identify the two unique non-background colors present in the input grid. Call them `color_A` and `color_B`.
3.  Find all distinct, contiguous objects composed of `color_A`.
4.  Find all distinct, contiguous objects composed of `color_B`.
5.  From one of the `color_A` objects, extract its shape pattern (the set of relative coordinates of its pixels from its anchor point, e.g., top-left corner). Call this `shape_A`.
6.  From one of the `color_B` objects, extract its shape pattern. Call this `shape_B`.
7.  Determine the list of anchor point coordinates (e.g., top-left corners) for all objects originally composed of `color_A`. Call this list `locations_A`.
8.  Determine the list of anchor point coordinates for all objects originally composed of `color_B`. Call this list `locations_B`.
9.  For each coordinate (`r`, `c`) in `locations_A`:
    *   Draw `shape_B` onto the output grid, using `color_B`, anchoring its pattern at (`r`, `c`).
10. For each coordinate (`r`, `c`) in `locations_B`:
    *   Draw `shape_A` onto the output grid, using `color_A`, anchoring its pattern at (`r`, `c`).
11. Return the final output grid.
