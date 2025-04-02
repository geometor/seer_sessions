
## train_1

**input:**
```
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
```


**output:**
```
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
```


**output:**
```
0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
```

**Perception**

1.  **Grid Structure:** The input and output are 2D grids of varying dimensions (Example 1 & 2: 7x9, Example 3: 8x9). The background color is consistently white (0).
2.  **Core Elements:** The key elements are the non-white pixels within each row. Their presence, count, position, and color dictate the transformation.
3.  **Row Independence:** The transformation process operates independently on each row. The changes in one row do not affect any other row.
4.  **Transformation Logic:** The transformation involves filling segments of rows horizontally based on the non-white pixels present in the input row.
5.  **Conditional Filling:** There are two distinct filling behaviors based on the *number* of non-white pixels in a row:
    *   **Single Non-White Pixel:** If a row contains exactly one non-white pixel, the output row is filled with that pixel's color starting from its column index and extending all the way to the right edge of the grid. Pixels to the left remain white.
    *   **Multiple Non-White Pixels:** If a row contains two or more non-white pixels, the output row is filled *between* the column index of the leftmost non-white pixel and the column index of the rightmost non-white pixel (inclusive). The color used for filling is the color of the *leftmost* non-white pixel in that row. Pixels outside this horizontal segment remain white.
    *   **No Non-White Pixels:** If a row contains only white pixels, the output row remains unchanged (all white).

**Facts**

```
yaml
task_type: grid_transformation
grid_properties:
  - background_color: 0 (white)
  - dimensions_vary: true # Seen 7x9 and 8x9
processing_granularity: row-wise # Each row processed independently
objects:
  - type: pixel
    attributes:
      - color: integer 0-9
      - position: (row_index, column_index)
  - type: non_white_pixel
    description: A pixel with color > 0.
    attributes:
      - color
      - position
row_analysis:
  - identify: non_white_pixels_in_row
    properties:
      - locations: list of (column_index, color) pairs
      - count: number of non_white_pixels
      - leftmost_pixel: pixel with minimum column_index (if count > 0)
      - rightmost_pixel: pixel with maximum column_index (if count > 0)
transformation_rule:
  - scope: per_row
  - conditions:
      - if: count == 0
        action: output_row = input_row (all white)
      - if: count == 1
        action:
          - get: color C and column index Col of the single non_white_pixel
          - fill: output_row from Col to grid_width-1 with C
          - keep: output_row from 0 to Col-1 as white
      - if: count > 1
        action:
          - get: color C and column index MinCol of leftmost_pixel
          - get: column index MaxCol of rightmost_pixel
          - fill: output_row from MinCol to MaxCol (inclusive) with C
          - keep: output_row outside [MinCol, MaxCol] as white

```python
import numpy as np

"""
Processes each row of the input grid independently based on the non-white pixels within that row.

Transformation rules:
1. If a row contains no non-white pixels (only white, 0), the output row remains unchanged (all white).
2. If a row contains exactly one non-white pixel:
   - Identify its color (C) and column index (Col).
   - Fill the corresponding output row with color C from column Col to the rightmost edge of the grid.
   - Pixels to the left of Col remain white (0).
3. If a row contains two or more non-white pixels:
   - Find the leftmost non-white pixel (at MinCol with color C) and the rightmost non-white pixel (at MaxCol).
   - Fill the corresponding output row with color C (the color of the leftmost pixel) from column MinCol to MaxCol (inclusive).
   - Pixels outside this range [MinCol, MaxCol] remain white (0).
"""

def find_non_white_pixels(row):
    """
    Finds the indices and colors of non-white pixels in a row.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        list: A list of tuples, where each tuple is (column_index, color).
              Returns an empty list if no non-white pixels are found.
    """
    pixels = []
    for col_idx, color in enumerate(row):
        if color != 0:
            pixels.append((col_idx, color))
    return pixels

