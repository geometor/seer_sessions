
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 9
0 8 0 0 0 8 0 8 0
0 8 8 8 7 8 7 8 0
0 8 0 8 0 8 0 8 0
0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 9 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 9
0 9 0 0 0 8 0 8 0
0 9 8 8 7 8 7 8 0
0 9 0 8 0 8 0 8 0
0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 9 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 8 8 8 0 8 8 8 0
0 8 0 8 7 8 0 8 0
9 8 0 8 8 8 0 8 9
0 8 0 0 0 0 0 8 0
0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 8 8 8 0 8 8 8 0
0 8 0 8 7 8 0 8 0
9 9 0 8 8 8 0 9 9
0 9 0 0 0 0 0 9 0
0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 9 0 0 0 0
0 8 8 8 8 8 8 8 0
0 8 7 0 0 0 0 8 0
0 8 8 8 8 8 8 8 0
0 8 0 0 8 0 0 8 0
0 8 8 8 8 8 8 8 0
0 8 0 0 0 0 7 8 0
0 8 8 8 8 8 8 8 0
0 0 0 0 9 0 0 0 0
```


**output:**
```
0 0 0 0 9 0 0 0 0
0 8 8 8 9 9 9 9 0
0 8 7 0 0 0 0 9 0
0 8 8 8 9 9 9 9 0
0 8 0 0 9 0 0 8 0
0 9 9 9 9 8 8 8 0
0 9 0 0 0 0 7 8 0
0 9 9 9 9 8 8 8 0
0 0 0 0 9 0 0 0 0
```

Okay, I will analyze the provided examples to understand the transformation rule.

**Perception**

1.  **Colors Involved:** The primary colors involved are white (0 - background), azure (8), maroon (9), and orange (7). The transformation specifically changes some azure (8) pixels to maroon (9). Orange (7) pixels seem unaffected and might be internal features of the main azure shape or irrelevant markers.
2.  **Core Object:** The central element in each input grid appears to be a shape or pattern composed mainly of azure (8) pixels. This shape varies across examples.
3.  **Transformation Trigger:** The presence and location of maroon (9) pixels relative to the azure (8) shape seem to dictate the transformation.
4.  **Transformation Effect:** The transformation involves changing specific columns of azure (8) pixels to maroon (9). The columns affected depend on the location of the trigger maroon (9) pixels.
5.  **Location Categories:** Maroon (9) pixels can be categorized based on their column index relative to the columns occupied by the azure (8) shape:
    *   **Left:** Maroon pixels in columns to the left of the azure shape's leftmost column.
    *   **Right:** Maroon pixels in columns to the right of the azure shape's rightmost column.
    *   **Middle:** Maroon pixels in columns that overlap with the azure shape's column span.
6.  **Rule Mapping:**
    *   If maroon pixels exist *only* in the Middle zone, the transformation affects azure pixels starting from the leftmost column containing a Middle maroon pixel, extending to the rightmost column of the azure shape. (Example 3)
    *   If maroon pixels exist in the Left zone, the *rightmost* column of azure pixels is transformed. (Example 2)
    *   If maroon pixels exist in the Right zone, the *leftmost* column of azure pixels is transformed. (Examples 1 and 2)
    *   If both Left and Right maroon pixels exist, both the leftmost and rightmost azure columns are transformed. (Example 2)
    *   The Left/Right rules seem to take precedence over the Middle rule. (Example 1 shows a Right and Middle maroon, but only the Leftmost azure column changes, consistent with the Right rule).

**Facts**


```yaml
Input_Grid:
  description: A 2D grid of pixels with values 0-9 representing colors.
  contains:
    - background: color 0 (white)
    - primary_shape:
        color: 8 (azure)
        description: A contiguous or patterned block of azure pixels. Its exact shape varies.
        properties:
          - bounding_box: Defined by min/max row and column containing azure pixels.
    - trigger_pixels:
        color: 9 (maroon)
        description: One or more maroon pixels located potentially inside, outside, or adjacent to the primary shape. Their column position relative to the primary shape's columns is critical.
    - other_pixels:
        color: 7 (orange)
        description: Appear within or near the azure shape, but seem unaffected by the transformation.

