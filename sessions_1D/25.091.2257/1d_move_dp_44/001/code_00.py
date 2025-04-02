import numpy as np
from typing import List

# Color constants (optional, but good practice)
WHITE = 0
MAROON = 9

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input 1D sequence (represented as a 1xN grid) based on the following rule:
    1. Identify the first contiguous block of identical non-white pixels (BlockA).
    2. Identify the contiguous block of white (0) pixels (BlockB) that immediately follows BlockA.
    3. Identify the index of the first occurrence of the maroon (9) pixel (Separator). This marks the end of the section to be modified.
    4. Construct the output sequence by first placing BlockB, followed immediately by BlockA.
    5. Append the rest of the original input sequence starting from the maroon (9) pixel (Separator) to the end.
    """

    # Ensure input is a 1xN grid and extract the sequence
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        # Return empty or original grid if input format is unexpected
        return input_grid

    sequence = input_grid[0]
    n = len(sequence)

    # --- Find BlockA (first non-white block) ---
    start_a = -1
    end_a = -1
    block_a = []
    for i in range(n):
        if sequence[i] != WHITE:
            start_a = i
            block_a_color = sequence[i]
            end_a = i
            # Extend BlockA as long as the color matches
            while end_a + 1 < n and sequence[end_a + 1] == block_a_color:
                end_a += 1
            block_a = sequence[start_a : end_a + 1]
            break # Found the first non-white block

    # If BlockA wasn't found, return the original sequence
    if start_a == -1:
        return input_grid

    # --- Find BlockB (white block immediately after BlockA) ---
    start_b = end_a + 1
    end_b = -1
    block_b = []
    if start_b < n and sequence[start_b] == WHITE:
        end_b = start_b
        # Extend BlockB as long as it's white
        while end_b + 1 < n and sequence[end_b + 1] == WHITE:
            end_b += 1
        block_b = sequence[start_b : end_b + 1]
    else:
        # If no white block immediately follows BlockA, return original
        return input_grid

    # --- Find Separator (first MAROON pixel after BlockB) ---
    separator_index = -1
    try:
        # Search specifically *after* BlockB ends
        search_start_index = end_b + 1
        if search_start_index < n:
             separator_index = sequence.index(MAROON, search_start_index)
        # If the separator is not found *after* BlockB, the pattern is broken
        if separator_index == -1:
             return input_grid # Pattern assumption failed
        # We also need to ensure Block B is *immediately* before the separator if there's nothing else between them.
        # The structure implied is BlockA -> BlockB -> Separator...
        # Our find logic ensures A then B. We need B then Separator (potentially with other elements before A).
        # The index() method finds the *first* MAROON after Block B. Let's check if it's immediately after.
        # The examples show it can be right after (train_1, train_3) or have other elements after the separator (train_2).
        # The crucial part is that BlockA and BlockB are swapped *before* the separator.
        # The find logic above correctly identifies the separator *after* B.

    except ValueError:
        # If MAROON (9) is not found anywhere after BlockB, return original
        return input_grid


    # --- Construct the Output Sequence ---
    # Get the prefix (part before BlockA, should be empty based on examples)
    prefix = sequence[:start_a]

    # Get the suffix (part from the separator onwards)
    suffix = sequence[separator_index:]

    # Combine: prefix + BlockB + BlockA + suffix
    output_sequence = prefix + block_b + block_a + suffix

    # Return the result as a 1xN grid
    return [output_sequence]
