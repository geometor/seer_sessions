"""
1.  **Identify Azure Pixels:** Locate all pixels with the color azure (8) within the input grid.
2.  **Vertical Extraction:** Extract the *rows* that contain the azure (8) pixels
3.  **Construct Output:** Create a new grid with a single column.
4.  **Populate Output:** Place azure pixels into the output grid. The number of rows in the output grid is equal to the number of rows containing azure in the input.
"""

import numpy as np

def get_rows_with_azure(input_grid):
    """
    Finds the indices of rows containing azure (8) pixels.
    """
    input_grid = np.array(input_grid)
    rows_with_azure = []
    for i, row in enumerate(input_grid):
        if 8 in row:
            rows_with_azure.append(i)
    return rows_with_azure

def transform(input_grid):
    """
    Transforms the input grid according to the rules.
    """
    # Identify rows containing azure
    rows_with_azure = get_rows_with_azure(input_grid)

    # Construct output grid: Number of rows = number of rows with azure. 1 column.
    output_grid = np.zeros((len(rows_with_azure), 1), dtype=int)

    # Populate with Azure, and copy the value
    row_index = 0
    for row_num in rows_with_azure:
       for col in range(len(input_grid[0])):
          if input_grid[row_num][col] == 8:
            output_grid[row_index,0] = 8
            break; # only copy once per row
       row_index += 1


    return output_grid.tolist()