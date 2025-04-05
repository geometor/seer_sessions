
## train_1

**input:**
```
0 7 7 7 7 7 7 2 0 0 0 0
```


**output:**
```
0 7 7 7 7 7 7 2 0 0 0 0
```


## train_2

**input:**
```
6 2 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 2 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 2 5 5 5 5 5 5 5 5 5
```


**output:**
```
0 0 2 5 5 5 5 5 5 5 5 5
```


## train_4

**input:**
```
0 0 0 0 0 0 0 2 3 3 3 3
```


**output:**
```
0 0 0 0 0 0 0 2 3 3 3 3
```


## train_5

**input:**
```
5 5 5 5 5 0 0 0 0 2 0 0
```


**output:**
```
0 0 0 0 5 5 5 5 5 2 0 0
```


## train_6

**input:**
```
0 0 0 0 0 4 0 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 4 2 0 0 0 0
```


## train_7

**input:**
```
2 0 5 5 5 5 5 5 5 5 5 0
```


**output:**
```
2 5 5 5 5 5 5 5 5 5 0 0
```

*   **Perception of Elements:** The task operates on sequences of single digits. Each sequence contains the digit `2` exactly once. The sequences also contain blocks of identical non-zero digits and potentially zeros (`0`). The core transformation involves the digit `2` and its relationship with adjacent non-zero blocks and intervening zeros. In some cases, the input and output are identical, suggesting the transformation conditions are not met. In other cases, zeros located between the `2` and an adjacent block of non-zero digits are moved to the outer side of that block.

*   **YAML Facts:**
    
```yaml
    Task: Rearrange digits in a sequence based on the position of '2'.

    Objects:
      - Sequence: A list of single-digit integers.
      - Digit '2': A unique marker within the sequence.
      - Non-Zero Block: A contiguous subsequence of identical digits greater than 0.
      - Intervening Zeros: Zeros located between the '2' and an adjacent Non-Zero Block.

    Properties:
      - Sequence: Has length, contains digits.
      - Digit '2': Has a specific index (position).
      - Non-Zero Block: Has a starting index, ending index, and a specific digit value.
      - Intervening Zeros: Have count and original positions.

    Relationships:
      - Adjacency: A Non-Zero Block can be adjacent to '2', potentially separated only by Intervening Zeros. Adjacency can be to the left or right of '2'.
      - Containment: Intervening Zeros are contained within the segment between '2' and the boundary of the adjacent Non-Zero Block.

    Actions:
      - Find: Locate the index of '2'.
      - Identify: Find Non-Zero Blocks adjacent (allowing for zeros) to '2'.
      - Collect: Gather Intervening Zeros between '2' and an adjacent Non-Zero Block.
      - Move: Relocate the collected Intervening Zeros to the outer side of the identified Non-Zero Block.
        - If the block is to the left of '2', move zeros to the position immediately before the block's start.
        - If the block is to the right of '2', move zeros to the position immediately after the block's end.
      - Reconstruct: Form the output sequence based on the moved elements.

    Conditionality:
      - The move action only occurs if Intervening Zeros exist between '2' and an adjacent Non-Zero Block.
      - If no such condition is met on either side of '2', the sequence remains unchanged.
      - The process checks one side (e.g., left) first. If a move occurs, the process may terminate without checking the other side (based on examples).
    ```


*   **Natural Language Program:**
    1.  Read the input sequence of digits.
    2.  Find the index position of the digit `2`.
    3.  Examine the segment of the sequence immediately to the left of the `2`. Scan leftwards from the position before the `2`.
    4.  Count and collect any consecutive `0`s found (`intervening_zeros`). Stop scanning left if a non-zero digit is encountered or the beginning of the sequence is reached.
    5.  If `intervening_zeros` were found AND a non-zero digit `d` was encountered immediately before them:
        a.  Identify the full contiguous block of `d` digits ending at this position (`adjacent_block`).
        b.  Remove the `intervening_zeros` from their original positions.
        c.  Insert the `intervening_zeros` into the sequence immediately before the start of the `adjacent_block`.
        d.  Output the modified sequence and terminate.
    6.  If no change was made in the previous steps, examine the segment of the sequence immediately to the right of the `2`. Scan rightwards from the position after the `2`.
    7.  Count and collect any consecutive `0`s found (`intervening_zeros`). Stop scanning right if a non-zero digit is encountered or the end of the sequence is reached.
    8.  If `intervening_zeros` were found AND a non-zero digit `d` was encountered immediately after them:
        a.  Identify the full contiguous block of `d` digits starting at this position (`adjacent_block`).
        b.  Remove the `intervening_zeros` from their original positions.
        c.  Insert the `intervening_zeros` into the sequence immediately after the end of the `adjacent_block`.
        d.  Output the modified sequence and terminate.
    9.  If no changes were made in any of the previous steps, output the original input sequence.
