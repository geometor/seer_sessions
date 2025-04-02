
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
5 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Perception**

The input grids consist primarily of white pixels (0), with a few scattered non-white pixels. In each example, the non-white pixels appear in pairs within specific rows. Each pair within a row consists of two pixels of the *same* non-white color (orange (7) in train_1, green (3) in train_2, gray (5) in train_3).

The corresponding output grids show that the space *between* these pairs of same-colored pixels in each row has been filled with that same color, effectively drawing a horizontal line segment connecting the original pair. The transformation operates independently on each row. Rows that do not contain exactly two pixels of the same non-white color remain unchanged (although this case isn't explicitly shown, it's implied by the structure).

**Facts**


```yaml
elements:
  - type: grid
    properties:
      - background_color: white (0)
      - contains: sparse colored pixels
  - type: object
    description: Colored pixels acting as endpoints.
    properties:
      - color: non-white (3, 5, 7 in examples)
      - quantity_per_row: exactly two (in relevant rows)
      - arrangement: horizontally aligned within the same row
      - relationship: form pairs of the same color
  - type: action
    description: Filling the space between endpoint pairs.
    input: a pair of same-colored pixels in a row
    output: a horizontal line segment of that color connecting the pair
    scope: operates independently on each row
  - type: result
    description: Output grid where pairs are connected.
    properties:
      - contains: horizontal line segments of non-white colors
      - segment_color: matches the color of the endpoint pair it connects
      - segment_location: spans the columns between (and including) the original endpoint pair within their row
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each row of the input grid.
3.  For the current row, identify all non-white pixels and their column indices.
4.  Check if there are exactly two non-white pixels in this row *and* if they both have the same color.
5.  If the condition in step 4 is met:
    a.  Determine the color of these two pixels (let's call it `fill_color`).
    b.  Determine the column indices of these two pixels (let's call them `col1` and `col2`).
    c.  Find the minimum column index (`min_col`) and the maximum column index (`max_col`) from `col1` and `col2`.
    d.  In the corresponding row of the *output* grid, change the color of all pixels from column `min_col` to `max_col` (inclusive) to `fill_color`.
6.  If the condition in step 4 is not met, the row in the output grid remains unchanged from the input grid (it was already copied in step 1).
7.  After processing all rows, the modified grid is the final output.
```python
import numpy as np

"""
Transformation rule:
Iterate through each row of the input grid. If a row contains exactly two non-white pixels, and both pixels have the same color, then fill the segment between these two pixels (inclusive) with that color in the corresponding row of the output grid. Otherwise, the row remains unchanged. The output grid starts as a copy of the input grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to connect pairs of same-colored pixels within each row.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each row
    for r in range(height):
        row = input_grid[r, :]
        
        # Find indices and colors of non-white pixels in the current row
        non_white_indices = np.where(row != 0)[0]
        non_white_colors = row[non_white_indices]

        # Check if there are exactly two non-white pixels
        if len(non_white_indices) == 2:
            # Check if both non-white pixels have the same color
            if non_white_colors[0] == non_white_colors[1]:
                # Get the fill color and the column indices
                fill_color = non_white_colors[0]
                col1, col2 = non_white_indices
                
                # Determine the start and end columns for filling
                min_col = min(col1, col2)
                max_col = max(col1, col2)
                
                # Fill the segment in the output grid's corresponding row
                output_grid[r, min_col:max_col + 1] = fill_color
                
    # Return the modified grid
    return output_grid
```
```python
import numpy as np
import math

"""
Transformation rule:
1. Parse the input string of space-separated integers into a 2D grid. Assume a height of 3 based on visual inspection of the examples, and calculate the width accordingly.
2. Initialize the output grid as a copy of the input grid.
3. Iterate through each row of the input grid.
4. For the current row, find all non-white pixels (value != 0).
5. If there are exactly two non-white pixels in the row and they have the same color value:
   a. Identify the color value.
   b. Identify the column indices of the two pixels.
   c. Determine the minimum and maximum of these column indices.
   d. In the corresponding row of the output grid, set all pixels from the minimum column index to the maximum column index (inclusive) to the identified color value.
