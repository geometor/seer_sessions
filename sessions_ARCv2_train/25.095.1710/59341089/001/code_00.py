import copy

"""
Transforms a 3x3 input grid of digits into a 3x12 output grid.
For each row in the input grid:
1. Reverse the sequence of digits in the row.
2. Concatenate the reversed sequence with the original sequence to create a 6-digit intermediate sequence.
3. Concatenate the intermediate sequence with itself to create the final 12-digit output row.
The output grid consists of these transformed rows.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A 3x3 list of lists containing integer digits.

    Returns:
        A 3x12 list of lists containing the transformed integer digits.
    """
    output_grid = [] # Initialize the final output grid

    # Iterate through each row of the input grid
    for row in input_grid:
        # 1a. Let the sequence of the three digits in the current input row be R.
        r = row # In Python, lists are sequences

        # 1b. Reverse the sequence R to create a new sequence R_reversed.
        # Create a copy to avoid modifying the original row list if it's needed later, though not strictly necessary here.
        r_reversed = r[::-1]

        # 1c. Concatenate R_reversed and R to form a new sequence of six digits, M_row.
        m_row = r_reversed + r

        # 3. Construct the final 12-digit output row by horizontally concatenating M_row with itself.
        output_row = m_row + m_row

        # Add the generated 12-element row to the output_grid
        output_grid.append(output_row)

    # Return the completed output grid
    return output_grid
