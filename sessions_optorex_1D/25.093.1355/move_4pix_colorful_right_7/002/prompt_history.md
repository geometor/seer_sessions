
## train_1

**input:**
```
0 0 3 7 5 6 5 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 3 7 5 6 5 0
```


## train_2

**input:**
```
0 4 8 1 8 9 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 8 1 8 9 0 0
```


## train_3

**input:**
```
0 5 1 7 8 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 5 1 7 8 0 0 0
```


## train_4

**input:**
```
4 3 4 3 6 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 4 3 4 3 6 0 0 0
```


## train_5

**input:**
```
0 8 2 4 2 8 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 8 2 4 2 8 0 0
```


## train_6

**input:**
```
3 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 9 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 4
```

*   **Perception:** The task operates on fixed-length sequences of 12 integers. Each input sequence contains a single contiguous block of non-zero integers, surrounded by zeros. The transformation involves relocating this non-zero block within the sequence while preserving the block itself and the surrounding zeros. The core action is a rightward shift of the non-zero block by a fixed amount.

*   **Facts:**
    
```yaml
    task_type: sequence_manipulation
    input_type: list_of_integers
    output_type: list_of_integers
    sequence_length: 12
    elements:
      - type: zero
        role: padding/background
      - type: non_zero_block
        description: A contiguous subsequence of non-zero integers.
        properties:
          - content: the sequence of non-zero integers
          - start_index_input: the index where the block begins in the input
          - length: the number of elements in the block
    action:
      type: shift
      direction: right
      amount: 4
      target: non_zero_block
    relationship: The output sequence is constructed by taking the input sequence, identifying the non_zero_block, and placing it in a new sequence (initially all zeros) starting at `start_index_input + 4`. The relative order of elements within the non_zero_block is preserved.
    constraints: Assumes only one contiguous non-zero block exists in the input. Assumes the shifted block fits within the sequence length of 12.
    ```


*   **Natural Language Program:**
    1.  Initialize an output sequence of length 12 with all zeros.
    2.  Scan the input sequence to find the first non-zero integer. Record its index as `start_index`.
    3.  Continue scanning from `start_index` to find the end of the contiguous block of non-zero integers. Record this block of numbers as the `payload`.
    4.  Calculate the `target_start_index` by adding 4 to the `start_index`.
    5.  Place the `payload` into the output sequence, starting at the `target_start_index`.
    6.  Return the output sequence.
```python
"""
Transforms an input sequence of 12 integers by identifying a single contiguous block of non-zero integers and shifting this block 4 positions to the right, preserving the block's content and the surrounding zeros.

1. Initialize an output sequence of length 12 with all zeros.
2. Scan the input sequence to find the first non-zero integer. Record its index as `start_index`.
3. Continue scanning from `start_index` to find the end of the contiguous block of non-zero integers. Record this block of numbers as the `payload`.
4. Calculate the `target_start_index` by adding 4 to the `start_index`.
5. Place the `payload` into the output sequence, starting at the `target_start_index`.
6. Return the output sequence.
"""

import re # Using regex to easily find the non-zero block

def find_non_zero_block(input_list):
    """
    Finds the first contiguous block of non-zero integers in a list.

    Args:
        input_list: A list of integers.

    Returns:
        A tuple containing:
        - start_index: The starting index of the block (or -1 if not found).
        - payload: A list containing the non-zero integers in the block (or empty list if not found).
    """
    start_index = -1
    payload = []
    in_block = False
    for i, num in enumerate(input_list):
        if num != 0 and not in_block:
            start_index = i
            in_block = True
            payload.append(num)
        elif num != 0 and in_block:
            payload.append(num)
        elif num == 0 and in_block:
            # Found the end of the block
            break
        # Handle case where block goes to the end of the list implicitly
    if not payload: # Handle case of all zeros or no block found
        return -1, []
    return start_index, payload


def transform(input_str):
    """
    Applies the described transformation rule to the input string.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Parse input string into a list of integers
    input_list = [int(x) for x in input_str.strip().split()]
    n = len(input_list) # Should be 12 based on examples

    # 1. Initialize an output sequence of length 12 with all zeros.
    output_grid = [0] * n

    # 2. & 3. Find the start index and the payload (non-zero block)
    start_index, payload = find_non_zero_block(input_list)

    # Check if a block was found
    if start_index != -1:
        # 4. Calculate the target_start_index by adding 4 to the start_index.
        target_start_index = start_index + 4

        # 5. Place the payload into the output sequence, starting at the target_start_index.
        # Ensure the placement doesn't go out of bounds (though examples suggest it fits)
        payload_len = len(payload)
        if target_start_index + payload_len <= n:
            for i in range(payload_len):
                output_grid[target_start_index + i] = payload[i]
        else:
            # Handle potential out-of-bounds placement if necessary,
            # though not observed in provided examples.
            # For now, place as much as fits, or raise an error, or wrap around?
            # Based on example 7, it seems it just shifts and fits within bounds.
            # Let's stick to direct placement assuming it fits.
             for i in range(payload_len):
                 if target_start_index + i < n:
                    output_grid[target_start_index + i] = payload[i]


    # 6. Return the output sequence.
    return output_grid
```
