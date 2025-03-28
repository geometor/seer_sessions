"""
Transformation rule:
1. Determine the dimensions (height H, width W) of the input grid.
2. Identify the delimiter color from the bottom-right pixel (H-1, W-1) of the input grid.
3. Create a new output grid of the same dimensions (H x W).
4. For each row r in the input grid:
    a. Extract the sequence of colors S from the start of the row up to, but not including, the first occurrence of the delimiter color. If the delimiter is not found, the entire row is S.
    b. Find the shortest repeating pattern P within S. This is the smallest prefix of S which, when repeated, generates S (or the beginning of S).
    c. Create a shifted pattern P_shifted by cyclically shifting P one position to the left (first element moves to the end).
    d. Fill row r of the output grid by repeating P_shifted across the entire width W.
5. Return the completed output grid.
"""

import numpy as np

def find_shortest_repeating_pattern(sequence):
    """
    Finds the shortest repeating pattern that generates the sequence.
    For example, [1, 2, 3, 1, 2, 3, 1, 2] -> [1, 2, 3]
                [5, 5, 5, 5] -> [5]
                [1, 2, 1, 3, 1, 2] -> [1, 2, 1, 3] (or the whole sequence if no shorter pattern)
    """
    n = len(sequence)
    if n == 0:
        return []
    for length in range(1, n + 1):
        pattern = sequence[:length]
        is_repeating = True
        # Check if repeating the pattern matches the sequence
        for i in range(n):
            if sequence[i] != pattern[i % length]:
                is_repeating = False
                break
        if is_repeating:
            return pattern
    # Should not happen based on problem description, but as fallback:
    return sequence 


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the pattern shift and tile transformation to the input grid.
    """
    input_grid = np.array(input_grid) # Ensure input is a numpy array
    height, width = input_grid.shape

    # Initialize output_grid with the same shape, filled with a placeholder (e.g., -1)
    # Using the same dtype as input grid
    output_grid = np.full((height, width), -1, dtype=input_grid.dtype) 

    # 1 & 2. Identify the delimiter color from the bottom-right pixel
    delimiter_color = input_grid[height - 1, width - 1]

    # 4. Process each row
    for r in range(height):
        input_row = input_grid[r, :]
        
        # 4a. Extract the sequence S up to the delimiter
        sequence_s = []
        for pixel in input_row:
            if pixel == delimiter_color:
                break
            sequence_s.append(pixel)

        # Handle empty sequence (e.g., if the first pixel is the delimiter)
        if not sequence_s:
           # If the sequence is empty, find the pattern from the whole row excluding the delimiter if it exists
           # This handles cases where the delimiter might be the pattern itself or edge cases
           temp_seq = [p for p in input_row if p != delimiter_color]
           if not temp_seq: # If row is ALL delimiters or empty
               # Need a defined behavior. Let's assume we repeat the delimiter? Or maybe based on neighbors?
               # Given the examples, the non-delimiter part seems crucial. If it's all delimiters, maybe output is too?
               # Let's try finding pattern in the full row if S is empty initially.
               sequence_s = list(input_row) 
               # If the entire row consists *only* of the delimiter color, handle this explicitly.
               if all(p == delimiter_color for p in sequence_s):
                   # Option 1: Fill output row with delimiter color? 
                   # Option 2: Try to find pattern in row above/below? (Complex)
                   # Option 3: Based on example 1, even delimiter rows seem ignored/overwritten. 
                   # Let's assume for now we need *some* non-delimiter pattern. If none found, this row might be problematic.
                   # Revisit: Maybe just find pattern in the whole row *including* delimiter if S is empty?
                   pattern_p = find_shortest_repeating_pattern(sequence_s) # This will likely be just [delimiter_color]
               else:
                  # If S was empty but row has other colors, find pattern in the whole row
                  pattern_p = find_shortest_repeating_pattern(sequence_s)

           else: 
               # Original sequence S was empty, but the row wasn't all delimiters. Use the full row.
               sequence_s = list(input_row)
               pattern_p = find_shortest_repeating_pattern(sequence_s)
        else:
            # 4b. Find the shortest repeating pattern P
            pattern_p = find_shortest_repeating_pattern(sequence_s)

        # 4c. Create the shifted pattern P_shifted
        if not pattern_p: # Handle case of empty pattern (shouldn't happen with above logic)
             # Fallback: fill with a default color like 0 (black)? Or copy input row?
             # Let's fill with 0 for now if pattern is somehow empty.
             output_grid[r, :] = 0
             continue # Go to next row

        pattern_len = len(pattern_p)
        if pattern_len == 1:
            shifted_pattern = pattern_p # Shifting a single element does nothing
        else:
            shifted_pattern = pattern_p[1:] + pattern_p[:1] # Move first element to the end

        # 4d. Fill the output row by tiling P_shifted
        shifted_len = len(shifted_pattern)
        for c in range(width):
            output_grid[r, c] = shifted_pattern[c % shifted_len]

    # 5. Return the output grid
    return output_grid.tolist() # Return as list of lists per ARC standard
