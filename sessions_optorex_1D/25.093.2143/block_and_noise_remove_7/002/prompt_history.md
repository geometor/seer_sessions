
## train_1

**input:**
```
0 4 0 4 4 4 4 4 0 0 0 4
```


**output:**
```
0 0 0 4 4 4 4 4 0 0 0 0
```


## train_2

**input:**
```
1 1 1 1 1 1 1 1 1 1 0 1
```


**output:**
```
1 1 1 1 1 1 1 1 1 1 0 0
```


## train_3

**input:**
```
0 9 9 9 9 9 9 0 9 0 9 0
```


**output:**
```
0 9 9 9 9 9 9 0 0 0 0 0
```


## train_4

**input:**
```
0 0 9 9 9 9 9 9 0 0 0 9
```


**output:**
```
0 0 9 9 9 9 9 9 0 0 0 0
```


## train_5

**input:**
```
4 4 4 0 0 4 0 0 4 0 0 4
```


**output:**
```
4 4 4 0 0 0 0 0 0 0 0 0
```


## train_6

**input:**
```
7 0 0 7 0 0 7 7 0 0 7 0
```


**output:**
```
0 0 0 0 0 0 7 7 0 0 0 0
```


## train_7

**input:**
```
0 0 1 0 1 0 1 1 1 1 0 0
```


**output:**
```
0 0 0 0 0 0 1 1 1 1 0 0
```

*   **Perception of task elements**:
    *   The input and output are sequences (lists) of single-digit integers.
    *   The length of the output sequence is always the same as the length of the input sequence.
    *   The transformation rule appears to involve identifying contiguous blocks (subsequences) of identical non-zero numbers within the input sequence.
    *   Specifically, the rule focuses on the *longest* such block.
    *   The output sequence retains only this longest block of identical non-zero numbers, preserving its original value and position.
    *   All other elements in the output sequence are set to zero.
    *   If there are multiple blocks of the same maximum length, the examples suggest the one occurring earliest (minimum starting index) or latest (maximum starting index) might be chosen, but all examples provided have a unique longest block or the relative position doesn't matter for the outcome shown. Based on the examples, preserving the block at its original index seems key.

*   **YAML Facts**:
    
```yaml
    task_elements:
      - object: input_sequence
        properties:
          - type: list of integers
          - contains: single digits (0-9)
      - object: output_sequence
        properties:
          - type: list of integers
          - contains: single digits (0-9)
          - length: same as input_sequence
      - object: block
        properties:
          - type: contiguous sub-sequence within input_sequence
          - criteria: elements are identical and non-zero
          - attributes: value, length, start_index, end_index
      - object: zero
        properties:
          - value: 0
          - role: placeholder/replacement value
    relationships:
      - input_sequence transformed_to output_sequence
      - output_sequence derived_from input_sequence
    actions:
      - identify: all contiguous blocks of identical non-zero numbers in the input_sequence.
      - find: the block with the maximum length among those identified. (Assume uniqueness or a tie-breaking rule if necessary, though not explicit in examples).
      - create: an output sequence of the same length as the input, initially filled with zeros.
      - copy: the identified longest block from the input_sequence to the output_sequence, maintaining its original position (start and end indices).
    ```


*   **Natural Language Program**:
    1.  Examine the input sequence and identify all contiguous sub-sequences (blocks) where all elements are identical and greater than zero. Record the value, length, and starting index of each such block.
    2.  Determine the maximum length found among all identified blocks.
    3.  Select the block that has this maximum length. (If multiple blocks share the maximum length, assume the one with the smallest starting index is chosen, although the provided examples do not definitively test this tie-breaking scenario).
    4.  Create a new sequence of the same length as the input sequence, filled entirely with zeros.
    5.  If a longest block was identified in step 3, copy the elements of that block into the corresponding positions (using its original starting index and length) in the new sequence created in step 4.
    6.  The resulting sequence is the output.
```python
import collections

def find_blocks(sequence):
    """
    Identifies contiguous blocks of identical non-zero numbers in a sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'value', 'length', 'start_index', and 'end_index'.
        Returns an empty list if no non-zero blocks are found.
    """
    blocks = []
    if not sequence:
        return blocks

    current_block_val = None
    current_block_len = 0
    current_block_start = -1

    for i, val in enumerate(sequence):
        if val != 0:
            if val == current_block_val:
                # Continue existing block
                current_block_len += 1
            else:
                # End previous block (if it existed)
                if current_block_val is not None:
                    blocks.append({
                        'value': current_block_val,
                        'length': current_block_len,
                        'start_index': current_block_start,
                        'end_index': i - 1
                    })
                # Start new block
                current_block_val = val
                current_block_len = 1
                current_block_start = i
        else:
            # End previous block (if it existed)
            if current_block_val is not None:
                blocks.append({
                    'value': current_block_val,
                    'length': current_block_len,
                    'start_index': current_block_start,
                    'end_index': i - 1
                })
            # Reset block tracking
            current_block_val = None
            current_block_len = 0
            current_block_start = -1

    # Add the last block if the sequence ends with one
    if current_block_val is not None:
        blocks.append({
            'value': current_block_val,
            'length': current_block_len,
            'start_index': current_block_start,
            'end_index': len(sequence) - 1
        })

    return blocks

def find_longest_block(blocks):
    """
    Finds the longest block from a list of blocks.
    If there's a tie in length, selects the one with the smallest start index.

    Args:
        blocks: A list of block dictionaries as returned by find_blocks.

    Returns:
        The dictionary representing the longest block, or None if the list is empty.
    """
    if not blocks:
        return None

    longest_block = blocks[0]
    max_length = blocks[0]['length']

    for block in blocks[1:]:
        if block['length'] > max_length:
            max_length = block['length']
            longest_block = block
        elif block['length'] == max_length:
            # Tie-breaker: choose the one with the smaller start index
            if block['start_index'] < longest_block['start_index']:
                longest_block = block

    return longest_block

def transform(input_sequence):
    """
    Transforms the input sequence by identifying the longest contiguous block
    of identical non-zero numbers. The output sequence retains only this
    longest block at its original position, with all other elements set to zero.
    If multiple blocks share the maximum length, the one starting earliest
    (minimum start index) is chosen. If no non-zero blocks exist, the output
    is all zeros.
    """
    # Find all contiguous blocks of identical non-zero numbers
    blocks = find_blocks(input_sequence)

    # Determine the longest block (with tie-breaking for earliest start index)
    longest_block_info = find_longest_block(blocks)

    # Initialize the output sequence with zeros, same length as input
    output_sequence = [0] * len(input_sequence)

    # If a longest block was found, copy its elements into the output sequence
    if longest_block_info:
        start = longest_block_info['start_index']
        end = longest_block_info['end_index']
        value = longest_block_info['value']
        # Fill the corresponding segment in the output sequence
        for i in range(start, end + 1):
            output_sequence[i] = value

    return output_sequence
```
