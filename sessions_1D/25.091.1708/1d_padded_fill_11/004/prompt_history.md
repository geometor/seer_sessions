
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0
```


## train_2

**input:**
```
5 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 0 0
```

**Perception of Task Elements:**

The task involves modifying rows in a grid based on the presence and arrangement of non-white pixels within those rows. Specifically, it identifies rows containing exactly two pixels of the same non-white color. The transformation then fills the horizontal space between these two pixels with the same color. Rows that do not meet this specific condition (e.g., have zero, one, or more than two pixels of the same non-white color, or pairs of different colors) remain unchanged. The background color is consistently white (0) in the examples, and this is the color that gets replaced during the filling process. The grid dimensions stay the same.

**YAML Facts:**


```yaml
task_context:
  grid_properties:
    - dimensions_preserved: True
    - background_color: white (0)
  transformation_type: row_based_filling
objects:
  - type: pixel
    properties:
      - color: non-white (1-9) or white (0)
      - position: (row_index, column_index)
  - type: row
    properties:
      - content: sequence of pixels
      - identified_features: pairs of identical non-white pixels
relationships:
  - type: horizontal_adjacency
    description: Pixels located within the same row.
  - type: betweenness
    description: Pixels located horizontally between two specific pixels in the same row.
actions:
  - name: identify_pairs
    inputs: row
    outputs: list of pairs, where each pair consists of [color, index1, index2] for rows with exactly two identical non-white pixels.
    condition: A row must contain exactly two pixels of the same non-white color.
  - name: fill_between
    inputs: row, identified_pair [color, index1, index2]
    outputs: modified_row
    description: Change the color of pixels from index1 + 1 to index2 - 1 (exclusive) to the identified color.
    condition: Operates only on rows where a valid pair was identified.
    target_pixels: white (0) pixels between the pair.
  - name: copy_row
    inputs: row
    outputs: identical_row
    condition: Row does not meet the criteria for identify_pairs.
transformation_flow:
  - step: Iterate through each row of the input grid.
  - step: For each row, apply the identify_pairs action.
  - step: If a pair is identified, apply the fill_between action to that row using the pair's information.
  - step: If no pair is identified, apply the copy_row action.
  - step: Collect the resulting rows (modified or copied) to form the output grid.

```


**Natural Language Program:**

1.  Initialize an empty output grid with the same dimensions as the input grid.
2.  Process the input grid one row at a time.
3.  For each row:
    a.  Find all non-white pixels, noting their color and column index.
    b.  Group these pixels by color.
    c.  Check if there is exactly one color group that contains exactly two pixels.
    d.  **If** such a group exists (let the color be C and the column indices be col1 and col2, assuming col1 < col2):
        i.  Copy the row from the input to the corresponding row in the output.
        ii. Fill the segment of the output row between col1 and col2 (i.e., from column index col1 + 1 up to col2 - 1) with color C.
    e.  **Else** (if the row contains zero non-white pixels, one non-white pixel, more than two pixels of the same color, or pairs of different colors):
        i.  Copy the row directly from the input to the corresponding row in the output without modification.
4.  Return the completed output grid.
```python
import numpy as np
from collections import defaultdict

"""
Processes the input grid row by row. 
For each row, it identifies if there are exactly two pixels of the same non-white color. 
If such a pair exists, it fills the horizontal segment between these two pixels (exclusive of the endpoints) with that same color in the output grid. 
If a row does not contain exactly two pixels of the same non-white color (e.g., zero, one, more than two of the same color, or pairs of different colors), the row is copied to the output grid without modification.
The background color is assumed to be white (0).
"""

