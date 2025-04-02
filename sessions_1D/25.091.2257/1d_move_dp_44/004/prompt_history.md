
## train_1

**input:**
```
7 7 7 0 0 0 9
```


**output:**
```
0 0 0 7 7 7 9
```


## train_2

**input:**
```
3 3 3 0 0 9 0
```


**output:**
```
0 0 3 3 3 9 0
```


## train_3

**input:**
```
8 8 8 0 0 0 9
```


**output:**
```
0 0 0 8 8 8 9
```

**Perception:**

The input and output are single-row grids (1D arrays). Each example shows a sequence of colors. The core pattern involves identifying two adjacent blocks of colors before a specific separator color (maroon, 9). One block consists of a repeated non-white color, and the other block consists of repeated white colors (0). These two blocks swap their positions in the output sequence, while the separator color (maroon, 9) and any subsequent colors remain in their relative positions after the swapped blocks.

**Facts:**


```yaml
task_type: sequence_manipulation
grid_dimensionality: 1D
color_palette: [white(0), green(3), orange(7), azure(8), maroon(9)] # Colors observed in examples
objects:
  - type: block
    description: Contiguous sequence of identical non-white pixels. Denoted as BlockA.
    properties:
      - color: Varies (orange, green, azure in examples)
      - position: Immediately precedes BlockB.
  - type: block
    description: Contiguous sequence of white (0) pixels. Denoted as BlockB.
    properties:
      - color: white (0)
      - position: Immediately follows BlockA.
  - type: separator
    description: A single maroon (9) pixel.
    properties:
      - color: maroon (9)
      - position: Immediately follows BlockB.
  - type: remainder
    description: Sequence of pixels following the separator.
    properties:
      - position: Follows the separator.
      - content: Can be empty or contain other pixels.
relationships:
  - type: adjacency
    description: BlockA is immediately followed by BlockB.
  - type: adjacency
    description: BlockB is immediately followed by the Separator.
action:
  - type: swap
    description: The positions of BlockA and BlockB are swapped.
    operands: [BlockA, BlockB]
  - type: maintain_relative_position
    description: The Separator and Remainder maintain their positions relative to the end of the swapped blocks.
    operands: [Separator, Remainder]
constraints:
  - The swap operation occurs only on the portion of the sequence *before* the maroon (9) separator.
```


**Natural Language Program:**

1.  Identify the first contiguous block of identical non-white pixels (`BlockA`) in the input sequence.
2.  Identify the contiguous block of white (0) pixels (`BlockB`) that immediately follows `BlockA`.
3.  Identify the index of the first occurrence of the maroon (9) pixel (`Separator`). This marks the end of the section to be modified.
4.  Construct the output sequence by first placing `BlockB`, followed immediately by `BlockA`.
5.  Append the rest of the original input sequence starting from the maroon (9) pixel (`Separator`) to the end.
```python
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

```
```python
"""
Transforms an input 1xN sequence (represented as a list containing a single list of integers)
by identifying a specific adjacent pattern: a contiguous block of identical non-white pixels (BlockA),
immediately followed by a contiguous block of white (0) pixels (BlockB), immediately followed by
a maroon (9) pixel (Separator). If this pattern (BlockA -> BlockB -> Separator) is found,
the positions of BlockA and BlockB are swapped, while the portion of the sequence before BlockA (Prefix)
and the portion including and after the Separator (Suffix) remain in their relative positions.
If the pattern is not found, the original input sequence is returned unchanged.
"""

import numpy as np
from typing import List, Optional, Tuple

# Define color constants
WHITE = 0
MAROON = 9

def find_first_non_white_block(sequence: List[int]) -> Optional[Tuple[int, int, int]]:
    """Finds the start index, end index, and color of the first contiguous block of non-white pixels."""
    n = len(sequence)
    start_index = -1
    color = -1

    for i in range(n):
        if sequence[i] != WHITE:
            start_index = i
            color = sequence[i]
            end_index = i
            # Extend the block as long as the color matches
            while end_index + 1 < n and sequence[end_index + 1] == color:
                end_index += 1
            return start_index, end_index, color
    return None # No non-white block found

def find_following_white_block(sequence: List[int], start_search_index: int) -> Optional[Tuple[int, int]]:
    """Finds the start and end index of a contiguous white block starting immediately after start_search_index."""
    n = len(sequence)
    if start_search_index >= n or sequence[start_search_index] != WHITE:
        return None # No white block starts immediately after

    start_index = start_search_index
    end_index = start_index
    # Extend the block as long as it's white
    while end_index + 1 < n and sequence[end_index + 1] == WHITE:
        end_index += 1
    return start_index, end_index

def check_separator(sequence: List[int], index: int) -> bool:
    """Checks if the pixel at the given index is the MAROON separator."""
    return index < len(sequence) and sequence[index] == MAROON

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the block swapping transformation based on the identified pattern.
    """
    # --- Input Validation ---
    if not input_grid or not isinstance(input_grid, list) or len(input_grid) != 1 or \
       not input_grid[0] or not isinstance(input_grid[0], list):
        # Return input if it's not a valid 1xN grid representation
        return input_grid

    sequence = input_grid[0]
    n = len(sequence)

    # --- Find Pattern: BlockA -> BlockB -> Separator ---
    block_a_info = find_first_non_white_block(sequence)

    if block_a_info is None:
        # BlockA not found, pattern fails
        return input_grid

    start_a, end_a, _ = block_a_info
    block_a = sequence[start_a : end_a + 1]

    # Look for BlockB immediately after BlockA
    block_b_info = find_following_white_block(sequence, end_a + 1)

    if block_b_info is None:
        # BlockB not found immediately after BlockA, pattern fails
        return input_grid

    start_b, end_b = block_b_info
    block_b = sequence[start_b : end_b + 1]

    # Look for Separator immediately after BlockB
    separator_index = end_b + 1
    if not check_separator(sequence, separator_index):
        # Separator not found immediately after BlockB, pattern fails
        return input_grid

    # --- Pattern Found: Perform Transformation ---

    # Identify Prefix (before BlockA)
    prefix = sequence[:start_a]

    # Identify Suffix (Separator and onwards)
    suffix = sequence[separator_index:]

    # Reconstruct the sequence with swapped blocks
    output_sequence = prefix + block_b + block_a + suffix

    # Return the result in the expected format
    return [output_sequence]

```
