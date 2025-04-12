```python
import numpy as np
import copy

"""
Transformation Rule (Hypothesis V9):

1. Identify the global minimum non-zero value (R) and the global maximum 
   non-zero value (T) in the input grid.
2. Process each column independently.
3. Within a column, find the row index of the first occurrence of R 
   (`first_r_row`).
4. Scan downwards from `first_r_row`.
5. Replacement is potentially triggered if a T is encountered at or after 
   row `first_r_row + 2`. Let's call this state 'activation_pending'.
6. Once 'activation_pending' is true, the *next* T encountered starts the 
   actual replacement process ('currently_replacing').
7. While 'currently_replacing' is true, change all subsequent T's to R.
8. The 'currently_replacing' state stops if a non-T value is encountered, 
   or if another R is encountered.
9. Seeing another R resets the state machine for that column segment.

"""

def find_key_values(grid: np.ndarray) -> tuple[int | None, int | None]:
    """Finds the smallest (R) and largest (T) non-zero values in the grid."""
    non_zeros = grid[grid > 0]
    if non_zeros.size == 0:
        return None, None  # No non-zero numbers found
    
    min_val = np.min(non_zeros)
    max_val = np.max(non_zeros)
    
    # Handle case where only one unique non-zero value exists
    if min_val == max_val:
        return None, None 
        
    return min_val, max_val

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation based on Hypothesis V9. Replaces the max 
    non-zero value (T) with the min non-zero value (R) under specific 
    conditions within each column, triggered by T appearing >= 2 rows 
    below the first R, and starting replacement from the subsequent T.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    
    # Get grid dimensions
    rows, cols = input_np.shape

    # Find the smallest (R) and largest (T) non-zero numbers
    r_val, t_val = find_key_values(input_np)

    # If no R/T found (all zeros, or only one unique non-zero), return copy
    if r_val is None or t_val is None:
        return output_np.tolist()

    # Iterate through each column
    for j in range(cols):
        first_r_row = -1
        activation_pending = False  # True if trigger condition (T >= first_r + 2) met
        currently_replacing = False # True if we should replace current/subsequent T's
        
        # Iterate through rows in the current column
        for i in range(rows):
            val = input_np[i, j]

            # State machine logic based on V9
            if first_r_row == -1:
                # State: Before seeing the first R
                if val == r_val:
                    first_r_row = i
            else:
                # State: After seeing the first R
                if val == r_val:
                    # Seeing another R resets the process for this segment
                    activation_pending = False
                    currently_replacing = False
                    # Update first_r_row to this new R's position to handle multiple segments correctly
                    first_r_row = i 
                elif val == t_val:
                    # Found a T after the first R
                    if currently_replacing:
                        # Already in replacing mode, so replace this T
                        output_np[i, j] = r_val
                    elif activation_pending:
                        # Activation was pending, start replacing from this T
                        currently_replacing = True
                        output_np[i, j] = r_val
                    elif i >= first_r_row + 2:
                        # Met the activation condition (T is >= 2 rows below first R)
                        # Set activation pending, don't replace this T yet
                        activation_pending = True
                    # Implicit else: T found at first_r_row + 1, doesn't activate, do nothing yet
                        
                else:
                    # Found a non-R, non-T value (including 0)
                    # Stop replacing if we were, but activation might still be pending
                    currently_replacing = False 

    # Convert the result back to a list of lists
    return output_np.tolist()
```