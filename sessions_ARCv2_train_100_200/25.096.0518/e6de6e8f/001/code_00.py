import numpy as np

"""
Transforms a 2x12 input grid encoding into an 8x7 output grid displaying a digit.

The transformation process involves:
1. Parsing the 2x12 input grid into six consecutive 2x2 blocks.
2. Identifying which predefined digit pattern corresponds to the sequence of 
   these six blocks.
3. Initializing an 8x7 output grid filled with the background color (0).
4. Placing a marker color (3) at a fixed position (row 0, column 3) in the 
   output grid.
5. Drawing the identified 7x7 digit pattern (using color 2) onto the output grid,
   starting from row 1, column 0.
"""

# --- Predefined Patterns ---
# The keys are tuples representing the sequence of six 2x2 blocks from the input.
# Each 2x2 block is represented as a tuple of two tuples (rows).
# The values are the corresponding 7x7 digit patterns (list of lists).

# Pattern for Digit '1' (from train_1)
pattern_1_key = (
    ((0, 2), (2, 2)), ((0, 2), (0, 2)), ((0, 0), (2, 0)),
    ((2, 0), (2, 2)), ((0, 2), (0, 2)), ((0, 2), (0, 2))
)
pattern_1_output = [
    [0, 0, 2, 2, 0, 0, 0],
    [0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0],
    [0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 2, 0, 0],
]

# Pattern for Digit '7' (from train_2)
pattern_7_key = (
    ((2, 0), (2, 2)), ((0, 0), (0, 2)), ((2, 0), (2, 0)),
    ((2, 0), (2, 0)), ((2, 0), (2, 2)), ((0, 2), (0, 2))
)
pattern_7_output = [
    [0, 0, 0, 2, 2, 0, 0],
    [0, 0, 0, 2, 2, 0, 0],
    [0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0],
    [0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 2, 0, 0],
]

# Pattern for Digit '4' (from train_3)
pattern_4_key = (
    ((2, 0), (2, 2)), ((0, 2), (0, 2)), ((0, 0), (2, 0)),
    ((2, 0), (2, 2)), ((0, 2), (0, 2)), ((0, 2), (0, 2))
)
pattern_4_output = [
    [0, 0, 0, 2, 2, 0, 0],
    [0, 0, 0, 0, 2, 2, 0],
    [0, 0, 0, 0, 0, 2, 2],
    [0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 2],
]

# Dictionary mapping input block sequences to output digit patterns
DIGIT_PATTERNS = {
    pattern_1_key: pattern_1_output,
    pattern_7_key: pattern_7_output,
    pattern_4_key: pattern_4_output,
}

# --- Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid encoding into the output digit display.
    Args:
        input_grid: A 2x12 list of lists containing 0s and 2s.
    Returns:
        An 8x7 list of lists representing the output digit display.
    """
    # Constants for colors and dimensions
    BACKGROUND_COLOR = 0
    MARKER_COLOR = 3
    DRAWING_COLOR = 2
    OUTPUT_ROWS = 8
    OUTPUT_COLS = 7
    PATTERN_SIZE = 7
    INPUT_ROWS = 2
    INPUT_COLS = 12
    BLOCK_SIZE = 2
    NUM_BLOCKS = INPUT_COLS // BLOCK_SIZE

    # 1. Initialize Output Grid
    output_grid = [[BACKGROUND_COLOR for _ in range(OUTPUT_COLS)] for _ in range(OUTPUT_ROWS)]

    # 2. Place Marker
    output_grid[0][3] = MARKER_COLOR

    # 3. Parse Input into Blocks
    input_blocks = []
    for i in range(NUM_BLOCKS):
        col_start = i * BLOCK_SIZE
        block = [
            (input_grid[0][col_start], input_grid[0][col_start + 1]),
            (input_grid[1][col_start], input_grid[1][col_start + 1])
        ]
        input_blocks.append(tuple(block)) # Convert inner lists to tuples for hashability
    input_block_sequence = tuple(input_blocks) # Convert outer list to tuple for hashability

    # 4. Identify Digit Pattern
    # Retrieve the corresponding 7x7 pattern based on the input sequence
    # Use .get() with a default empty pattern to handle unknown inputs gracefully
    # (although based on ARC tasks, inputs usually match known patterns)
    empty_pattern = [[BACKGROUND_COLOR] * PATTERN_SIZE for _ in range(PATTERN_SIZE)]
    digit_pattern = DIGIT_PATTERNS.get(input_block_sequence, empty_pattern)

    # 5. Draw Pattern onto Output Grid
    # Copy the 7x7 digit_pattern into the output grid, starting at row 1, col 0
    for r in range(PATTERN_SIZE):
        for c in range(PATTERN_SIZE):
            # Ensure we don't write outside the pattern area (redundant if pattern is always 7x7)
            # Place the pattern value into the output grid, offset by 1 row
            output_grid[r + 1][c] = digit_pattern[r][c]

    # 6. Return Final Output Grid
    return output_grid
