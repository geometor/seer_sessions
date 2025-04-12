"""
Transformation Rule:

1.  **Analyze Input Structure**: Determine the grid's separator color (from the top-left pixel). Find the block height (H) and width (W) by locating the first full row and column of the separator color. Calculate the number of block rows (R) and columns (C).
2.  **Extract and Count Patterns**: Extract the HxW pattern from each block in the input grid. Store each distinct pattern along with a list of all its positions (r, c) and its total frequency (count). Keep track of the first position (top-leftmost) where each distinct pattern appears.
3.  **Identify Unique Patterns**: Create a list of all patterns that have a frequency count of exactly 1.
4.  **Select Target Pattern**:
    *   **If** the list of unique patterns is not empty: Sort the unique patterns based on their position (first by row index, then by column index). The target pattern is the pattern from the first entry in this sorted list (the top-leftmost unique pattern).
    *   **Else** (if no unique patterns exist): Find the highest frequency count among all patterns. Identify all patterns that have this highest frequency (the most common patterns). Sort these most common patterns based on their *first* recorded position (first by row index, then by column index). The target pattern is the pattern from the first entry in this sorted list (the top-leftmost occurrence of the most common patterns).
5.  **Construct Output Grid**: Create a new grid with dimensions corresponding to R blocks high and 1 block wide (total pixels: (R*H + R + 1) rows, (W + 2) columns).
6.  **Populate Output Grid**: Fill the entire output grid with the separator color. Then, place the selected target pattern into the HxW area within each of the R block locations in the single output column.
"""

import collections
import numpy as np

# --- Helper Functions ---

def to_np(grid: list[list[int]]) -> np.ndarray:
    """Converts a list of lists grid to a numpy array."""
    return np.array(grid, dtype=int)

def pattern_to_tuple(pattern_np: np.ndarray) -> tuple[tuple[int]]:
    """Converts a numpy pattern array to a hashable tuple of tuples."""
    return tuple(tuple(int(x) for x in row) for row in pattern_np)

def find_grid_parameters(np_grid: np.ndarray) -> tuple[int, int, int, int, int]:
    """
    Analyzes the numpy grid to find separator color, block dimensions (H, W),
    and grid block count (R, C). Looks for full separator lines.
    """
    input_height, input_width = np_grid.shape

    # Separator color is assumed to be at (0, 0)
    separator_color = int(np_grid[0, 0])

    # Find block height H by finding the first full separator row
    h = -1
    for r in range(1, input_height):
        if np.all(np_grid[r, :] == separator_color):
            h = r - 1
            break
    if h == -1: # No full horizontal separator found, assume single row of blocks
        if input_height > 1:
             h = input_height - 2
        else: # Cannot determine height if grid is 1xN
             raise ValueError("Cannot determine block height H.")


    # Find block width W by finding the first full separator column
    w = -1
    for c in range(1, input_width):
         if np.all(np_grid[:, c] == separator_color):
            w = c - 1
            break
    if w == -1: # No full vertical separator found, assume single column of blocks
        if input_width > 1:
            w = input_width - 2
        else: # Cannot determine width if grid is Nx1
             raise ValueError("Cannot determine block width W.")

    # Validate H and W
    if h <= 0 or w <= 0:
         raise ValueError(f"Invalid block dimensions determined: H={h}, W={w}")

    # Calculate number of block rows (R) and columns (C)
    # Check divisibility first for robust calculation
    if (input_height - 1) % (h + 1) != 0:
         # Allow for single row case
         if input_height == h + 2:
             r_blocks = 1
         else:
            raise ValueError(f"Grid height {input_height} inconsistent with block height H={h}.")
    else:
        r_blocks = (input_height - 1) // (h + 1)

    if (input_width - 1) % (w + 1) != 0:
        # Allow for single col case
         if input_width == w + 2:
             c_blocks = 1
         else:
            raise ValueError(f"Grid width {input_width} inconsistent with block width W={w}.")
    else:
        c_blocks = (input_width - 1) // (w + 1)


    # Final validation check on dimensions based on calculated R,C,H,W
    if input_height != r_blocks * h + (r_blocks + 1) or input_width != c_blocks * w + (c_blocks + 1):
         raise ValueError(f"Grid dimensions Ht={input_height}, Wd={input_width} do not match calculated structure R={r_blocks}, C={c_blocks}, H={h}, W={w}.")

    if r_blocks <= 0 or c_blocks <= 0:
        raise ValueError("Could not determine valid block counts R and C.")

    return separator_color, h, w, r_blocks, c_blocks