def transform(input_grid):
    """
    Transforms the input grid based on filling between pairs of identical non-white pixels in each row.

    Args:
        input_grid (list of lists or np.ndarray): The input grid representing pixel colors.

    Returns:
        np.ndarray: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    
    rows, cols = input_grid_np.shape

    # Iterate through each row of the input grid
    for r in range(rows):
        row = input_grid_np[r, :]
        
        # Find non-white pixels and their indices in the current row
        non_white_pixels = defaultdict(list)
        for c in range(cols):
            pixel_color = row[c]
            if pixel_color != 0: # 0 is white/background
                non_white_pixels[pixel_color].append(c)
        
        # Check for exactly one color group with exactly two pixels
        valid_pair_found = False
        fill_color = -1
        col1 = -1
        col2 = -1
        
        num_colors_with_pairs = 0
        target_color = -1
        indices = []

        for color, idx_list in non_white_pixels.items():
            if len(idx_list) == 2:
                num_colors_with_pairs += 1
                target_color = color
                indices = sorted(idx_list) # Ensure col1 < col2

        # Condition: Exactly one color must form a pair
        if num_colors_with_pairs == 1:
            valid_pair_found = True
            fill_color = target_color
            col1 = indices[0]
            col2 = indices[1]

        # If a valid pair is identified, fill the segment between them
        if valid_pair_found:
            # Fill the segment in the output grid row
            # Note: range(col1 + 1, col2) covers the indices strictly between col1 and col2
            for c_fill in range(col1 + 1, col2):
                output_grid[r, c_fill] = fill_color
                
        # Else (no valid pair found or other conditions not met), 
        # the row in output_grid remains unchanged (as it was initially copied)

    return output_grid.tolist() # Return as list of lists if required by ARC standard

```
```python
import numpy as np
from collections import defaultdict
from typing import List, Tuple, Optional

"""
Processes the input grid row by row.
For each row:
1. Identifies all non-white pixels and groups their column indices by color.
2. Counts how many distinct colors appear exactly twice in the row.
3. If exactly one color (C) appears exactly twice:
    a. Finds the column indices (col1, col2, where col1 < col2) of these two pixels.
    b. Fills the segment of the row strictly between col1 and col2 (columns col1 + 1 to col2 - 1) with color C.
4. Otherwise (if no color appears exactly twice, or multiple colors do), the row remains unchanged.
The output grid is initially a copy of the input grid, and modifications are applied directly to the output grid's rows.
"""

def analyze_row(row: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Analyzes a single row to find if there is exactly one color
    that appears exactly twice.

    Args:
        row (np.ndarray): A 1D numpy array representing a row of the grid.

    Returns:
        Optional[Tuple[int, int, int]]: A tuple (color, col1, col2) if the
                                         condition is met, otherwise None.
                                         col1 and col2 are the sorted indices.
    """
    non_white_pixels = defaultdict(list)
    for c, pixel_color in enumerate(row):
        if pixel_color != 0:  # 0 is white/background
            non_white_pixels[pixel_color].append(c)

    # Find colors that appear exactly twice
    colors_with_two_pixels = []
    for color, indices in non_white_pixels.items():
        if len(indices) == 2:
            colors_with_two_pixels.append((color, sorted(indices))) # Store color and sorted indices

    # Check if exactly one such color exists
    if len(colors_with_two_pixels) == 1:
        color, indices = colors_with_two_pixels[0]
        return color, indices[0], indices[1]
    else:
        return None

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on filling between pairs of identical
    non-white pixels in each row, if that pair is unique for its color count.

    Args:
        input_grid (List[List[int]]): The input grid.

    Returns:
        List[List[int]]: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    rows, cols = input_grid_np.shape

    # Iterate through each row of the input grid
    for r in range(rows):
        current_row = input_grid_np[r, :]

        # Analyze the row to find if the specific pair condition is met
        analysis_result = analyze_row(current_row)

        # If a unique pair satisfying the condition is found
        if analysis_result is not None:
            fill_color, col1, col2 = analysis_result

            # Fill the segment in the output grid row
            # range(col1 + 1, col2) covers indices strictly between col1 and col2
            if col1 + 1 < col2: # Ensure there's actually space to fill
                 output_grid[r, col1 + 1 : col2] = fill_color
            # If col1 + 1 == col2, there are no pixels between them, so nothing to fill.

        # Else (no unique pair condition met), the row in output_grid
        # remains unchanged (as it was initially copied).

    # Convert the result back to list of lists
    return output_grid.tolist()
```
