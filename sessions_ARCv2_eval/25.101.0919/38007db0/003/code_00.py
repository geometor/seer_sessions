import collections
import numpy as np

"""
Transformation Rule:

1.  **Analyze Input Structure**: Determine the grid's separator color (the color at the top-left corner). Identify the height (H) and width (W) of the repeating pattern blocks by finding the first full row and column consisting solely of the separator color. Calculate the number of block rows (R) and block columns (C) based on H, W, and the overall grid dimensions.
2.  **Extract Patterns**: Go through each block location in the input grid (from row 0 to R-1, column 0 to C-1). Extract the HxW pattern from within each block. Keep track of the original row and column index (r, c) for each extracted pattern.
3.  **Identify Unique Patterns**: Count how many times each distinct pattern appears in the extracted list. Create a list of patterns that appear exactly once, along with their original (r, c) positions.
4.  **Select Target Pattern**: From the list of unique patterns, choose the one whose original position (r, c) comes first when ordered primarily by row index (r) and secondarily by column index (c). This is the target pattern.
5.  **Construct Output Grid**: Create a new grid with R block rows and 1 block column. The total pixel dimensions will be (R*H + R + 1) rows and (W + 2) columns.
6.  **Populate Output Grid**: Fill the entire output grid initially with the separator color. Then, for each block row `r` (from 0 to R-1), place the selected target pattern into the block area, which starts at grid row `r*(H+1) + 1` and grid column 1.
"""

def find_grid_parameters(input_grid: list[list[int]]) -> tuple[int, int, int, int, int]:
    """
    Analyzes the input grid to find separator color, block dimensions (H, W),
    and grid block count (R, C). Looks for full separator lines.
    """
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    np_grid = np.array(input_grid, dtype=int)

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
         raise ValueError(f"Grid height {input_height} inconsistent with block height H={h}.")
    if (input_width - 1) % (w + 1) != 0:
         raise ValueError(f"Grid width {input_width} inconsistent with block width W={w}.")

    r_blocks = (input_height - 1) // (h + 1)
    c_blocks = (input_width - 1) // (w + 1)

    # Final validation
    if r_blocks <= 0 or c_blocks <= 0:
        raise ValueError("Could not determine valid block counts R and C.")
    if input_height != r_blocks * h + (r_blocks + 1) or input_width != c_blocks * w + (c_blocks + 1):
        raise ValueError("Grid dimensions do not match calculated block structure.")


    return separator_color, h, w, r_blocks, c_blocks

def extract_patterns(input_grid: list[list[int]], h: int, w: int, r_blocks: int, c_blocks: int) -> list[tuple[tuple[tuple[int]], tuple[int, int]]]:
    """
    Extracts all HxW internal patterns and their block positions (r, c).
    Returns a list of tuples: ((pattern_tuple), (row_idx, col_idx))
    """
    patterns = []
    np_grid = np.array(input_grid, dtype=int)
    for r in range(r_blocks):
        for c in range(c_blocks):
            start_row = r * (h + 1) + 1
            start_col = c * (w + 1) + 1
            # Extract pattern using numpy slicing and convert rows to tuples
            pattern_np = np_grid[start_row : start_row + h, start_col : start_col + w]
            pattern_tuple = tuple(tuple(row) for row in pattern_np)
            patterns.append((pattern_tuple, (r, c)))
    return patterns

def find_target_pattern(patterns_with_pos: list[tuple[tuple[tuple[int]], tuple[int, int]]]) -> tuple[tuple[int]]:
    """
    Counts patterns, identifies unique ones, and selects the top-leftmost unique pattern.
    """
    # Count frequencies of each pattern
    pattern_counts = collections.Counter(p[0] for p in patterns_with_pos)

    # Identify unique patterns (count == 1) and store with their positions
    unique_patterns_with_pos = []
    for pattern, pos in patterns_with_pos:
        if pattern_counts[pattern] == 1:
            unique_patterns_with_pos.append({'pattern': pattern, 'pos': pos})

    # Check if any unique patterns were found
    if not unique_patterns_with_pos:
        # According to the examples, a unique pattern is expected.
        # If this fails in a real test case, the logic might need adjustment
        # (e.g., fallback to most common, or first pattern).
        raise ValueError("No unique pattern found in the input grid.")

    # Sort unique patterns by position: primary key row (pos[0]), secondary key col (pos[1])
    unique_patterns_with_pos.sort(key=lambda x: (x['pos'][0], x['pos'][1]))

    # Return the pattern part of the first element in the sorted list
    return unique_patterns_with_pos[0]['pattern']


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding the top-leftmost unique pattern
    and replicating it in a single column structure with the original separators.
    """

    # 1. Analyze Input Structure
    try:
        separator_color, h, w, r_blocks, c_blocks = find_grid_parameters(input_grid)
    except ValueError as e:
        print(f"Error finding grid parameters: {e}")
        # Depending on requirements, could return input, empty, or raise
        raise e # Reraise the error for clarity during testing

    # 2. Extract Patterns
    patterns_with_pos = extract_patterns(input_grid, h, w, r_blocks, c_blocks)
    if not patterns_with_pos:
         raise ValueError("No patterns extracted from the grid.")

    # 3. Identify and Select Target Pattern
    try:
        target_pattern = find_target_pattern(patterns_with_pos)
    except ValueError as e:
        print(f"Error finding target pattern: {e}")
        raise e # Reraise the error

    # 4. Construct Output Grid Dimensions
    output_height = r_blocks * h + (r_blocks + 1)
    output_width = w + 2 # One block width + 2 separator columns

    # 5. Initialize Output Grid with separator color
    # Use numpy for easier initialization and slicing
    output_grid_np = np.full((output_height, output_width), separator_color, dtype=int)

    # 6. Populate Output Grid with the target pattern
    for r in range(r_blocks):
        # Calculate top-left corner for placing the pattern in the output
        start_row = r * (h + 1) + 1
        start_col = 1 # Pattern always starts in the second column (index 1)

        # Place the target pattern (which is a tuple of tuples)
        for i in range(h):
            for j in range(w):
                 # Make sure indices are within bounds (though they should be by design)
                if i < len(target_pattern) and j < len(target_pattern[i]):
                    output_grid_np[start_row + i, start_col + j] = target_pattern[i][j]

    # Convert numpy array back to list of lists for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid