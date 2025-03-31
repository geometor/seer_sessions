import numpy as np
from typing import List, Dict, Tuple, Optional

"""
Transforms the input grid based on the following rules:
1.  Identify the single vertical segment composed of connected maroon (9) pixels in the input grid. Let its length be `L`.
2.  Create a copy of the input grid.
3.  In the copied grid, replace the identified maroon segment with the background color (orange, 7).
4.  Calculate the required output maroon length: `L_output = L + 1`.
5.  Identify all distinct vertical segments composed of connected azure (8) pixels in the *original* input grid.
6.  Filter these azure segments, keeping only those whose length is greater than or equal to `L_output`.
7.  If no azure segments meet the length requirement, return the grid with only the input maroon segment removed.
8.  From the filtered list, find the minimum length present (`L_min_azure`).
9.  Further filter the list, keeping only segments whose length is exactly `L_min_azure`.
10. From this final list, select the one with the smallest column index (leftmost). Let its starting row be `R_target` and column be `C_target`.
11. In the copied grid, change the color of the pixels from `(R_target, C_target)` down to `(R_target + L_output - 1, C_target)` to maroon (9).
12. Return the modified grid.
"""

def find_vertical_segments(grid: np.ndarray, color: int) -> List[Dict]:
    """
    Finds all contiguous vertical segments of a given color in the grid.

    Args:
        grid: The input numpy array representing the grid.
        color: The integer value of the color to find segments for.

    Returns:
        A list of dictionaries, where each dictionary represents a segment
        and contains 'length', 'row' (start row), and 'col'.
        Returns an empty list if no segments are found.
    """
    segments = []
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool) # Keep track of visited cells within segments

    for c in range(cols):
        for r in range(rows):
            # Check if the cell has the target color and hasn't been visited as part of a segment yet
            if grid[r, c] == color and not visited[r, c]:
                # Found the start of a potential segment
                segment_len = 0
                current_r = r
                # Extend downwards as long as the color matches and within bounds
                while current_r < rows and grid[current_r, c] == color:
                    visited[current_r, c] = True
                    segment_len += 1
                    current_r += 1

                # Store the found segment details
                if segment_len > 0:
                    segments.append({'length': segment_len, 'row': r, 'col': c})
    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rules to the input grid.
    """
    # Define colors
    background_color = 7
    maroon = 9
    azure = 8

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 1. Find the input maroon segment
    maroon_segments = find_vertical_segments(input_grid, maroon)

    # Assume there is exactly one maroon segment based on examples.
    # If not found (edge case), return the original grid copy.
    if not maroon_segments:
        return output_grid
    
    input_maroon_segment = maroon_segments[0]
    maroon_len = input_maroon_segment['length']
    maroon_start_row = input_maroon_segment['row']
    maroon_col = input_maroon_segment['col']

    # 3. Replace the input maroon segment with the background color
    output_grid[maroon_start_row : maroon_start_row + maroon_len, maroon_col] = background_color

    # 4. Calculate the required output maroon length
    l_output = maroon_len + 1

    # 5. Identify all azure segments in the original grid
    azure_segments = find_vertical_segments(input_grid, azure)

    # If no azure segments exist at all, return the grid after removing maroon
    if not azure_segments:
        return output_grid

    # 6. Filter azure segments: length >= L_output
    valid_azure_segments = [seg for seg in azure_segments if seg['length'] >= l_output]

    # 7. If no segments meet the length requirement, return the grid
    if not valid_azure_segments:
        return output_grid

    # 8. Find the minimum length among the valid segments
    min_valid_length = min(seg['length'] for seg in valid_azure_segments)

    # 9. Filter again: keep only segments with the minimum valid length
    shortest_valid_segments = [seg for seg in valid_azure_segments if seg['length'] == min_valid_length]

    # 10. Select the leftmost segment among the shortest valid ones
    target_azure_segment = min(shortest_valid_segments, key=lambda seg: seg['col'])

    target_start_row = target_azure_segment['row']
    target_col = target_azure_segment['col']

    # 11. Replace the top L_output pixels of the target segment with maroon
    # Ensure we don't write past the grid boundary (slicing handles this).
    # Ensure we don't write more pixels than the target segment has (use min).
    # Although step 6 guarantees target_azure_segment['length'] >= l_output,
    # using min is safer programming practice.
    num_pixels_to_change = min(l_output, target_azure_segment['length'])
    end_row = target_start_row + num_pixels_to_change
    
    output_grid[target_start_row : end_row, target_col] = maroon

    # 12. Return the modified grid
    return output_grid