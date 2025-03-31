```python
import numpy as np
from collections import Counter

"""
Transforms the input grid based on the following rules:
1. Create an output grid twice the height (2H) and twice the width (2W) of the input grid (HxW).
2. Determine a 'characteristic color' for each input row (R_i) and column (C_j):
   - Identify all non-white (non-zero) pixels in the row/column.
   - Count the frequency of each non-white color.
   - The characteristic color is the most frequent non-white color.
   - Ties in frequency are broken by the color that appears earliest (leftmost for rows, topmost for columns) in the original input row/column.
   - If a row or column contains only white pixels (all zeros), its characteristic color defaults to the characteristic color of the *first* row (for rows) or the *first* column (for columns). Store the indices of these all-white rows and columns. It is assumed the first row and first column are never all white.
3. Populate the Top-Left (TL) quadrant (output[0:H, 0:W]):
   - Initially, copy the input grid to the TL quadrant.
   - For each row `i` that was all-white in the input, fill the entire row `i` of the TL quadrant with its characteristic color R_i.
   - For each column `j` that was all-white in the input, fill the entire column `j` of the TL quadrant with its characteristic color C_j. (Column filling happens after row filling, potentially overwriting corners).
4. Fill the Top-Right (TR) quadrant (output[0:H, W:2W]): Each column `j` (relative to the quadrant, 0 to W-1) is filled entirely with the characteristic color C_j.
5. Fill the Bottom-Left (BL) quadrant (output[H:2H, 0:W]): Each row `i` (relative to the quadrant, 0 to H-1) is filled entirely with the characteristic color R_i.
6. Fill the Bottom-Right (BR) quadrant (output[H:2H, W:2W]): For a cell at relative coordinates (i, j) within this quadrant (0<=i<H, 0<=j<W), set its color to R_i if i >= j, otherwise set it to C_j.
"""

def _get_characteristic_color(line):
    """
    Helper function to find the characteristic color of a single row or column.

    Args:
        line: A list or 1D numpy array representing a row or column.

    Returns:
        Tuple: (characteristic_color, is_all_white)
               characteristic_color (int): The determined color, or None if all white initially.
               is_all_white (bool): True if the input line contained only 0s.
    """
    # Filter out white pixels (value 0)
    non_white_pixels = [p for p in line if p != 0]

    # If no non-white pixels, mark as all white
    if not non_white_pixels:
        return None, True

    # Count frequencies of non-white colors
    counts = Counter(non_white_pixels)
    
    # Find the maximum frequency
    max_freq = 0
    for color in counts:
         if counts[color] > max_freq:
             max_freq = counts[color]

    # Find all colors that have the maximum frequency
    candidates = [color for color, freq in counts.items() if freq == max_freq]

    # If only one color has the max frequency, return it
    if len(candidates) == 1:
        return candidates[0], False
    else:
        # Tie-breaking: find the first occurrence in the original line
        first_occurrence_index = {}
        for idx, pixel in enumerate(line):
             if pixel in candidates and pixel not in first_occurrence_index:
                 first_occurrence_index[pixel] = idx
        
        # Find the candidate color with the minimum first occurrence index
        best_candidate = -1 # Placeholder
        min_idx = float('inf')
        # Ensure all candidates are found in the line before proceeding
        # (this should always be true if candidates came from 'line')
        found_candidates = {pixel: index for pixel, index in first_occurrence_index.items() if pixel in candidates}
        
        for color in candidates:
             # Use the pre-calculated index; handle cases where a candidate might not be found (shouldn't happen here)
            idx = found_candidates.get(color, float('inf')) 
            if idx < min_idx:
                 min_idx = idx
                 best_candidate = color
        return best_candidate, False

def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    
    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape # Get height and width

    # Initialize the output grid with zeros, twice the dimensions
    output_grid = np.zeros((2 * H, 2 * W), dtype=int)

    # --- Step 2: Calculate Characteristic Colors and track all-white lines ---
    R = [0] * H # Characteristic colors for rows
    C = [0] * W # Characteristic colors for columns
    all_white_rows = []
    all_white_cols = []

    # Calculate for Row 0 (assumed not all white)
    R[0], is_white = _get_characteristic_color(input_np[0, :])
    if is_white:
        # This case should not happen based on observed patterns/implicit constraints
        # If it did, the logic breaks down. Defaulting R[0] might be needed, or raise error.
        # For now, let's assume input constraints prevent this.
        pass # Or raise ValueError("First row cannot be all white") 
        
    # Calculate for remaining rows
    for i in range(1, H):
        row_color, is_white = _get_characteristic_color(input_np[i, :])
        if is_white:
            R[i] = R[0] # Default to first row's color
            all_white_rows.append(i)
        else:
            R[i] = row_color

    # Calculate for Column 0 (assumed not all white)
    C[0], is_white = _get_characteristic_color(input_np[:, 0])
    if is_white:
         # Assume input constraints prevent this.
         pass # Or raise ValueError("First column cannot be all white")
         
    # Calculate for remaining columns
    for j in range(1, W):
        col_color, is_white = _get_characteristic_color(input_np[:, j])
        if is_white:
            C[j] = C[0] # Default to first column's color
            all_white_cols.append(j)
        else:
            C[j] = col_color

    # --- Step 3: Populate Top-Left (TL) Quadrant ---
    # 3a: Copy input grid
    output_grid[0:H, 0:W] = input_np

    # 3b: Fill rows corresponding to all-white input rows
    for i in all_white_rows:
        output_grid[i, 0:W] = R[i]

    # 3c: Fill columns corresponding to all-white input columns
    # (This happens *after* row filling, potentially overwriting corners)
    for j in all_white_cols:
        output_grid[0:H, j] = C[j]

    # --- Step 4: Fill Top-Right (TR) Quadrant ---
    # Each column j in the TR quadrant is filled with C[j]
    for j in range(W):
        output_grid[0:H, W + j] = C[j]

    # --- Step 5: Fill Bottom-Left (BL) Quadrant ---
    # Each row i in the BL quadrant is filled with R[i]
    for i in range(H):
        output_grid[H + i, 0:W] = R[i]

    # --- Step 6: Fill Bottom-Right (BR) Quadrant ---
    # Color depends on relative row/column index (i, j) within the quadrant
    for i in range(H): # Relative row index within BR quadrant
        for j in range(W): # Relative column index within BR quadrant
            output_row = H + i
            output_col = W + j
            # Apply the comparison rule
            if i >= j:
                output_grid[output_row, output_col] = R[i]
            else:
                output_grid[output_row, output_col] = C[j]

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```