
## train_1

**input:**
```
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 7 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 5 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0
```

Okay, let's break down the transformation.

**Perception:**

1.  **Input Structure:** The input grids consist primarily of a white background (color 0) with a few scattered pixels of a single non-white color (blue=1, orange=7, or gray=5 in the examples). These non-white pixels appear in specific rows.
2.  **Output Structure:** The output grids have the same dimensions as the input grids. The original non-white pixels remain in their positions. Additionally, horizontal segments are filled with the same non-white color.
3.  **Transformation:** The core transformation appears to happen row by row. Within each row containing two or more non-white pixels, the space between the leftmost and rightmost non-white pixel (inclusive) is filled with that same non-white color. Rows with zero or one non-white pixel remain unchanged. The color used for filling is dictated by the color of the pixels already present in that row.

**YAML Facts:**


```yaml
Grid:
  Properties:
    - Dimensions: Same for input and output in each example pair.
    - BackgroundColor: White (0).
Objects:
  - Type: NonWhitePixel
    Properties:
      - Color: Varies (1, 7, 5 in examples), but consistent within a single input grid.
      - Location: Specific row and column indices.
    Identification: Any pixel with color > 0.
  - Type: HorizontalSegment
    Properties:
      - Color: Same as the NonWhitePixels in its row.
      - Location: Spans horizontally within a single row in the output grid.
Relationship:
  - NonWhitePixels define the bounds (start and end column) of the HorizontalSegment within a row.
Action:
  - Name: FillHorizontalSpan
  - Input: A row from the input grid.
  - Output: A potentially modified row for the output grid.
  - Condition: The row must contain at least two NonWhitePixels.
  - Process:
      1. Identify all NonWhitePixels in the row.
      2. Determine their color (assumed unique non-white color per row/grid).
      3. Find the minimum column index (leftmost_col) of these pixels.
      4. Find the maximum column index (rightmost_col) of these pixels.
      5. Fill all pixels from leftmost_col to rightmost_col (inclusive) with the identified color.
  - NoActionCondition: If a row contains zero or one NonWhitePixel, it is copied directly to the output without modification.
```


**Natural Language Program:**

1.  Initialize an empty output grid with the same dimensions as the input grid.
2.  Process the input grid row by row.
3.  For each row:
    a.  Find the locations (column indices) of all non-white pixels (pixels with color > 0).
    b.  If there are fewer than two non-white pixels in the current row, copy the row directly from the input to the corresponding row in the output grid.
    c.  If there are two or more non-white pixels:
        i.  Determine the color of these non-white pixels (it will be the same color for all of them in the row based on the examples).
        ii. Find the minimum column index (`min_col`) among the non-white pixels found in step 3a.
        iii. Find the maximum column index (`max_col`) among the non-white pixels found in step 3a.
        iv. Create the output row by copying the input row, but then change the color of all pixels from column `min_col` to `max_col` (inclusive) to the non-white color determined in step 3(c)i.
        v. Place this modified row into the corresponding row of the output grid.
