
## train_1

**input:**
```
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 5 0 0 0 0 0 0 0
0 0 2 0 5 0 0 5 0 0 0 0 0 0 0
0 0 5 0 5 0 0 5 0 0 0 0 0 0 0
0 0 5 0 5 0 0 5 0 0 0 0 0 0 0
0 0 2 0 2 0 0 2 0 0 0 0 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 2 0 5 0 0 2 0 0 0 0 0 0 0
0 0 5 0 5 0 0 2 0 0 0 0 0 0 0
0 0 5 0 5 0 0 2 0 0 0 0 0 0 0
0 0 2 0 2 0 0 2 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 2 0 0 0 3 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 2 0 0 0 2 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 3 0 0 0 2 0 0 0
0 0 3 0 0 0 2 0 0 0
0 0 2 0 0 0 2 0 0 0
```


## train_3

**input:**
```
1 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 3 0 0 0 0
0 0 7 0 0 0 0 0 0 0 5 0 0 0 0
0 0 7 0 0 1 0 0 0 0 5 0 0 3 0
0 0 7 0 0 7 0 1 0 0 5 0 0 5 0
0 0 7 0 0 7 0 7 0 0 5 0 0 5 0
0 0 1 0 0 1 0 1 0 0 3 0 0 3 0
```


**output:**
```
1 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 3 0 0 0 0
0 0 1 0 0 0 0 0 0 0 5 0 0 0 0
0 0 1 0 0 1 0 0 0 0 5 0 0 3 0
0 0 1 0 0 7 0 1 0 0 5 0 0 3 0
0 0 1 0 0 7 0 7 0 0 5 0 0 3 0
0 0 1 0 0 1 0 1 0 0 3 0 0 3 0
```

**Perception of Task Elements**

1.  **Grids:** The task operates on 2D grids of colored pixels (0-9). The background is white (0).
2.  **Objects:** While contiguous blocks of color exist, the core logic seems to operate column-wise, focusing on the vertical relationships between pixels within the same column rather than distinct multi-pixel objects.
3.  **Colors:** Specific colors play key roles:
    *   Red (2) and Blue (1) act as "trigger" or "dominant" colors in different examples.
    *   Gray (5), Green (3), and Orange (7) act as "target" or "susceptible" colors that can be changed.
    *   White (0) is the background and is ignored.
    *   Green (3) is susceptible to Red(2) but not to Blue(1). Gray (5) is susceptible to both Red(2) and Blue(1). Orange (7) is susceptible to Blue(1).
4.  **Transformation:** The transformation involves changing the color of certain pixels based on the presence and position of a trigger color within the same column. Specifically, susceptible pixels *below* the lowest instance of a trigger color in a column adopt the trigger color.
5.  **Columnar Focus:** The transformation rule is applied independently to each column of the grid. The presence and vertical position of specific colors within a column dictate the changes in that column.

**YAML Facts**


```yaml
Grid_Properties:
  - dimensionality: 2
  - background_color: white (0)
  - value_range: 0-9 (colors)

Columnar_Operation:
  - scope: Transformation is applied independently to each column.
  - vertical_dependency: Changes depend on the pixels above within the same column.

Color_Roles:
  - Trigger_Colors:
      - Red (2): Triggers changes in Example 1 and 2.
      - Blue (1): Triggers changes in Example 3.
  - Susceptible_Colors_Mapping:
      - When Red (2) is the trigger: [Gray (5), Green (3)]
      - When Blue (1) is the trigger: [Gray (5), Orange (7)]
  - Unaffected_Colors_Example:
      - Green (3) is not affected by Blue (1) trigger in Example 3.

Transformation_Rule_Summary:
  - Identify the trigger color present in the input (assume only one type, Red or Blue, per input based on examples).
  - For each column:
      - Find the lowest row index (`r_trigger`) containing the trigger color.
      - If a trigger color exists in the column:
          - For all rows `r` below `r_trigger`:
              - If the pixel at `(r, column)` has a color susceptible to the identified trigger color:
                  - Change the pixel's color to the trigger color.
              - Otherwise, keep the original color.
      - If no trigger color exists, the column remains unchanged.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Determine the active "trigger" color (`C_trigger`) for the entire grid. Based on the examples, if Red (2) is present anywhere in the input, `C_trigger` is Red (2). Otherwise, if Blue (1) is present, `C_trigger` is Blue (1). (If neither is present, no changes occur).
3.  Define the set of "susceptible" colors (`S_target`) based on the identified `C_trigger`:
    *   If `C_trigger` is Red (2), `S_target` includes Gray (5) and Green (3).
    *   If `C_trigger` is Blue (1), `S_target` includes Gray (5) and Orange (7).
4.  Iterate through each column index `c` from left to right.
5.  Within each column `c`, find the row index `r_trigger` corresponding to the *lowest* occurrence of `C_trigger`. If `C_trigger` does not exist in column `c`, proceed to the next column.
6.  If `r_trigger` was found, iterate through all row indices `r` *below* `r_trigger` (i.e., from `r_trigger + 1` down to the last row).
7.  For each pixel at position `(r, c)`, check if its original color (from the input grid) is present in the set `S_target`.
8.  If the pixel's color is in `S_target`, update the color of the pixel at `(r, c)` in the *output* grid to `C_trigger`.
9.  After processing all columns, return the final output grid.
```python
import numpy as np

"""
Transformation Rule:

1. Identify the active "trigger" color (C_trigger) for the entire grid.
   - If Red (2) is present anywhere, C_trigger is Red (2).
   - Otherwise, if Blue (1) is present, C_trigger is Blue (1).
   - If neither is present, no changes occur.
2. Determine the set of "susceptible" colors (S_target) based on C_trigger:
   - If C_trigger is Red (2), S_target = {Gray (5), Green (3)}.
   - If C_trigger is Blue (1), S_target = {Gray (5), Orange (7)}.
3. Initialize the output grid as a copy of the input grid.
4. Iterate through each column of the grid.
5. For each column:
   - Find the row index of the *lowest* occurrence of C_trigger in that column.
   - If C_trigger is found at row `r_trigger`:
     - Iterate through all rows `r` *below* `r_trigger` (from `r_trigger + 1` to the bottom).
     - If the original color of the pixel at `(r, column)` is in S_target:
       - Change the color of the pixel at `(r, column)` in the *output* grid to C_trigger.
6. Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies a transformation rule where a trigger color (Red or Blue)
    changes susceptible colors below it in the same column.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    trigger_color = None
    susceptible_colors = set()

    # 1. & 2. Determine trigger and susceptible colors
    if np.any(input_array == 2): # Check if Red (2) exists
        trigger_color = 2
        susceptible_colors = {5, 3} # Gray, Green
    elif np.any(input_array == 1): # Check if Blue (1) exists
        trigger_color = 1
        susceptible_colors = {5, 7} # Gray, Orange

    # If no trigger color found, return the original grid
    if trigger_color is None:
        return input_grid # Return as list of lists

    # 4. Iterate through each column
    for c in range(width):
        # 5. Find the lowest trigger color index in the current column
        trigger_indices = np.where(input_array[:, c] == trigger_color)[0]

        if len(trigger_indices) > 0:
            lowest_trigger_row = np.max(trigger_indices)

            # 5a. Iterate through rows below the lowest trigger
            for r in range(lowest_trigger_row + 1, height):
                # 5b. Check if the original pixel color is susceptible
                original_color = input_array[r, c]
                if original_color in susceptible_colors:
                    # 5c. Change the output pixel color to the trigger color
                    output_array[r, c] = trigger_color

    # Return the modified grid as a list of lists
    return output_array.tolist()
```
