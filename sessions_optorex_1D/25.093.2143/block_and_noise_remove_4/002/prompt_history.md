
## train_1

**input:**
```
9 0 0 0 0 0 9 9 9 9 9 9
```


**output:**
```
0 0 0 0 0 0 9 9 9 9 9 9
```


## train_2

**input:**
```
0 0 0 0 4 4 4 0 4 0 4 0
```


**output:**
```
0 0 0 0 4 4 4 0 0 0 0 0
```


## train_3

**input:**
```
0 9 0 0 9 0 0 9 9 9 0 9
```


**output:**
```
0 0 0 0 0 0 0 9 9 9 0 0
```


## train_4

**input:**
```
2 2 2 0 0 0 0 0 2 0 2 0
```


**output:**
```
2 2 2 0 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
2 2 2 2 0 0 0 0 0 2 0 0
```


**output:**
```
2 2 2 2 0 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 8 0 0 0 8 8 8 8 0 0 0
```


**output:**
```
0 0 0 0 0 8 8 8 8 0 0 0
```


## train_7

**input:**
```
1 0 1 1 1 1 1 1 1 1 0 0
```


**output:**
```
0 0 1 1 1 1 1 1 1 1 0 0
```

**Perception of Elements:**

The task involves transforming a sequence of single-digit integers into another sequence of the same length. The key elements are the integers themselves, specifically whether they are zero or non-zero, and their positions within the sequence. The transformation seems to operate based on identifying contiguous groups (or "blocks") of non-zero numbers within the input sequence. The length and position of these blocks appear crucial. The output retains only one specific block of non-zero numbers from the input, replacing all other elements with zeros.

**Facts:**


```yaml
Task: Sequence Transformation

Input:
  Type: List of integers
  Properties:
    - Contains single-digit integers (0-9)
    - Can contain zeros and non-zeros
    - Elements are ordered

Output:
  Type: List of integers
  Properties:
    - Same length as the input list
    - Derived from the input list

Core Objects:
  - Sequence: The input and output lists.
  - Element: Individual integer within a sequence.
  - Block: A contiguous subsequence of non-zero integers within the input sequence.
    Properties:
      - Start Index
      - End Index
      - Length (number of elements)
      - Elements (the actual non-zero integers)

Relationships & Actions:
  - Identification: The process identifies all contiguous blocks of non-zero numbers in the input sequence.
  - Comparison: The lengths of these blocks are compared.
  - Selection: The block with the maximum length is selected. If multiple blocks share the maximum length, the one occurring earliest (smallest start index) in the sequence is chosen. (Note: Although ties weren't explicitly tested with conflicting outcomes in the examples, selecting the first longest is a reasonable default assumption).
  - Transformation: An output sequence of the same length as the input is created, initially filled with zeros.
  - Preservation: The elements of the selected longest block are copied from the input sequence to their original positions in the output sequence. All other positions in the output sequence remain zero.
```


**Natural Language Program:**

1.  Examine the input sequence of integers.
2.  Identify all contiguous blocks (sequences) of non-zero integers. For each block, note its starting position, ending position, and length.
3.  Find the block that has the greatest length among all identified blocks. If there is a tie for the greatest length, select the block that appears earliest in the input sequence (i.e., the one with the smallest starting position).
4.  Create a new sequence of the same length as the input sequence, filled entirely with zeros.
5.  Copy the integers from the selected longest block (identified in step 3) into the corresponding positions (using the starting and ending positions noted in step 2) in the new sequence created in step 4.
6.  The resulting sequence is the output.
```python
import math
import collections

def find_nonzero_blocks(sequence):
    """
    Identifies contiguous blocks of non-zero numbers in a sequence.

    Args:
        sequence: A list of numbers.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'start', 'end', and 'length' keys.
        Returns an empty list if no non-zero blocks are found.
    """
    blocks = []
    start_index = -1
    for i, num in enumerate(sequence):
        if num != 0 and start_index == -1:
            # Start of a new block
            start_index = i
        elif (num == 0 or i == len(sequence) - 1) and start_index != -1:
            # End of the current block
            end_index = i if num != 0 else i - 1 # Adjust end index if last element is non-zero
            blocks.append({
                'start': start_index,
                'end': end_index,
                'length': end_index - start_index + 1
            })
            start_index = -1 # Reset for the next block
    return blocks

def select_longest_block(blocks):
    """
    Selects the longest block from a list of blocks.
    If there's a tie in length, selects the one with the smallest start index.

    Args:
        blocks: A list of block dictionaries (output from find_nonzero_blocks).

    Returns:
        The dictionary representing the selected block, or None if the input list is empty.
    """
    if not blocks:
        return None

    longest_block = blocks[0]
    max_length = blocks[0]['length']

    for block in blocks[1:]:
        if block['length'] > max_length:
            max_length = block['length']
            longest_block = block
        # Tie-breaking (smallest start index) is implicitly handled
        # because we only update if the current block is *strictly* longer.
        # If lengths are equal, the earlier block (with smaller index) remains selected.

    return longest_block


def transform(input_list):
    """
    Transforms the input sequence by identifying all contiguous blocks of non-zero
    integers, selecting the longest block (earliest one in case of a tie),
    and creating an output sequence containing only that block, with all other
    elements set to zero.
    """
    # 1. Identify all contiguous blocks of non-zero integers.
    blocks = find_nonzero_blocks(input_list)

    # 2. Find the block with the greatest length (earliest wins ties).
    selected_block = select_longest_block(blocks)

    # 3. Create a new sequence of the same length, filled with zeros.
    output_list = [0] * len(input_list)

    # 4. If a longest block was found, copy its elements to the output list.
    if selected_block:
        start = selected_block['start']
        end = selected_block['end']
        # Copy the elements from the selected block into the corresponding positions
        output_list[start : end + 1] = input_list[start : end + 1]

    # 5. Return the resulting sequence.
    return output_list
```
