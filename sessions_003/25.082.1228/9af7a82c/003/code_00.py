"""
1.  **Input:** Receive the input grid as a 2D array of integers representing colors.
2.  **Unique Colors:** Extract the unique integer values (colors) present in the input grid.
3.  **Sort Colors:** Sort the unique colors in ascending order.
4.  **Output Dimensions:**
    *   The output grid's width is equal to the number of unique colors.
    *   The output grid height is determined by the original height of the input grid
5.  **Populate Output:**
    *   Iterate through each sorted unique color.
    *   For each color, create a column in the output grid.
    *   Populate this column from top to bottom by iterating through the input grid.
    *   When you find an instance of the current color you are iterating over, put it at the top of the column.
    *   When you find another instance of the color, add it to the column below the current instance, and so forth until the whole column is populated.
    *   Move to the next column.
6.  **Fill with Zero:** If a column runs out of unique values, it is not necessary to fill the rest of that column - it is zero by default.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)

    # Extract unique values and sort them in ascending order
    unique_values = np.unique(input_array)
    sorted_values = np.sort(unique_values)

    # Create an output grid of size input_height x number of unique values, filled with 0s
    output_grid = np.zeros((len(input_array), len(sorted_values)), dtype=int)

    # Populate the output grid with the sorted values
    for col_index, value in enumerate(sorted_values):
        row_index = 0 #reset index for each column
        for i in range(input_array.shape[0]): #iterate through each row of input
            for j in range(input_array.shape[1]): #iterate through each column of the input
                if input_array[i,j] == value:
                   output_grid[row_index, col_index] = value
                   row_index+=1
                if row_index >= len(input_array):
                    break
            if row_index >= len(input_array):
                break


    return output_grid.tolist()