
## train_1

**input:**
```
0 2 0 2 0 2 0
3 2 3 3 3 2 3
0 2 0 2 0 2 0
3 2 3 3 3 2 3
0 2 0 2 0 2 0
3 2 3 3 3 2 3
0 2 0 2 0 2 0
```


**output:**
```
0 2 0 0 0 2 0
3 2 3 3 3 2 3
0 2 0 0 0 2 0
3 2 3 3 3 2 3
0 2 0 0 0 2 0
3 2 3 3 3 2 3
0 2 0 0 0 2 0
```


## train_2

**input:**
```
0 4 0 0 4 0 0
0 4 0 0 4 0 0
1 1 1 1 4 1 1
0 4 0 0 4 0 0
1 1 1 1 4 1 1
0 4 0 0 4 0 0
0 4 0 0 4 0 0
```


**output:**
```
0 0 0 0 4 0 0
0 0 0 0 4 0 0
1 1 1 1 4 1 1
0 0 0 0 4 0 0
1 1 1 1 4 1 1
0 0 0 0 4 0 0
0 0 0 0 4 0 0
```


## train_3

**input:**
```
0 0 0 9 0 0 0
6 6 6 6 6 6 6
0 0 0 9 0 0 0
0 0 0 9 0 0 0
0 0 0 9 0 0 0
0 0 0 9 0 0 0
0 0 0 9 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
6 6 6 6 6 6 6
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

*   **Perception:**
    *   The task involves modifying input grids based on patterns within their columns.
    *   The input and output grids always have the same dimensions.
    *   The modification involves changing certain non-white pixels to white (0).
    *   The rule for modification depends on the colors present within each column and their vertical arrangement.
    *   Two main cases seem to exist: columns with only one non-white color and columns with multiple non-white colors.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_properties:
      - dimensions_preserved: True # Input and output grids have the same height and width
      - background_color: 0 # White is the primary background/default color
    transformation_scope: column_based # The transformation logic operates independently on each column
    column_analysis:
      - counts_non_white_colors: True # The number of distinct non-white colors matters
      - frequency_of_colors: True # The relative frequency (majority) of colors matters in some cases
      - vertical_contiguity: True # Whether pixels of the same color form unbroken vertical segments matters
      - vertical_adjacency: True # Whether pixels of a specific color are vertically next to others of the same color matters
    actions:
      - color_change: # Specific non-white pixels are changed
          target_color: 0 # The target color is always white
          conditions: # The conditions depend on the column analysis results
            - condition_1: # Applies to columns with exactly one non-white color (C)
                trigger: if pixels of color C are NOT vertically contiguous (interrupted by white)
                effect: change all pixels of color C to white (0)
            - condition_2: # Applies to columns with more than one non-white color
                trigger: if a unique majority non-white color (C) exists AND no pixel of color C is vertically adjacent to another pixel of color C
                effect: change all pixels of color C to white (0)
            - condition_default: # Otherwise
                effect: keep the column unchanged
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each column of the input grid independently, from left to right.
    3.  For the current column:
        a.  Identify all unique non-white colors present in the column and count their occurrences.
        b.  **If** exactly one unique non-white color (let's call it `C`) is present in the column:
            i.  Check if all pixels of color `C` form a single, uninterrupted vertical block within the column.
            ii. If they do **not** form a single contiguous block (i.e., they are separated by white pixels), change all pixels of color `C` in this column of the output grid to white (0).
        c.  **Else if** more than one unique non-white color is present in the column:
            i.  Determine if there is a single color (let's call it `MajC`) that occurs more frequently than any other non-white color in the column.
            ii. If such a unique majority color `MajC` exists:
                1.  Check if any pixel of color `MajC` in the column is immediately above or below another pixel of color `MajC`.
                2.  If **no** pixel of color `MajC` is vertically adjacent to another pixel of color `MajC`, change all pixels of color `MajC` in this column of the output grid to white (0).
        d.  **Else** (column contains only white pixels, or multiple non-white colors with a tie for the most frequent, or other conditions not met): Leave the column in the output grid unchanged from the input.
    4.  Return the modified output grid.
```python
import numpy as np
from collections import Counter

"""
The transformation rule operates independently on each column of the input grid.

1. Identify the unique non-white colors present in a column and their counts.
2. **Single Non-White Color Case:** If a column contains exactly one unique non-white color (let's call it C):
   - Check if any pixel of color C is vertically adjacent (immediately above or below) to another pixel of color C within that column.
   - If NO vertical adjacency exists for color C, change all occurrences of C in that column to white (0).
   - Otherwise (if vertical adjacency exists), keep the column as is.
3. **Multiple Non-White Colors Case:** If a column contains more than one unique non-white color:
   - Determine if there is a single color (let's call it MajC) that occurs strictly more frequently than any other non-white color in the column.
   - If such a unique majority color MajC exists, change all occurrences of MajC in that column to white (0).
   - Otherwise (if there is no unique majority non-white color, or only white pixels), keep the column as is.
4. Repeat for all columns.
"""

def has_vertical_adjacency(col: np.ndarray, color: int) -> bool:
    """Checks if a given color has vertically adjacent instances in a column."""
    if len(col) < 2:
        return False
    for i in range(len(col) - 1):
        if col[i] == color and col[i+1] == color:
            return True
    return False

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on column analysis.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Iterate through each column
    for j in range(width):
        col = input_array[:, j]
        
        # Find unique non-white colors and their counts
        non_white_pixels = col[col != 0]
        if len(non_white_pixels) == 0:
            continue # Skip columns with only white pixels

        counts = Counter(non_white_pixels)
        unique_non_white_colors = list(counts.keys())

        # Case 1: Exactly one unique non-white color
        if len(unique_non_white_colors) == 1:
            color_c = unique_non_white_colors[0]
            # Check for vertical adjacency for this single color
            if not has_vertical_adjacency(col, color_c):
                # If no adjacency, change all instances of color_c to 0
                output_array[:, j][output_array[:, j] == color_c] = 0
        
        # Case 2: More than one unique non-white color
        elif len(unique_non_white_colors) > 1:
            # Find if there is a unique majority color
            if not counts: # Should not happen if len(unique_non_white_colors) > 1
                 continue
                 
            sorted_counts = counts.most_common()
            
            # Check for unique majority
            is_unique_majority = False
            if len(sorted_counts) == 1: # Only one non-white color, handled above
                 pass # Should not happen
            elif len(sorted_counts) > 1:
                 if sorted_counts[0][1] > sorted_counts[1][1]:
                      is_unique_majority = True

            if is_unique_majority:
                majority_color_majc = sorted_counts[0][0]
                # If a unique majority color exists, change all its instances to 0
                output_array[:, j][output_array[:, j] == majority_color_majc] = 0
                
            # Else (no unique majority): column remains unchanged implicitly
            
    return output_array.tolist()
```
