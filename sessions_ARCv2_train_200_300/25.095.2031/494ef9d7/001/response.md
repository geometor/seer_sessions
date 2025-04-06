```python
import copy

"""
Processes a 2D grid of digits row by row. 
If a row contains exactly two non-zero digits, and these digits form the pair {1, 8} or {4, 7}, 
the rightmost of these two digits is moved to the position immediately to the right of the leftmost digit. 
The original position of the moved digit becomes 0. 
Rows not meeting these conditions remain unchanged.
"""

def find_non_zeros(row: list[int]) -> list[tuple[int, int]]:
    """
    Finds non-zero digits and their indices in a row.
    
    Args:
        row: A list of integers representing a grid row.
        
    Returns:
        A list of tuples, where each tuple is (value, index) for a non-zero digit.
    """
    non_zeros = []
    for index, value in enumerate(row):
        if value != 0:
            non_zeros.append((value, index))
    return non_zeros

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists of integers representing the input grid.

    Returns:
        A list of lists of integers representing the transformed grid.
    """
    # Initialize output_grid as a deep copy to avoid modifying the input directly
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each row of the grid
    for r_idx, row in enumerate(output_grid):
        
        # Find all non-zero digits and their original column indices in the current row
        non_zero_elements = find_non_zeros(row)
        
        # Check if the row contains exactly two non-zero digits
        if len(non_zero_elements) == 2:
            # Extract the values and indices
            val1, idx1 = non_zero_elements[0]
            val2, idx2 = non_zero_elements[1]
            
            # Determine the set of values
            value_set = {val1, val2}
            
            # Check if the set of values matches the required pairs {1, 8} or {4, 7}
            if value_set == {1, 8} or value_set == {4, 7}:
                # Identify the leftmost and rightmost non-zero elements
                # Indices are already sorted as find_non_zeros iterates left-to-right
                left_val, c_left = non_zero_elements[0]
                right_val, c_right = non_zero_elements[1]

                # Perform the move:
                # 1. Place the rightmost value immediately to the right of the leftmost value's original position
                output_grid[r_idx][c_left + 1] = right_val
                # 2. Set the original position of the rightmost value to 0
                output_grid[r_idx][c_right] = 0
                
        # If conditions (count != 2 or pair not matched) are not met, the row remains unchanged (already copied)

    return output_grid
```