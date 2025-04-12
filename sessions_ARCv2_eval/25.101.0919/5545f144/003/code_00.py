import numpy as np
from collections import Counter, defaultdict

"""
Transformation rule:
1. Determine the background color (most frequent color in the input grid).
2. Find all full-height, single-color vertical lines (separator lines) whose color is not the background color.
3. Identify the primary separator color, which is the color that forms the most separator lines. Ties are broken by choosing the color whose first separator line appears earliest (leftmost). Record the column indices of all lines formed by this primary color.
4. Count the number of primary separator lines (num_primary_lines).
5. Determine the output grid dimensions: Height H is the same as the input grid height. Width W_out is the column index of the first primary separator line.
6. Check the count of primary separator lines:
    a. If num_primary_lines is exactly 3:
        i. Create an output grid of size H x W_out, initially filled with the background color.
        ii. Identify the 'last section' of the input grid. This section starts at the column immediately after the last primary separator line and has a width equal to W_out.
        iii. Extract all unique row patterns (sequences of colors in a row) from this last section that contain at least one non-background color.
        iv. For each unique pattern found, determine the minimum row index (r_min, 0-based) at which it first appears within the last section.
        v. Calculate the target row index in the output grid for each pattern as target_row = r_min + 2.
        vi. If the target_row is a valid row index within the output grid (0 <= target_row < H), place the corresponding pattern into that row of the output grid, overwriting the initial background color.
    b. Else (if num_primary_lines is not 3):
        i. The output grid is simply a direct copy of the 'first section' of the input grid, which consists of columns 0 up to (but not including) W_out.
7. Return the final output grid.
"""

def find_most_frequent_color(grid: np.ndarray) -> int:
    """Finds the most frequent color (pixel value) in the grid."""
    if grid.size == 0:
        # Return a default (e.g., 0) or raise error for empty grid
        return 0 
    colors, counts = np.unique(grid, return_counts=True)
    # Handle case where grid contains only one color or is empty after unique
    if colors.size == 0:
         return 0 # Or another appropriate default/error
    return int(colors[np.argmax(counts)])

def find_separator_lines(grid: np.ndarray, bg_color: int) -> dict[int, list[int]]:
    """
    Finds all full-height, single-color, non-background vertical lines.
    Returns a dictionary mapping separator color to a list of column indices.
    """
    h, w = grid.shape
    separator_lines = defaultdict(list)
    if h == 0: # Handle grids with zero height
        return separator_lines
        
    for c_idx in range(w):
        col = grid[:, c_idx]
        # Check if column height matches grid height and all elements are the same
        # np.all implicitly checks size > 0 if comparison is made
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
    if not separator_lines:
        return -1, [] # No separators found

    primary_sep_col = -1
    max_lines = -1
    
    # Iterate through colors sorted by their first appearance index
    # This handles the tie-breaking rule correctly.
    sorted_colors = sorted(separator_lines.keys(), key=lambda color: separator_lines[color][0])

    for color in sorted_colors:
        indices = separator_lines[color]
        count = len(indices)
        
        # If this color has more lines, it becomes the new primary
        if count > max_lines:
             max_lines = count
             primary_sep_col = color
        # If counts are equal, the one encountered first (due to sorting) remains primary.

    if primary_sep_col != -1:
        # Return the primary color and its sorted indices
        return primary_sep_col, sorted(separator_lines[primary_sep_col])
    else:
         # This case should ideally not be reached if separator_lines is not empty
        return -1, []


def extract_unique_patterns(section: np.ndarray, bg_color: int) -> dict[tuple, int]:
    """
    Extracts unique row patterns containing non-background colors from a given grid section.
    Returns a dictionary mapping tuple(pattern) -> min_row_index (relative to the section's rows).
    """
    patterns = {}
    if section.size == 0: # Handle empty section
        return patterns
        
    h = section.shape[0]
    for r in range(h):
        # Convert row slice to a tuple for use as dictionary key
        row_pattern = tuple(section[r, :]) 
        # Check if pattern contains any non-background color
        if any(pixel != bg_color for pixel in row_pattern):
            # Store the first row index (relative to section) where this pattern is encountered
            if row_pattern not in patterns:
                patterns[row_pattern] = r
    return patterns

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the analysis of vertical separator lines.
    Either copies the first section or constructs the output from patterns
    in the last section based on the number of primary separator lines.
    """
    # Convert list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)

    # Handle empty input grid
    if input_array.size == 0:
        return []

    H, W_in = input_array.shape

    # Step 1: Determine background color
    bg_color = find_most_frequent_color(input_array)

    # Step 2: Find all separator lines
    separator_lines = find_separator_lines(input_array, bg_color)

    # Step 3: Find primary separator info
    primary_sep_color, primary_sep_indices = find_primary_separator_info(separator_lines)

    # Handle case where no primary separator is found (might indicate input is output, or error)
    # Assuming based on examples that a primary separator always exists.
    if primary_sep_color == -1:
         # If no separators define the structure, maybe return the input?
         # Or an empty grid if the rule requires structure.
         # Let's default to returning the input for now if no structure found.
         return input_grid 
         
    # Step 4: Count primary separator lines
    num_primary_lines = len(primary_sep_indices)

    # Step 5: Determine output dimensions
    first_sep_idx = primary_sep_indices[0]
    W_out = first_sep_idx # Width is determined by the first separator's position
    
    # Handle edge case: separator at column 0 means zero width output
    if W_out <= 0:
        return [[] for _ in range(H)] # Return list of empty lists for correct height

    # Step 6 & 7: Apply transformation based on number of primary lines

    # Mode 1: Pattern Transfer (if exactly 3 primary lines)
    if num_primary_lines == 3:
        # Initialize output grid with background color
        output_array = np.full((H, W_out), bg_color, dtype=int)
        
        # Identify the last section
        last_sep_idx = primary_sep_indices[-1]
        section_start_col = last_sep_idx + 1
        section_end_col = section_start_col + W_out # Theoretical end based on output width

        # Extract the last section, respecting input grid boundaries
        if section_start_col < W_in:
            actual_end_col = min(section_end_col, W_in)
            last_section = input_array[:, section_start_col:actual_end_col]

            # Proceed only if the extracted section has the expected width
            if last_section.shape[1] == W_out:
                 # Find unique patterns and their min row index within the section
                 unique_patterns = extract_unique_patterns(last_section, bg_color)

                 # Place patterns into the output grid based on r_min + 2 rule
                 for pattern_tuple, r_min in unique_patterns.items():
                     target_row = r_min + 2
                     # Check if target row is valid within output grid height
                     if 0 <= target_row < H:
                         output_array[target_row, :] = list(pattern_tuple)
            # else: The last section was too narrow. Output remains bg_color filled.
            # This implicitly handles cases where the input isn't wide enough
            # after the last separator.
        # else: No columns exist after the last separator. Output remains bg_color filled.

    # Mode 2: Copy First Section (if num_primary_lines is NOT 3)
    else:
        # Extract the first section (columns 0 to W_out-1)
        output_array = input_array[:, 0:W_out]

    # Convert final NumPy array back to list of lists format for the ARC standard
    output_grid = output_array.tolist()

    return output_grid