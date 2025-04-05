
## train_1

**input:**
```
0 0 2 0 0 0 0 4 4 4 4 0
```


**output:**
```
0 0 2 4 4 4 4 0 0 0 0 0
```


## train_2

**input:**
```
2 0 0 0 0 7 7 7 7 7 7 0
```


**output:**
```
2 7 7 7 7 7 7 0 0 0 0 0
```


## train_3

**input:**
```
0 2 0 0 3 3 3 3 3 3 0 0
```


**output:**
```
0 2 3 3 3 3 3 3 0 0 0 0
```


## train_4

**input:**
```
0 2 0 0 0 0 0 0 3 3 3 3
```


**output:**
```
0 2 0 0 3 3 3 3 0 0 0 0
```


## train_5

**input:**
```
2 7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
2 7 7 7 7 7 7 7 7 7 7 7
```


## train_6

**input:**
```
9 9 9 9 9 9 2 0 0 0 0 0
```


**output:**
```
9 9 9 9 9 9 2 0 0 0 0 0
```


## train_7

**input:**
```
0 2 0 1 1 1 1 1 1 1 0 0
```


**output:**
```
0 2 1 1 1 1 1 1 1 0 0 0
```

Okay, let's break down the transformation logic for this task.

## Perception

1.  **Input/Output Format:** Both input and output are sequences of 12 single-digit integers.
2.  **Key Elements:** The sequences consist of zeros and non-zero digits. A significant feature appears to be contiguous blocks of identical non-zero digits.
3.  **Core Transformation:** The primary action involves relocating a specific block of identical non-zero digits. This block seems to "slide" leftwards, moving over some or all of the zeros that immediately precede it. The zeros that are "overwritten" by the sliding block are then moved to the end of the sequence.
4.  **Trigger Condition:** This transformation seems contingent on finding a non-zero digit, followed by one or more zeros, followed by a block of identical non-zero digits. If this pattern doesn't exist, or if there are no zeros between the initial non-zero digit and the block, the sequence remains unchanged.
5.  **Shift Amount:** The distance the block shifts left seems limited by either the number of preceding zeros or the length of the block itself, whichever is smaller.

## Facts


```yaml
Objects:
  - Sequence:
      Properties:
        - A list of 12 single-digit integers.
        - Contains Digits.
  - Digit:
      Properties:
        - Value (0-9).
        - Position (index in the sequence).
      Types:
        - ZeroDigit (Value is 0).
        - NonZeroDigit (Value is 1-9).
  - Block:
      Properties:
        - A contiguous sub-sequence of identical NonZeroDigits.
        - StartPosition (index of the first digit).
        - EndPosition (index of the last digit).
        - Length (number of digits in the block).
        - DigitValue (the repeated non-zero digit).
  - AnchorDigit:
      Properties:
        - The first NonZeroDigit encountered before a potential Block, when scanning left-to-right.
        - Must be followed by at least one ZeroDigit before the Block starts.
  - PrecedingZeros:
      Properties:
        - A contiguous sub-sequence of ZeroDigits.
        - Located between an AnchorDigit and a Block.
        - Count (number of zeros).

Relationships:
  - An AnchorDigit *precedes* PrecedingZeros.
  - PrecedingZeros *precede* a Block.
  - The transformation *acts upon* the first occurrence of the AnchorDigit -> PrecedingZeros -> Block pattern.

Action:
  - Identify: Find the first AnchorDigit, the subsequent PrecedingZeros, and the immediately following Block.
  - Calculate Shift: Determine the number of positions to shift (`shift_count`) as the minimum of the PrecedingZeros count and the Block length.
  - Conditional Execution: If `shift_count` is greater than 0:
      - Remove: Delete the `shift_count` ZeroDigits immediately before the Block.
      - Relocate: Move the entire Block `shift_count` positions to the left.
      - Append: Add `shift_count` ZeroDigits to the very end of the Sequence.
  - No Action: If no AnchorDigit -> PrecedingZeros -> Block pattern is found, or if `shift_count` is 0, the Sequence remains unchanged.

```


