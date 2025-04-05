import numpy as np

"""
Transforms a 2D grid of single-digit integers by applying a rule independently to each row.
The rule operates on contiguous horizontal blocks (runs) of identical non-zero digits within a row.
If a run of a non-zero digit has a length of 3 or more, the first and last digits
of the run are kept, and all digits in between are replaced with 0.
Runs of non-zero digits with length 1 or 2, and all runs of 0s, remain unchanged.
The overall dimensions of the grid are preserved.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule row-wise to the input 2D NumPy array grid.

    Args:
        input_grid: A 2D NumPy array of single-digit integers.

    Returns:
        A 2D NumPy array containing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    num_rows, num_cols = input_grid.shape

    # Iterate through each row of the grid
    for r in range(num_rows):
        # Process the current row
        row = input_grid[r]
        # Use a list to build the transformed row elements
        output_row_elements = []
        i = 0
        # Iterate through the columns of the current row to find blocks
        while i < num_cols:
            # Get the current digit value
            current_digit = row[i]
            # Find the end index j of the current block of identical digits
            j = i + 1
            while j < num_cols and row[j] == current_digit:
                j += 1

            # Calculate the length of the block
            block_length = j - i

            # Apply transformation logic based on the digit and block length
            if current_digit == 0:
                # Keep blocks of 0s as they are
                output_row_elements.extend([0] * block_length)
            else:
                # Handle non-zero blocks
                if block_length < 3:
                    # Keep short blocks (length 1 or 2) as they are
                    output_row_elements.extend([current_digit] * block_length)
                else:
                    # Modify blocks of length 3 or more
                    # Keep the first digit
                    output_row_elements.append(current_digit)
                    # Add 0s in the middle
                    output_row_elements.extend([0] * (block_length - 2))
                    # Keep the last digit
                    output_row_elements.append(current_digit)

            # Move the index to the start of the next block
            i = j

        # Update the corresponding row in the output grid
        # Ensure the generated row has the correct length (should match num_cols)
        if len(output_row_elements) == num_cols:
             output_grid[r, :] = np.array(output_row_elements, dtype=int)
        else:
             # This case should ideally not happen if logic is correct, but adding safety print
             print(f"Warning: Row {r} processing resulted in unexpected length {len(output_row_elements)}, expected {num_cols}. Input row: {row}")
             # Fallback: keep original row if something went wrong
             output_grid[r, :] = input_grid[r, :]


    return output_grid