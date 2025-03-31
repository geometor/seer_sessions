
## train_1

**input:**
```
1 1 4 6 0
1 1 4 6 0
4 4 4 6 0
6 6 6 6 0
0 0 0 0 0
```


**output:**
```
1 1 4 6 1 1 4 6 1 1
1 1 4 6 1 1 4 6 1 1
4 4 4 6 1 1 4 6 1 1
6 6 6 6 1 1 4 6 1 1
1 1 1 1 1 1 4 6 1 1
1 1 1 1 1 1 4 6 1 1
4 4 4 4 4 4 4 6 1 1
6 6 6 6 6 6 6 6 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
```


## train_2

**input:**
```
2 2 2 3 0
2 2 2 3 0
2 2 2 3 0
3 3 3 3 0
0 0 0 0 0
```


**output:**
```
2 2 2 3 2 2 2 3 2 2
2 2 2 3 2 2 2 3 2 2
2 2 2 3 2 2 2 3 2 2
3 3 3 3 2 2 2 3 2 2
2 2 2 2 2 2 2 3 2 2
2 2 2 2 2 2 2 3 2 2
2 2 2 2 2 2 2 3 2 2
3 3 3 3 3 3 3 3 2 2
2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2
```


## train_3

**input:**
```
2 3 4 1 6
3 3 4 1 6
4 4 4 1 6
1 1 1 1 6
6 6 6 6 6
```


**output:**
```
2 3 4 1 6 2 3 4 1 6
3 3 4 1 6 2 3 4 1 6
4 4 4 1 6 2 3 4 1 6
1 1 1 1 6 2 3 4 1 6
6 6 6 6 6 2 3 4 1 6
2 2 2 2 2 2 3 4 1 6
3 3 3 3 3 3 3 4 1 6
4 4 4 4 4 4 4 4 1 6
1 1 1 1 1 1 1 1 1 6
6 6 6 6 6 6 6 6 6 6
```

**Perception:**

1.  **Input/Output Size:** The input is an H x W grid. The output is always a 2H x 2W grid. In the examples, the input is 5x5 and the output is 10x10.
2.  **Output Structure:** The output grid appears to be composed of four quadrants, each the size of the input grid (H x W).
3.  **Top-Left Quadrant:** This quadrant is an identical copy of the input grid.
4.  **Other Quadrants:** The remaining three quadrants (Top-Right, Bottom-Left, Bottom-Right) are filled based on derived properties of the input grid's rows and columns.
5.  **Row/Column Property:** For each row and column in the input grid, a single "characteristic color" is determined. This color seems to be the most frequent non-white (non-zero) color within that row or column.
6.  **Tie-Breaking:** If multiple non-white colors share the highest frequency in a row or column, the characteristic color is the one that appears first (at the lowest index) in that row or column.
7.  **All-White Case:** If a row or column contains only white (zero) pixels, its characteristic color defaults to the characteristic color of the *first* row (for rows) or the *first* column (for columns).
8.  **Top-Right Quadrant Filling:** Each column `j` in the Top-Right quadrant is filled entirely with the characteristic color `C_j` derived from the corresponding column `j` of the input grid.
9.  **Bottom-Left Quadrant Filling:** Each row `i` in the Bottom-Left quadrant is filled entirely with the characteristic color `R_i` derived from the corresponding row `i` of the input grid.
10. **Bottom-Right Quadrant Filling:** The color of a cell at relative coordinates `(i, j)` within the Bottom-Right quadrant depends on the characteristic row color `R_i` and the characteristic column color `C_j`. Specifically, the cell color is `R_i` if the row index `i` is greater than or equal to the column index `j` (`i >= j`), and it is `C_j` otherwise (`i < j`).

**Facts YAML:**


