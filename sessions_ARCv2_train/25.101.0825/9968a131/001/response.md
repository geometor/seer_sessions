```python
import copy

"""
Processes each row of the input grid independently.
Searches for the first occurrence (leftmost) of either the sequence [8, 3] (azure, green) or [5, 0] (gray, white).
If one of these sequences is found, it inserts the color 7 (orange) immediately before the sequence.
The resulting row is then truncated from the right to maintain the original row width.
If neither sequence is found in a row, the row remains unchanged.
"""

def find_first_sequence(row: list[int], seq: list[int]) -> int:
    """
    Finds the starting index of the first occurrence of a sequence within a row.
    Returns -1 if the sequence is not found.
    """
    seq_len = len(seq)
    row_len = len(row)
    for i in range(row_len - seq_len + 1):
        if row[i:i + seq_len] == seq:
            return i
    return -1

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on row-specific sequence detection and insertion.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Define trigger sequences and insertion color
    trigger_sequence_1 = [8, 3]  # azure, green
    trigger_sequence_2 = [5, 0]  # gray, white
    inserted_color = 7         # orange

    # Get the width of the grid (assuming all rows have the same width)
    if not input_grid:
        return []
    grid_width = len(input_grid[0])
    if grid_width == 0:
        return [[] for _ in input_grid]


    # Initialize output grid as a deep copy to avoid modifying the input directly
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each row of the input grid
    for r, row in enumerate(input_grid):
        # Find the first occurrence of each trigger sequence in the current row
        index1 = find_first_sequence(row, trigger_sequence_1)
        index2 = find_first_sequence(row, trigger_sequence_2)

        # Determine the index of the earliest sequence found
        target_index = -1
        if index1 != -1 and index2 != -1:
            target_index = min(index1, index2)
        elif index1 != -1:
            target_index = index1
        elif index2 != -1:
            target_index = index2

        # If a trigger sequence was found in the row
        if target_index != -1:
            # Construct the new row: part before sequence + inserted color + sequence and onwards
            new_row = row[:target_index] + [inserted_color] + row[target_index:]
            # Truncate the new row to the original grid width
            output_grid[r] = new_row[:grid_width]
        # Otherwise (no trigger sequence found), the row in output_grid remains unchanged (already copied)

    return output_grid
```