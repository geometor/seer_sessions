import numpy as np
from collections import Counter
import itertools

"""
Constructs an output grid by combining two blocks derived from specific regions 
of an input grid. The process involves identifying two source blocks (B1, B2) 
in the input, generating the right block from B1, applying a context-dependent 
transformation (T) to B2 to get the left block, and combining them.

Key steps:
1. Identify the least frequent color (lfc) and its minimum row index (r_min) 
   in the input grid.
2. Calculate potential output height H based on a pattern observed in one 
   example (H = r_min - 1). Note: This height calculation is a hypothesis and 
   is known not to generalize to all provided examples. Correct dimensions 
   (H_out, W_out) ideally need to be observed from the target output.
3. Determine the widths of the two concatenated blocks (W1 = H, W2 depends on 
   input width and a fixed column offset).
4. Calculate the starting position (r_start, c_start) for the second source 
   block (B2) based on r_min.
5. Extract the first source block (B1) from the input grid's top-left.
6. Generate the right output block (OutputRight) by repeating B1's first row.
7. Extract the second source block (B2) starting from (r_start, c_start).
8. Apply a specific transformation T to B2 to create the left output block 
   (OutputLeft). Note: The transformation T is context-dependent; this 
   implementation uses the column swap observed in example 'train_2'.
9. Horizontally concatenate OutputLeft and OutputRight.

Limitations: This implementation assumes the output height H can be derived using 
the 'H = r_min - 1' rule and uses the transformation T specific to 'train_2'. 
It cannot observe the actual target output dimensions or determine the correct 
transformation T for other instances like 'train_1'.
"""

def find_least_frequent_color_and_min_row(grid: np.ndarray) -> tuple[int, int]:
    """
    Finds the least frequent color (smallest value in case of tie)
    and its minimum row index in the grid.

    Args:
        grid: The input NumPy array.

    Returns:
        A tuple containing (least_frequent_color, min_row_index).
        Returns (-1, -1) if the grid is empty or no colors are found.
    """
    if grid.size == 0:
        return -1, -1

    counts = Counter(grid.flatten())
    if not counts: 
        return -1, -1
        
    # Find the minimum frequency
    min_freq = min(counts.values())
    # Find all colors with that minimum frequency
    least_frequent_colors = [color for color, freq in counts.items() if freq == min_freq]
    # Tie-breaking: choose the smallest color value
    target_color = min(least_frequent_colors)

    # Find all row, col indices where the target color appears
    indices = np.argwhere(grid == target_color)
    if indices.size == 0:
         # This case should ideally not happen if the Counter found the color
         return target_color, -1 

    # Find the minimum row index among these occurrences
    min_row_index = np.min(indices[:, 0])
    return target_color, min_row_index

def transform_b2_specific_case(block_b2: np.ndarray) -> np.ndarray:
    """
    Applies the specific transformation T observed in 'train_2':
    swapping columns 1 and 2 (0-indexed).
    Returns the block unchanged if it has fewer than 3 columns.
    
    Note: This transformation is specific to one observed pattern and may not apply
    to other task instances.

    Args:
        block_b2: The NumPy array representing block B2.

    Returns:
        The transformed NumPy array (OutputLeft for the 'train_2' case).
    """
    # Check if B2 is empty or too narrow for the specific swap
    if block_b2.size == 0 or block_b2.shape[1] < 3:
        return block_b2.copy() # Return unchanged copy

    transformed_b2 = block_b2.copy()
    # Swap column 1 (index 1) and column 2 (index 2)
    transformed_b2[:, [1, 2]] = transformed_b2[:, [2, 1]]
    return transformed_b2


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the transformation logic based on observed patterns, primarily 
    following the rules derived from 'train_2' due to inability to observe 
    target output dimensions or determine the correct transformation T for 
    all cases.

    Args:
        input_grid: The input grid as a list of lists.

    Returns:
        The transformed grid as a list of lists, or an empty list if the
        derived parameters or extraction steps fail or lead to invalid states.
    """
    # Handle empty input
    if not input_grid or not input_grid[0]:
        return []

    # Convert input to NumPy array for easier slicing and manipulation
    input_array = np.array(input_grid, dtype=int)
    input_height, input_width = input_array.shape

    # --- Identify Least Frequent Color Info ---
    lfc, r_min = find_least_frequent_color_and_min_row(input_array)
    if r_min == -1:
        # Failed to find the least frequent color or its row
        return [] 

    # --- Determine Dimensions (Hypothesized based on 'train_2') ---
    # Calculate potential output height H. 
    # !! This is a major assumption based on one example !!
    H_out = r_min - 1 
    if H_out <= 0:
        # Derived height is not positive, rule likely doesn't apply
        return [] 

    # Calculate block widths based on derived H_out
    W1 = H_out # Width of right block B1/OutputRight is H_out
    c_start = 1 # Fixed starting column for B2
    # Width of left block B2/OutputLeft based on remaining input width
    W2 = input_width - c_start
    if W2 < 0: W2 = 0 # Ensure width is not negative

    # --- Calculate B2 Start Indices ---
    r_start = r_min - 1 # Starting row for B2

    # --- Extract Input Block B1 (Top-Left) ---
    # Check boundaries before slicing
    if not (0 <= H_out <= input_height and 0 <= W1 <= input_width):
        return [] # Derived dimensions are out of input bounds for B1
    B1 = input_array[0:H_out, 0:W1]
    # Verify extracted shape
    if B1.shape != (H_out, W1):
         return [] # Slicing did not produce expected shape

    # --- Generate Output Right Block ---
    OutputRight = np.empty((H_out, 0), dtype=int) # Initialize as empty (H_out x 0)
    if B1.size > 0: # Check if B1 has content (i.e., W1 > 0)
        first_row_b1 = B1[0:1, :] # Get first row, keeping it 2D
        OutputRight = np.repeat(first_row_b1, H_out, axis=0) # Repeat row vertically
    elif W1 > 0: 
        # This case (W1>0 but B1 empty) indicates an issue, should have been caught by shape check
        return []

    # --- Extract Input Block B2 ---
    B2 = np.empty((H_out, 0), dtype=int) # Initialize as empty (H_out x 0)
    end_row_b2 = r_start + H_out
    end_col_b2 = c_start + W2

    # Check boundaries carefully before slicing for B2
    valid_r_start = (0 <= r_start < input_height)
    valid_c_start = (0 <= c_start < input_width) # c_start=1, usually valid if width > 1
    valid_end_row = (end_row_b2 <= input_height)
    valid_end_col = (end_col_b2 <= input_width)
    
    if W2 > 0: # Only try to extract if calculated width is positive
        if valid_r_start and valid_c_start and valid_end_row and valid_end_col:
            B2 = input_array[r_start : end_row_b2, c_start : end_col_b2]
            # Verify shape again
            if B2.shape != (H_out, W2):
                return [] # Extraction failed to produce expected shape
        else:
            # Indices are out of bounds for extracting a non-empty B2
            return [] 
    # If W2 == 0, B2 remains the initialized empty array (H_out x 0)

    # --- Apply Transformation T (Instance-Specific) ---
    # Apply the transformation logic known from 'train_2'
    # !! This is the second major assumption / limitation !!
    OutputLeft = transform_b2_specific_case(B2)

    # --- Concatenate Output Blocks ---
    try:
        # Final check: ensure both blocks have H_out rows before stacking
        if OutputLeft.shape[0] != H_out or OutputRight.shape[0] != H_out:
            return [] 

        # Use numpy's hstack for horizontal concatenation. Handles empty arrays correctly if dims match.
        final_output_array = np.hstack((OutputLeft, OutputRight))

    except ValueError as e:
        # Catch potential errors during hstack (e.g., unexpected dimension issues)
        return [] 

    # Convert the final NumPy array result back to a list of lists
    return final_output_array.tolist()