```yaml
input_grid:
  type: 2D array of integers (colors)
  properties:
    height: H
    width: W
output_grid:
  type: 2D array of integers (colors)
  properties:
    height: 2 * H
    width: 2 * W
    structure: Composed of 4 quadrants (TL, TR, BL, BR), each H x W.
transformation:
  - step: Define Quadrants
    description: Divide the output grid into four HxW quadrants.
  - step: Populate Top-Left (TL) Quadrant
    action: Copy
    source: input_grid
    target: output_grid[0:H, 0:W]
  - step: Calculate Characteristic Colors
    description: Determine a characteristic color for each row and column of the input_grid.
    variables:
      R: list of H characteristic row colors
      C: list of W characteristic column colors
    logic:
      for_each: row i in input_grid
        non_white_colors: Filter out white (0) pixels.
        if non_white_colors is empty:
          R[i] = R[0] # Default to first row's characteristic color
        else:
          frequencies: Count occurrences of each non_white_color.
          max_frequency: Find the maximum count.
          candidates: List colors with max_frequency.
          if candidates count is 1:
            R[i] = the single candidate color
          else: # Tie-breaking
            R[i] = the candidate color that appears first (lowest index) in the original row i.
      for_each: column j in input_grid
        non_white_colors: Filter out white (0) pixels.
        if non_white_colors is empty:
          C[j] = C[0] # Default to first column's characteristic color
        else:
          frequencies: Count occurrences of each non_white_color.
          max_frequency: Find the maximum count.
          candidates: List colors with max_frequency.
          if candidates count is 1:
            C[j] = the single candidate color
          else: # Tie-breaking
            C[j] = the candidate color that appears first (lowest index) in the original column j.
    dependencies: R[0] and C[0] must be calculated first or handled during iteration.
  - step: Populate Top-Right (TR) Quadrant
    target: output_grid[0:H, W:2*W]
    logic:
      for_each: column j (0 to W-1)
        fill column j of TR quadrant with color C[j]
  - step: Populate Bottom-Left (BL) Quadrant
    target: output_grid[H:2*H, 0:W]
    logic:
      for_each: row i (0 to H-1)
        fill row i of BL quadrant with color R[i]
  - step: Populate Bottom-Right (BR) Quadrant
    target: output_grid[H:2*H, W:2*W]
    logic:
      for_each: cell at relative coordinates (i, j) within the BR quadrant (0 <= i < H, 0 <= j < W)
        if i >= j:
          set cell color to R[i]
        else:
          set cell color to C[j]

```


**Natural Language Program:**

1.  Create a new grid (the output) that is twice the height and twice the width of the input grid.
2.  Copy the input grid directly into the top-left quadrant of the output grid.
3.  Determine the characteristic color for each row of the input grid:
    a.  For a given row, identify all non-white pixels.
    b.  Count the occurrences of each non-white color.
    c.  Find the color(s) that occur most frequently.
    d.  If one color is most frequent, that is the characteristic color for the row.
    e.  If there's a tie for the most frequent color, the characteristic color is the tied color that appears earliest (leftmost) in the row.
    f.  If a row contains only white pixels, its characteristic color is the same as the characteristic color calculated for the first row. Store these row characteristic colors (e.g., in a list `R`).