def extract_patterns_and_details(np_grid: np.ndarray, h: int, w: int, r_blocks: int, c_blocks: int) -> list[dict]:
    """
    Extracts patterns, calculates frequencies, and records all positions and the first position.
    Returns a list of dictionaries, one for each distinct pattern:
    [{'pattern': tuple, 'count': int, 'positions': list[tuple], 'first_pos': tuple}]
    """
    patterns_data = {} # Use dict for easy aggregation: {pattern_tuple: {'count':..., 'positions':..., 'first_pos':...}}

    for r in range(r_blocks):
        for c in range(c_blocks):
            start_row = r * (h + 1) + 1
            start_col = c * (w + 1) + 1
            # Extract pattern using numpy slicing
            pattern_np = np_grid[start_row : start_row + h, start_col : start_col + w]
            pattern_tuple = pattern_to_tuple(pattern_np)
            current_pos = (r, c)

            if pattern_tuple not in patterns_data:
                patterns_data[pattern_tuple] = {
                    'pattern': pattern_tuple,
                    'count': 0,
                    'positions': [],
                    'first_pos': current_pos # Record first time seen
                }
            patterns_data[pattern_tuple]['count'] += 1
            patterns_data[pattern_tuple]['positions'].append(current_pos)

    # Convert the aggregated dictionary back to a list
    return list(patterns_data.values())

def select_target_pattern(patterns_details: list[dict]) -> tuple[tuple[int]]:
    """
    Selects the target pattern based on uniqueness and position.
    Prioritizes top-leftmost unique pattern. If none, selects top-leftmost most common pattern.
    """
    unique_patterns = [p for p in patterns_details if p['count'] == 1]

    if unique_patterns:
        # Sort unique patterns by position (row, then column)
        # We use the first position encountered, which IS the top-leftmost for a unique pattern
        unique_patterns.sort(key=lambda p: p['first_pos'])
        return unique_patterns[0]['pattern']
    else:
        # No unique patterns, find the most common
        if not patterns_details:
             raise ValueError("No patterns found to select from.")

        max_count = 0
        for p in patterns_details:
            if p['count'] > max_count:
                max_count = p['count']
        # Could also use: max_count = max(p['count'] for p in patterns_details)

        most_common_patterns = [p for p in patterns_details if p['count'] == max_count]

        # Tie-break most common using the first position encountered
        most_common_patterns.sort(key=lambda p: p['first_pos'])
        return most_common_patterns[0]['pattern']

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding the top-leftmost unique pattern (or
    top-leftmost most common if no uniques exist) and replicating it in a
    single column structure with the original separators.
    """
    # Convert input to numpy array for easier processing
    np_grid = to_np(input_grid)

    # 1. Analyze Input Structure
    try:
        separator_color, h, w, r_blocks, c_blocks = find_grid_parameters(np_grid)
    except ValueError as e:
        print(f"Error analyzing grid structure: {e}")
        raise # Re-raise error for clear feedback

    # 2. Extract and Count Patterns
    patterns_details = extract_patterns_and_details(np_grid, h, w, r_blocks, c_blocks)
    if not patterns_details:
         raise ValueError("No patterns extracted from the grid.")

    # 3. & 4. Select Target Pattern
    try:
        target_pattern = select_target_pattern(patterns_details)
    except ValueError as e:
        print(f"Error selecting target pattern: {e}")
        raise # Re-raise error

    # 5. Construct Output Grid Dimensions
    output_height = r_blocks * h + (r_blocks + 1)
    output_width = w + 2 # One block width + 2 separator columns

    # 6. Initialize Output Grid and Populate
    output_grid_np = np.full((output_height, output_width), separator_color, dtype=int)

    for r in range(r_blocks):
        # Calculate top-left corner for placing the pattern in the output
        start_row = r * (h + 1) + 1
        start_col = 1 # Pattern always starts in the second column (index 1)

        # Place the target pattern (which is a tuple of tuples)
        for i in range(h):
            for j in range(w):
                # Ensure indices are within bounds (should be guaranteed by correct H/W)
                if i < len(target_pattern) and j < len(target_pattern[i]):
                    output_grid_np[start_row + i, start_col + j] = target_pattern[i][j]
                else:
                    # This indicates an error in H/W or pattern extraction
                    print(f"Warning: Index out of bounds when placing pattern at block row {r}, pattern coords ({i},{j})")

    # Convert numpy array back to list of lists for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid