```python
import math

"""
Transforms an input grid of integers by padding each row with zeros. 
The total number of zeros added to each row is one less than the total number of rows (N-1).
For each row (indexed i from 0), N-1-i zeros are prepended and i zeros are appended.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a row-wise padding transformation to the input grid.

    Args:
        input_grid: A list of lists of integers representing the input grid.

    Returns:
        A list of lists of integers representing the transformed grid.
    """
    # Initialize the output grid
    output_grid = []
    
    # Determine the number of rows (N)
    num_rows = len(input_grid)
    
    # Handle edge case of empty input
    if num_rows == 0:
        return []
        
    # Calculate the total number of zeros to add per row (Z)
    total_padding_per_row = num_rows - 1
    
    # Iterate through each row of the input grid with its index
    for i, input_row in enumerate(input_grid):
        # Calculate the number of zeros to prepend (left padding)
        num_left_zeros = total_padding_per_row - i
        
        # Calculate the number of zeros to append (right padding)
        num_right_zeros = i
        
        # Create the left padding list
        left_padding = [0] * num_left_zeros
        
        # Create the right padding list
        right_padding = [0] * num_right_zeros
        
        # Construct the new output row by concatenating left padding, original row, and right padding
        output_row = left_padding + input_row + right_padding
        
        # Add the newly constructed row to the output grid
        output_grid.append(output_row)

    # Return the completed output grid
    return output_grid

```