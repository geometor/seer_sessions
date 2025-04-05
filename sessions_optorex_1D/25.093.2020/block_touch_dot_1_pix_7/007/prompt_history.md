
## train_1

**input:**
```
0 0 0 0 0 0 0 2 7 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 2 7 7 7 7
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 2 5
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 2 5
```


## train_3

**input:**
```
0 0 4 4 4 0 0 0 0 2 0 0
```


**output:**
```
0 0 0 4 4 4 0 0 0 2 0 0
```


## train_4

**input:**
```
2 0 0 0 0 0 0 0 0 3 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 3 0 0 0
```


## train_5

**input:**
```
0 2 0 0 0 0 1 1 1 0 0 0
```


**output:**
```
0 2 0 0 0 1 1 1 0 0 0 0
```


## train_6

**input:**
```
0 0 5 0 0 0 0 2 0 0 0 0
```


**output:**
```
0 0 0 5 0 0 0 2 0 0 0 0
```


## train_7

**input:**
```
0 4 4 4 4 4 4 4 4 0 2 0
```


**output:**
```
0 0 4 4 4 4 4 4 4 4 2 0
```

**Perception of the Elements:**

The task involves transforming a sequence of 12 integers based on specific rules.
1.  **Input/Output Format:** Both input and output are fixed-length sequences (arrays or lists) of 12 integers.
2.  **Key Element:** The integer '2' plays a crucial role in determining the transformation. Its position is important.
3.  **Other Non-Zero Elements:** Other non-zero integers often appear in contiguous blocks (e.g., `4 4 4`, `7 7 7 7`, `1 1 1`). The integer '0' acts as a background or filler.
4.  **Transformation:** The core transformation involves shifting these non-zero blocks (excluding '2') either one position to the left or one position to the right.
5.  **Condition for Shifting:** The direction of the shift depends on the block's position relative to the '2'. Blocks *before* the '2' shift right. Blocks *after* the '2' shift left.
6.  **Exception to Shifting:** Blocks that are immediately adjacent to the '2' (either directly before or directly after) do not shift.
7.  **Mechanism of Shifting:** When a block shifts, the position it vacates is filled with a '0'. The '2' itself does not move.

**Facts:**


```yaml
elements:
  - object: sequence
    description: A list of 12 integers representing the input and output state.
  - object: integer_2
    description: A specific integer '2' acting as a reference point within the sequence.
    properties:
      - position: The index of '2' in the sequence.
  - object: block
    description: A contiguous subsequence of one or more non-zero integers, excluding '2'.
    properties:
      - values: The integers comprising the block.
      - start_index: The starting index of the block in the sequence.
      - end_index: The ending index of the block in the sequence.
      - location_relative_to_2: Whether the block appears before or after '2' in the sequence.
      - adjacent_to_2: Whether the block is immediately next to '2' (no '0's in between).
  - object: integer_0
    description: The integer '0', often acting as a separator or filler.

actions:
  - action: find_integer_2
    description: Locate the index of the integer '2'.
  - action: identify_blocks
    description: Find all contiguous blocks of non-zero integers (not '2') in the sequence.
  - action: check_adjacency
    description: Determine if a block's start or end index is immediately adjacent to the index of '2'.
  - action: determine_relative_location
    description: Determine if a block's indices are all less than (before) or all greater than (after) the index of '2'.
  - action: shift_block_right
    description: Move all elements of a block one position to the right, filling the original start_index with '0'.
  - action: shift_block_left
    description: Move all elements of a block one position to the left, filling the original end_index with '0'.
  - action: copy_sequence
    description: Create a modifiable copy of the input sequence to build the output.

relationships:
  - relationship: shift_dependency
    description: The decision to shift a block and the direction of the shift depend on its adjacency and location relative to '2'.
    conditions:
      - if: block is adjacent_to_2 == true
        then: no shift occurs.
      - if: block is adjacent_to_2 == false AND location_relative_to_2 == before
        then: shift_block_right is performed.
      - if: block is adjacent_to_2 == false AND location_relative_to_2 == after
        then: shift_block_left is performed.
```