6. If the condition in step 5 is not met for a row, that row in the output grid remains unchanged.
7. Return the modified output grid.
"""

def parse_input(input_str):
    """
    Parses a string of space-separated integers into a 2D NumPy array.
    Assumes a height of 3 based on the training examples.

    Args:
        input_str (str): The input string.

    Returns:
        np.ndarray: The 2D grid representation.
    """
    pixels = [int(p) for p in input_str.split()]
    num_pixels = len(pixels)
    
    # Assuming height is 3 based on training examples
    height = 3
    if num_pixels % height != 0:
         # Fallback or error handling if height isn't 3?
         # For now, let's try finding factors. Find largest factor <= 30 for height.
         factors = [i for i in range(1, int(math.sqrt(num_pixels)) + 1) if num_pixels % i == 0]
         possible_heights = sorted([f for pair in [(f, num_pixels//f) for f in factors] for f in pair if f <= 30], reverse=True)
         if not possible_heights:
             raise ValueError(f"Cannot determine valid dimensions for {num_pixels} pixels.")
         # Simple heuristic: pick the largest possible height <= 30
         height = possible_heights[0] 
         # Re-evaluate based on example structure (height seems fixed at 3)
         height = 3 # Force height = 3 as per observed examples
         if num_pixels % height != 0:
             raise ValueError(f"Input string with {num_pixels} pixels cannot form a grid with height 3.")

    width = num_pixels // height
    if width > 30:
        raise ValueError(f"Calculated width {width} exceeds maximum of 30.")
        
    grid = np.array(pixels).reshape((height, width))
    return grid

def transform(input_grid_repr):
    """
    Applies the transformation rule to connect pairs of same-colored pixels within each row.

    Args:
        input_grid_repr (str or np.ndarray): Input grid representation, either as a string 
                                             (to be parsed) or a pre-parsed numpy array.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Parse the input if it's a string
    if isinstance(input_grid_repr, str):
        input_grid = parse_input(input_grid_repr)
    elif isinstance(input_grid_repr, np.ndarray):
        input_grid = input_grid_repr
    else:
        raise TypeError("Input must be a string or a NumPy ndarray.")

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each row
    for r in range(height):
        row = input_grid[r, :]
        
        # Find indices and colors of non-white pixels in the current row
        non_white_indices = np.where(row != 0)[0]
        
        # Check if there are exactly two non-white pixels
        if len(non_white_indices) == 2:
            idx1, idx2 = non_white_indices
            color1 = row[idx1]
            color2 = row[idx2]
            
            # Check if both non-white pixels have the same color
            if color1 == color2:
                # Get the fill color
                fill_color = color1
                
                # Determine the start and end columns for filling
                min_col = min(idx1, idx2)
                max_col = max(idx1, idx2)
                
                # Fill the segment in the output grid's corresponding row
                # Slicing is exclusive of the end index, so add 1 to max_col
                output_grid[r, min_col:max_col + 1] = fill_color
                
    # Return the modified grid
    return output_grid
```
```python
import numpy as np

"""
Transformation rule:
Iterate through each row of the input grid. If a row contains exactly two non-white pixels (value != 0), and both pixels have the same color value, then fill the horizontal segment between these two pixels (inclusive) with that color in the corresponding row of the output grid. Otherwise, the row remains unchanged. The output grid starts as a copy of the input grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to connect pairs of same-colored pixels within each row.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each row
    for r in range(height):
        # Select the current row
        row = input_grid[r, :]
        
        # Find indices of non-white pixels in the current row
        non_white_indices = np.where(row != 0)[0]
        
        # Check if there are exactly two non-white pixels
        if len(non_white_indices) == 2:
            # Get the column indices of the two non-white pixels
            idx1, idx2 = non_white_indices
            
            # Get the colors of these two pixels
            color1 = row[idx1]
            color2 = row[idx2]
            
            # Check if both non-white pixels have the same color
            if color1 == color2:
                # Get the fill color (which is the color of the pair)
                fill_color = color1
                
                # Determine the start and end columns for filling (inclusive)
                min_col = min(idx1, idx2)
                max_col = max(idx1, idx2)
                
                # Fill the segment in the corresponding row of the output grid
                # Use slicing: [start_col : end_col + 1] to include the end column
                output_grid[r, min_col : max_col + 1] = fill_color
                
        # If the conditions (exactly 2 non-white pixels, same color) are not met,
        # the row in output_grid remains as it was copied from input_grid.
                
    # Return the modified grid
    return output_grid
```
