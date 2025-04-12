import numpy as np
from collections import Counter, defaultdict

"""
Transformation rule:
1. Determine the `background_color` (most frequent color) in the input grid.
2. Identify all full-height, single-color vertical `separator_lines`. A separator line is a column where all pixels share the same color, and this color is not the `background_color`. Record the color and column index for each separator line found.
3. Determine the `primary_separator_color`. This is the color that forms the maximum number (`N`) of `separator_lines`. If multiple colors form the maximum number of lines, choose the color whose first separator line appears at the smallest column index (leftmost).
4. Get the sorted list of column indices `[idx_1, idx_2, ..., idx_N]` where separator lines of the `primary_separator_color` occur.
5. If no primary separators are found (`N=0`), return the input grid unmodified.
6. Determine the output grid dimensions: height `H` is the same as the input height; width `W_out` is the index of the first primary separator line (`idx_1`). If `W_out` is 0 or less, return an empty grid of height H.
7. Create the `output_grid` of size `H` x `W_out`, initialized entirely with the `background_color`.
8. Define the `source_section` of the input grid: it comprises all rows and the columns from index `idx_N + 1` up to `idx_N + W_out`.
9. Validate the `source_section`: Check if it exists within the input grid bounds and if its actual width is exactly `W_out`. If not valid, proceed to step 13 (return the background-filled output grid).
10. Extract unique row patterns from the valid `source_section`. A pattern is considered unique if its sequence of colors has not been encountered before in a lower row index within the source section. Only consider patterns that contain at least one pixel different from the `background_color`.
11. For each unique non-background pattern `P` identified, record the minimum row index `r_min` (0-based, relative to the grid) where it first appeared in the `source_section`.
12. Determine the target row `target_row` for placing each unique pattern `P` into the `output_grid`:
    *   If `N` (the count of primary separators) is exactly 3, then `target_row = r_min + 2`.
    *   If `N` is not 3 (i.e., `N=1`, `N=2`, or `N>3`), then `target_row = r_min`.
    *   (Self-Correction Note: This `N!=3` rule is known to produce incorrect results for `train_1` (N=2) and `train_3` (N=1) by including more patterns than expected. The correct rule likely involves filtering the patterns from the source section before placement, but the exact filter is not yet determined.)
13. For each unique pattern `P` and its corresponding calculated `target_row`: if the `target_row` is a valid row index within the output grid (i.e., `0 <= target_row < H`), place the pattern `P` into the `output_grid` at that row, overwriting the background pixels.
14. Return the final `output_grid`.
"""

def find_most_frequent_color(grid: np.ndarray) -> int:
    """Finds the most frequent color (pixel value) in the grid."""
    if grid.size == 0:
        return 0 # Default for empty grid
    colors, counts = np.unique(grid, return_counts=True)
    if colors.size == 0:
         # This case shouldn't happen if grid.size > 0, but handle defensively
         return 0 
    return int(colors[np.argmax(counts)])

def find_separator_lines(grid: np.ndarray, bg_color: int) -> dict[int, list[int]]:
    """
    Finds all full-height, single-color, non-background vertical lines.
    Returns a dictionary mapping separator color to a list of column indices.
    """
    separator_lines = defaultdict(list)
    # Return empty if grid has no height
    if grid.shape[0] == 0: 
        return separator_lines
        
    h, w = grid.shape
    for c_idx in range(w):
        col = grid[:, c_idx]
        # Check if all elements in the column are the same
        if np.all(col == col[0]): 
            col_color = int(col[0])
            # Check if it's not the background color
            if col_color != bg_color:
                separator_lines[col_color].append(c_idx)
    return separator_lines

def find_primary_separator_info(separator_lines: dict[int, list[int]]) -> tuple[int, list[int]]:
    """
    Determines the primary separator color (most frequent, tie-break by first appearance)
    and returns the color and its sorted list of column indices.
    Returns (-1, []) if no separators are found.
    """
    # Return defaults if no separators dictionary provided or it's empty
    if not separator_lines:
        return -1, []

    primary_sep_col = -1
    max_lines = -1
    
    # Iterate through colors sorted by their first appearance index for tie-breaking
    sorted_colors = sorted(separator_lines.keys(), key=lambda color: separator_lines[color][0])

    for color in sorted_colors:
        indices = separator_lines[color]
        count = len(indices)
        
        # If this color has more lines, it becomes the new primary.
        # Tie-breaking is handled implicitly by the sort order.
        if count > max_lines:
             max_lines = count
             primary_sep_col = color

    if primary_sep_col != -1:
        # Return the identified primary color and its sorted indices
        return primary_sep_col, sorted(separator_lines[primary_sep_col])
    else:
         # This case should not be reached if separator_lines was not empty initially
        return -1, [] 

