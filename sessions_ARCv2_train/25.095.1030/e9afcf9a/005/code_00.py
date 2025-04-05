import numpy as np

"""
Generate a 2xN grid where each row contains alternating elements derived from the 
two unique numbers present in the input 2xN grid. The first output row starts 
with the number from the first input row, and the second output row starts with 
the number from the second input row.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms a 2xN input NumPy array by creating two new rows with alternating 
    elements derived from the input rows.

    Args:
        input_grid: A 2D NumPy array with shape (2, N) containing integer 
                    repetitions in each row.

    Returns:
        A 2D NumPy array with shape (2, N) representing the transformed grid.
    """
    # --- Data Extraction ---
    # Identify the unique number from the first row (index 0)
    # Since all elements in the row are the same, we can take the first one.
    num1 = input_grid[0, 0]

    # Identify the unique number from the second row (index 1)
    num2 = input_grid[1, 0]

    # Determine the length (number of columns) of the sequences
    length = input_grid.shape[1]

    # --- Initialize Output Structures ---
    # Create empty lists to hold the elements for the output rows
    output_row1_list = []
    output_row2_list = []

    # --- Generate Output Rows ---
    # Iterate through the indices from 0 up to length - 1
    for i in range(length):
        # Check if the current index is even or odd to determine alternation
        if i % 2 == 0:
            # Even index: first row gets num1, second row gets num2
            output_row1_list.append(num1)
            output_row2_list.append(num2)
        else:
            # Odd index: first row gets num2, second row gets num1
            output_row1_list.append(num2)
            output_row2_list.append(num1)

    # --- Construct Output Grid ---
    # Create the final 2D NumPy array from the generated lists
    # Ensure the data type matches the input (or is integer)
    output_grid = np.array([output_row1_list, output_row2_list], dtype=input_grid.dtype)

    return output_grid