**Natural Language Program:**

1.  Create a copy of the input sequence to serve as the initial output sequence.
2.  Find the index (position) of the integer '2' in the input sequence.
3.  Identify all contiguous blocks of non-zero integers (where the integers are not '2') in the input sequence. For each block, record its start and end indices.
4.  Iterate through each identified block:
    a.  Check if the block is immediately adjacent to '2'. A block ending at index `position_of_2 - 1` or starting at index `position_of_2 + 1` is considered adjacent.
    b.  If the block is adjacent to '2', do nothing and proceed to the next block.
    c.  If the block is not adjacent to '2':
        i.  Determine if the block is located entirely *before* '2' (i.e., the block's end index is less than the position of '2').
        ii. If the block is before '2', shift the elements of this block in the *output sequence* one position to the right. Place a '0' in the original starting position (start index) of the block in the output sequence.
        iii. Determine if the block is located entirely *after* '2' (i.e., the block's start index is greater than the position of '2').
        iv. If the block is after '2', shift the elements of this block in the *output sequence* one position to the left. Place a '0' in the original ending position (end index) of the block in the output sequence.
5.  Return the modified output sequence.

*(Self-correction during thought process: Initially considered shifting based only on relative position, but examples 1 & 2 showed adjacency matters. Also clarified the shifting mechanism involves moving the block content and inserting a zero at the vacated end.)*
*(Self-correction 2: The program needs to operate on a copy of the input or apply changes carefully to avoid issues if multiple blocks shift. The description now specifies modifying an output sequence initialized from the input.)*
```python
import copy

def _find_integer_2(grid):
    """
    Finds the index of the first occurrence of the integer 2 in the grid.

    Args:
        grid: A list of integers.

    Returns:
        The index of the integer 2, or -1 if not found.
    """
    try:
        return grid.index(2)
    except ValueError:
        return -1

def _find_blocks(grid, index_of_2):
    """
    Finds contiguous blocks of non-zero integers (excluding the integer 2)
    in the grid.

    Args:
        grid: A list of integers.
        index_of_2: The index of the integer 2 in the grid.

    Returns:
        A list of tuples, where each tuple represents a block and contains
        its (start_index, end_index).
    """
    blocks = []
    n = len(grid)
    i = 0
    while i < n:
        # Start of a potential block: non-zero and not the '2' itself
        if grid[i] != 0 and i != index_of_2:
            start_index = i
            # Extend the block as long as elements are non-zero and not '2'
            while i + 1 < n and grid[i + 1] != 0 and (i + 1) != index_of_2:
                i += 1
            end_index = i
            blocks.append((start_index, end_index))
        i += 1
    return blocks

def transform(input_grid):
    """
    Transforms the input sequence based on the position of the integer '2'.
    Contiguous blocks of non-zero integers (excluding '2') are identified.
    Blocks located before '2' and not adjacent to it are shifted one position to the right.
    Blocks located after '2' and not adjacent to it are shifted one position to the left.
    The position vacated by a shift is filled with '0'. The integer '2' and blocks
    immediately adjacent to it remain unchanged.
    """
    # Create a modifiable copy of the input sequence
    output_grid = copy.deepcopy(input_grid)
    n = len(input_grid)

    # Find the index of the integer '2'
    index_of_2 = _find_integer_2(input_grid)

    # If '2' is not found, return the original grid (or handle as error)
    if index_of_2 == -1:
        return output_grid # Or raise ValueError("Integer 2 not found in input")

    # Identify all contiguous blocks of non-zero integers (not '2')
    # Store them with their original start and end indices
    blocks = _find_blocks(input_grid, index_of_2)

    # Iterate through each identified block and apply shifts if necessary
    for start_index, end_index in blocks:
        # Check if the block is immediately adjacent to '2'
        is_adjacent_before = (end_index == index_of_2 - 1)
        is_adjacent_after = (start_index == index_of_2 + 1)

        if is_adjacent_before or is_adjacent_after:
            # If adjacent, do nothing
            continue
        else:
            # Determine if the block is before or after '2'
            block_is_before_2 = (end_index < index_of_2)
            block_is_after_2 = (start_index > index_of_2)

            if block_is_before_2:
                # Shift the block one position to the right in the output_grid
                # Ensure we don't shift past the end of the grid
                if end_index + 1 < n:
                    # Extract block content from the *original* grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new position in output_grid
                    output_grid[start_index + 1 : end_index + 2] = block_content
                    # Set the original starting position to 0
                    output_grid[start_index] = 0
            elif block_is_after_2:
                # Shift the block one position to the left in the output_grid
                # Ensure we don't shift past the beginning of the grid
                if start_index - 1 >= 0:
                     # Extract block content from the *original* grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new position in output_grid
                    output_grid[start_index - 1 : end_index] = block_content
                    # Set the original ending position to 0
                    output_grid[end_index] = 0

    return output_grid
```
```python
import numpy as np
import copy

"""
Transforms an input sequence (1D NumPy array of 12 integers) based on the 
position of the integer '2'. Contiguous blocks of non-zero integers 
(excluding '2') are identified. Blocks located before '2' and not immediately 
adjacent to it are shifted one position to the right in a copy of the sequence. 
Blocks located after '2' and not immediately adjacent to it are shifted one 
position to the left. The position vacated by a shift (the original start for a 
right shift, the original end for a left shift) is filled with '0'. The integer 
'2' itself and any blocks immediately adjacent to it remain unchanged.
"""

def _find_integer_2(grid):
    """
    Finds the index of the first occurrence of the integer 2 in the grid.

    Args:
        grid: A 1D NumPy array of integers.

    Returns:
        The index of the integer 2, or -1 if not found.
    """
    indices = np.where(grid == 2)[0]
    if len(indices) > 0:
        return indices[0]
    else:
        return -1

def _find_blocks(grid, index_of_2):
    """
    Finds contiguous blocks of non-zero integers (excluding the integer 2)
    in the grid.

    Args:
        grid: A 1D NumPy array of integers.
        index_of_2: The index of the integer 2 in the grid.

    Returns:
        A list of tuples, where each tuple represents a block and contains
        its (start_index, end_index).
    """
    blocks = []
    n = len(grid)
    i = 0
    while i < n:
        # Start of a potential block: non-zero and not the '2' itself
        if grid[i] != 0 and i != index_of_2:
            start_index = i
            # Extend the block as long as elements are non-zero and not '2'
            while i + 1 < n and grid[i + 1] != 0 and (i + 1) != index_of_2:
                i += 1
            end_index = i
            blocks.append((start_index, end_index))
        i += 1
    return blocks

def transform(input_grid):
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid) # Convert if necessary

    # Create a modifiable copy of the input sequence
    output_grid = np.copy(input_grid)
    n = len(input_grid)

    # Find the index (position) of the integer '2'
    index_of_2 = _find_integer_2(input_grid)

    # If '2' is not found, return the original grid unmodified
    if index_of_2 == -1:
        return output_grid 

    # Identify all contiguous blocks of non-zero integers (not '2') in the *input* sequence
    blocks = _find_blocks(input_grid, index_of_2)

    # Iterate through each identified block and apply shifts if necessary
    for start_index, end_index in blocks:
        # Check if the block is immediately adjacent to '2'
        is_adjacent_before = (end_index == index_of_2 - 1)
        is_adjacent_after = (start_index == index_of_2 + 1)

        # If the block is adjacent, make no changes for this block
        if is_adjacent_before or is_adjacent_after:
            continue
        else:
            # Determine if the block is located entirely before '2'
            block_is_before_2 = (end_index < index_of_2)
            # Determine if the block is located entirely after '2'
            block_is_after_2 = (start_index > index_of_2)

            if block_is_before_2:
                # Check if shifting right is possible (within array bounds)
                if end_index + 1 < n:
                    # Extract block content from the *original* grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new position in *output_grid*
                    output_grid[start_index + 1 : end_index + 2] = block_content
                    # Set the original starting position to 0 in *output_grid*
                    output_grid[start_index] = 0
            elif block_is_after_2:
                # Check if shifting left is possible (within array bounds)
                if start_index - 1 >= 0:
                    # Extract block content from the *original* grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new position in *output_grid*
                    output_grid[start_index - 1 : end_index] = block_content
                    # Set the original ending position to 0 in *output_grid*
                    output_grid[end_index] = 0

    # Return the modified output sequence
    return output_grid
```
```python
import numpy as np
import copy

"""
Transforms an input sequence (1D NumPy array of 12 integers) based on the 
position of the integer '2'. Contiguous blocks of non-zero integers 
(excluding '2') are identified. Blocks located before '2' and not immediately 
adjacent to it are shifted one position to the right in a copy of the sequence. 
Blocks located after '2' and not immediately adjacent to it are shifted one 
position to the left. The position vacated by a shift (the original start for a 
right shift, the original end for a left shift) is filled with '0'. The integer 
'2' itself and any blocks immediately adjacent to it remain unchanged.
"""

def _find_integer_2(grid):
    """
    Finds the index of the first occurrence of the integer 2 in the grid.

    Args:
        grid: A 1D NumPy array of integers.

    Returns:
        The index of the integer 2, or -1 if not found.
    """
    # Use np.where to find indices where the value is 2
    indices = np.where(grid == 2)[0]
    # Return the first index if found, otherwise -1
    if len(indices) > 0:
        return indices[0]
    else:
        return -1

def _find_blocks(grid, index_of_2):
    """
    Finds contiguous blocks of non-zero integers (excluding the integer 2)
    in the grid. Uses standard Python iteration to avoid potential NumPy 
    boolean ambiguity errors in loop conditions.

    Args:
        grid: A 1D NumPy array of integers.
        index_of_2: The index of the integer 2 in the grid.

    Returns:
        A list of tuples, where each tuple represents a block and contains
        its (start_index, end_index).
    """
    blocks = []
    n = len(grid)
    i = 0
    while i < n:
        # Check if the current element is the start of a potential block
        # It must be non-zero and not be the marker '2'
        if grid[i] != 0 and i != index_of_2:
            start_index = i
            # Extend the block: move 'i' forward as long as elements 
            # are non-zero, not '2', and within bounds.
            # Check i+1 < n *before* accessing grid[i+1]
            while (i + 1 < n) and (grid[i + 1] != 0) and ((i + 1) != index_of_2):
                i += 1
            # The block ends at the current index 'i'
            end_index = i
            blocks.append((start_index, end_index))
        # Move to the next potential start position
        i += 1
    return blocks

def transform(input_grid):
    # Ensure input is a NumPy array for consistency
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int) 

    # Create a modifiable copy of the input sequence to store the output
    output_grid = np.copy(input_grid)
    n = len(input_grid) # Length of the sequence

    # Find the index (position) of the integer '2'
    index_of_2 = _find_integer_2(input_grid)

    # If '2' is not found, the transformation rules don't apply; return the original grid
    if index_of_2 == -1:
        return output_grid 

    # Identify all contiguous blocks of non-zero integers (not '2') in the *original input* sequence
    # This ensures shifts of one block don't affect the identification/position of others
    blocks = _find_blocks(input_grid, index_of_2)

    # Iterate through each identified block (defined by start and end index)
    for start_index, end_index in blocks:
        
        # Check if the block is immediately adjacent to '2'
        # Adjacent if it ends right before '2' OR starts right after '2'
        is_adjacent_before = (end_index == index_of_2 - 1)
        is_adjacent_after = (start_index == index_of_2 + 1)

        # If the block is adjacent, make no changes for this block; continue to the next block
        if is_adjacent_before or is_adjacent_after:
            continue
        else:
            # Block is not adjacent. Determine its relative location.
            # Check if the block is located entirely before '2'
            block_is_before_2 = (end_index < index_of_2)
            # Check if the block is located entirely after '2'
            block_is_after_2 = (start_index > index_of_2)

            if block_is_before_2:
                # Shift right if possible (check array bounds)
                if end_index + 1 < n:
                    # Extract block content from the *original* input grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new shifted position in the *output_grid*
                    output_grid[start_index + 1 : end_index + 2] = block_content
                    # Set the original starting position (vacated space) to 0 in the *output_grid*
                    output_grid[start_index] = 0
            elif block_is_after_2:
                # Shift left if possible (check array bounds)
                if start_index - 1 >= 0:
                    # Extract block content from the *original* input grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new shifted position in the *output_grid*
                    output_grid[start_index - 1 : end_index] = block_content
                    # Set the original ending position (vacated space) to 0 in the *output_grid*
                    output_grid[end_index] = 0

    # Return the final modified output sequence
    return output_grid
```

Previous Code:
```python
import numpy as np
import copy

"""
Transforms an input sequence (1D NumPy array of 12 integers) based on the 
position of the integer '2'. Contiguous blocks of non-zero integers 
(excluding '2') are identified. Blocks located before '2' and not immediately 
adjacent to it are shifted one position to the right in a copy of the sequence. 
Blocks located after '2' and not immediately adjacent to it are shifted one 
position to the left. The position vacated by a shift (the original start for a 
right shift, the original end for a left shift) is filled with '0'. The integer 
'2' itself and any blocks immediately adjacent to it remain unchanged.
"""

def _find_integer_2(grid):
    """
    Finds the index of the first occurrence of the integer 2 in the grid.

    Args:
        grid: A 1D NumPy array of integers.

    Returns:
        The index of the integer 2, or -1 if not found.
    """
    # Use np.where to find indices where the value is 2
    indices = np.where(grid == 2)[0]
    # Return the first index if found, otherwise -1
    if len(indices) > 0:
        return indices[0]
    else:
        return -1

def _find_blocks(grid, index_of_2):
    """
    Finds contiguous blocks of non-zero integers (excluding the integer 2)
    in the grid. Uses standard Python iteration to avoid potential NumPy 
    boolean ambiguity errors in loop conditions.

    Args:
        grid: A 1D NumPy array of integers.
        index_of_2: The index of the integer 2 in the grid.

    Returns:
        A list of tuples, where each tuple represents a block and contains
        its (start_index, end_index).
    """
    blocks = []
    n = len(grid)
    i = 0
    while i < n:
        # Check if the current element is the start of a potential block
        # It must be non-zero and not be the marker '2'
        if grid[i] != 0 and i != index_of_2:
            start_index = i
            # Extend the block: move 'i' forward as long as elements 
            # are non-zero, not '2', and within bounds.
            # Check i+1 < n *before* accessing grid[i+1]
            while (i + 1 < n) and (grid[i + 1] != 0) and ((i + 1) != index_of_2):
                i += 1
            # The block ends at the current index 'i'
            end_index = i
            blocks.append((start_index, end_index))
        # Move to the next potential start position
        i += 1
    return blocks

def transform(input_grid):
    # Ensure input is a NumPy array for consistency
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int) 

    # Create a modifiable copy of the input sequence to store the output
    output_grid = np.copy(input_grid)
    n = len(input_grid) # Length of the sequence

    # Find the index (position) of the integer '2'
    index_of_2 = _find_integer_2(input_grid)

    # If '2' is not found, the transformation rules don't apply; return the original grid
    if index_of_2 == -1:
        return output_grid 

    # Identify all contiguous blocks of non-zero integers (not '2') in the *original input* sequence
    # This ensures shifts of one block don't affect the identification/position of others
    blocks = _find_blocks(input_grid, index_of_2)

    # Iterate through each identified block (defined by start and end index)
    for start_index, end_index in blocks:
        
        # Check if the block is immediately adjacent to '2'
        # Adjacent if it ends right before '2' OR starts right after '2'
        is_adjacent_before = (end_index == index_of_2 - 1)
        is_adjacent_after = (start_index == index_of_2 + 1)

        # If the block is adjacent, make no changes for this block; continue to the next block
        if is_adjacent_before or is_adjacent_after:
            continue
        else:
            # Block is not adjacent. Determine its relative location.
            # Check if the block is located entirely before '2'
            block_is_before_2 = (end_index < index_of_2)
            # Check if the block is located entirely after '2'
            block_is_after_2 = (start_index > index_of_2)

            if block_is_before_2:
                # Shift right if possible (check array bounds)
                if end_index + 1 < n:
                    # Extract block content from the *original* input grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new shifted position in the *output_grid*
                    output_grid[start_index + 1 : end_index + 2] = block_content
                    # Set the original starting position (vacated space) to 0 in the *output_grid*
                    output_grid[start_index] = 0
            elif block_is_after_2:
                # Shift left if possible (check array bounds)
                if start_index - 1 >= 0:
                    # Extract block content from the *original* input grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new shifted position in the *output_grid*
                    output_grid[start_index - 1 : end_index] = block_content
                    # Set the original ending position (vacated space) to 0 in the *output_grid*
                    output_grid[end_index] = 0

    # Return the final modified output sequence
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 2:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 3:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 4:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 5:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 6:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 7:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

Test Set Results:

## Example 1:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
**General Assessment and Strategy**

The previous attempt correctly identified the core transformation logic: shifting blocks of non-zero integers (excluding '2') towards the position of '2', unless the block is immediately adjacent to '2'. The failure occurred during execution due to a NumPy-specific error ("The truth value of an array with more than one element is ambiguous"). This suggests an issue in how boolean conditions involving NumPy arrays were handled, likely within the `_find_blocks` helper function's loop, even though the intended logic appeared sound for 1D arrays.

The strategy is to:
1.  Re-confirm the transformation logic against all provided examples.
2.  Refine the description of objects, properties, and actions based on this confirmed logic.
3.  Rewrite the natural language program to be precise and unambiguous, emphasizing the conditions for shifting (non-adjacency and relative position) and the mechanism (copy, shift block, fill vacated space with 0).
4.  The subsequent coding phase should pay close attention to implementing the block finding and shifting logic, potentially using standard Python iteration instead of relying heavily on NumPy vectorization for the control flow aspects that caused the previous error, while still using NumPy for array handling if beneficial.

**Metrics**

Manual analysis confirms the logic across all training examples:

| Example | Input Sequence             | Output Sequence            | Index of '2' | Blocks Found (start, end) | Relative Pos | Adjacent | Action        | Output Matches? |
| :------ | :------------------------- | :------------------------- | :----------- | :------------------------ | :----------- | :------- | :------------ | :-------------- |
| train_1 | `[0 0 0 0 0 0 0 2 7 7 7 7]` | `[0 0 0 0 0 0 0 2 7 7 7 7]` | 7            | (8, 11)                   | After        | Yes      | None          | Yes             |
| train_2 | `[0 0 0 0 0 0 0 0 0 0 2 5]` | `[0 0 0 0 0 0 0 0 0 0 2 5]` | 10           | (11, 11)                  | After        | Yes      | None          | Yes             |
| train_3 | `[0 0 4 4 4 0 0 0 0 2 0 0]` | `[0 0 0 4 4 4 0 0 0 2 0 0]` | 9            | (2, 4)                    | Before       | No       | Shift Right   | Yes             |
| train_4 | `[2 0 0 0 0 0 0 0 0 3 0 0]` | `[2 0 0 0 0 0 0 0 3 0 0 0]` | 0            | (9, 9)                    | After        | No       | Shift Left    | Yes             |
| train_5 | `[0 2 0 0 0 0 1 1 1 0 0 0]` | `[0 2 0 0 0 1 1 1 0 0 0 0]` | 1            | (6, 8)                    | After        | No       | Shift Left    | Yes             |
| train_6 | `[0 0 5 0 0 0 0 2 0 0 0 0]` | `[0 0 0 5 0 0 0 2 0 0 0 0]` | 7            | (2, 2)                    | Before       | No       | Shift Right   | Yes             |
| train_7 | `[0 4 4 4 4 4 4 4 4 0 2 0]` | `[0 0 4 4 4 4 4 4 4 4 2 0]` | 10           | (1, 8)                    | Before       | No       | Shift Right   | Yes             |

**Facts**


```yaml
elements:
  - object: sequence
    description: A fixed-length list or 1D array of 12 integers representing the input and output state.
    properties:
      - length: Always 12.
      - values: Integers, including 0, 2, and others.
  - object: marker_2
    description: The integer '2', acting as a static reference point.
    properties:
      - position: The index (0-11) of '2' within the sequence. Assumed to appear at most once.
  - object: block
    description: A contiguous subsequence of one or more non-zero integers, excluding the marker '2'.
    properties:
      - values: The sequence of integers comprising the block.
      - start_index: The index of the first element of the block in the original input sequence.
      - end_index: The index of the last element of the block in the original input sequence.
      - location_relative_to_2: Whether the block appears entirely before (all indices < position of '2') or entirely after (all indices > position of '2') the marker_2.
      - is_adjacent_to_2: Boolean indicating if the block's end_index is `position_of_2 - 1` or its start_index is `position_of_2 + 1`.
  - object: integer_0
    description: The integer '0', acting as background/filler and used to replace vacated positions during shifts.

actions:
  - action: initialize_output
    description: Create a modifiable copy of the input sequence.
  - action: locate_marker_2
    description: Find the index of the integer '2' in the input sequence. Handle cases where '2' might be missing.
  - action: identify_blocks
    description: Iterate through the input sequence to find all contiguous blocks of non-zero integers (that are not '2'), recording their start and end indices.
  - action: evaluate_block_condition
    description: For each identified block, determine its location relative to '2' and whether it is adjacent to '2'.
  - action: shift_block_right
    description: If a block is before '2' and not adjacent, copy its elements one position to the right in the output sequence. Set the original start_index position in the output sequence to '0'. Check array bounds.
  - action: shift_block_left
    description: If a block is after '2' and not adjacent, copy its elements one position to the left in the output sequence. Set the original end_index position in the output sequence to '0'. Check array bounds.
  - action: no_shift
    description: If a block is adjacent to '2', make no changes related to this block in the output sequence.

relationships:
  - relationship: shift_logic
    description: The transformation applied to a block depends on its position relative to '2' and its adjacency.
    conditions:
      - if: block.is_adjacent_to_2 == true
        then: perform no_shift.
      - if: block.is_adjacent_to_2 == false AND block.location_relative_to_2 == before
        then: perform shift_block_right.
      - if: block.is_adjacent_to_2 == false AND block.location_relative_to_2 == after
        then: perform shift_block_left.
```


**Natural Language Program**

1.  Create an exact, modifiable copy of the input sequence; this will become the output sequence.
2.  Find the index (position) of the integer '2' in the original input sequence. If '2' is not present, return the unmodified copy.
3.  Identify all contiguous blocks of non-zero integers (excluding '2') in the *original input* sequence. For each block, record its starting and ending index.
4.  Iterate through the identified blocks based on their positions in the original input sequence. For each block:
    a.  Check if the block is immediately adjacent to '2'. Adjacency means the block ends exactly one position before '2' (at index `position_of_2 - 1`) or starts exactly one position after '2' (at index `position_of_2 + 1`).
    b.  If the block *is* adjacent to '2', do nothing to the output sequence for this block and proceed to the next block.
    c.  If the block is *not* adjacent to '2':
        i.  Determine if the block is located entirely *before* '2' (i.e., the block's end index is less than `position_of_2`).
        ii. If the block is before '2', shift its elements one position to the right *within the output sequence*. Specifically, copy the block's values from the input sequence (`input[start_index:end_index+1]`) into the output sequence at the new positions (`output[start_index+1:end_index+2]`). Then, set the element at the original starting position of the block (`output[start_index]`) to '0'. Ensure the shift does not go beyond the sequence bounds.
        iii. Determine if the block is located entirely *after* '2' (i.e., the block's start index is greater than `position_of_2`).
        iv. If the block is after '2', shift its elements one position to the left *within the output sequence*. Specifically, copy the block's values from the input sequence (`input[start_index:end_index+1]`) into the output sequence at the new positions (`output[start_index-1:end_index]`). Then, set the element at the original ending position of the block (`output[end_index]`) to '0'. Ensure the shift does not go beyond the sequence bounds.
5.  After processing all blocks, return the modified output sequence.
