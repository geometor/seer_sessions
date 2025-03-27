"""
Iterate through each row of the input grid. If a row contains only zeros, skip it. If a row contains any non-zero values, extract all non-zero values, preserving their original order, and create a new row in the output grid with these values. The output is a list of lists (ragged array).
"""

def transform(input_grid):
    # Initialize an empty list to hold the output rows.
    output_grid = []

    # Iterate through each row of the input grid.
    for row in input_grid:
        # Extract non-zero values from the current row.
        non_zero_values = [value for value in row if value != 0]

        # If the row contained any non-zero values, add it to the output.
        if non_zero_values:
            output_grid.append(non_zero_values)

    return output_grid