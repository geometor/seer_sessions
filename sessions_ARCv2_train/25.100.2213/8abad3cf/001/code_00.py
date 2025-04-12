import numpy as np
from collections import Counter
import itertools

# Note: The natural language description and the implemented logic below are primarily
# based on reverse-engineering the 'train_2' example. The 'train_1' example follows
# significantly different rules for determining dimensions (H, W) and for transforming
# the second block (B2), indicating this logic is not general across all examples.
# This implementation attempts to capture the specific pattern observed in 'train_2'.

"""
Transform the input grid based on the location of its least frequent color, following a pattern observed in one specific example (train_2).

1. Convert the input list of lists grid to a NumPy array.
2. Find the color (digit) that appears least frequently in the entire grid. If there's a tie in frequency, choose the smallest color value.
3. Find the minimum row index (r_min) where this least frequent color first appears.
4. Determine the height (H) for constructing output blocks, hypothesized as r_min - 1. If H <= 0, the rule is considered inapplicable.
5. Define the starting column index (c_start) for extracting the second input block (B2) as 1.
6. Calculate the width (W2) of the second block (B2) as the input grid's width minus c_start.
7. Set the width (W1) of the first block (B1) equal to H.
8. Extract the top-left subgrid B1 from the input array, with dimensions H x W1 (input_array[0:H, 0:W1]). Handle boundary conditions.
9. Create the right part of the output grid (OutputRight) by taking the first row of B1 and repeating it vertically H times. OutputRight has dimensions H x W1.
10. Define the starting row index (r_start) for extracting B2 as r_min - 1 (which equals H).
11. Extract the subgrid B2 from the input array, starting at (r_start, c_start) with dimensions H x W2 (input_array[r_start : r_start+H, c_start : c_start+W2]). Handle boundary conditions.
12. Transform B2 to create the left part of the output grid (OutputLeft). The specific transformation observed in train_2 involves swapping the second and third columns of B2 (0-indexed columns 1 and 2). If B2 has fewer than 3 columns, it remains unchanged.
13. Horizontally concatenate OutputLeft and OutputRight to form the final output NumPy array.
14. Convert the final NumPy array back to a list of lists.
"""

def find_least_frequent_color_and_min_row(grid: np.ndarray) -> tuple[int, int]:
    """
    Finds the least frequent color (smallest value in case of tie)
    and its minimum row index in the grid.

    Args:
        grid: The input NumPy array.

    Returns:
        A tuple containing (least_frequent_color, min_row_index).
        Returns (-1, -1) if the grid is empty.
    """
    if grid.size == 0:
        return -1, -1

    counts = Counter(grid.flatten())
    if not counts: # Check if counter is empty (e.g., grid was empty)
        return -1, -1
        
    min_freq = min(counts.values())
    # Get all colors with the minimum frequency
    least_frequent_colors = [color for color, freq in counts.items() if freq == min_freq]
    # Tie-breaking: choose the smallest color value
    target_color = min(least_frequent_colors)

    # Find all indices where the target color appears
    indices = np.argwhere(grid == target_color)
    if indices.size == 0:
         # This case should theoretically not be reached if Counter found the color
         return target_color, -1 # Indicate color found, but index finding failed

    # Find the minimum row index among these occurrences
    min_row_index = np.min(indices[:, 0])
    return target_color, min_row_index

