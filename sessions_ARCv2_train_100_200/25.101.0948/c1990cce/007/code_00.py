import numpy as np

"""
Processes a 1D input grid (single row) containing exactly one red pixel (2).
Generates a 2D square output grid (WxW) where W is the width of the input row.
The first row (r=0) of the output is a copy of the input.
Subsequent rows (r=1 to W-1) are generated based on a cellular automaton rule using the diagonal predecessors (L, R) from the row above (r-1).
The rule depends on the row number (r), the colors of L and R, the propagation direction (L or R), the horizontal distance ('dist') of the current cell (c) from the column of the initial red pixel ('center_c'), and parity comparisons between r and dist for certain cases.

Rule details for cell (r, c):
1. Find center_c: Column index of the red pixel in row 0.
2. Get L = output[r-1, c-1] (or 0 if c=0), R = output[r-1, c+1] (or 0 if c=W-1).
3. Calculate dist = abs(c - center_c).
4. Apply rules:
   a. Collision (L!=0 and R!=0): result = 0.
   b. Propagate L (L!=0, R==0):
      - If L=1: result = 1.
      - If L=2:
         - If r <= 2: result = 2.
         - If r >= 3:
             - If dist == 1: result = 1.
             - If dist > 1: result = 1 if (r%2!=0 and dist%2!=0) else 2. (Result is 1 only if both r and dist are odd)
   c. Propagate R (L==0, R!=0):
      - If R=1: result = 0. (Blue annihilates propagating right)
      - If R=2:
         - If r <= 2: result = 2.
         - If r >= 3:
             - If dist == 1: result = 0.
             - If dist > 1: result = 0 if (r%2 == dist%2) else 2. (Result is 0 only if r and dist have same parity)
   d. No Propagation (L==0, R==0): result = 0. (Note: Ignores observed boundary anomalies where expected output is 1)
5. Set output[r, c] = result.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the described cellular automaton rules.

    Args:
        input_grid: A list containing a single list of integers (1D grid).

    Returns:
        A list of lists of integers representing the transformed 2D grid.
    """
    # Convert input to numpy array for easier handling and validation
    input_np = np.array(input_grid, dtype=int)

    # Ensure input is 1 row and determine width W
    if input_np.ndim == 1: # Handle case if input is truly 1D array
        W = input_np.shape[0]
        input_np = input_np.reshape(1, W) # Reshape to 2D (1 row)
    elif input_np.ndim == 2 and input_np.shape[0] == 1:
        W = input_np.shape[1]
    else:
        raise ValueError("Input grid must be a single row (1D array or 2D array with shape (1, W)).")

    # Find the column index of the initial red pixel (2)
    center_c_candidates = np.where(input_np[0] == 2)[0]
    if len(center_c_candidates) != 1:
        # Check if it's all zeros (allowed case for some edge scenarios, return zeros)
        if np.all(input_np == 0):
             return np.zeros((W, W), dtype=int).tolist()
        raise ValueError("Input row must contain exactly one red pixel (2).")
    center_c = center_c_candidates[0]

    # Initialize the output grid of size W x W with zeros (white)
    output_grid = np.zeros((W, W), dtype=int)

    # Copy the input row (row 0) into the first row of the output grid
    output_grid[0, :] = input_np[0, :]

    # Iterate through the rows of the output grid, starting from the second row (index 1)
    for r in range(1, W):
        # Get the previous row from the output grid being built
        prev_row = output_grid[r-1, :]

        # Iterate through the columns of the current row
        for c in range(W):
            # Get the values of the diagonal predecessors (top-left and top-right)
            # Handle boundary conditions: treat out-of-bounds cells as white (0)
            L = prev_row[c-1] if c > 0 else 0
            R = prev_row[c+1] if c < W - 1 else 0

            # Calculate the horizontal distance from the center column
            dist = abs(c - center_c)

            # Determine the value for the current cell based on the rules
            result = 0 # Default to white

            # Rule 1: Collision
            if L != 0 and R != 0:
                result = 0
            # Rule 2: Propagation from Left
            elif L != 0 and R == 0:
                if L == 1: # Blue propagates as blue
                    result = 1
                elif L == 2: # Red propagation depends on row and distance
                    if r <= 2:
                        result = 2
                    else: # r >= 3
                        if dist == 1:
                            result = 1
                        else: # dist > 1
                            # Result is 1 only if both r and dist are odd
                            result = 1 if (r % 2 != 0 and dist % 2 != 0) else 2
            # Rule 3: Propagation from Right
            elif L == 0 and R != 0:
                if R == 1: # Blue annihilates when propagating right
                    result = 0
                elif R == 2: # Red propagation depends on row and distance
                    if r <= 2:
                        result = 2
                    else: # r >= 3
                        if dist == 1:
                            result = 0
                        else: # dist > 1
                             # Result is 0 only if r and dist have same parity
                            result = 0 if (r % 2 == dist % 2) else 2
            # Rule 4: No Propagation (L == 0 and R == 0)
            else:
                result = 0

            # Assign the calculated result to the current cell
            output_grid[r, c] = result

    # Convert the final numpy array back to a standard Python list of lists
    return output_grid.tolist()