def extract_unique_patterns(section: np.ndarray, bg_color: int) -> dict[tuple, int]:
    """
    Extracts unique row patterns containing non-background colors from a given grid section.
    Returns a dictionary mapping tuple(pattern) -> min_row_index (relative to the section's rows).
    """
    patterns = {}
    # Return empty if section is empty or has zero width
    if section.size == 0 or section.shape[1] == 0: 
        return patterns
        
    h = section.shape[0]
    for r in range(h):
        # Convert row slice to a tuple for use as dictionary key
        row_pattern = tuple(section[r, :]) 
        # Check if pattern contains any non-background color
        if any(pixel != bg_color for pixel in row_pattern):
            # Store the first row index where this pattern is encountered
            if row_pattern not in patterns:
                patterns[row_pattern] = r
    return patterns

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on vertical separator lines and pattern extraction/placement.
    """
    # Convert list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)

    # Handle empty input grid early
    if input_array.size == 0:
        return []

    H, W_in = input_array.shape

    # Step 1: Determine background color
    bg_color = find_most_frequent_color(input_array)

    # Step 2: Find all separator lines
    separator_lines = find_separator_lines(input_array, bg_color)

    # Step 3: Find primary separator info
    primary_sep_color, primary_sep_indices = find_primary_separator_info(separator_lines)

    # Step 4 & 5: Get count N and handle N=0 case (return input)
    N = len(primary_sep_indices)
    if N == 0:
        return input_grid # Return input unchanged if no primary separators

    # Step 6: Determine output dimensions (W_out) and handle edge case (W_out <= 0)
    idx_1 = primary_sep_indices[0]
    W_out = idx_1 # Width is determined by the first separator's position
    
    # Handle edge case: separator at column 0 means zero width output
    if W_out <= 0:
        return [[] for _ in range(H)] # Return list of empty lists for correct height

    # Step 7: Initialize output grid with background color
    output_array = np.full((H, W_out), bg_color, dtype=int)

    # Step 8 & 9: Define and validate the source section
    idx_N = primary_sep_indices[-1]
    source_start_col = idx_N + 1
    source_end_col = source_start_col + W_out # Theoretical end column (exclusive)

    source_section_valid = False
    source_section = np.array([[] for _ in range(H)], dtype=int) # Default empty section

    # Check if source section starts within bounds
    if source_start_col < W_in:
        actual_end_col = min(source_end_col, W_in)
        # Check if the slice is non-empty before creating it
        if actual_end_col > source_start_col:
             extracted_section = input_array[:, source_start_col:actual_end_col]
             # Validate if the extracted section has the required width
             if extracted_section.shape[1] == W_out:
                 source_section = extracted_section
                 source_section_valid = True

    # Step 10 & 11: Extract unique patterns if source section is valid
    unique_patterns = {}
    if source_section_valid:
        unique_patterns = extract_unique_patterns(source_section, bg_color)

    # Step 12 & 13: Place patterns into the output grid based on N and r_min
    for pattern_tuple, r_min in unique_patterns.items():
        # Determine target row based on N
        if N == 3:
            target_row = r_min + 2
        else: # N != 3 (includes N=1, N=2, N>3)
            target_row = r_min
            # Note: This rule is known to be incomplete for N=1, N=2 cases based on examples.
            
        # Check if target row is valid within output grid height
        if 0 <= target_row < H:
            # Ensure pattern length matches output width before assignment
            # (Should always match if extracted from valid source section, but check defensively)
            if len(pattern_tuple) == W_out:
                output_array[target_row, :] = list(pattern_tuple)

    # Step 14: Convert final NumPy array back to list of lists
    output_grid = output_array.tolist()

    return output_grid