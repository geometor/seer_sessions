import numpy as np
import collections

"""
Natural Language Program:
1. Examine the input grid to determine the type of uniformity:
    a. Check if all rows in the input grid are identical (Grid-wise Uniformity).
    b. If not, check if each row consists of only a single value repeated across its columns (Row-wise Uniformity).
2. If Grid-wise Uniformity is detected:
    a. Take one instance of the identical row pattern.
    b. Process this row pattern by removing any consecutive duplicate values within it.
    c. Return the processed pattern as a single output row (1xM grid).
3. If Row-wise Uniformity is detected:
    a. Create a vertical sequence where each element is the unique value from the corresponding input row.
    b. Process this sequence by removing any consecutive duplicate values within it.
    c. Return the processed sequence as a single output column (Nx1 grid).
"""

def _deduplicate_consecutive(sequence):
    """Removes consecutive duplicate elements from a list."""
    if not sequence:
        return []
    deduplicated = [sequence[0]]
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[i-1]:
            deduplicated.append(sequence[i])
    return deduplicated

def _is_grid_uniform(grid_np):
    """Checks if all rows in the numpy grid are identical."""
    if grid_np.shape[0] <= 1: # A grid with 0 or 1 row is considered uniform
        return True
    first_row = grid_np[0, :]
    for i in range(1, grid_np.shape[0]):
        if not np.array_equal(grid_np[i, :], first_row):
            return False
    return True

def _all_rows_have_single_value(grid_np):
    """Checks if each row in the numpy grid consists of only one repeated value."""
    if grid_np.shape[1] <= 1: # A grid with 0 or 1 column always satisfies this
         return True
    for i in range(grid_np.shape[0]):
        first_element = grid_np[i, 0]
        # Check if all elements in the row are equal to the first element
        if not np.all(grid_np[i, :] == first_element):
            return False
    return True

def transform(input_grid):
    """
    Transforms the input grid based on detected uniformity patterns (grid-wise or row-wise)
    and removes consecutive duplicates accordingly.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Check for Grid-wise Uniformity (all rows are identical)
    if _is_grid_uniform(input_np):
        # Extract the unique row pattern (first row)
        row_pattern = input_np[0, :].tolist()
        # Deduplicate consecutive values horizontally within the pattern
        deduplicated_pattern = _deduplicate_consecutive(row_pattern)
        # Return as a single row numpy array (1xM)
        output_grid = np.array([deduplicated_pattern], dtype=int)
        return output_grid.tolist() # Convert back to list of lists if required by spec

    # Check for Row-wise Uniformity (each row has only one repeating value)
    elif _all_rows_have_single_value(input_np):
        # Create a sequence of the unique value from each row
        column_sequence = [input_np[i, 0] for i in range(height)]
        # Deduplicate consecutive values vertically in the sequence
        deduplicated_sequence = _deduplicate_consecutive(column_sequence)
        # Return as a single column numpy array (Nx1)
        output_grid = np.array(deduplicated_sequence, dtype=int).reshape(-1, 1)
        return output_grid.tolist() # Convert back to list of lists if required by spec

    else:
        # Fallback or error case if neither pattern is detected (based on examples, one should match)
        # Returning the input unchanged or raising an error might be options.
        # For now, let's return the input as per the observed patterns in training.
        # This part might need refinement if test cases show other patterns.
        print("Warning: Neither grid-wise nor row-wise uniformity detected. Returning input.")
        return input_grid