4.  Return the completed output grid.
```python
"""
Processes the input grid row by row. 
For each row:
1. Finds all non-white pixels (color > 0).
2. If a row contains two or more non-white pixels:
   a. Determines their color (assumes a single non-white color per row).
   b. Finds the leftmost (minimum column index) and rightmost (maximum column index) non-white pixel.
   c. Fills the segment between the leftmost and rightmost pixel (inclusive) with that color in the output grid.
3. If a row contains fewer than two non-white pixels, it is copied directly to the output grid without modification.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the fill-horizontal-span transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    # Initialize the output array as a copy of the input
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape

    # Process each row independently
    for r in range(height):
        # Find the column indices of non-white pixels in the current row
        non_white_cols = np.where(input_array[r, :] > 0)[0]

        # Check if there are at least two non-white pixels
        if len(non_white_cols) >= 2:
            # Get the color of the non-white pixels (assuming they are all the same color in a row)
            # We take the color of the first non-white pixel found
            fill_color = input_array[r, non_white_cols[0]]
            
            # Find the minimum (leftmost) and maximum (rightmost) column index
            min_col = np.min(non_white_cols)
            max_col = np.max(non_white_cols)
            
            # Fill the span between min_col and max_col (inclusive) in the output row
            output_array[r, min_col:max_col+1] = fill_color
        # else: If fewer than 2 non-white pixels, the row remains unchanged (already copied)

    # Convert the output NumPy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid

```
```python
"""
Processes the input grid row by row. 
For each row:
1. Finds all non-white pixels (color > 0).
2. If a row contains two or more non-white pixels:
   a. Determines their color (assuming a single non-white color per row, uses the color of the first non-white pixel found).
   b. Finds the leftmost (minimum column index) and rightmost (maximum column index) non-white pixel in that row.
   c. Fills the horizontal segment between the leftmost and rightmost pixel (inclusive) with that color in the corresponding row of the output grid. Pixels outside this range retain their original color.
3. If a row contains fewer than two non-white pixels (zero or one), the row is copied directly from the input to the output grid without modification.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the fill-horizontal-span transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    # Initialize the output array as a copy of the input. This handles rows
    # with < 2 non-white pixels automatically, as they won't be modified.
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape

    # Process each row independently
    for r in range(height):
        # Find the column indices of non-white pixels (color > 0) in the current row
        non_white_cols = np.where(input_array[r, :] > 0)[0]

        # Check if there are at least two non-white pixels in this row
        if len(non_white_cols) >= 2:
            # Get the color to fill with. Assume all non-white pixels in a
            # row needing filling have the same color, take the first one.
            fill_color = input_array[r, non_white_cols[0]]
            
            # Find the minimum (leftmost) column index among non-white pixels
            min_col = np.min(non_white_cols)
            # Find the maximum (rightmost) column index among non-white pixels
            max_col = np.max(non_white_cols)
            
            # Fill the horizontal span from min_col to max_col (inclusive) 
            # in the corresponding output row with the determined fill_color.
            output_array[r, min_col:max_col+1] = fill_color
        # No explicit 'else' needed: if len(non_white_cols) < 2, the row in 
        # output_array remains as it was copied from input_array.

    # Convert the output NumPy array back to a standard Python list of lists
    output_grid = output_array.tolist()
    
    return output_grid

```
```python
"""
Processes the input grid row by row. 
For each row:
1. Finds all non-white pixels (color > 0).
2. If a row contains two or more non-white pixels:
   a. Determines their color (assuming a single non-white color per row, uses the color of the first non-white pixel found).
   b. Finds the leftmost (minimum column index) and rightmost (maximum column index) non-white pixel in that row.
   c. Fills the horizontal segment between the leftmost and rightmost pixel (inclusive) with that color in the corresponding row of the output grid. Pixels outside this range retain their original color from the input.
3. If a row contains fewer than two non-white pixels (zero or one), the row is copied directly from the input to the output grid without modification.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the fill-horizontal-span transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize the output array as a copy of the input. This handles rows
    # with < 2 non-white pixels automatically, as they won't be modified later.
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape

    # Process each row independently
    for r in range(height):
        # Find the column indices of non-white pixels (color > 0) in the current row
        non_white_cols = np.where(input_array[r, :] > 0)[0]

        # Check if there are at least two non-white pixels in this row
        if len(non_white_cols) >= 2:
            # Get the color to fill with. Assume all non-white pixels in a
            # row needing filling have the same color; take the first one found.
            fill_color = input_array[r, non_white_cols[0]]
            
            # Find the minimum (leftmost) column index among non-white pixels
            min_col = np.min(non_white_cols)
            # Find the maximum (rightmost) column index among non-white pixels
            max_col = np.max(non_white_cols)
            
            # Fill the horizontal span from min_col to max_col (inclusive) 
            # in the corresponding output row with the determined fill_color.
            # Only this segment of the output row is modified.
            output_array[r, min_col:max_col+1] = fill_color
            
        # No explicit 'else' needed: if len(non_white_cols) < 2, the row in 
        # output_array remains as it was initially copied from input_array.

    # Convert the output NumPy array back to a standard Python list of lists
    output_grid = output_array.tolist()
    
    return output_grid
```
