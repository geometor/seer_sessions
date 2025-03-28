import numpy as np
from typing import List, Tuple, Dict, Set

"""
Identify horizontal sequences of non-background colors (patterns) and isolated non-background pixels (markers).
For each marker, find a pattern that contains the marker's color.
Copy that pattern onto the grid, aligning it such that the pixel in the pattern matching the marker's color is placed at the original marker's location.
The original patterns and markers remain unless overwritten by a newly copied pattern.
"""

def find_horizontal_segments(grid: np.ndarray) -> List[Tuple[List[int], int, int]]:
    """
    Finds all contiguous horizontal segments of non-zero colors.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list of tuples, where each tuple contains:
        - color_sequence (List[int]): The sequence of colors in the segment.
        - row (int): The row index of the segment.
        - start_col (int): The starting column index of the segment.
    """
    height, width = grid.shape
    segments = []
    visited_cols_in_row = set() # Keep track of cols already part of a found segment in the current row

    for r in range(height):
        visited_cols_in_row.clear()
        for c in range(width):
            if c in visited_cols_in_row:
                continue
            if grid[r, c] != 0:
                # Found the start of a potential segment
                segment_colors = []
                start_c = c
                current_c = c
                while current_c < width and grid[r, current_c] != 0:
                    segment_colors.append(grid[r, current_c])
                    visited_cols_in_row.add(current_c)
                    current_c += 1
                
                segments.append((segment_colors, r, start_c))
                # No need to update c here because the outer loop will continue from c+1,
                # and the visited check handles skipping the rest of the segment.
    return segments

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on identified patterns and markers.

    1. Finds all horizontal segments of non-background colors.
    2. Segments of length 1 are markers.
    3. Segments of length 2 or more are patterns.
    4. For each marker, finds a pattern containing the marker's color.
    5. Copies the found pattern to the marker's row, aligning the matching color.
    """
    
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # 1. Find all horizontal segments
    all_segments = find_horizontal_segments(input_np)

    # 2. & 3. Separate segments into markers and patterns
    markers = []
    patterns = []
    unique_pattern_sequences = set() # Store unique patterns as tuples to handle duplicates

    for colors, r, c in all_segments:
        if len(colors) == 1:
            markers.append((colors[0], r, c)) # Store as (color, row, col)
        elif len(colors) >= 2:
            # Store the unique pattern sequence
            pattern_tuple = tuple(colors)
            if pattern_tuple not in unique_pattern_sequences:
                 patterns.append(colors) # Store the list version for easier indexing later
                 unique_pattern_sequences.add(pattern_tuple)
            # We don't need the original location of patterns for the transformation rule itself

    # 4. & 5. Process each marker
    for marker_color, r, c in markers:
        found_pattern = None
        # Find a pattern containing the marker's color
        for p in patterns:
            if marker_color in p:
                found_pattern = p
                break # Use the first matching pattern found

        if found_pattern:
            # Find the index of the marker color within the pattern
            try:
                idx = found_pattern.index(marker_color)
            except ValueError:
                # This shouldn't happen if the pattern was selected correctly
                continue 

            # Calculate the target start column for copying
            target_start_col = c - idx

            # Copy the pattern to the output grid
            for j, p_color in enumerate(found_pattern):
                current_col = target_start_col + j
                # Check boundaries before writing
                if 0 <= current_col < width:
                    output_grid[r, current_col] = p_color

    return output_grid.tolist()