## Natural Language Program

1.  Parse the input string into a list of integers.
2.  Iterate through the list to find the first instance of the following pattern:
    *   A non-zero digit (the "anchor").
    *   Followed immediately by one or more zeros (the "preceding zeros").
    *   Followed immediately by a contiguous block of identical non-zero digits (the "moving block").
3.  If this pattern is not found, return the original list.
4.  If the pattern is found:
    *   Record the index of the anchor digit.
    *   Count the number of preceding zeros (`zero_count`).
    *   Record the starting index of the moving block.
    *   Determine the length of the moving block (`block_length`).
    *   Record the value of the digit in the moving block.
5.  Calculate the number of positions to shift the block left (`shift_amount`) as the minimum of `zero_count` and `block_length`.
6.  If `shift_amount` is 0, return the original list.
7.  If `shift_amount` > 0:
    *   Create a new list.
    *   Copy elements from the original list up to (but not including) the first preceding zero that will be removed.
    *   Append the digits of the moving block to the new list.
    *   Append any remaining digits from the original list that were *after* the moving block.
    *   Append `shift_amount` zeros to the end of the new list.
8.  Return the modified list.
9.  Format the final list back into a space-separated string for the output.
```python
import math
import collections

"""
Transformation Rule:

The transformation operates on a sequence of 12 single-digit integers.
It searches for the first occurrence of a specific pattern: a non-zero digit (anchor), 
followed immediately by one or more zeros, followed immediately by a contiguous block 
of identical non-zero digits (moving block).

If this pattern is found, the moving block shifts leftwards, overwriting some of the 
preceding zeros. The number of positions shifted (`shift_amount`) is the minimum of 
the count of preceding zeros and the length of the moving block. The zeros that were 
overwritten by the shift are moved to the end of the sequence.

If the pattern is not found, or if the calculated `shift_amount` is zero (meaning 
there are no zeros between the anchor and the block, or the block has length zero, 
which shouldn't happen with non-zero blocks), the sequence remains unchanged.
"""

def parse_input(input_str: str) -> list[int]:
    """Converts the space-separated string input into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output(grid: list[int]) -> str:
    """Converts the list of integers back into a space-separated string."""
    return " ".join(map(str, grid))

def find_pattern(grid: list[int]):
    """
    Finds the first occurrence of the anchor -> zeros -> block pattern.

    Returns:
        A dictionary containing pattern details 
        {'anchor_index', 'zero_count', 'block_start', 'block_length', 'block_value'} 
        if found, otherwise None.
    """
    n = len(grid)
    i = 0
    while i < n:
        # 1. Find a potential anchor (non-zero digit)
        if grid[i] != 0:
            anchor_index = i
            
            # 2. Look for preceding zeros immediately after the anchor
            j = i + 1
            if j < n and grid[j] == 0:
                zero_start = j
                while j < n and grid[j] == 0:
                    j += 1
                zero_count = j - zero_start

                # 3. Look for a block of identical non-zero digits immediately after the zeros
                if j < n and grid[j] != 0:
                    block_start = j
                    block_value = grid[j]
                    k = j + 1
                    while k < n and grid[k] == block_value:
                        k += 1
                    block_length = k - block_start
                    
                    # Pattern found!
                    return {
                        "anchor_index": anchor_index,
                        "zero_count": zero_count,
                        "block_start": block_start,
                        "block_length": block_length,
                        "block_value": block_value,
                    }
                else:
                    # Zeros found, but no block afterwards. Continue search from end of zeros.
                    i = j 
            else:
                # Anchor found, but no zeros immediately after. Continue search from next position.
                i += 1
        else:
            # Current element is zero, continue search from next position.
            i += 1
            
    # Pattern not found after scanning the whole grid
    return None

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.
    """
    # Parse the input string into a list of integers
    grid = parse_input(input_str)
    n = len(grid)

    # Find the first occurrence of the anchor -> zeros -> block pattern
    pattern_info = find_pattern(grid)

    # If the pattern is not found, return the original grid formatted as a string
    if pattern_info is None:
        return format_output(grid)

    # Extract pattern details
    zero_count = pattern_info["zero_count"]
    block_start = pattern_info["block_start"]
    block_length = pattern_info["block_length"]
    block_value = pattern_info["block_value"]

    # Calculate the shift amount
    shift_amount = min(zero_count, block_length)

    # If shift_amount is 0, no transformation needed
    if shift_amount == 0:
         return format_output(grid)

    # Construct the new grid
    new_grid = []
    
    # Part before the removed zeros
    # The zeros to be removed start at index block_start - shift_amount
    new_grid.extend(grid[0 : block_start - shift_amount])
    
    # The moved block
    new_grid.extend([block_value] * block_length)
    
    # The part after the original block
    new_grid.extend(grid[block_start + block_length : n])
    
    # The zeros moved to the end
    new_grid.extend([0] * shift_amount)
    
    # Ensure the output grid has the correct length (should be handled by logic above)
    # assert len(new_grid) == n, f"Length mismatch: expected {n}, got {len(new_grid)}"

    # Format the final list back into a space-separated string for the output
    return format_output(new_grid)

```
```python
import math
import collections
import numpy as np # Import numpy to handle potential ndarray input

"""
Transformation Rule:

The transformation operates on a sequence (list or NumPy array) of 12 single-digit integers.
It searches for the first occurrence from the left of a specific pattern: 
1. A non-zero digit (the "anchor").
2. Immediately followed by one or more zero digits (the "preceding zeros").
3. Immediately followed by a contiguous block of identical non-zero digits (the "moving block").

If this pattern is found:
- Calculate the shift amount: `shift_amount = min(count of preceding zeros, length of moving block)`.
- If `shift_amount` is greater than 0:
    - Reconstruct the sequence:
        - Take the elements *before* the `shift_amount` zeros that immediately precede the block.
        - Append the *entire* moving block.
        - Append the elements that originally came *after* the moving block.
        - Append `shift_amount` zeros to the very end.
- If `shift_amount` is 0, the sequence remains unchanged.

If the pattern (anchor -> zeros -> block) is not found anywhere in the sequence, 
the sequence remains unchanged.

The final output should be a space-separated string of the digits in the potentially 
modified sequence.
"""

def find_first_pattern(grid: list[int]):
    """
    Finds the details of the first occurrence of the anchor -> zeros -> block pattern.

    Args:
        grid: The input list of integers.

    Returns:
        A dictionary containing pattern details:
        {'anchor_index', 'zero_start', 'zero_count', 
         'block_start', 'block_length', 'block_value'} 
        if a valid pattern is found, otherwise None.
    """
    n = len(grid)
    i = 0
    while i < n:
        # 1. Find a potential anchor (non-zero digit)
        if grid[i] != 0:
            anchor_index = i
            
            # 2. Look for preceding zeros immediately after the anchor
            j = i + 1
            if j < n and grid[j] == 0:
                zero_start = j
                # Find the end of the zero sequence
                while j < n and grid[j] == 0:
                    j += 1
                zero_count = j - zero_start # Should be > 0 because we checked grid[i+1]==0

                # 3. Look for a block of identical non-zero digits immediately after the zeros
                if j < n and grid[j] != 0:
                    block_start = j
                    block_value = grid[j]
                    k = j + 1
                    # Find the end of the block
                    while k < n and grid[k] == block_value:
                        k += 1
                    block_length = k - block_start # Will be at least 1

                    # Pattern found! Return its details
                    return {
                        "anchor_index": anchor_index,
                        "zero_start": zero_start,
                        "zero_count": zero_count,
                        "block_start": block_start,
                        "block_length": block_length,
                        "block_value": block_value,
                    }
                else:
                    # Zeros found, but no valid block afterwards. 
                    # Continue search *from the end of the zeros* to avoid re-checking.
                    i = j 
            else:
                # Anchor found, but no zeros immediately after. 
                # Continue search from the position *after* the anchor.
                i += 1
        else:
            # Current element is zero, continue search from the next position.
            i += 1
            
    # Pattern not found after scanning the whole grid
    return None

def format_output(grid: list[int]) -> str:
    """Converts the list of integers back into a space-separated string."""
    return " ".join(map(str, grid))

def transform(input_grid) -> str:
    """
    Applies the transformation rule to the input grid (list or NumPy array).
    """
    # Handle potential NumPy array input by converting to list
    if isinstance(input_grid, np.ndarray):
        grid = input_grid.tolist()
    else:
        # Assuming input is already a list-like structure (e.g., list)
        grid = list(input_grid) 
        
    n = len(grid)

    # Find the first occurrence of the anchor -> zeros -> block pattern
    pattern_info = find_first_pattern(grid)

    # If the pattern is not found, return the original grid formatted as a string
    if pattern_info is None:
        return format_output(grid)

    # Extract pattern details
    zero_count = pattern_info["zero_count"]
    block_start = pattern_info["block_start"]
    block_length = pattern_info["block_length"]
    block_value = pattern_info["block_value"]
    # zero_start is also block_start - zero_count

    # Calculate the number of positions to shift the block left
    shift_amount = min(zero_count, block_length)

    # If shift_amount is 0, no transformation is needed
    if shift_amount == 0:
         return format_output(grid)

    # Construct the new grid based on the transformation
    new_grid = []
    
    # Part 1: Elements before the zeros that get removed/overwritten.
    # The zeros to be removed start at index (block_start - shift_amount).
    prefix_end_index = block_start - shift_amount
    new_grid.extend(grid[0 : prefix_end_index])
    
    # Part 2: The moved block (append the entire block).
    new_grid.extend([block_value] * block_length)
    
    # Part 3: Elements that were originally *after* the block.
    suffix_start_index = block_start + block_length
    new_grid.extend(grid[suffix_start_index : n])
    
    # Part 4: The zeros that were shifted out, appended to the end.
    new_grid.extend([0] * shift_amount)
    
    # The new_grid should have the same length as the original.
    # No explicit length check needed if logic is correct, but useful for debugging:
    # assert len(new_grid) == n, f"Length mismatch: expected {n}, got {len(new_grid)}"

    # Format the final list back into a space-separated string for the output
    output_grid_str = format_output(new_grid)
    return output_grid_str
```
```python
import numpy as np
import math
import collections

"""
Transformation Rule:

The transformation operates on a sequence (list or NumPy array) of 12 single-digit integers.
It searches for the first occurrence from the left of a specific pattern: 
1. A non-zero digit (the "anchor").
2. Immediately followed by one or more zero digits (the "preceding zeros").
3. Immediately followed by a contiguous block of identical non-zero digits (the "moving block").

If this pattern is found:
- Calculate the shift amount: `shift_amount = min(count of preceding zeros, length of moving block)`.
- If `shift_amount` is greater than 0:
    - Reconstruct the sequence:
        - Take the elements *before* the `shift_amount` zeros that immediately precede the block.
        - Append the *entire* moving block.
        - Append the elements that originally came *after* the moving block.
        - Append `shift_amount` zeros to the very end.
- If `shift_amount` is 0, the sequence remains unchanged.

If the pattern (anchor -> zeros -> block) is not found anywhere in the sequence, 
the sequence remains unchanged.

The final output should be a space-separated string of the digits in the potentially 
modified sequence.
"""

def parse_input_string(input_str: str) -> list[int]:
    """Converts a space-separated string input into a list of integers."""
    try:
        return [int(digit) for digit in input_str.split()]
    except ValueError:
        # Handle cases where the string might not be directly splittable/convertible
        # This might happen if the input is already list-like but as a string '[1, 2,..]'
        # A more robust parser might be needed depending on actual error source.
        # For now, re-raise or return an empty list/error indicator.
        raise ValueError(f"Could not parse input string: {input_str}")


def find_first_pattern(grid: list[int]):
    """
    Finds the details of the first occurrence of the anchor -> zeros -> block pattern.

    Args:
        grid: The input list of integers.

    Returns:
        A dictionary containing pattern details:
        {'anchor_index', 'zero_start', 'zero_count', 
         'block_start', 'block_length', 'block_value'} 
        if a valid pattern is found, otherwise None.
    """
    n = len(grid)
    i = 0
    while i < n:
        # 1. Find a potential anchor (non-zero digit)
        if grid[i] != 0:
            anchor_index = i
            
            # 2. Look for preceding zeros immediately after the anchor
            j = i + 1
            if j < n and grid[j] == 0:
                zero_start = j
                # Find the end of the zero sequence
                while j < n and grid[j] == 0:
                    j += 1
                zero_count = j - zero_start # Should be > 0 because we checked grid[i+1]==0

                # 3. Look for a block of identical non-zero digits immediately after the zeros
                if j < n and grid[j] != 0:
                    block_start = j
                    block_value = grid[j]
                    k = j + 1
                    # Find the end of the block
                    while k < n and grid[k] == block_value:
                        k += 1
                    block_length = k - block_start # Will be at least 1

                    # Pattern found! Return its details
                    return {
                        "anchor_index": anchor_index,
                        "zero_start": zero_start,
                        "zero_count": zero_count,
                        "block_start": block_start,
                        "block_length": block_length,
                        "block_value": block_value,
                    }
                else:
                    # Zeros found, but no valid block afterwards. 
                    # Continue search *from the end of the zeros* to avoid re-checking.
                    i = j 
            else:
                # Anchor found, but no zeros immediately after. 
                # Continue search from the position *after* the anchor.
                i += 1
        else:
            # Current element is zero, continue search from the next position.
            i += 1
            
    # Pattern not found after scanning the whole grid
    return None

def format_output(grid: list[int]) -> str:
    """Converts the list of integers back into a space-separated string."""
    return " ".join(map(str, grid))

def transform(input_grid) -> str:
    """
    Applies the transformation rule to the input grid.
    """
    # Input Processing: Handle string, list, or numpy array input
    if isinstance(input_grid, str):
        grid = parse_input_string(input_grid)
    elif isinstance(input_grid, np.ndarray):
        grid = input_grid.tolist()
    else:
        # Assume input is already list-like (e.g., list, tuple)
        grid = list(input_grid) 
        
    n = len(grid)

    # Pattern Search: Find the first occurrence of the anchor -> zeros -> block pattern
    pattern_info = find_first_pattern(grid)

    # Conditional Transformation:
    # If the pattern is not found, return the original grid formatted as a string
    if pattern_info is None:
        return format_output(grid)

    # Extract pattern details
    zero_count = pattern_info["zero_count"]
    block_start = pattern_info["block_start"]
    block_length = pattern_info["block_length"]
    block_value = pattern_info["block_value"]

    # Calculate the shift amount
    shift_amount = min(zero_count, block_length)

    # If shift_amount is 0, no transformation is needed
    if shift_amount == 0:
         return format_output(grid)

    # Construct the new grid based on the transformation
    new_grid = []
    
    # Part 1: Elements before the zeros that get removed/overwritten.
    # The zeros to be removed start at index (block_start - shift_amount).
    prefix_end_index = block_start - shift_amount
    new_grid.extend(grid[0 : prefix_end_index])
    
    # Part 2: The moved block (append the entire block).
    new_grid.extend([block_value] * block_length)
    
    # Part 3: Elements that were originally *after* the block.
    suffix_start_index = block_start + block_length
    new_grid.extend(grid[suffix_start_index : n])
    
    # Part 4: The zeros that were shifted out, appended to the end.
    new_grid.extend([0] * shift_amount)

    # Output Formatting: Format the final list back into a space-separated string
    output_grid_str = format_output(new_grid)
    
    return output_grid_str
```
