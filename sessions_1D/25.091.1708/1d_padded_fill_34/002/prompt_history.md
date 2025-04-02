
## train_1

**input:**
```
0 0 5 0 0 0 0 0 0 0 0 5 0 0 0 0 5 0 0 0 0 0 0 0 0 5 0 0 0 0 5 0 0 0 0 0 0 0 0 5 0 0
```


**output:**
```
0 0 5 5 5 5 5 5 5 5 5 5 0 0 0 0 5 5 5 5 5 5 5 5 5 5 0 0 0 0 5 5 5 5 5 5 5 5 5 5 0 0
```


## train_2

**input:**
```
0 0 7 0 0 0 0 0 0 0 0 7 0 0 0 0 7 0 0 0 0 0 0 0 0 7 0 0 0 0 7 0 0 0 0 0 0 0 0 7 0 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 7 7 7 0 0 0 0 7 7 7 7 7 7 7 7 7 7 0 0 0 0 7 7 7 7 7 7 7 7 7 7 0 0
```


## train_3

**input:**
```
2 0 0 0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 0
```


**output:**
```
2 2 2 2 2 2 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0 0
```

Okay, let's break down this task.

**Perception:**

1.  **Grid Structure:** The input and output are grids. Based on the number of elements (42) and the visual pattern in the examples, the grids appear to be 3 rows high and 14 columns wide.
2.  **Color Usage:** Each example uses exactly two colors: white (0) as the background and one other color (gray=5, orange=7, or red=2). The specific non-white color changes between examples but is consistent within a single input/output pair.
3.  **Input Pattern:** In the input grids, the non-white pixels are sparsely placed within each row. Often, there are two or more non-white pixels per row, separated by white pixels.
4.  **Output Pattern:** In the output grids, horizontal segments are formed using the non-white color. These segments appear to span the gap between the leftmost and rightmost non-white pixels found in the corresponding input row.
5.  **Transformation:** The core transformation seems to involve finding the horizontal extent (leftmost to rightmost occurrence) of the non-white color in each row of the input and then filling that entire horizontal span with the same non-white color in the output grid. Rows containing only white pixels in the input remain unchanged in the output.

**Facts:**


```yaml
task_description: Fill horizontal segments defined by the first and last non-white pixels in each row.
grid_properties:
  height: 3
  width: 14
objects:
  - type: pixel
    properties:
      color: white (0), gray (5), orange (7), or red (2)
  - type: horizontal_segment
    definition: A contiguous sequence of pixels within a single row.
relationships:
  - The non-white color used is consistent within an input-output pair but varies across pairs.
  - In the input, non-white pixels act as markers for segment boundaries within each row.
  - In the output, horizontal segments are filled with the non-white color.
transformation:
  - Identify the unique non-white color present in the input grid.
  - For each row:
    - Find the column index of the first occurrence of the non-white color.
    - Find the column index of the last occurrence of the non-white color.
    - If non-white pixels exist in the row:
      - Create the corresponding output row by filling all pixels between the first and last column index (inclusive) with the non-white color.
      - Pixels outside this range remain white.
    - If no non-white pixels exist in the row:
      - Copy the row unchanged (all white) to the output.
  - The output grid dimensions are the same as the input grid dimensions.
```


**Natural Language Program:**

1.  Determine the dimensions (height and width) of the input grid.
2.  Identify the single non-white color present in the input grid. Let this color be `C`.
3.  Create a new output grid of the same dimensions as the input, initially filled with white (0).
4.  Iterate through each row of the input grid, from top to bottom (row index `r` from 0 to height-1).
5.  For the current row `r`:
    a.  Find the column index of the first (leftmost) pixel with color `C`. Store this as `start_col`. If no pixel has color `C`, `start_col` is undefined.
    b.  Find the column index of the last (rightmost) pixel with color `C`. Store this as `end_col`. If no pixel has color `C`, `end_col` is undefined.
    c.  If both `start_col` and `end_col` were found for row `r`:
        i.  Iterate through the columns from `start_col` to `end_col` (inclusive).
        ii. For each column index `c` in this range, set the pixel at `(r, c)` in the output grid to color `C`.
    d.  If color `C` was not found in row `r` (i.e., `start_col` and `end_col` are undefined), leave row `r` of the output grid as all white.
6.  Return the completed output grid.
```python
import numpy as np

"""
Fill horizontal segments in each row defined by the first and last occurrence of the non-white pixel color.

For each row in the input grid:
1. Identify the unique non-white color present in the entire input grid.
2. Find the column index of the leftmost occurrence of this non-white color in the row.
3. Find the column index of the rightmost occurrence of this non-white color in the row.
4. If non-white pixels are found in the row, fill the corresponding row in the output grid 
   between the leftmost and rightmost indices (inclusive) with that non-white color.
5. If a row contains only the background color (white, 0), leave the corresponding row in the 
   output grid as all white.
"""

def find_non_white_color(grid):
  """Finds the first non-white (non-zero) color in the grid."""
  unique_colors = np.unique(grid)
  for color in unique_colors:
    if color != 0:
      return color
  return 0 # Should not happen based on task examples, but return background if no other color found

def transform(input_grid):
  """
  Applies the horizontal segment filling transformation.
  """
  # Convert input list of lists to numpy array for easier processing
  input_grid_np = np.array(input_grid, dtype=int)
  height, width = input_grid_np.shape

  # Initialize output grid with the background color (white, 0)
  output_grid = np.zeros_like(input_grid_np)

  # Find the dominant non-white color in the input grid
  fill_color = find_non_white_color(input_grid_np)

  # If no non-white color is found (e.g., all white input), return the all-white grid
  if fill_color == 0:
      return output_grid.tolist() # Return as list of lists

  # Process each row independently
  for r in range(height):
    row = input_grid_np[r, :]
    
    # Find the indices of the fill_color in the current row
    indices = np.where(row == fill_color)[0]

    # If the fill_color exists in this row
    if len(indices) > 0:
      # Find the first (leftmost) and last (rightmost) occurrences
      start_col = np.min(indices)
      end_col = np.max(indices)

      # Fill the segment in the output grid's corresponding row
      output_grid[r, start_col : end_col + 1] = fill_color

  # Return the result as a list of lists, as required by the ARC format
  return output_grid.tolist()

```
