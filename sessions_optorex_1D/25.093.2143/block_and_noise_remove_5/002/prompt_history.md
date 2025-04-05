
## train_1

**input:**
```
0 0 8 0 0 0 8 8 8 0 0 8
```


**output:**
```
0 0 0 0 0 0 8 8 8 0 0 0
```


## train_2

**input:**
```
7 7 7 0 0 0 7 0 0 0 0 7
```


**output:**
```
7 7 7 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 5 5 5 0 5 0 5 0 0 0 5
```


**output:**
```
0 5 5 5 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 6 0 0 6 0 0 0 6 6 0 6
```


**output:**
```
0 0 0 0 0 0 0 0 6 6 0 0
```


## train_5

**input:**
```
0 0 9 9 9 9 9 0 9 0 9 0
```


**output:**
```
0 0 9 9 9 9 9 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 8 0 8 0 8 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 8 8 0 0
```


## train_7

**input:**
```
4 4 4 0 0 0 0 0 4 0 0 0
```


**output:**
```
4 4 4 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output are sequences of single-digit integers.
    *   The length of the input sequence is preserved in the output sequence.
    *   The core operation involves identifying contiguous blocks (sequences) of identical non-zero digits within the input.
    *   A selection process occurs based on the length of these blocks. Specifically, the longest block of identical non-zero digits seems to be preserved.
    *   If there are multiple blocks of the same maximum length, the block that appears latest (furthest to the right) in the sequence is the one preserved.
    *   All digits in the input sequence that are not part of the selected block (including zeros and digits from other non-selected blocks) are replaced with '0' in the output sequence.

*   **YAML Facts:**
    
```yaml
    objects:
      - sequence:
          description: A list of single-digit integers.
          properties:
            - length: The number of digits in the sequence.
            - digits: The individual integer elements.
      - block:
          description: A contiguous subsequence of identical non-zero digits within the main sequence.
          properties:
            - digit_value: The non-zero integer that makes up the block.
            - length: The number of digits in the block.
            - start_index: The index of the first digit of the block in the main sequence.
            - end_index: The index of the last digit of the block in the main sequence.
    actions:
      - identify_blocks:
          description: Scan the input sequence to find all contiguous blocks of identical non-zero digits.
          inputs: input_sequence
          outputs: list_of_blocks
      - find_max_length:
          description: Determine the maximum length among all identified blocks.
          inputs: list_of_blocks
          outputs: max_length
      - filter_by_max_length:
          description: Select blocks that have the maximum length.
          inputs: list_of_blocks, max_length
          outputs: list_of_longest_blocks
      - select_last_block:
          description: If multiple blocks have the maximum length, choose the one with the highest start_index.
          inputs: list_of_longest_blocks
          outputs: selected_block
      - generate_output:
          description: Create the output sequence by placing the selected block's digits at the correct indices and filling the rest with zeros.
          inputs: input_sequence_length, selected_block
          outputs: output_sequence
    relationships:
      - comparison: Block lengths are compared to find the maximum.
      - position: Block start indices are compared to select the last block in case of ties in length.
      - inclusion: The selected block is a part of the original input sequence and determines a part of the output sequence.
    ```


*   **Natural Language Program:**
    1.  Initialize an empty list to store information about contiguous blocks of identical non-zero digits found in the input sequence.
    2.  Iterate through the input sequence, identifying the start index, end index, digit value, and length of each contiguous block of identical non-zero digits. Store this information for each block found.
    3.  If no non-zero blocks are found, create an output sequence of the same length as the input, filled entirely with zeros, and return it.
    4.  Determine the maximum length among all the identified blocks.
    5.  Filter the list of blocks, keeping only those whose length equals the maximum length found in the previous step.
    6.  From the filtered list of longest blocks, select the block with the largest start index (the one occurring latest in the input sequence). This is the `selected_block`.
    7.  Create a new sequence (the output sequence) of the same length as the input sequence, initially filled with zeros.
    8.  Iterate from the `start_index` to the `end_index` (inclusive) of the `selected_block`. For each index in this range, set the corresponding element in the output sequence to the `digit_value` of the `selected_block`.
    9.  Return the generated output sequence.
```python
import math
import re

"""
Identify all contiguous blocks of identical non-zero digits in the input sequence. 
Find the maximum length among these blocks. Select the block(s) with this maximum length. 
If there are multiple blocks with the maximum length, choose the one that appears latest (furthest to the right, i.e., highest start index) in the sequence. 
Create an output sequence of the same length as the input, initially filled with zeros. 
Place the digits of the selected block at their original positions in the output sequence. 
All other positions remain zero.
"""

def _find_blocks(sequence):
    """
    Finds all contiguous blocks of identical non-zero digits.

    Args:
        sequence: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'digit_value', 'start_index', 'end_index', and 'length'.
        Returns an empty list if no non-zero blocks are found.
    """
    blocks = []
    if not sequence:
        return blocks

    current_digit = None
    start_index = -1
    length = 0

    for i, digit in enumerate(sequence):
        if digit != 0:
            if digit == current_digit:
                # Continue existing block
                length += 1
            else:
                # End previous block if it existed and was non-zero
                if current_digit is not None and current_digit != 0:
                    blocks.append({
                        'digit_value': current_digit,
                        'start_index': start_index,
                        'end_index': i - 1,
                        'length': length
                    })
                # Start new block
                current_digit = digit
                start_index = i
                length = 1
        else:
            # End previous block if it existed and was non-zero
            if current_digit is not None and current_digit != 0:
                 blocks.append({
                    'digit_value': current_digit,
                    'start_index': start_index,
                    'end_index': i - 1,
                    'length': length
                })
            # Reset block tracking
            current_digit = None
            start_index = -1
            length = 0

    # Handle the last block if it was non-zero and went to the end
    if current_digit is not None and current_digit != 0:
        blocks.append({
            'digit_value': current_digit,
            'start_index': start_index,
            'end_index': len(sequence) - 1,
            'length': length
        })

    return blocks


def transform(input_str):
    """
    Transforms the input sequence string based on the rule:
    Keep only the latest occurring longest contiguous block of identical non-zero digits,
    replacing everything else with zeros.

    Args:
        input_str: A string of space-separated single-digit integers.

    Returns:
        A string of space-separated single-digit integers representing the transformed sequence.
    """
    # Parse input string into a list of integers
    input_sequence = [int(d) for d in input_str.split()]
    n = len(input_sequence)

    # Initialize output sequence with zeros
    output_sequence = [0] * n

    # 1. & 2. Identify all contiguous blocks of identical non-zero digits
    blocks = _find_blocks(input_sequence)

    # 3. If no non-zero blocks are found, return the sequence of zeros
    if not blocks:
        return " ".join(map(str, output_sequence))

    # 4. Determine the maximum length among the identified blocks
    max_length = 0
    for block in blocks:
        if block['length'] > max_length:
            max_length = block['length']

    # 5. Filter the list of blocks to keep only those with the maximum length
    longest_blocks = [block for block in blocks if block['length'] == max_length]

    # 6. Select the block with the largest start index (latest occurring)
    selected_block = None
    max_start_index = -1
    for block in longest_blocks:
        if block['start_index'] > max_start_index:
            max_start_index = block['start_index']
            selected_block = block

    # 7. & 8. Create the output sequence using the selected block
    if selected_block:
        start = selected_block['start_index']
        end = selected_block['end_index']
        value = selected_block['digit_value']
        for i in range(start, end + 1):
            output_sequence[i] = value

    # 9. Return the generated output sequence as a string
    return " ".join(map(str, output_sequence))
```
