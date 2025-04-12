import numpy as np
import copy

"""
Identify the smallest non-zero integer (replacement_num) and the largest 
non-zero integer (target_num) in the input grid.
Create a copy of the input grid for the output.
Iterate through each column of the grid.
For each column:
  Find the row index of the first occurrence of replacement_num.
  If replacement_num is found in the column:
    Iterate through the rows below the first occurrence of replacement_num.
    If a cell in these lower rows contains target_num, change its value 
    in the output grid to replacement_num.
Return the modified output grid.
"""

def find_key_values(grid: np.ndarray) -> tuple[int | None, int | None]:
    """Finds the smallest and largest non-zero values in the grid."""
    non_zeros = grid[grid > 0]
    if non_zeros.size == 0:
        return None, None  # No non-zero numbers found
    
    min_val = np.min(non_zeros)
    max_val = np.max(non_zeros)
    return min_val, max_val

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule: replaces the largest non-zero number 
    with the smallest non-zero number in cells below the first occurrence 
    of the smallest number within each column.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    
    # Get grid dimensions
    rows, cols = input_np.shape

    # Find the smallest (replacement) and largest (target) non-zero numbers
    replacement_num, target_num = find_key_values(input_np)

    # If no non-zero numbers or only one unique non-zero number, return copy
    if replacement_num is None or target_num is None or replacement_num == target_num:
        return output_np.tolist()

    # Iterate through each column
    for j in range(cols):
        col = input_np[:, j]
        
        # Find the index of the first occurrence of replacement_num in the column
        first_occurrence_indices = np.where(col == replacement_num)[0]
        
        # If replacement_num exists in this column
        if len(first_occurrence_indices) > 0:
            first_occurrence_row = first_occurrence_indices[0]
            
            # Iterate through rows below the first occurrence
            for i in range(first_occurrence_row + 1, rows):
                # If the cell in the input grid contains the target number
                if input_np[i, j] == target_num:
                    # Change the corresponding cell in the output grid to replacement_num
                    output_np[i, j] = replacement_num

    # Convert the result back to a list of lists
    return output_np.tolist()