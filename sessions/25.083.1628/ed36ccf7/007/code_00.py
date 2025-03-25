"""
Transformation rule based on identifying a fixed row or column and reflecting, or a special case
where the first row of the input becomes the first column of the output, combined with a horizontal reflection.

1.  **Identify Fixed Row/Column:** Check for a row or column identical in input and output.
2.  **Conditional Reflection:**
    *   Fixed row: Reflect other rows vertically across the fixed row.
    *   Fixed column: Reflect other columns horizontally across the fixed column.
3. **Special Case for the first row.**
    If no fixed row or column is found directly: Check if the top row consists of identical color,
    and if this color row appears in the first column of the output grid.
    If this special case is identified:
    *   Copy the first row of the input to the first column of the output.
    *  Reflect the input horizontally to construct rest of the output.

"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on fixed row/column reflection or a special case.
    """
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    output_array = input_array.copy()

    # 1. Identify Fixed Row/Column
    fixed_row = -1
    for i in range(rows):
        if np.array_equal(input_array[i, :], output_array[i, :]):
            fixed_row = i
            break

    fixed_col = -1
    for j in range(cols):
        if np.array_equal(input_array[:, j], output_array[:, j]):
            fixed_col = j
            break

    # 2. Conditional Reflection
    if fixed_row != -1:
        # Vertical reflection across the fixed row
        for i in range(rows):
            if i != fixed_row:
                output_array[i, :] = input_array[rows - 1 - i if rows - 1 - i != fixed_row else i, :]
        return output_array.tolist()
    elif fixed_col != -1:
        # Horizontal reflection across the fixed column
        for j in range(cols):
            if j != fixed_col:
                output_array[:, j] = input_array[:, cols - 1 - j if cols -1 - j != fixed_col else j]
        return output_array.tolist()

    # 3. Special Case: First row becomes first column + Horizontal reflection

    first_row = input_array[0, :]
    if np.all(first_row == first_row[0]):  # Check if the first row has uniform color.
      first_col_output = [row[0] for row in output_array]

      if np.array_equal(first_row, first_col_output):
          output_array[:,0] = input_array[0,:]

          for j in range(1,cols):
            output_array[:,j] = input_array[:,cols-j]

          return output_array.tolist()


    return output_array.tolist()