def transform(input_grid):
    """
    Transforms the input grid based on the rules described above.

    Args:
        input_grid (list or np.ndarray): A 2D list or numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_array.shape

    # Initialize output grid with the background color (white, 0)
    output_array = np.zeros_like(input_array)

    # Process each row independently
    for r in range(num_rows):
        input_row = input_array[r, :]
        output_row = output_array[r, :] # Get a reference to the output row for modification

        # Find non-white pixels in the current input row
        non_white_pixels = find_non_white_pixels(input_row)
        count = len(non_white_pixels)

        # Apply transformation rules based on the count of non-white pixels
        if count == 0:
            # Rule 1: No non-white pixels, row remains white (already initialized)
            pass
        elif count == 1:
            # Rule 2: Exactly one non-white pixel
            col, color = non_white_pixels[0]
            # Fill from the pixel's column to the end of the row
            output_row[col:] = color
        else: # count > 1
            # Rule 3: Two or more non-white pixels
            # Find leftmost and rightmost pixel indices
            min_col = min(p[0] for p in non_white_pixels)
            max_col = max(p[0] for p in non_white_pixels)
            # Get the color of the leftmost pixel
            leftmost_color = input_row[min_col]
            # Fill between min_col and max_col (inclusive) with the leftmost color
            output_row[min_col:max_col + 1] = leftmost_color

    return output_array.tolist() # Return as list of lists to match ARC format if needed
```
```python
import numpy as np

"""
Transforms an input grid based on the non-white pixels within each row, considering a global property.

1. Determine the maximum column index (`max_col_overall`) containing any non-white pixel across the entire input grid. If the grid is all white, the output is also all white.
2. Process each row independently:
   - Find the non-white pixels in the current input row.
   - If a row has zero non-white pixels, the corresponding output row remains white (0).
   - If a row has exactly one non-white pixel (at column `col`, color `C`):
     - Fill the corresponding output row with color `C` starting from column `col` up to and including the pre-calculated `max_col_overall`.
   - If a row has two or more non-white pixels:
     - Find the leftmost non-white pixel (at `min_col_row` with color `C`) and the rightmost non-white pixel (at `max_col_row`) *within that specific row*.
     - Fill the corresponding output row with color `C` (the color of the leftmost pixel) from column `min_col_row` to `max_col_row` (inclusive).
3. Pixels outside the specified filled ranges in the output row remain white (0).
"""

def find_non_white_pixel_data(row):
    """
    Finds indices and colors of non-white pixels in a row.

    Args:
        row (np.array): A 1D numpy array representing a row.

    Returns:
        list: A list of tuples (column_index, color). Empty if none found.
    """
    # Helper function to identify non-white pixels and their locations/colors in a single row
    pixels = []
    for col_idx, color in enumerate(row):
        if color != 0: # 0 is the background/white color
            pixels.append((col_idx, color))
    return pixels

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input grid (list of lists) to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_array.shape

    # Initialize the output grid with the same dimensions, filled with background color (0)
    output_array = np.zeros_like(input_array)

    # --- Global Analysis Step ---
    # Find the column indices of all non-white pixels in the entire grid
    non_white_coords = np.where(input_array != 0)
    # Check if there are any non-white pixels at all
    if non_white_coords[1].size == 0:
        # If the grid is entirely white, return an all-white grid of the same size
        return output_array.tolist()
    # Determine the maximum column index reached by any non-white pixel
    max_col_overall = non_white_coords[1].max()

    # --- Row-wise Processing Step ---
    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Get the current row from the input array
        input_row = input_array[r, :]
        # Get a reference to the corresponding row in the output array for modification
        output_row = output_array[r, :]

        # Find non-white pixel data (index, color) specifically for this row
        non_white_pixels_in_row = find_non_white_pixel_data(input_row)
        count = len(non_white_pixels_in_row)

        # --- Apply Transformation Rules Based on Pixel Count in the Row ---
        if count == 0:
            # Rule 1: No non-white pixels in this row.
            # Output row remains all zeros (as initialized).
            pass # No action needed
        elif count == 1:
            # Rule 2: Exactly one non-white pixel in this row.
            col, color = non_white_pixels_in_row[0]
            # Fill the output row from this pixel's column up to the global max column index.
            # The slice end index needs to be `max_col_overall + 1` to include `max_col_overall`.
            fill_end_col = max_col_overall + 1
            # Apply the fill to the output row using numpy slicing
            output_row[col:fill_end_col] = color
        else: # count > 1
            # Rule 3: Two or more non-white pixels in this row.
            # Extract just the column indices of non-white pixels in this row
            cols_in_row = [p[0] for p in non_white_pixels_in_row]
            # Find the minimum (leftmost) and maximum (rightmost) column index for this row
            min_col_row = min(cols_in_row)
            max_col_row = max(cols_in_row)
            # Get the color of the leftmost pixel in this row
            # We can access this directly from the input row using the calculated min_col_row
            leftmost_color = input_row[min_col_row]
            # Fill the output row between the row-specific min and max columns (inclusive).
            # The slice end index needs to be `max_col_row + 1` to include `max_col_row`.
            output_row[min_col_row : max_col_row + 1] = leftmost_color

    # Convert the final numpy array back to a list of lists format
    return output_array.tolist()
```
```python
import numpy as np

"""
Transforms an input grid based on the non-white pixels within each row, considering a global property.

