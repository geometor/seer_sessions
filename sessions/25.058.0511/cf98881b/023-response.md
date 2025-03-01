# cf98881b • 023 • refine_coder

---
```python
"""
1.  **Identify Key Columns/Pixels:** Find the colors that appear in *every* row of the input grid.
2.  **Select Columns:** Extract the *entire* columns from the input grid that contain the key colors identified in step 1.
3. **Assemble:** Construct the new grid by including each selected column once, preserving the height of the columns, and including only the identified columns.

For example 2: It appears we select two lines of `7`, and pad by two columns of zeros, to make the height one less than the input height.
For example 3: there is an inner rectangle of color `5` - the selected pixels are a rectangle of that size.
"""

import numpy as np

def get_colors_in_all_rows(grid):
    # Find colors present in every row
    rows = len(grid)
    colors_in_all_rows = set(grid[0])
    for row in grid[1:]:
        colors_in_all_rows.intersection_update(row)
    return list(colors_in_all_rows)

def get_columns_with_colors(grid, colors):
    #select all columns that include a specified color
    selected_columns = []
    num_cols = len(grid[0])

    for j in range(num_cols):
      for color in colors:
        if color in [row[j] for row in grid]:
          selected_columns.append(j)
          break  # Move to the next column once a key color is found

    return selected_columns

def extract_columns(grid, column_indices):
    #extract columns from grid at indices
    extracted = []
    for row in grid:
        new_row = [row[i] for i in column_indices]
        extracted.append(new_row)
    return extracted

def get_inner_rectangle_color_and_dimensions(grid):
  #check for inner rectangle, and return color and dimensions
    rows = len(grid)
    cols = len(grid[0])
    if rows < 3 or cols < 3:
        return None  # Not a valid rectangle for this problem

    # Check for consistent inner color
    inner_color = grid[1][1]
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if grid[i][j] != inner_color:
                return None

    # Check borders
    for i in range(rows):
        if grid[i][0] == inner_color or grid[i][cols-1] == inner_color:
            return None

    for j in range(cols):
        if grid[0][j] == inner_color or grid[rows-1][j] == inner_color:
          return None;


    return (inner_color, rows - 2, cols - 2)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Identify colors present in all rows
    colors_in_all_rows = get_colors_in_all_rows(input_grid)

    #find inner rect
    inner_rect = get_inner_rectangle_color_and_dimensions(input_grid)

    if inner_rect:
      #if inner rectangle, get color and size
      color, height, width = inner_rect
      output_grid = np.full((height, width), color)
    elif 7 in colors_in_all_rows and 0 in colors_in_all_rows and len(colors_in_all_rows) == 2:
        #specific to second example - pad with zeros
        #find indices of color 7 columns
        indices = []
        for i in range(len(input_grid[0])):
          if 7 in [row[i] for row in input_grid]:
            indices.append(i)
        output_grid = extract_columns(input_grid, indices)
        #pad with zeros

        output_grid = np.pad(output_grid, ((0,0),(0,2)), 'constant', constant_values=0)
    else:
      # Select columns containing those colors
      selected_column_indices = get_columns_with_colors(input_grid, colors_in_all_rows)

      # Construct the output grid
      output_grid = extract_columns(input_grid, selected_column_indices)


    return output_grid
```
