import numpy as np
from typing import List, Tuple, Set

"""
Recolor vertical segments of red(2) pixels based on whether they are the first segment encountered when scanning from top to bottom, left to right.

1. Create an output grid as a copy of the input grid.
2. Find all contiguous vertical segments of red(2) pixels.
3. Keep track of the starting row (minimum row index) for each segment.
4. Identify the overall minimum starting row among all found segments.
5. Recolor the pixels of the segment(s) that start at this minimum row to maroon(9).
6. Recolor the pixels of all other red(2) segments to orange(7).
7. White(0) pixels remain unchanged.
"""

def find_vertical_red_segments(input_grid: np.ndarray) -> Tuple[List[Tuple[int, List[Tuple[int, int]]]], int]:
    """
    Finds all contiguous vertical segments of red(2) pixels.

    Args:
        input_grid: The input numpy array grid.

    Returns:
        A tuple containing:
        - A list of segments, where each segment is a tuple: (start_row, list_of_coordinates).
        - The minimum start row found across all segments.
    """
    height, width = input_grid.shape
    visited_pixels: Set[Tuple[int, int]] = set()
    red_segments: List[Tuple[int, List[Tuple[int, int]]]] = []
    min_start_row = height  # Initialize with a value larger than any possible row index

    # Iterate through grid, column by column, then row by row
    for c in range(width):
        for r in range(height):
            # If pixel is red and not yet part of a found segment
            if input_grid[r, c] == 2 and (r, c) not in visited_pixels:
                current_segment_pixels: List[Tuple[int, int]] = []
                current_row = r
                # Scan downwards to find the full vertical segment
                while current_row < height and input_grid[current_row, c] == 2:
                    pixel_coord = (current_row, c)
                    # Only add if not visited (this check might be redundant given the outer check, but safe)
                    if pixel_coord not in visited_pixels:
                         current_segment_pixels.append(pixel_coord)
                         visited_pixels.add(pixel_coord)
                    else:
                        # If we hit a visited pixel in the same column scan, break
                        # This handles cases where segments might technically touch corners
                        # but we process based on the top-most unvisited pixel.
                        # In simple vertical lines, this break won't be hit mid-segment.
                         break
                    current_row += 1

                # If a segment was found (at least one pixel)
                if current_segment_pixels:
                    segment_start_row = r # The starting row is the 'r' where we initiated the search
                    red_segments.append((segment_start_row, current_segment_pixels))
                    min_start_row = min(min_start_row, segment_start_row)

    return red_segments, min_start_row

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by recoloring vertical red segments.

    Args:
        input_grid: The input numpy array grid.

    Returns:
        The transformed numpy array grid.
    """
    # Initialize output_grid as a copy
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find all vertical red segments and the minimum starting row
    red_segments, first_segment_start_row = find_vertical_red_segments(input_grid)

    # Check if any red segments were found
    if not red_segments:
        return output_grid # No red pixels, return the copy

    # Recolor the segments based on their start row
    for start_row, pixel_list in red_segments:
        # Determine the color based on whether it's the first segment
        new_color = 9 if start_row == first_segment_start_row else 7 # 9: maroon, 7: orange

        # Apply the color to all pixels in the segment
        for r, c in pixel_list:
            output_grid[r, c] = new_color

    return output_grid