4.  Determine the characteristic color for each column of the input grid using the same logic as in step 3, but applied to columns: check frequencies, break ties by choosing the topmost color, and default to the first column's characteristic color if a column is all white. Store these column characteristic colors (e.g., in a list `C`).
5.  Fill the top-right quadrant of the output grid: For each column index `j` (from 0 to width-1), fill the entire corresponding column in the top-right quadrant with the characteristic color `C[j]`.
6.  Fill the bottom-left quadrant of the output grid: For each row index `i` (from 0 to height-1), fill the entire corresponding row in the bottom-left quadrant with the characteristic color `R[i]`.
7.  Fill the bottom-right quadrant of the output grid: For each cell in this quadrant, let its row index within the quadrant be `i` and its column index be `j`. If `i` is greater than or equal to `j`, set the cell's color to `R[i]`. Otherwise (if `i` is less than `j`), set the cell's color to `C[j]`.
```python
import numpy as np
from collections import Counter

"""
Transforms the input grid based on the following rules:
1. Create an output grid twice the height and width of the input.
2. Copy the input grid to the top-left (TL) quadrant of the output.
3. Determine a 'characteristic color' for each input row (R_i) and column (C_j):
   - It's the most frequent non-white color.
   - Ties are broken by the color appearing earliest (topmost for columns, leftmost for rows).
   - If a row/column is all white (all zeros), its characteristic color defaults to the characteristic color of the first row (for rows) or the first column (for columns). It's assumed the first row and first column are never all white.
4. Fill the top-right (TR) quadrant: Each column j is filled entirely with the characteristic color C_j.
5. Fill the bottom-left (BL) quadrant: Each row i is filled entirely with the characteristic color R_i.
6. Fill the bottom-right (BR) quadrant: For a cell at relative coordinates (i, j) within this quadrant, set its color to R_i if i >= j, otherwise set it to C_j.
"""

def _get_characteristic_color(line):
    """
    Helper function to find the characteristic color of a single row or column (passed as a 1D numpy array or list).
    
    Args:
        line: A list or 1D numpy array representing a row or column.

    Returns:
        The characteristic color (int) based on frequency and tie-breaking rules,
        or None if the line contains only white (0) pixels.
    """
    # Filter out white pixels (value 0)
    non_white_pixels = [p for p in line if p != 0]

    # If no non-white pixels, return None
    if not non_white_pixels:
        return None

    # Count frequencies of non-white colors
    counts = Counter(non_white_pixels)
    
    # Find the maximum frequency
    max_freq = 0
    # Iterate through unique non-white colors found
    for color in counts:
         if counts[color] > max_freq:
             max_freq = counts[color]

    # Find all colors that have the maximum frequency
    candidates = [color for color, freq in counts.items() if freq == max_freq]

    # If only one color has the max frequency, return it
    if len(candidates) == 1:
        return candidates[0]
    else:
        # Tie-breaking: find the first occurrence in the original line
        # Store the index of the first time we see each candidate color
        first_occurrence_index = {}
        for idx, pixel in enumerate(line):
             # Check if the pixel is one of the tied candidates
             # and if we haven't recorded its first occurrence yet
             if pixel in candidates and pixel not in first_occurrence_index:
                 first_occurrence_index[pixel] = idx
        
        # Find the candidate color with the minimum first occurrence index
        best_candidate = -1 # Placeholder, should be overwritten
        min_idx = float('inf')
        for color in candidates:
            idx = first_occurrence_index[color]
            if idx < min_idx:
                 min_idx = idx
                 best_candidate = color
        return best_candidate

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

    # Step 1: Copy input grid to the Top-Left quadrant
    output_grid[0:H, 0:W] = input_np

    # Step 2: Calculate characteristic row colors (R)
    R = [0] * H # Initialize list to store characteristic colors for rows
    
    # Calculate characteristic color for the first row (R[0])
    # This is needed as the default for any subsequent all-white rows.
    # Assumption: The first row is guaranteed to have non-white pixels.
    R[0] = _get_characteristic_color(input_np[0, :])
    if R[0] is None:
        # This case should ideally not happen based on problem constraints/examples.
        # If it did, the definition of the default rule is ambiguous.
        # For now, raise an error, or potentially default to 0.
         raise ValueError("First row cannot be all white based on task description interpretation.")

    # Calculate characteristic colors for the remaining rows
    for i in range(1, H):
        row_color = _get_characteristic_color(input_np[i, :])
        # If the row is all white, use the default (R[0])
        if row_color is None:
            R[i] = R[0]
        else:
            R[i] = row_color

    # Step 3: Calculate characteristic column colors (C)
    C = [0] * W # Initialize list for column colors
    
    # Calculate for the first column (C[0]) - needed as default
    # Assumption: The first column is guaranteed to have non-white pixels.
    C[0] = _get_characteristic_color(input_np[:, 0])
    if C[0] is None:
         raise ValueError("First column cannot be all white based on task description interpretation.")

    # Calculate for the remaining columns
    for j in range(1, W):
        col_color = _get_characteristic_color(input_np[:, j])
        # If the column is all white, use the default (C[0])
        if col_color is None:
            C[j] = C[0]
        else:
            C[j] = col_color

    # Step 4: Fill Top-Right quadrant
    # Each column j in the TR quadrant is filled with C[j]
    for j in range(W):
        output_grid[0:H, W + j] = C[j]

    # Step 5: Fill Bottom-Left quadrant
    # Each row i in the BL quadrant is filled with R[i]
    for i in range(H):
        output_grid[H + i, 0:W] = R[i]

    # Step 6: Fill Bottom-Right quadrant
    # Color depends on relative row/column index (i, j) within the quadrant
    for i in range(H): # Relative row index within BR quadrant
        for j in range(W): # Relative column index within BR quadrant
            # Calculate actual indices in the full output grid
            output_row = H + i
            output_col = W + j
            # Apply the comparison rule
            if i >= j:
                output_grid[output_row, output_col] = R[i]
            else:
                output_grid[output_row, output_col] = C[j]

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
```
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