def transform_b2(block_b2: np.ndarray) -> np.ndarray:
    """
    Transforms Block B2 by swapping columns 1 and 2 (0-indexed).
    If the block has fewer than 3 columns, it's returned unchanged.

    Args:
        block_b2: The NumPy array representing block B2.

    Returns:
        The transformed NumPy array.
    """
    transformed_b2 = block_b2.copy()
    # Check if there are at least 3 columns to perform the swap
    if transformed_b2.shape[1] >= 3:
        # Swap column 1 (index 1) and column 2 (index 2)
        transformed_b2[:, [1, 2]] = transformed_b2[:, [2, 1]]
    return transformed_b2


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rules derived primarily from example train_2.

    Args:
        input_grid: A list of lists representing the input grid of digits.

    Returns:
        A list of lists representing the transformed output grid. Returns an empty list
        if the input is empty, or if the derived parameters (like H) are invalid,
        or if subgrid extraction fails due to boundary issues based on the derived rules.
    """
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []

    input_array = np.array(input_grid, dtype=int)
    input_height, input_width = input_array.shape

    # Steps 1 & 2: Find least frequent color and its minimum row index
    least_freq_color, r_min = find_least_frequent_color_and_min_row(input_array)

    # Check if finding the color/row failed
    if r_min == -1:
        return [] # Indicate failure or invalid input

    # Step 3: Determine H (Output Height and W1) based on train_2's pattern
    H = r_min - 1
    # Check if H is valid (must be positive)
    if H <= 0:
        # The rule H = r_min - 1 leads to invalid dimensions.
        return []

    # Step 4: Define c_start for B2 extraction
    c_start = 1

    # Step 5: Determine W2 (width of B2)
    W2 = input_width - c_start
    if W2 < 0: W2 = 0 # Ensure width is not negative

    # Step 6: Determine W1 (width of B1)
    W1 = H

    # Step 7: Extract B1 (top-left block)
    # Check boundaries to prevent slicing errors
    if 0 + H > input_height or 0 + W1 > input_width:
         # Cannot extract B1 with calculated dimensions
         return []
    B1 = input_array[0:H, 0:W1]

    # Check if B1 extraction resulted in an empty array unexpectedly (e.g., if H or W1 were valid > 0 but slicing failed)
    if B1.size == 0 and (H > 0 and W1 > 0):
         return []

    # Step 8: Create OutputRight by repeating the first row of B1
    # Check if B1 actually has rows before accessing B1[0]
    if B1.shape[0] == 0:
        return [] # B1 is empty, cannot proceed
    first_row_b1 = B1[0:1, :] # Use slicing to keep it 2D
    OutputRight = np.repeat(first_row_b1, H, axis=0)

    # Step 9: Define r_start for B2 extraction
    r_start = r_min - 1 # Note: r_start equals H based on the current rule

    # Step 10: Extract B2
    # Calculate end indices for B2
    end_row_b2 = r_start + H
    end_col_b2 = c_start + W2
    # Check boundaries for B2 extraction
    if r_start >= input_height or end_row_b2 > input_height or c_start >= input_width or end_col_b2 > input_width or W2 < 0 : # W2 check redundant due to earlier adjustment, but safe
         # Cannot extract B2 with calculated dimensions/indices
         # However, if W2 is 0, extraction might yield an empty array correctly.
         if W2 == 0:
             B2 = np.empty((H, 0), dtype=int) # Correctly represent an empty block B2
         else:
             return [] # Indices are out of bounds for a non-empty expected B2

    else:
         B2 = input_array[r_start : end_row_b2, c_start : end_col_b2]

    # Step 11: Transform B2 to create OutputLeft
    OutputLeft = transform_b2(B2)

    # Step 12: Concatenate OutputLeft and OutputRight horizontally
    # Need to handle cases where one or both might be empty arrays
    # np.hstack requires at least one array, and non-empty arrays must have matching number of rows.
    
    # If W2 is 0, OutputLeft will have shape (H, 0). Hstack works with this.
    # If H is 0 (handled earlier), this point wouldn't be reached.
    try:
        # Attempt concatenation
        if OutputLeft.shape[0] != H or OutputRight.shape[0] != H:
             # This check might be redundant given the logic flow, but adds safety
             return [] # Dimension mismatch
             
        # We need at least one non-empty array to stack
        if OutputLeft.size > 0 and OutputRight.size > 0:
             final_output_array = np.hstack((OutputLeft, OutputRight))
        elif OutputLeft.size > 0: # Only OutputLeft exists (e.g., if W1=H=0, though H>0 enforced)
             final_output_array = OutputLeft
        elif OutputRight.size > 0: # Only OutputRight exists (e.g., if W2=0)
             final_output_array = OutputRight
        else: # Both are empty (e.g., H > 0 but W1=0 and W2=0)
             final_output_array = np.empty((H, 0), dtype=int) # Output should have H rows, 0 columns

    except ValueError as e:
        # Catch potential hstack errors (e.g., dimension mismatch not caught above)
        # print(f"Error during concatenation: {e}")
        return [] # Indicate failure

    # Step 14: Convert final NumPy array back to list of lists
    return final_output_array.tolist()
