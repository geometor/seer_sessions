```python
import numpy as np
import copy

"""
Transforms a 2D grid by changing sequences of 0s to 2s if they are immediately 
adjacent horizontally (left or right) to a sequence of 5s within the same row.
"""

def find_sequences(row, target_value):
    """
    Finds all contiguous horizontal sequences of a target value in a row.

    Args:
        row (list or np.array): A single row from the grid.
        target_value (int): The value to find sequences of.

    Returns:
        list: A list of tuples, where each tuple is (start_col, end_col) 
              representing the inclusive start and end indices of a sequence.
    """
    sequences = []
    in_sequence = False
    start_col = -1
    for col_idx, value in enumerate(row):
        if value == target_value and not in_sequence:
            # Start of a new sequence
            in_sequence = True
            start_col = col_idx
        elif value != target_value and in_sequence:
            # End of the current sequence
            sequences.append((start_col, col_idx - 1))
            in_sequence = False
            start_col = -1
        # Handle sequence ending at the last element
        if in_sequence and col_idx == len(row) - 1:
             sequences.append((start_col, col_idx))
    return sequences

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.array): The input 2D grid.

    Returns:
        np.array: The transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Iterate through each row independently
    for r in range(rows):
        current_row = input_np[r, :]
        
        # Find all horizontal sequences of 0s in the current row
        zero_sequences = find_sequences(current_row, 0)
        
        # Find all horizontal sequences of 5s in the current row
        five_sequences = find_sequences(current_row, 5)
        
        # If there are no 5s in the row, no changes are needed for this row
        if not five_sequences:
            continue
            
        # Check each sequence of 0s for adjacency to any sequence of 5s
        for zero_start, zero_end in zero_sequences:
            is_adjacent_to_five = False
            for five_start, five_end in five_sequences:
                # Check if zero sequence is immediately to the left of a five sequence
                if zero_end + 1 == five_start:
                    is_adjacent_to_five = True
                    break 
                # Check if zero sequence is immediately to the right of a five sequence
                if five_end + 1 == zero_start:
                    is_adjacent_to_five = True
                    break
            
            # If an adjacent 5 sequence was found, change the 0s to 2s in the output grid
            if is_adjacent_to_five:
                for c in range(zero_start, zero_end + 1):
                    output_grid[r, c] = 2

    return output_grid.tolist() # Return as list of lists if preferred, or output_grid for numpy array
```