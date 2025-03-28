import numpy as np
from typing import List, Tuple, Dict

"""
Identifies the row with the widest horizontal extent of non-white pixels (template row).
For every other row containing non-white pixels (source row):
1. Extracts the sequence of non-white pixels from the start up to the last non-white pixel (source pattern).
2. Extracts the corresponding sequence from the template row (template pattern).
3. Finds the unique non-white colors in both patterns, preserving the order of first appearance.
4. Creates a mapping from the template's unique colors to the source's unique colors based on their respective order.
5. Reconstructs the source row in the output grid by applying this mapping to the template pattern, extending it to the template pattern's length. The rest of the row becomes white.
Rows that are all white or the template row itself remain unchanged.
If the number of unique colors in a source pattern doesn't match the template pattern, the source row also remains unchanged.
"""

def _get_pattern_info(row: np.ndarray) -> Tuple[np.ndarray, List[int], int]:
    """
    Finds the pattern, ordered unique colors, and length for a row.

    Args:
        row: A 1D numpy array representing a grid row.

    Returns:
        A tuple containing:
        - pattern: The slice of the row up to the last non-white pixel.
        - ordered_unique_colors: A list of unique non-white colors in order of appearance.
        - pattern_len: The length of the pattern (index of last non-white + 1).
        Returns (None, [], -1) if the row is all white.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) == 0:
        return None, [], -1  # Indicate all white row

    last_nz_index = non_white_indices[-1]
    pattern_len = last_nz_index + 1
    pattern = row[:pattern_len]

    ordered_unique_colors = []
    seen_colors = set()
    for color in pattern:
        if color != 0 and color not in seen_colors:
            ordered_unique_colors.append(color)
            seen_colors.add(color)

    return pattern, ordered_unique_colors, pattern_len

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on pattern mapping derived from a template row.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_arr = np.array(input_grid, dtype=int)
    output_arr = np.copy(input_arr)
    num_rows, num_cols = input_arr.shape

    template_row_index = -1
    max_pattern_len = -1
    template_pattern = None
    template_colors_ordered = []

    # 1. Find the template row (widest pattern)
    for r in range(num_rows):
        pattern, _, pattern_len = _get_pattern_info(input_arr[r])
        if pattern_len > max_pattern_len:
            max_pattern_len = pattern_len
            template_row_index = r
            template_pattern = pattern
            # Re-calculate ordered colors specifically for the final template
            _, template_colors_ordered, _ = _get_pattern_info(template_pattern)


    # If no non-white pixels found at all, return the original grid
    if template_row_index == -1:
        return output_arr.tolist()

    # 2. Iterate through rows and apply transformation if applicable
    for r in range(num_rows):
        # Skip the template row itself
        if r == template_row_index:
            continue

        current_row = input_arr[r]
        source_pattern, source_colors_ordered, source_len = _get_pattern_info(current_row)

        # Skip all-white rows or rows where pattern info couldn't be derived
        if source_len == -1:
            continue

        # Check if the number of unique colors matches the template
        if len(source_colors_ordered) == len(template_colors_ordered) and len(source_colors_ordered) > 0:
            # 3. Create the color mapping
            mapping: Dict[int, int] = {template_col: source_col for template_col, source_col
                                       in zip(template_colors_ordered, source_colors_ordered)}

            # 4. Construct the new row part based on the template pattern and mapping
            new_row_part = np.zeros(max_pattern_len, dtype=int)
            for c in range(max_pattern_len):
                template_color = template_pattern[c]
                # Map non-white template colors, keep white as white (0)
                new_row_part[c] = mapping.get(template_color, 0)

            # 5. Update the output grid row
            output_arr[r, :max_pattern_len] = new_row_part
            # Ensure the rest of the row is white
            output_arr[r, max_pattern_len:] = 0
        # Else: If color counts don't match, leave the row as it was (already copied)

    return output_arr.tolist()