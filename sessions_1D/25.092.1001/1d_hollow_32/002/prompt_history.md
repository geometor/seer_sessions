
## train_1

**input:**
```
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0
```


**output:**
```
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0
```


## train_2

**input:**
```
0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
```


**output:**
```
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

## Perception

1.  **Input/Output Format:** The inputs and outputs appear to be 1-dimensional grids (or single rows extracted from a larger grid). They consist of pixels represented by integers 0-9.
2.  **Colors:** The primary colors involved are white (0), azure (8), and gray (5). White seems to be the background color.
3.  **Structure:** Each input grid contains a single contiguous horizontal segment of a non-white color, surrounded by the white background color.
4.  **Transformation:** The core transformation observed is the modification of this non-white segment. In the output, only the first and last pixels of the original segment retain their color. All the pixels *between* the first and last pixels of the segment are changed to the background color (white, 0).
5.  **Consistency:** This pattern holds across all three examples, regardless of the specific non-white color (azure or gray) or the length of the segment (as long as the length is greater than 1). The position of the segment within the row also changes, but the rule remains the same.

## Facts


```yaml
observations:
  - task_type: object_transformation # Modifying existing objects
  - grid_dimensions: single_row # Examples are 1xN grids
  - background_color: 0 # White
  - objects:
      - type: contiguous_segment
        color: non-zero # Can be azure (8) or gray (5) in examples
        properties:
          - horizontal
          - surrounded_by_background
          - variable_length (must be > 1 for transformation to occur)
          - variable_position
  - actions:
      - identify: the contiguous segment of non-background color in the input row.
      - locate: the start and end indices of this segment.
      - modify:
          if segment_length > 1:
            preserve: the pixel color at the start index.
            preserve: the pixel color at the end index.
            change: all pixels between the start and end indices to the background color (0).
          else: # Segment length is 1 or 0
            preserve: the original row content. # No change
      - output: the modified row.
  - relationships:
      - The output row has the same dimensions as the input row.
      - The transformation depends only on the location and extent of the non-background segment within the row.
      - Pixels outside the identified segment remain unchanged.
```


## Natural Language Program

1.  Identify the background color (which is white, 0).
2.  For the input grid (which appears to be a single row in the examples):
    a.  Find the first column index (`start_col`) containing a non-background pixel.
    b.  Find the last column index (`end_col`) containing a non-background pixel.
    c.  If non-background pixels are found (`start_col` and `end_col` exist):
        i.  Create a new output row, initially identical to the input row.
        ii. If `start_col` is not equal to `end_col` (i.e., the segment length is greater than 1):
            - Iterate through the columns from `start_col + 1` up to, but not including, `end_col`.
            - For each column index in this range, set the pixel value in the output row to the background color (0).
    d.  If no non-background pixels are found, the output row is identical to the input row.
3.  Return the resulting output row.
```python
"""
Identifies a contiguous horizontal segment of a non-background color (0) in a single-row input grid. 
If the segment length is greater than 1, it preserves the color of the first and last pixels of the segment 
and changes all pixels between them to the background color (0). Pixels outside the segment remain unchanged. 
If the segment length is 1 or no segment exists, the input row is returned unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to a single-row input grid.

    Args:
        input_grid (np.array): A 1D numpy array representing the input row.

    Returns:
        np.array: A 1D numpy array representing the transformed output row.
    """
    
    # Ensure input is a numpy array (it should be 1D based on examples)
    grid = np.array(input_grid)
    
    # Find indices of non-background (non-zero) pixels
    non_background_indices = np.where(grid != 0)[0]

    # If no non-background pixels are found, return the original grid
    if len(non_background_indices) == 0:
        return grid

    # Identify the start and end indices of the contiguous segment
    start_col = np.min(non_background_indices)
    end_col = np.max(non_background_indices)

    # Initialize the output grid as a copy of the input grid
    output_grid = grid.copy()

    # Check if the segment length is greater than 1
    if start_col != end_col:
        # Iterate through the columns between the start and end indices (exclusive)
        for col in range(start_col + 1, end_col):
            # Set the pixel value in the output grid to the background color (0)
            output_grid[col] = 0
            
    # If segment length is 1 (start_col == end_col), no changes are needed beyond the initial copy.

    return output_grid
```