Transformation:
  action: Modifies the Input_Grid to produce the Output_Grid.
  changes: Converts specific azure (8) pixels to maroon (9) pixels.
  rule_based_on: The column positions of maroon (9) pixels relative to the column span of azure (8) pixels.

Relationships:
  - Maroon_Location_vs_Azure_Columns:
      azure_min_col: The minimum column index containing an azure (8) pixel.
      azure_max_col: The maximum column index containing an azure (8) pixel.
      maroon_locations:
        - left: Maroon pixels in columns < azure_min_col.
        - right: Maroon pixels in columns > azure_max_col.
        - middle: Maroon pixels in columns >= azure_min_col AND <= azure_max_col.
          properties:
            - min_middle_col: The minimum column index among 'middle' maroon pixels.
  - Transformation_Rules (Prioritized):
      1. If 'right' maroons exist:
         action: Change all azure (8) pixels in column `azure_min_col` to maroon (9).
      2. If 'left' maroons exist:
         action: Change all azure (8) pixels in column `azure_max_col` to maroon (9).
         note: Rules 1 and 2 can apply concurrently if both left and right maroons exist.
      3. If NEITHER 'left' NOR 'right' maroons exist, BUT 'middle' maroons exist:
         action: For each column `c` from `min_middle_col` up to `azure_max_col`, change all azure (8) pixels in column `c` to maroon (9).
      4. If no maroons exist according to these categories, or no azure pixels exist:
         action: No changes are made.

Output_Grid:
  description: The result of applying the transformation rules to the Input_Grid.
  content: Primarily identical to the Input_Grid, except for the azure pixels changed to maroon according to the rules.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all pixels with the color azure (8). If none exist, stop and return the copied grid.
3.  Determine the minimum column index (`min_col`) and maximum column index (`max_col`) occupied by any azure (8) pixel.
4.  Identify all pixels with the color maroon (9).
5.  Check if any maroon (9) pixels exist in columns *less than* `min_col`. Set a flag `left_maroon_exists` to true if found, otherwise false.
6.  Check if any maroon (9) pixels exist in columns *greater than* `max_col`. Set a flag `right_maroon_exists` to true if found, otherwise false.
7.  If `left_maroon_exists` is false AND `right_maroon_exists` is false:
    a.  Check if any maroon (9) pixels exist in columns *between* `min_col` and `max_col` (inclusive). Set a flag `middle_maroon_exists` to true if found, otherwise false.
    b.  If `middle_maroon_exists` is true:
        i.  Find the minimum column index (`min_middle_col`) among all maroon (9) pixels located in columns between `min_col` and `max_col`.
        ii. Iterate through each column `c` from `min_middle_col` up to `max_col`.
        iii. For each row `r` in the grid, if the pixel at `(r, c)` in the input grid is azure (8), change the corresponding pixel at `(r, c)` in the output grid to maroon (9).
        iv. Stop processing rules and proceed to step 9.
8.  If `left_maroon_exists` is true OR `right_maroon_exists` is true:
    a.  If `left_maroon_exists` is true: Iterate through each row `r`. If the pixel at `(r, max_col)` in the input grid is azure (8), change the corresponding pixel at `(r, max_col)` in the output grid to maroon (9).
    b.  If `right_maroon_exists` is true: Iterate through each row `r`. If the pixel at `(r, min_col)` in the input grid is azure (8), change the corresponding pixel at `(r, min_col)` in the output grid to maroon (9).