1. Determine the maximum column index (`max_col_overall`) containing any non-white pixel across the entire input grid. If the grid is all white, the output is also all white.
2. Process each row independently:
   - Find the non-white pixels in the current input row.
   - If a row has zero non-white pixels, the corresponding output row remains white (0).
   - If a row has exactly one non-white pixel (at column `col`, color `C`):
     - Fill the corresponding output row with color `C` starting from column `col` up to and including the pre-calculated `max_col_overall`.
   - If a row has two or more non-white pixels:
     - Find the leftmost non-white pixel (at `min_col_row` with color `C`).
     - Fill the corresponding output row with color `C` (the color of the leftmost pixel) from column `min_col_row` up to and including the pre-calculated `max_col_overall`.
3. Pixels outside the specified filled ranges in the output row remain white (0).
"""

def find_non_white_pixel_data(row):
    """
    Finds indices and colors of non-white pixels in a row.

    Args:
        row (np.array): A 1D numpy array representing a row.

    Returns:
        list: A list of tuples (column_index, color). Empty if none found.
    """
    pixels = []
    for col_idx, color in enumerate(row):
        if color != 0: # 0 is the background/white color
            pixels.append((col_idx, color))
    return pixels

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input grid (list of lists) to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_array.shape

    # Initialize the output grid with the same dimensions, filled with background color (0)
    output_array = np.zeros_like(input_array)

    # --- Global Analysis Step ---
    # Find the coordinates (row, col) of all non-white pixels in the entire grid
    non_white_coords = np.where(input_array != 0)

    # Check if there are any non-white pixels at all
    if non_white_coords[1].size == 0:
        # If the grid is entirely white, return an all-white grid of the same size
        return output_array.tolist()

    # Determine the maximum column index reached by any non-white pixel
    # non_white_coords[1] contains the column indices
    max_col_overall = non_white_coords[1].max()
    # Calculate the end index for slicing (exclusive)
    fill_end_col = max_col_overall + 1

    # --- Row-wise Processing Step ---
    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Get the current row from the input array
        input_row = input_array[r, :]
        # Get a reference to the corresponding row in the output array for modification
        output_row = output_array[r, :]

        # Find non-white pixel data (index, color) specifically for this row
        non_white_pixels_in_row = find_non_white_pixel_data(input_row)
        count = len(non_white_pixels_in_row)

        # --- Apply Transformation Rules Based on Pixel Count in the Row ---
        if count == 0:
            # Rule: No non-white pixels in this row.
            # Output row remains all zeros (as initialized).
            pass # No action needed

        elif count == 1:
            # Rule: Exactly one non-white pixel in this row.
            col, color = non_white_pixels_in_row[0]
            # Fill the output row from this pixel's column up to the global max column index (inclusive).
            # Apply the fill to the output row using numpy slicing
            output_row[col:fill_end_col] = color

        else: # count > 1
            # Rule: Two or more non-white pixels in this row.
            # Extract just the column indices of non-white pixels in this row
            cols_in_row = [p[0] for p in non_white_pixels_in_row]
            # Find the minimum (leftmost) column index for this row
            min_col_row = min(cols_in_row)
            # Get the color of the leftmost pixel in this row
            # We can access this directly from the input row using the calculated min_col_row
            leftmost_color = input_row[min_col_row]
            # Fill the output row from the row-specific min column up to the global max column index (inclusive).
            output_row[min_col_row : fill_end_col] = leftmost_color

    # Convert the final numpy array back to a list of lists format
    return output_array.tolist()
```
