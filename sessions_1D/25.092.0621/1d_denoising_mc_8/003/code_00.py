import collections
import copy # To ensure original input isn't modified if returned directly

"""
Transformation Rule:

1. Determine the dimensions (height `H` and width `W`) of the input grid.
2. Check if the grid represents a line: either `H=1` and `W>0` (row vector) or `W=1` and `H>0` (column vector).
3. If it's a row vector (`H=1`), extract the first (only) row as the `linear_sequence`.
4. If it's a column vector (`W=1`), extract the first (only) column as the `linear_sequence` (take the first element from each row).
5. If the grid is not a row or column vector (e.g., empty, 1x1, or multi-dimensional), return the input grid unchanged.
6. Find the index of the first non-white (non-zero) pixel (`start_index`) and the last non-white pixel (`end_index`) in the `linear_sequence`.
7. If no non-white pixels are found (`start_index` is None), return the original input grid unchanged.
8. Extract the leading white segment (pixels before `start_index`), the central segment (pixels from `start_index` to `end_index` inclusive), and the trailing white segment (pixels after `end_index`) from the `linear_sequence`.
9. Count the frequency of each color within the `central_segment`.
10. Identify the `dominant_color` (the color with the highest frequency).
11. Create a `new_central_segment` of the same length as the original `central_segment`, filled entirely with the `dominant_color`.
12. Construct the `output_sequence` by concatenating the `leading_white_segment`, the `new_central_segment`, and the `trailing_white_segment`.
13. Construct the `output_grid` by placing the `output_sequence` back into the original format:
    *   If the input was a row vector (1xN), the `output_grid` is `[output_sequence]`.
    *   If the input was a column vector (Nx1), the `output_grid` is `[[pixel] for pixel in output_sequence]`.
14. Return the `output_grid`.
"""

def find_central_segment_indices(input_list):
    """
    Finds the start and end indices of the first contiguous block of non-zero values.

    Args:
        input_list: A list of integers representing colors.

    Returns:
        A tuple (start_index, end_index).
        Returns (None, None) if no non-zero elements are found.
        start_index is the index of the first non-zero element.
        end_index is the index of the last non-zero element.
    """
    start_index = None
    end_index = None
    n = len(input_list)

    # Find the first non-zero element
    for i in range(n):
        if input_list[i] != 0:
            start_index = i
            break

    # If no non-zero element was found, return None, None
    if start_index is None:
        return None, None

    # Find the last non-zero element by searching from the end
    # Note: end_index should also be start_index if only one non-zero element exists
    for i in range(n - 1, start_index - 1, -1):
         if input_list[i] != 0:
            end_index = i
            break
            
    # This check should technically not be needed if start_index is not None,
    # but added for robustness.
    if end_index is None: 
        return None, None
        
    return start_index, end_index

def get_dominant_color(segment):
    """
    Finds the most frequent non-zero color in a list segment.

    Args:
        segment: A list of integers representing colors.

    Returns:
        The integer value of the most frequent non-zero color.
        Returns None if the segment is empty or contains only zeros.
    """
    if not segment:
        return None

    # Filter out zeros, though the central segment shouldn't contain them by definition
    non_zero_segment = [color for color in segment if color != 0]

    if not non_zero_segment:
        return None # Should not happen if segment comes from find_central_segment_indices

    counts = collections.Counter(non_zero_segment)
    # Find the color with the maximum count. If ties, most_common returns one arbitrarily.
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    
    # Ensure input is not empty
    if not input_grid or not input_grid[0]:
        return copy.deepcopy(input_grid) # Return copy if empty

    # 1. Determine dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # 2. Check if the grid represents a line (row or column vector)
    is_row_vector = height == 1 and width > 0
    is_col_vector = width == 1 and height > 0
    
    linear_sequence = []

    # 3. Extract sequence if row vector
    if is_row_vector:
        linear_sequence = input_grid[0]
    # 4. Extract sequence if column vector
    elif is_col_vector:
        linear_sequence = [input_grid[r][0] for r in range(height)]
    # 5. If not a line, return original grid
    else:
        # Handles 1x1 grids and multi-dimensional grids
        return copy.deepcopy(input_grid) 

    # 6. Find the boundaries of the central non-white segment
    start_index, end_index = find_central_segment_indices(linear_sequence)

    # 7. If no non-white pixels found, return original grid
    if start_index is None:
        return copy.deepcopy(input_grid)

    # 8. Extract segments
    leading_white_segment = linear_sequence[:start_index]
    central_segment_input = linear_sequence[start_index : end_index + 1]
    trailing_white_segment = linear_sequence[end_index + 1:]

    # 9 & 10. Find the dominant color in the central segment
    dominant_color = get_dominant_color(central_segment_input)

    # Defensive check - should have a dominant color if start_index was found
    if dominant_color is None:
         print("Warning: Could not determine dominant color despite finding a central segment.")
         return copy.deepcopy(input_grid) 

    # 11. Create the new central segment filled with the dominant color
    central_segment_output_len = len(central_segment_input)
    new_central_segment = [dominant_color] * central_segment_output_len

    # 12. Construct the output sequence
    output_sequence = leading_white_segment + new_central_segment + trailing_white_segment

    # 13. Reconstruct the output grid in the original format
    output_grid = []
    if is_row_vector:
        output_grid = [output_sequence]
    elif is_col_vector:
        output_grid = [[pixel] for pixel in output_sequence]
        
    # 14. Return the transformed grid
    return output_grid