9.  Return the final output grid.
```python
import numpy as np

"""
Identifies the column span of azure (8) pixels.
Categorizes maroon (9) pixels based on their column position relative to this span:
- 'left': columns to the left of the azure span.
- 'right': columns to the right of the azure span.
- 'middle': columns overlapping with the azure span.

Transformation Rules (applied in order of precedence):
1. If 'right' maroons exist, change all azure pixels in the *leftmost* column of the azure span to maroon.
2. If 'left' maroons exist, change all azure pixels in the *rightmost* column of the azure span to maroon. 
   (Rules 1 and 2 can apply simultaneously).
3. If NEITHER 'left' NOR 'right' maroons exist, BUT 'middle' maroons do exist:
   Find the minimum column index ('min_middle_col') among the 'middle' maroons.
   Change all azure pixels in columns from 'min_middle_col' up to and including the *rightmost* column of the azure span to maroon.
4. If none of the above conditions are met (e.g., no maroons, or no relevant maroons), no changes are made.
"""

def transform(input_grid):
    """
    Applies transformations to an input grid based on the relative positions 
    of azure (8) and maroon (9) pixels.
    """
    # Convert input list of lists to a numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    azure = 8
    maroon = 9

    # Find coordinates of all azure pixels
    azure_coords = np.argwhere(grid == azure)
    
    # If there are no azure pixels, return the original grid unchanged
    if azure_coords.size == 0:
        return output_grid.tolist() 

    # Determine the minimum and maximum column indices occupied by azure pixels
    azure_cols = azure_coords[:, 1]
    min_col = np.min(azure_cols)
    max_col = np.max(azure_cols)

    # Find coordinates of all maroon pixels
    maroon_coords = np.argwhere(grid == maroon)
    
    # If there are no maroon pixels, return the original grid unchanged
    if maroon_coords.size == 0:
        return output_grid.tolist() 

    # Get the column indices of maroon pixels
    maroon_cols = maroon_coords[:, 1]

    # Categorize maroon pixels based on their column relative to the azure span
    left_maroon_exists = np.any(maroon_cols < min_col)
    right_maroon_exists = np.any(maroon_cols > max_col)
    
    # Identify maroon pixels within the azure column span
    middle_maroon_mask = (maroon_cols >= min_col) & (maroon_cols <= max_col)
    middle_maroon_cols = maroon_cols[middle_maroon_mask]
    middle_maroon_exists = middle_maroon_cols.size > 0

    # Apply transformation rules based on maroon locations
    
    # Flag to track if left/right rules were applied, giving them precedence
    left_right_transformed = False 

    # Rule 1: If maroons exist to the right of the azure span
    if right_maroon_exists:
        # Find rows in the leftmost azure column containing azure pixels
        rows_to_change_min = np.where(grid[:, min_col] == azure)[0]
        # Change those azure pixels to maroon in the output grid
        if rows_to_change_min.size > 0:
             output_grid[rows_to_change_min, min_col] = maroon
             left_right_transformed = True # Mark that a transformation occurred

    # Rule 2: If maroons exist to the left of the azure span
    if left_maroon_exists:
        # Find rows in the rightmost azure column containing azure pixels
        rows_to_change_max = np.where(grid[:, max_col] == azure)[0]
         # Change those azure pixels to maroon in the output grid
        if rows_to_change_max.size > 0:
            output_grid[rows_to_change_max, max_col] = maroon
            left_right_transformed = True # Mark that a transformation occurred

    # Rule 3: If no left/right maroons, but middle maroons exist
    # This rule only applies if the left/right rules did NOT trigger
    if not left_right_transformed and middle_maroon_exists:
        # Find the minimum column index among the middle maroons
        min_middle_col = np.min(middle_maroon_cols)
        # Iterate through columns from the min_middle_col to the max_col of the azure span
        for c in range(min_middle_col, max_col + 1):
            # Find rows in the current column 'c' containing azure pixels
            rows_to_change_middle = np.where(grid[:, c] == azure)[0]
            # Change those azure pixels to maroon in the output grid
            if rows_to_change_middle.size > 0:
                 output_grid[rows_to_change_middle, c] = maroon

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()
```
