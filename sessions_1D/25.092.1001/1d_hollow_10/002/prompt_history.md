
## train_1

**input:**
```
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```


**output:**
```
7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0
```

*   **Perception:** The input is a 1-dimensional grid (a single row) containing a contiguous segment of a single non-white color. This colored segment might be preceded or followed by white pixels (color 0). The output grid has the same dimensions as the input. The transformation identifies the first and last pixel of the non-white segment in the input. In the output grid, these two pixels retain their original color and position. All other pixels in the output grid are set to white (color 0).

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D # Effectively 1xN
    input_characteristics:
      - Contains a single contiguous block of a non-white color (object).
      - May contain leading or trailing white pixels (color 0).
      - The non-white block has a start position and an end position.
    output_characteristics:
      - Same dimensions as the input.
      - Contains only two non-white pixels (unless the input block has length 1 or 2).
      - The first non-white pixel corresponds to the start position and color of the input block.
      - The second non-white pixel corresponds to the end position and color of the input block.
      - All other pixels are white (color 0).
    transformation:
      - Identify the indices and color of the first and last non-white pixels in the input row.
      - Create an output row of the same length, initialized with white pixels.
      - Place the color of the first non-white pixel at its original index in the output row.
      - Place the color of the last non-white pixel at its original index in the output row.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid with the same dimensions as the input grid, filled entirely with white pixels (0).
    2.  Iterate through the input grid from left to right to find the index and color of the first non-white pixel. If found, store this index and color.
    3.  Iterate through the input grid from right to left to find the index and color of the last non-white pixel. If found, store this index and color. (Note: This will be the same color as the first non-white pixel found).
    4.  If a first non-white pixel was found, set the pixel at the corresponding index in the output grid to its color.
    5.  If a last non-white pixel was found, set the pixel at the corresponding index in the output grid to its color. (If the first and last non-white pixel are the same, this step overwrites the same pixel if the segment length is 1, which is acceptable).
    6.  Return the modified output grid.
```python
"""
Identifies the first and last non-white pixels in a 1D input grid (row).
Creates an output grid of the same size, initialized to white (0).
Places the color of the first identified non-white pixel at its original position in the output.
Places the color of the last identified non-white pixel at its original position in the output.
All other pixels in the output remain white.
If the input contains only white pixels, the output is also all white.
If the input non-white segment has length 1, the first and last pixels are the same, resulting in one non-white pixel in the output.
"""

import numpy as np

def transform(input_grid_list):
    """
    Transforms a 1D input grid list based on the first and last non-white pixels.

    Args:
        input_grid_list: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Convert input list to a numpy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)
    
    # Get the dimensions (length) of the input grid
    width = input_grid.shape[0]
    
    # 1. Initialize the output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_grid)
    
    # 2. Find the indices of all non-white pixels (value != 0)
    non_white_indices = np.where(input_grid != 0)[0]
    
    # 3. Check if any non-white pixels were found
    if non_white_indices.size > 0:
        # Find the index of the first non-white pixel (minimum index)
        first_idx = np.min(non_white_indices)
        
        # Find the index of the last non-white pixel (maximum index)
        last_idx = np.max(non_white_indices)
        
        # Get the color of the non-white segment (all non-white pixels have the same color)
        # We can pick the color from the first non-white pixel found
        color = input_grid[first_idx]
        
        # 4. Place the color of the first non-white pixel at its original index in the output grid
        output_grid[first_idx] = color
        
        # 5. Place the color of the last non-white pixel at its original index in the output grid
        # Note: If first_idx == last_idx (segment length 1), this overwrites the same pixel, which is correct.
        output_grid[last_idx] = color
        
    # 6. Return the modified output grid as a list (to match expected output format if needed)
    return output_grid.tolist()

```
