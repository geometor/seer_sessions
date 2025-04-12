
Previous Code:
```python
import copy
from collections import Counter

"""
Transformation Rule:

1.  Identify vertical separator columns composed entirely of the background color (white/0).
2.  Define blocks as the contiguous vertical segments between separators (or grid edges). Let N be the number of blocks.
3.  If N < 2, return the input grid unchanged.
4.  Determine the majority color (M) and minority color (m) present in the non-background areas (assume consistency). If M or m cannot be found, return the input grid unchanged.
5.  Extract the relative minority pattern P[i] = {(row, col_relative)} for each block i (0-indexed) from the input grid.
6.  Determine the target output pattern for each block based on the parity of N:
    *   If N is ODD:
        *   Block 0 gets the pattern from input Block N-1, with relative columns shifted left by 1 (min 0).
        *   Blocks 1 to N-2 get the pattern from input Block i (unchanged).
        *   Block N-1 gets the pattern from input Block 0.
    *   If N is EVEN:
        *   Block 0 gets the pattern from input Block N-2, with relative columns shifted left by 1 (min 0).
        *   Blocks 1 to N-2 get the pattern from input Block i-1 (pattern shifts right).
        *   Block N-1 gets the pattern from input Block N-1 (unchanged).
7.  Create a copy of the input grid as the output grid.
8.  For each block j in the output grid:
    *   Iterate through its cells (r, c).
    *   If the cell is not background color:
        *   Calculate the relative column `c_rel`.
        *   Check if `(r, c_rel)` exists in the target pattern determined in step 6 for block j.
        *   If yes, set the output cell color to `m`.
        *   If no, set the output cell color to `M`.
9.  Return the modified output grid.
"""

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
        if sep_col > start_col:
            blocks.append((start_col, sep_col))
        start_col = sep_col + 1
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
        return None, None

    counts = Counter(colors)
    sorted_colors = counts.most_common()

    if len(sorted_colors) >= 2:
        majority_color = sorted_colors[0][0]
        minority_color = sorted_colors[1][0]
        # Ensure minority is actually less frequent than majority
        if counts[minority_color] > counts[majority_color]:
             majority_color, minority_color = minority_color, majority_color
        elif counts[minority_color] == counts[majority_color]:
             # Tie-breaking: arbitrary but consistent? Or error?
             # Let's assume the task guarantees distinct counts or the first one is M.
             pass

    elif len(sorted_colors) == 1:
        majority_color = sorted_colors[0][0]
        minority_color = None # Cannot perform swap without a minority color
    else:
        majority_color = None
        minority_color = None

    return majority_color, minority_color


def extract_minority_pattern(grid: list[list[int]], block_bounds: tuple[int, int], minority_color: int) -> set[tuple[int, int]]:
    """Extracts relative coordinates (row, col_in_block) of the minority color as a set."""
    start_col, end_col = block_bounds
    height = len(grid)
    pattern = set()
    if minority_color is None:
        return pattern
    for r in range(height):
        for c in range(start_col, end_col):
            if grid[r][c] == minority_color:
                pattern.add((r, c - start_col))
    return pattern

def apply_pattern_to_block(output_grid: list[list[int]], block_bounds: tuple[int, int], target_pattern: set[tuple[int, int]], majority_color: int, minority_color: int, background_color: int = 0):
    """Applies the target pattern to a block in the output grid."""
    start_col, end_col = block_bounds
    height = len(output_grid)
    for r in range(height):
        for c in range(start_col, end_col):
            # Only modify non-background cells
            if output_grid[r][c] != background_color:
                relative_col = c - start_col
                if (r, relative_col) in target_pattern:
                    output_grid[r][c] = minority_color
                else:
                    output_grid[r][c] = majority_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the grid by rearranging minority color patterns within blocks,
    with the rule depending on whether the number of blocks is odd or even.
    Includes a column shift for patterns moving into the first block.
    """
    # --- Initialization and Grid Analysis ---
    output_grid = copy.deepcopy(input_grid)
    if not input_grid or not input_grid[0]:
        return output_grid

    height = len(input_grid)
    width = len(input_grid[0])
    background_color = 0

    # 1. Identify Separators
    separator_cols = find_separator_columns(input_grid, background_color)

    # 2. Define Blocks
    blocks = define_blocks(separator_cols, width)
    num_blocks = len(blocks)

    # 3. Handle Simple Case (N < 2)
    if num_blocks < 2:
        return output_grid

    # 4. Identify Colors
    majority_color, minority_color = get_majority_minority_colors(input_grid, blocks, background_color)

    # Cannot proceed if minority color isn't defined
    if minority_color is None or majority_color is None:
        return output_grid # Return original grid copy

    # --- Pattern Extraction ---
    # 5. Extract Input Patterns (0-indexed)
    input_patterns = [extract_minority_pattern(input_grid, bounds, minority_color) for bounds in blocks]

    # --- Determine Target Patterns based on Parity ---
    # 6. Determine Output Patterns
    output_patterns = [set() for _ in range(num_blocks)] # Initialize list of empty sets

    if num_blocks % 2 != 0: # Odd number of blocks (N >= 3)
        # Block 0 gets shifted pattern from Block N-1
        last_pattern = input_patterns[num_blocks - 1]
        shifted_last_pattern = set((r, max(0, c_rel - 1)) for r, c_rel in last_pattern)
        output_patterns[0] = shifted_last_pattern

        # Blocks 1 to N-2 are unchanged (get pattern P[i])
        for i in range(1, num_blocks - 1):
            output_patterns[i] = input_patterns[i]

        # Block N-1 gets pattern from Block 0
        output_patterns[num_blocks - 1] = input_patterns[0]

    else: # Even number of blocks (N >= 2)
        # Block 0 gets shifted pattern from Block N-2
        # Handle N=2 case separately as N-2 would be 0
        if num_blocks == 2:
             # B0 gets shifted P0, B1 gets P1
             pattern_0 = input_patterns[0]
             shifted_pattern_0 = set((r, max(0, c_rel - 1)) for r, c_rel in pattern_0)
             output_patterns[0] = shifted_pattern_0
             output_patterns[1] = input_patterns[1] # Last block unchanged
        else: # N >= 4
            pattern_n_minus_2 = input_patterns[num_blocks - 2]
            shifted_pattern_n_minus_2 = set((r, max(0, c_rel - 1)) for r, c_rel in pattern_n_minus_2)
            output_patterns[0] = shifted_pattern_n_minus_2

            # Blocks 1 to N-2 get pattern from Block i-1
            for i in range(1, num_blocks - 1):
                output_patterns[i] = input_patterns[i - 1]

            # Block N-1 is unchanged (gets pattern P[N-1])
            output_patterns[num_blocks - 1] = input_patterns[num_blocks - 1]


    # --- Apply Transformations ---
    # 7. Apply the determined patterns to the output grid
    for i, block_bounds in enumerate(blocks):
        apply_pattern_to_block(
            output_grid,
            block_bounds,
            output_patterns[i],
            majority_color,
            minority_color,
            background_color
        )

    # 8. Return Output
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 3 3 0 3 3 0 3 3 0 4 4 0
0 3 4 0 3 3 0 3 3 0 3 3 0
0 3 3 0 4 3 0 3 4 0 4 3 0
0 3 3 0 3 4 0 3 3 0 3 4 0
0 4 3 0 3 4 0 3 3 0 3 3 0
0 3 3 0 3 3 0 3 3 0 3 3 0
```
Expected Output:
```
0 3 3 0 3 3 0 3 3 0 4 4 0
0 3 3 0 3 4 0 3 3 0 3 3 0
0 3 4 0 3 3 0 4 3 0 4 3 0
0 3 3 0 3 3 0 3 4 0 3 4 0
0 3 3 0 4 3 0 3 4 0 3 3 0
0 3 3 0 3 3 0 3 3 0 3 3 0
```
Transformed Output:
```
0 3 3 0 3 3 0 3 3 0 4 4 0
0 3 3 0 3 4 0 3 3 0 3 3 0
0 4 3 0 3 3 0 4 3 0 4 3 0
0 3 3 0 3 3 0 3 4 0 3 4 0
0 3 3 0 4 3 0 3 4 0 3 3 0
0 3 3 0 3 3 0 3 3 0 3 3 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 2.564102564102569

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 7 7 7 0 7 7 7 0
0 6 6 6 0 7 7 7 0 7 7 7 0
0 7 7 7 0 6 6 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 7 6 7 0
0 7 7 7 0 7 7 7 0 7 7 7 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 7 7 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 6 6 6 0
0 7 7 7 0 6 6 7 0 7 7 7 0
0 7 6 7 0 7 7 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 7 7 7 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 7 7 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 6 6 6 0
0 7 7 7 0 6 6 7 0 7 7 7 0
0 6 7 7 0 7 7 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 7 7 7 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 2.564102564102569
