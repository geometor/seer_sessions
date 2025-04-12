"""
Transformation Rule:

1.  Identify vertical separator columns composed entirely of the background color (white/0).
2.  Define blocks as the contiguous vertical segments between separators (or grid edges). Let N be the number of blocks.
3.  If N < 2, return the input grid unchanged.
4.  Determine the majority color (M) and minority color (m) present in the non-background areas across all blocks. If M or m cannot be found, return the input grid unchanged.
5.  Extract the relative minority pattern P[i] = {(row, col_relative)} for each block i (0-indexed) from the input grid.
6.  Determine the target output pattern for each block based on the parity of N:
    *   If N is ODD (and N >= 3):
        *   Output Block 0 gets the pattern from input Block N-1.
        *   Output Blocks 1 to N-2 get the pattern from the corresponding input Block i.
        *   Output Block N-1 gets the pattern from input Block 0.
    *   If N is EVEN (and N >= 2):
        *   Output Block 0 gets the pattern from input Block N-2.
        *   Output Blocks 1 to N-2 get the pattern from the preceding input Block i-1.
        *   Output Block N-1 gets the pattern from input Block N-1 (unchanged).
7.  Create a copy of the input grid as the output grid.
8.  For each block j in the output grid:
    *   Iterate through its non-background cells (r, c).
    *   Calculate the relative column `c_rel`.
    *   Check if `(r, c_rel)` exists in the target pattern determined in step 6 for block j.
    *   If yes, set the output cell color to `m`.
    *   If no, set the output cell color to `M`.
9.  Return the modified output grid.
"""

import copy
from collections import Counter

# --- Helper Functions ---

def find_separator_columns(grid: list[list[int]], background_color: int = 0) -> list[int]:
    """Finds columns composed entirely of the background color."""
    if not grid or not grid[0]:
        return []
    height = len(grid)
    width = len(grid[0])
    separator_cols = []
    for c in range(width):
        is_separator = True
        for r in range(height):
            if grid[r][c] != background_color:
                is_separator = False
                break
        if is_separator:
            separator_cols.append(c)
    return separator_cols

def define_blocks(separator_cols: list[int], width: int) -> list[tuple[int, int]]:
    """Defines block boundaries (start_col, end_col_exclusive) based on separators."""
    blocks = []
    start_col = 0
    for sep_col in separator_cols:
        # Add block if content exists before the separator
        if sep_col > start_col:
            blocks.append((start_col, sep_col))
        # Next block starts after the separator
        start_col = sep_col + 1
    # Add the last block if content exists after the last separator
    if start_col < width:
        blocks.append((start_col, width))
    return blocks

def get_majority_minority_colors(grid: list[list[int]], blocks: list[tuple[int, int]], background_color: int = 0) -> tuple[int | None, int | None]:
    """Identifies the majority and minority non-background colors across all blocks."""
    colors = []
    height = len(grid)
    for start_col, end_col in blocks:
        for r in range(height):
            for c in range(start_col, end_col):
                if grid[r][c] != background_color:
                    colors.append(grid[r][c])

    if not colors:
        return None, None # No non-background colors found

    counts = Counter(colors)
    sorted_colors = counts.most_common()

    if len(sorted_colors) >= 2:
        majority_color = sorted_colors[0][0]
        minority_color = sorted_colors[1][0]
        # Ensure the less frequent one is minority, handle ties by picking second
        if counts[minority_color] > counts[majority_color]:
             majority_color, minority_color = minority_color, majority_color
    elif len(sorted_colors) == 1:
        # Only one non-background color present
        majority_color = sorted_colors[0][0]
        minority_color = None # Cannot perform pattern swap logic
    else: # Should not happen if colors list is not empty
        majority_color = None
        minority_color = None

    return majority_color, minority_color

