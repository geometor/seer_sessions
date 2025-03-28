import numpy as np

"""
Identifies a non-white rectangular object at the top-left of the input grid.
The width of this object is W.
The remaining area to the right (originally white) is filled based on the columns of the object.
The fill pattern consists of N repetitions of the object's first column (C0), followed by the object's remaining columns (C1 to C(W-1)).
The number of repetitions N is calculated such that the total width of the fill pattern matches the available white space width (W_total - W).
Specifically, N = (W_total - W) - (W - 1).
The output grid consists of the original object followed by the constructed fill pattern.
"""

def find_source_object_width(grid: np.ndarray) -> int:
    """
    Finds the width W of the non-white rectangular object starting at column 0.
    The width is determined by the index of the first column that consists entirely of white (0) pixels.
    If no such column exists, the object spans the entire grid width.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        The width (W) of the source object.
    """
    height, total_width = grid.shape
    for j in range(total_width):
        is_column_all_white = True
        for i in range(height):
            if grid[i, j] != 0:
                is_column_all_white = False
                break
        if is_column_all_white:
            # Found the first all-white column, its index is the width W
            return j
    # If no all-white column was found, the object spans the entire width
    return total_width

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling the white area to the right of a 
    top-left object based on the object's columns.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Check for empty input grid
    if input_np.size == 0:
        return []
        
    height, W_total = input_np.shape

    # Identify the width (W) of the source_object starting at column 0
    W = find_source_object_width(input_np)

    # If the object width is 0 (e.g., all white input) or fills the entire grid,
    # no transformation is needed, return the original grid format.
    if W == 0 or W == W_total:
        return input_grid

    # Initialize the output grid as a copy of the input numpy array
    output_np = np.copy(input_np)

    # Extract the columns of the source_object
    # source_object_cols = input_np[:, :W] # Not strictly needed as separate var
    col_0 = input_np[:, 0:1] # First column (C0), kept as 2D slice (H x 1)
    
    # Calculate parameters for the fill pattern
    W_fill = W_total - W  # Width of the area to be filled (white space)
    
    # Determine the columns C1 to C(W-1) and their total width (W_app)
    if W > 1:
        # Extract columns C1 through C(W-1)
        cols_1_to_W_minus_1 = input_np[:, 1:W] 
        # Calculate the width of this appended part
        W_app = cols_1_to_W_minus_1.shape[1] # This will be W - 1
    else:
        # If W is 1, there are no columns C1 to C(W-1)
        cols_1_to_W_minus_1 = None
        W_app = 0

    # Calculate the number of repetitions (N) required for the first column (C0)
    # N must cover the remaining fill width after the appended columns are placed.
    N = W_fill - W_app
    
    # Basic validation: N should not be negative based on the observed pattern.
    # If N < 0, it means W_fill < W_app, or W_total - W < W - 1, 
    # implying W_total + 1 < 2 * W. This scenario wasn't seen in examples.
    # If it occurs, the transformation rule might be incomplete.
    # For now, we proceed assuming N >= 0 as per examples.
    if N < 0:
        # If this happens, returning the original state might be safest,
        # as the derived rule doesn't fit.
        print(f"Warning: Calculated repetition count N={N} is negative. "
              f"(W={W}, W_total={W_total}, W_fill={W_fill}, W_app={W_app}). "
              f"Rule might not apply. Returning original grid.")
        return input_grid

    # --- Construct the fill pattern and place it into the output grid ---
    
    # Start filling from the column immediately after the source object
    current_col_index = W 

    # 1. Place N copies of the first column (C0)
    for _ in range(N):
        # Check bounds just in case, though N is calculated to fit W_fill
        if current_col_index < W_total:
            output_np[:, current_col_index:current_col_index+1] = col_0
            current_col_index += 1
        else:
            # This boundary check should ideally not be hit if N is correct
            print("Warning: Fill boundary exceeded while placing C0 repetitions.")
            break 

    # 2. Place the remaining columns (C1 to C(W-1)) if they exist
    if cols_1_to_W_minus_1 is not None:
        num_app_cols = cols_1_to_W_minus_1.shape[1] # Should be W_app
        for j in range(num_app_cols):
            # Check bounds just in case
            if current_col_index < W_total:
                # Extract the j-th column from cols_1_to_W_minus_1
                col_to_append = cols_1_to_W_minus_1[:, j:j+1] 
                # Place it in the output grid
                output_np[:, current_col_index:current_col_index+1] = col_to_append
                current_col_index += 1
            else:
                # This boundary check should ideally not be hit
                print("Warning: Fill boundary exceeded while placing C1-C(W-1).")
                break

    # Convert the resulting numpy array back to a list of lists format
    output_grid = output_np.tolist()
    
    return output_grid