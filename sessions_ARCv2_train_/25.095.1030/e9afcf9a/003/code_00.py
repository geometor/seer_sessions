import numpy as np

"""
Generate two output sequences by alternating elements derived from the rows of an input NumPy array.
The first row contains repetitions of num1, the second row contains repetitions of num2.
The first output line starts with num1 and alternates with num2.
The second output line starts with num2 and alternates with num1.
Both output lines have the same length as the input rows.
The final output is a single string with the two lines separated by a newline.
"""

def transform(input_grid: np.ndarray) -> str:
    """
    Transforms the input 2D NumPy array based on the alternating pattern.

    Args:
        input_grid: A 2D NumPy array with shape (2, N) containing integer repetitions
                    in each row.

    Returns:
        A string containing two lines, representing the transformed output.
    """

    # --- Data Extraction ---
    # Identify the unique number from the first row (index 0)
    # Since all elements in the row are the same, we can take the first one.
    num1 = input_grid[0, 0]

    # Identify the unique number from the second row (index 1)
    num2 = input_grid[1, 0]

    # Determine the length (number of columns) of the sequences
    length = input_grid.shape[1]

    # --- Create the first output line ---
    output_line1_list = []
    # Iterate through the indices from 0 up to length - 1
    for i in range(length):
        # If the index is even, use num1
        if i % 2 == 0:
            output_line1_list.append(num1)
        # If the index is odd, use num2
        else:
            output_line1_list.append(num2)
    # Convert numbers to strings and format the sequence as a space-separated string
    output_line1 = ' '.join(map(str, output_line1_list))

    # --- Create the second output line ---
    output_line2_list = []
    # Iterate through the indices from 0 up to length - 1
    for i in range(length):
        # If the index is even, use num2
        if i % 2 == 0:
            output_line2_list.append(num2)
        # If the index is odd, use num1
        else:
            output_line2_list.append(num1)
    # Convert numbers to strings and format the sequence as a space-separated string
    output_line2 = ' '.join(map(str, output_line2_list))

    # --- Combine Output Lines ---
    # Combine the two output strings with a newline character in between
    output_str = output_line1 + '\n' + output_line2

    return output_str