import numpy as np

"""
1.  **Analyze Input:** Examine the input grid.
2.  **Identify Colors:** Find all unique non-white pixel colors present in the input grid.
3.  **Determine Sequence:** Create an ordered sequence `S` from the unique non-white colors. The order is determined by scanning the input grid along successive anti-diagonals (where `row + column` is constant, starting from 0). Add each unique non-white color to the sequence `S` the *first* time it is encountered during this scan. Let the length of `S` be `N`.
4.  **Determine First Color Position:** Record the coordinates `(r0, c0)` where the *first* color added to the sequence `S` (i.e., `S[0]`) appears in the input grid during the anti-diagonal scan.
5.  **Calculate Offset:** Calculate the pattern offset `k` using the formula `k = -(r0 + c0) mod N`. Note that the modulo operation should handle negative results correctly to produce an offset in the range `[0, N-1]`.
6.  **Create Output Grid:** Create a new grid with the same dimensions as the input grid.
7.  **Fill Output Grid:** For each cell in the new grid at position (`row`, `col`):
    *   Calculate the index `idx = (row + col + k) mod N`.
    *   Set the color of the cell (`row`, `col`) to the color at index `idx` in the sequence `S` (i.e., `S[idx]`).
8.  **Finalize:** The fully filled new grid is the output.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by tiling a diagonal pattern based on the sequence of unique non-white colors found in the input.

    The steps are:
    1. Find unique non-white colors and their order of appearance by scanning anti-diagonals.
    2. Determine the coordinates (r0, c0) of the first appearance of the first color in the sequence.
    3. Calculate a pattern offset k based on (r0, c0).
    4. Fill the output grid using the sequence S and offset k, where output[r, c] = S[(r + c + k) % len(S)].
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # --- Step 1 & 2: Determine Sequence S and find (r0, c0) for S[0] ---
    S = [] # The ordered sequence of unique non-white colors
    seen_colors = set() # Keep track of colors already added to S
    first_color_coords = None # Stores (r, c) for the very first unique non-white color encountered

    # Iterate through anti-diagonals (sum of row + column = s)
    for s in range(H + W - 1):
        # Iterate through rows valid for the current anti-diagonal s
        # The row r must satisfy 0 <= r < H and 0 <= s - r < W
        # which means s - W < r <= s
        # Combined with 0 <= r < H, the range is max(0, s - W + 1) <= r < min(H, s + 1)
        for r in range(max(0, s - W + 1), min(H, s + 1)):
            c = s - r
            color = input_np[r, c]

            # Check if it's a non-white color and hasn't been seen yet
            if color != 0 and color not in seen_colors:
                S.append(color)
                seen_colors.add(color)
                # If this is the first unique color we've found overall, record its coordinates
                if first_color_coords is None:
                    first_color_coords = (r, c)

    # Handle the edge case where the input grid has no non-white colors
    if not S:
        # Return a grid of zeros with the same dimensions as the input
        return np.zeros_like(input_np).tolist()

    N = len(S) # Length of the color sequence

    # --- Step 3: Calculate Offset k ---
    # This should theoretically always be found if N > 0, but add a check for safety.
    if first_color_coords is None:
         raise ValueError("Logic error: Sequence S is not empty but first_color_coords was not set.")

    r0, c0 = first_color_coords
    # Calculate the offset k. Python's % operator handles negative dividends correctly
    # to produce a result with the same sign as the divisor N (which is positive).
    # k = (- (r0 + c0)) mod N
    k = (-(r0 + c0)) % N

    # --- Step 4: Create and Fill Output Grid ---
    output_np = np.zeros((H, W), dtype=int)
    for r in range(H):
        for c in range(W):
            # Calculate the index in the sequence S based on row, col, and offset k
            idx = (r + c + k) % N
            # Assign the color from the sequence to the output grid cell
            output_np[r, c] = S[idx]

    # --- Step 5: Convert back to list of lists and return ---
    return output_np.tolist()