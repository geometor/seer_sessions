import numpy as np
from typing import List, Tuple, Optional

# COLOR_MAP = {
#     0: (238, 238, 238),  # white
#     1: (30, 147, 255),  # blue
#     2: (220, 50, 40),  # red
#     3: (79, 204, 48),  # green
#     4: (230, 200, 0),  # yellow
#     5: (85, 85, 85),  # gray
#     6: (229, 58, 163),  # magenta
#     7: (230, 120, 20),  # orange
#     8: (135, 216, 241),  # azure
#     9: (146, 18, 49),  # maroon
# }

"""
Transformation rule:
1. Determine the dimensions (height H, width W) of the input grid.
2. Identify the delimiter color D from the bottom-right pixel (H-1, W-1).
3. Scan the input grid row by row to find the base repeating patterns present in the sequences before the delimiter.
    a. For each row, extract the sequence S of colors from the start up to, but not including, the first occurrence of D. If D is not in the row, S is the entire row.
    b. If S is not empty, find its shortest repeating pattern P.
    c. Store the first unique pattern found as P0.
    d. Store the second unique pattern found (different from P0) as P1. If only one unique pattern exists across all rows, P1 will be the same as P0.
4. Calculate the left-shifted versions of these patterns:
    a. P0_shifted is P0 cyclically shifted one position to the left.
    b. P1_shifted is P1 cyclically shifted one position to the left.
5. Create a new output grid of the same dimensions (H x W).
6. Fill the output grid row by row:
    a. For even-numbered rows (0, 2, 4,...), tile the row completely with P0_shifted.
    b. For odd-numbered rows (1, 3, 5,...), tile the row completely with P1_shifted.
7. Return the completed output grid.
"""

def find_shortest_repeating_pattern(sequence: List[int]) -> List[int]:
    """
    Finds the shortest repeating pattern that generates the sequence.
    Example: [1, 2, 3, 1, 2, 3, 1, 2] -> [1, 2, 3]
             [5, 5, 5, 5] -> [5]
    """
    n = len(sequence)
    if n == 0:
        return []
    for length in range(1, n + 1):
        pattern = sequence[:length]
        # Check if repeating the pattern matches the sequence
        is_repeating = True
        for i in range(n):
            if sequence[i] != pattern[i % length]:
                is_repeating = False
                break
        if is_repeating:
            return pattern
    # Should only happen if input is empty, handled above.
    return sequence # Fallback

def shift_pattern(pattern: List[int]) -> List[int]:
    """Cyclically shifts a pattern one position to the left."""
    if not pattern or len(pattern) <= 1:
        return pattern
    return pattern[1:] + pattern[:1]

def tile_pattern(pattern: List[int], width: int) -> List[int]:
    """Tiles a pattern to fill a given width."""
    if not pattern:
        # Decide on fallback behavior for empty pattern.
        # Let's default to color 0 (white/background).
        # Although based on the logic, pattern should not be empty if derived correctly.
        return [0] * width
    
    pattern_len = len(pattern)
    return [pattern[i % pattern_len] for i in range(width)]

def get_sequence_before_delimiter(row: List[int], delimiter: int) -> List[int]:
    """Extracts the sequence from the start of the row until the delimiter."""
    sequence_s = []
    for pixel in row:
        if pixel == delimiter:
            break
        sequence_s.append(pixel)
    return sequence_s

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the alternating shifted pattern transformation based on row parity.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. & 2. Get dimensions and delimiter
    if height == 0 or width == 0:
        return [] # Handle empty grid
    delimiter_color = input_np[height - 1, width - 1]

    # 3. Find the base patterns P0 and P1
    pattern0: Optional[List[int]] = None
    pattern1: Optional[List[int]] = None

    for r in range(height):
        row_list = input_np[r, :].tolist()
        sequence_s = get_sequence_before_delimiter(row_list, delimiter_color)

        if sequence_s: # Only process if sequence before delimiter is non-empty
            current_pattern = find_shortest_repeating_pattern(sequence_s)
            if not current_pattern: # Should not happen if sequence_s is not empty
                continue

            if pattern0 is None:
                pattern0 = current_pattern
                # print(f"Found P0 at row {r}: {pattern0}") # Debug
            elif pattern1 is None and current_pattern != pattern0:
                pattern1 = current_pattern
                # print(f"Found P1 at row {r}: {pattern1}") # Debug
                break # Found both distinct patterns

    # Handle cases where only one pattern was found or no patterns found
    if pattern0 is None:
         # This case means no row had any content before the delimiter,
         # or the grid was empty. Or all rows started with the delimiter.
         # Based on examples, this is unlikely. If it happens,
         # perhaps return the input or an empty/default grid.
         # Let's return a grid of zeros for now as a fallback.
         # print("Warning: No base pattern found.") # Debug
         return np.zeros_like(input_np).tolist()

    if pattern1 is None:
        # print("Only one unique pattern found, using P0 for P1.") # Debug
        pattern1 = pattern0 # Only one unique pattern exists

    # 4. Calculate shifted patterns
    p0_shifted = shift_pattern(pattern0)
    p1_shifted = shift_pattern(pattern1)

    # 5. Create output grid
    output_grid = np.zeros_like(input_np)

    # 6. Fill the output grid based on row parity
    for r in range(height):
        if r % 2 == 0: # Even row index
            output_row = tile_pattern(p0_shifted, width)
        else: # Odd row index
            output_row = tile_pattern(p1_shifted, width)
        
        # Ensure output_row has the correct length (should be guaranteed by tile_pattern)
        if len(output_row) == width:
             output_grid[r, :] = output_row
        else:
            # Fallback or error handling if tiling failed
            # print(f"Error: Tiling row {r} resulted in incorrect width.") # Debug
            # Fill with a default value, e.g. 0
             output_grid[r, :] = 0


    # 7. Return the completed output grid
    return output_grid.tolist()