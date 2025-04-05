
## train_1

**input:**
```
3 0 3 0 3 0 0 3 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 0 0 0
```


## train_2

**input:**
```
3 0 0 3 3 3 3 3 0 3 0 0
```


**output:**
```
0 0 0 3 3 3 3 3 0 0 0 0
```


## train_3

**input:**
```
0 5 5 0 5 0 0 0 5 0 5 0
```


**output:**
```
0 5 5 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 2 0 0 0 2 2 2 2 2 2 2
```


**output:**
```
0 0 0 0 0 2 2 2 2 2 2 2
```


## train_5

**input:**
```
0 4 4 4 4 4 4 4 4 4 0 4
```


**output:**
```
0 4 4 4 4 4 4 4 4 4 0 0
```


## train_6

**input:**
```
1 1 0 0 0 1 0 0 1 0 0 0
```


**output:**
```
1 1 0 0 0 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 6 0 0 6 0 6 0 0 0 6 6
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 6 6
```

Okay, let's break down the transformation.

**Perception of the Elements:**

1.  **Input/Output Data Type:** Both input and output are sequences (represented as space-separated strings) of single-digit non-negative integers.
2.  **Core Operation:** The transformation modifies the input sequence by selectively changing some non-zero numbers to zero. The positions of the zeros in the input generally seem to be preserved, unless a non-zero number at that position is changed to zero.
3.  **Key Pattern:** The transformation appears to operate on contiguous blocks (or runs) of identical non-zero numbers. For each unique non-zero number present in the input (e.g., '3' in `train_1`, '5' in `train_3`), the rule identifies all contiguous blocks of that number.
4.  **Filtering Logic:** Within the set of blocks for a specific number, the block with the maximum length is identified. Only the elements belonging to this longest block are retained in the output sequence. All other occurrences of that same number (belonging to shorter blocks) are replaced with 0.
5.  **Independence:** This process seems to be applied independently for each distinct non-zero value found in the input sequence.

**YAML Facts:**


```yaml
task_elements:
  - object: Sequence
    description: A list of single-digit integers.
    properties:
      - length: The number of elements in the sequence.
      - elements: The individual integers in the sequence.

  - object: Element
    description: A single integer within the sequence.
    properties:
      - value: The integer itself (0-9).
      - position: The index of the element in the sequence.

  - object: Block
    description: A contiguous sub-sequence of identical non-zero elements.
    properties:
      - value: The non-zero integer that makes up the block.
      - start_index: The position of the first element of the block.
      - end_index: The position of the last element of the block.
      - length: The number of elements in the block (end_index - start_index + 1).

relationships:
  - type: BelongsTo
    description: An Element belongs to a Sequence.
  - type: Forms
    description: Multiple contiguous Elements with the same non-zero value form a Block.

actions:
  - action: IdentifyBlocks
    description: For a given non-zero value N, find all contiguous Blocks of N within the input Sequence.
    inputs:
      - Sequence
      - N (non-zero integer value)
    outputs:
      - List of Blocks (each containing value, start_index, end_index, length)

  - action: FindLongestBlock
    description: From a list of Blocks for a specific value N, find the Block with the maximum length. (Assumes a unique longest block based on examples).
    inputs:
      - List of Blocks for value N
    outputs:
      - The single Block with the greatest length.

  - action: FilterSequence
    description: Create the output sequence by preserving elements belonging to the longest block for each non-zero value and replacing all other non-zero elements with 0.
    inputs:
      - Input Sequence
      - Set of longest Blocks (one for each unique non-zero value in the input)
    outputs:
      - Output Sequence
```


**Natural Language Program:**

1.  Initialize the output sequence as a copy of the input sequence.
2.  Identify all unique non-zero integer values present in the input sequence.
3.  For each unique non-zero value `N` identified:
    a.  Find all contiguous blocks (runs) of `N` within the input sequence. Record their start index, end index, and length.
    b.  If no blocks of `N` are found, continue to the next unique non-zero value.
    c.  Determine the maximum length among all found blocks of `N`.
    d.  Identify the specific block of `N` that has this maximum length. (Based on the examples, there appears to be only one such block for each `N`). Let this be the `longest_block`.
    e.  Iterate through all the originally found blocks of `N`. For every block that is *not* the `longest_block`:
        i.  Iterate through the indices from the block's start index to its end index.
        ii. Set the element at each of these indices in the *output* sequence to 0.
4.  Return the modified output sequence.
```python
import math
import collections

"""
Identify all unique non-zero integer values present in the input sequence.
For each unique non-zero value N:
  Find all contiguous blocks (runs) of N within the input sequence.
  Determine the maximum length among all found blocks of N.
  Identify the specific block of N that has this maximum length.
Create an output sequence initialized with zeros, having the same length as the input.
For each unique non-zero value N, if a longest block was found:
  Copy the value N into the output sequence at the indices corresponding to the longest block.
Return the resulting output sequence.
"""

def parse_input(input_str):
  """Converts a space-separated string of digits into a list of integers."""
  return [int(x) for x in input_str.split()]

def format_output(output_list):
  """Converts a list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def find_blocks(data, value):
  """Finds all contiguous blocks of a specific value in the data list.

  Args:
    data: A list of integers.
    value: The integer value to search for blocks of.

  Returns:
    A list of dictionaries, where each dictionary represents a block
    and contains 'value', 'start', 'end', and 'length'.
    Returns an empty list if the value is 0 or no blocks are found.
  """
  if value == 0:
    return []

  blocks = []
  start_index = -1
  for i, element in enumerate(data):
    if element == value:
      if start_index == -1:
        start_index = i  # Start of a potential block
    elif start_index != -1:
      # End of the block
      blocks.append({
          'value': value,
          'start': start_index,
          'end': i - 1,
          'length': (i - 1) - start_index + 1
      })
      start_index = -1 # Reset for the next block

  # Check if the last element was part of a block
  if start_index != -1:
    blocks.append({
        'value': value,
        'start': start_index,
        'end': len(data) - 1,
        'length': (len(data) - 1) - start_index + 1
    })

  return blocks

def find_longest_block(blocks):
  """Finds the block with the maximum length from a list of blocks.

  Args:
    blocks: A list of block dictionaries (from find_blocks).

  Returns:
    The block dictionary with the maximum length, or None if the list is empty.
    If multiple blocks share the max length, the first one encountered is returned.
  """
  if not blocks:
    return None
  return max(blocks, key=lambda b: b['length'])


def transform(input_str):
  """
  Transforms the input sequence by keeping only the longest contiguous block
  for each non-zero number present in the sequence. All other non-zero numbers
  are replaced with 0. Zeros in the input are preserved unless overwritten
  by a kept block element (which won't happen with this implementation).
  """
  # Parse the input string into a list of integers
  input_list = parse_input(input_str)
  n = len(input_list)

  # Initialize the output list with zeros
  output_list = [0] * n

  # Identify unique non-zero values in the input
  unique_non_zeros = sorted(list(set(val for val in input_list if val != 0)))

  # Process each unique non-zero value
  for value in unique_non_zeros:
    # Find all contiguous blocks of the current value
    current_blocks = find_blocks(input_list, value)

    # If blocks were found for this value
    if current_blocks:
      # Find the longest block among them
      longest = find_longest_block(current_blocks)

      # If a longest block exists (should always exist if current_blocks is not empty)
      if longest:
        # Copy the value into the output list at the indices of the longest block
        for i in range(longest['start'], longest['end'] + 1):
          output_list[i] = longest['value'] # Use value from block for clarity

  # Format the output list back into a space-separated string
  return format_output(output_list)

```