```python
import sys
import math
# Add any other necessary imports here (e.g., numpy if needed for complex grid operations)

"""
Transformation Rule Natural Language Description:

1.  Find the index of the digit `2` in the input sequence.
2.  Check the segment immediately to the left of `2`. Scan leftwards, collecting consecutive `0`s (`intervening_zeros`).
3.  If `intervening_zeros` are found and they are immediately preceded by a non-zero digit `d`, identify the full block of `d` digits (`adjacent_block`).
4.  If such a block and zeros are found on the left, move the `intervening_zeros` to the position immediately before the start of the `adjacent_block`. Reconstruct and return the sequence.
5.  If no change was made on the left, check the segment immediately to the right of `2`. Scan rightwards, collecting consecutive `0`s (`intervening_zeros`).
6.  If `intervening_zeros` are found and they are immediately followed by a non-zero digit `d`, identify the full block of `d` digits (`adjacent_block`).
7.  If such a block and zeros are found on the right, move the `intervening_zeros` to the position immediately after the end of the `adjacent_block`. Reconstruct and return the sequence.
8.  If no changes were made on either side, return the original sequence.
"""

def find_block_left(grid, start_scan_idx):
    """
    Finds a contiguous block of identical non-zero digits ending at start_scan_idx.
    Returns the block's digit, start index, and end index, or None if no such block exists.
    """
    if start_scan_idx < 0 or grid[start_scan_idx] == 0:
        return None, -1, -1

    block_digit = grid[start_scan_idx]
    block_end_idx = start_scan_idx
    block_start_idx = block_end_idx
    while block_start_idx > 0 and grid[block_start_idx - 1] == block_digit:
        block_start_idx -= 1
    return block_digit, block_start_idx, block_end_idx

def find_block_right(grid, start_scan_idx):
    """
    Finds a contiguous block of identical non-zero digits starting at start_scan_idx.
    Returns the block's digit, start index, and end index, or None if no such block exists.
    """
    if start_scan_idx >= len(grid) or grid[start_scan_idx] == 0:
        return None, -1, -1

    block_digit = grid[start_scan_idx]
    block_start_idx = start_scan_idx
    block_end_idx = block_start_idx
    while block_end_idx < len(grid) - 1 and grid[block_end_idx + 1] == block_digit:
        block_end_idx += 1
    return block_digit, block_start_idx, block_end_idx


def transform(input_str):
    """
    Applies the transformation rule to the input string sequence.
    """
    # Parse input string into a list of integers
    grid = [int(d) for d in input_str.split()]
    n = len(grid)

    # Find the index of '2'
    try:
        idx2 = grid.index(2)
    except ValueError:
        # '2' not found, which shouldn't happen based on the problem description
        # Return original string as a fallback
        return input_str

    # --- Check Left Side ---
    num_zeros_left = 0
    scan_idx_left = idx2 - 1
    # Scan leftwards for zeros immediately preceding '2'
    while scan_idx_left >= 0 and grid[scan_idx_left] == 0:
        num_zeros_left += 1
        scan_idx_left -= 1

    # If zeros were found, check for an adjacent non-zero block
    if num_zeros_left > 0:
        block_digit_left, block_start_idx_left, block_end_idx_left = find_block_left(grid, scan_idx_left)
        # Ensure the block found is indeed adjacent (ends right before the zeros)
        if block_digit_left is not None and block_end_idx_left == idx2 - num_zeros_left - 1:
            # Perform the move: Move zeros from [block_end+1, idx2-1] to before block_start
            segment_before_block = grid[:block_start_idx_left]
            moved_zeros = grid[block_end_idx_left + 1 : idx2]
            the_block = grid[block_start_idx_left : block_end_idx_left + 1]
            segment_after_2 = grid[idx2:] # Includes the '2'

            # Reconstruct the grid
            new_grid = segment_before_block + moved_zeros + the_block + segment_after_2
            return " ".join(map(str, new_grid))

    # --- Check Right Side (only if no change was made on the left) ---
    num_zeros_right = 0
    scan_idx_right = idx2 + 1
    # Scan rightwards for zeros immediately following '2'
    while scan_idx_right < n and grid[scan_idx_right] == 0:
        num_zeros_right += 1
        scan_idx_right += 1

    # If zeros were found, check for an adjacent non-zero block
    if num_zeros_right > 0:
        block_digit_right, block_start_idx_right, block_end_idx_right = find_block_right(grid, scan_idx_right)
         # Ensure the block found is indeed adjacent (starts right after the zeros)
        if block_digit_right is not None and block_start_idx_right == idx2 + num_zeros_right + 1:
            # Perform the move: Move zeros from [idx2+1, block_start-1] to after block_end
            segment_before_2 = grid[:idx2 + 1] # Includes the '2'
            moved_zeros = grid[idx2 + 1 : block_start_idx_right]
            the_block = grid[block_start_idx_right : block_end_idx_right + 1]
            segment_after_block = grid[block_end_idx_right + 1:]

            # Reconstruct the grid
            new_grid = segment_before_2 + the_block + moved_zeros + segment_after_block
            return " ".join(map(str, new_grid))

    # If no changes were made on either side, return the original string
    return input_str

```
```python
import sys
import math
# No special imports seem necessary for this logic

"""
Transformation Rule Natural Language Description:

1.  Receive the input sequence of digits as a space-separated string.
2.  Find the index (`idx2`) of the digit `2`.
3.  Check Left:
    a.  Scan leftwards from `idx2 - 1` counting consecutive `0`s (`zeros_left_count`).
    b.  If `zeros_left_count > 0`, check if the digit immediately preceding these zeros (`grid[idx2 - zeros_left_count - 1]`) is non-zero (`block_digit`).
    c.  If a non-zero `block_digit` is found, identify the full contiguous block of this digit ending at that position (`block_start_idx`, `block_end_idx`).
    d.  If the full pattern (Block - Zeros - 2) is confirmed, reconstruct the sequence: (elements before block) + (zeros) + (block) + (2 and elements after). Return the result as a space-separated string.
4.  Check Right (only if no change was made in step 3):
    a.  Scan rightwards from `idx2 + 1` counting consecutive `0`s (`zeros_right_count`).
    b.  If `zeros_right_count > 0`, check if the digit immediately following these zeros (`grid[idx2 + zeros_right_count + 1]`) is non-zero (`block_digit`).
    c.  If a non-zero `block_digit` is found, identify the full contiguous block of this digit starting at that position (`block_start_idx`, `block_end_idx`).
    d.  If the full pattern (2 - Zeros - Block) is confirmed, reconstruct the sequence: (elements before 2, including 2) + (block) + (zeros) + (elements after block). Return the result as a space-separated string.
5.  If no changes were made in steps 3 or 4, return the original input string.
"""

def find_block_left(grid, end_idx):
    """
    Finds a contiguous block of identical non-zero digits ending at end_idx.
    Returns the block's digit, start index, and end index, or None if no such block exists
    or if the digit at end_idx is zero.
    """
    if end_idx < 0 or grid[end_idx] == 0:
        return None, -1, -1

    block_digit = grid[end_idx]
    block_end_idx = end_idx
    block_start_idx = block_end_idx
    # Scan left to find the start of the block
    while block_start_idx > 0 and grid[block_start_idx - 1] == block_digit:
        block_start_idx -= 1
    return block_digit, block_start_idx, block_end_idx

def find_block_right(grid, start_idx):
    """
    Finds a contiguous block of identical non-zero digits starting at start_idx.
    Returns the block's digit, start index, and end index, or None if no such block exists
    or if the digit at start_idx is zero.
    """
    n = len(grid)
    if start_idx >= n or grid[start_idx] == 0:
        return None, -1, -1

    block_digit = grid[start_idx]
    block_start_idx = start_idx
    block_end_idx = block_start_idx
    # Scan right to find the end of the block
    while block_end_idx < n - 1 and grid[block_end_idx + 1] == block_digit:
        block_end_idx += 1
    return block_digit, block_start_idx, block_end_idx


def transform(input_str):
    """
    Applies the transformation rule to the input sequence string.
    """
    # Parse input string into a list of integers
    # Assuming input is a space-separated string of digits.
    # If input_str is actually already a list/array, this line needs adjustment.
    try:
        grid = [int(d) for d in input_str.split()]
    except AttributeError:
         # If input is not a string (e.g., numpy array passed by test harness)
         # try converting elements to int directly.
         # This handles the error seen previously.
         grid = [int(d) for d in input_str]
         
    n = len(grid)
    output_grid = list(grid) # Make a copy to modify potentially

    # --- Find the marker '2' ---
    try:
        idx2 = grid.index(2)
    except ValueError:
        # '2' not found, return original string representation
        return " ".join(map(str, grid))

    # --- Check Left Side ---
    zeros_left_count = 0
    scan_idx = idx2 - 1
    # Scan leftwards for zeros immediately preceding '2'
    while scan_idx >= 0 and grid[scan_idx] == 0:
        zeros_left_count += 1
        scan_idx -= 1

    # If zeros were found, check for an adjacent non-zero block to their left
    if zeros_left_count > 0:
        block_end_check_idx = idx2 - zeros_left_count - 1
        if block_end_check_idx >= 0: # Ensure there's space for a block
             block_digit, block_start_idx, block_end_idx = find_block_left(grid, block_end_check_idx)
             # Check if a valid block was found ending exactly where expected
             if block_digit is not None and block_end_idx == block_end_check_idx:
                # Perform the move: (elements before block) + (zeros) + (block) + (2 and elements after)
                segment_before_block = grid[:block_start_idx]
                moved_zeros = grid[block_end_idx + 1 : idx2] # The zeros found
                the_block = grid[block_start_idx : block_end_idx + 1]
                segment_from_2_onwards = grid[idx2:] # Includes the '2'

                # Reconstruct the grid
                output_grid = segment_before_block + moved_zeros + the_block + segment_from_2_onwards
                return " ".join(map(str, output_grid)) # Return transformed result

    # --- Check Right Side (only if no change was made on the left) ---
    zeros_right_count = 0
    scan_idx = idx2 + 1
    # Scan rightwards for zeros immediately following '2'
    while scan_idx < n and grid[scan_idx] == 0:
        zeros_right_count += 1
        scan_idx += 1

    # If zeros were found, check for an adjacent non-zero block to their right
    if zeros_right_count > 0:
        block_start_check_idx = idx2 + zeros_right_count + 1
        if block_start_check_idx < n: # Ensure there's space for a block
            block_digit, block_start_idx, block_end_idx = find_block_right(grid, block_start_check_idx)
            # Check if a valid block was found starting exactly where expected
            if block_digit is not None and block_start_idx == block_start_check_idx:
                 # Perform the move: (elements before 2, including 2) + (block) + (zeros) + (elements after block)
                 segment_up_to_2 = grid[:idx2 + 1] # Includes the '2'
                 moved_zeros = grid[idx2 + 1 : block_start_idx] # The zeros found
                 the_block = grid[block_start_idx : block_end_idx + 1]
                 segment_after_block = grid[block_end_idx + 1:]

                 # Reconstruct the grid
                 output_grid = segment_up_to_2 + the_block + moved_zeros + segment_after_block
                 return " ".join(map(str, output_grid)) # Return transformed result

    # If no changes were made on either side, return the original grid as a string
    return " ".join(map(str, grid))
```