def extract_minority_pattern(grid: list[list[int]], block_bounds: tuple[int, int], minority_color: int) -> set[tuple[int, int]]:
    """Extracts relative coordinates (row, col_in_block) of the minority color as a set."""
    start_col, end_col = block_bounds
    height = len(grid)
    pattern = set()
    # Return empty set if minority color wasn't identified
    if minority_color is None:
        return pattern
    for r in range(height):
        for c in range(start_col, end_col):
            if grid[r][c] == minority_color:
                pattern.add((r, c - start_col))
    return pattern

def apply_pattern_to_block(output_grid: list[list[int]], input_grid: list[list[int]], block_bounds: tuple[int, int], target_pattern: set[tuple[int, int]], majority_color: int, minority_color: int, background_color: int = 0):
    """Applies the target pattern to a block in the output grid by setting colors."""
    start_col, end_col = block_bounds
    height = len(output_grid)
    # Ensure minority color is valid before proceeding
    if minority_color is None or majority_color is None:
        return

    for r in range(height):
        for c in range(start_col, end_col):
            # Only modify cells that were originally non-background
            if input_grid[r][c] != background_color:
                relative_col = c - start_col
                if (r, relative_col) in target_pattern:
                    output_grid[r][c] = minority_color
                else:
                    output_grid[r][c] = majority_color
            # else: keep background color

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # 1. Initialize output grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    if not input_grid or not input_grid[0]:
        return output_grid # Handle empty grid case

    height = len(input_grid)
    width = len(input_grid[0])
    background_color = 0

    # 2. Identify Background and Separators
    separator_cols = find_separator_columns(input_grid, background_color)

    # 3. Define Blocks
    blocks = define_blocks(separator_cols, width)
    num_blocks = len(blocks)

    # 4. Handle Simple Case (N < 2)
    if num_blocks < 2:
        return output_grid

    # 5. Identify Majority (M) and Minority (m) Colors
    majority_color, minority_color = get_majority_minority_colors(input_grid, blocks, background_color)

    # Cannot proceed if minority color isn't defined
    if minority_color is None or majority_color is None:
        # If only majority exists, the output should just be the majority color in non-background areas
        if majority_color is not None:
             for r in range(height):
                  for c in range(width):
                       if output_grid[r][c] != background_color:
                            output_grid[r][c] = majority_color
        return output_grid # Return potentially modified grid or original copy


    # 6. Extract Input Patterns (0-indexed)
    input_patterns = [extract_minority_pattern(input_grid, bounds, minority_color) for bounds in blocks]

    # 7. Determine Target Output Patterns based on Parity of N
    output_patterns = [set() for _ in range(num_blocks)] # Initialize list of empty sets

    if num_blocks % 2 != 0: # Odd number of blocks (N >= 3)
        # Rule: B0<-P[N-1], B[1..N-2]<-P[i], B[N-1]<-P[0]
        output_patterns[0] = input_patterns[num_blocks - 1]
        for i in range(1, num_blocks - 1):
            output_patterns[i] = input_patterns[i]
        if num_blocks > 0: # Avoid index error if somehow N=1 reached here
             output_patterns[num_blocks - 1] = input_patterns[0]

    else: # Even number of blocks (N >= 2)
        # Rule: B0<-P[N-2], B[1..N-2]<-P[i-1], B[N-1]<-P[N-1]
        if num_blocks >= 2: # N=2 case: B0<-P[0], B1<-P1, so N-2 is P[0]
            output_patterns[0] = input_patterns[num_blocks - 2]
            for i in range(1, num_blocks - 1): # This loop runs only if N >= 4
                output_patterns[i] = input_patterns[i - 1]
            output_patterns[num_blocks - 1] = input_patterns[num_blocks - 1]
        # Note: If N=0, this section isn't reached due to step 4.


    # 8. Apply Transformations (Coloring based on target patterns)
    for i, block_bounds in enumerate(blocks):
        apply_pattern_to_block(
            output_grid,
            input_grid, # Pass input grid to check original background
            block_bounds,
            output_patterns[i],
            majority_color,
            minority_color,
            background_color
        )

    # 9. Return Output
    return output_grid