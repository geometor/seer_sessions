
## train_1

**input:**
```
0 0 0 0 2 2 0 0 0 0 0 0
```


**output:**
```
0 0 2 2 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 8 8 8 0 0
```


**output:**
```
0 0 0 0 8 8 8 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 9 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 3 3 3 3 0
```


**output:**
```
0 0 0 3 3 3 3 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 2 2 2 0
```


**output:**
```
0 0 0 0 0 2 2 2 0 0 0 0
```


## train_6

**input:**
```
0 0 5 5 0 0 0 0 0 0 0 0
```


**output:**
```
5 5 0 0 0 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 1 1 1 1 0 0 0 0
```


**output:**
```
1 1 1 1 0 0 0 0 0 0 0 0
```

**Perception of Task Elements:**

The task involves transforming a one-dimensional list of single-digit integers. Each input list contains a single contiguous block of identical non-zero digits, surrounded by zeros. The output list is the result of shifting this block of non-zero digits to the left. The magnitude of the shift appears to be directly related to the length of the non-zero block itself. The overall length of the list remains constant throughout the transformation.

**YAML Fact Document:**


```yaml
task_description: "Shift a contiguous block of identical non-zero digits within a list to the left."
data_representation:
  input: "List of single-digit integers."
  output: "List of single-digit integers, same length as input."
objects:
  - name: list
    properties:
      - type: "1D sequence of integers"
      - length: "Constant (12 in examples)"
      - content: "Mostly zeros with one contiguous block of identical non-zero digits."
  - name: non_zero_block
    properties:
      - type: "Sub-sequence of the list"
      - content: "Consists of identical non-zero digits."
      - length: "Variable (1 to 4 in examples)"
      - position: "Starting index within the list."
relationships:
  - type: "Transformation"
    applies_to: "non_zero_block"
    action: "Shift position within the list."
    direction: "Left"
    magnitude: "Equal to the length of the non_zero_block."
constraints:
  - "Input contains exactly one non-zero block."
  - "Digits within the block are identical."
  - "List length remains unchanged."
  - "The block does not wrap around; sufficient space exists for the left shift."
```


**Natural Language Program:**

1.  **Identify** the contiguous block of identical non-zero digits within the input list.
2.  **Determine** the starting index and the length of this identified block.
3.  **Calculate** the new starting index for the block by subtracting the block's length from its original starting index.
4.  **Create** a new output list of the same length as the input list, initially filled entirely with zeros.
5.  **Place** the identified non-zero block into the new output list, starting at the calculated new starting index.
6.  **Return** the modified output list.
```python
"""
Identifies a contiguous block of identical non-zero digits in a list of integers
(represented as a space-separated string) and shifts this block to the left
by a distance equal to its own length. The rest of the list remains zeros.
"""

# No specific imports needed beyond standard list operations

def find_non_zero_block_info(data_list):
    """
    Finds the start index, length, and value of the first contiguous
    block of identical non-zero digits. Assumes exactly one such block exists.

    Args:
        data_list: A list of integers.

    Returns:
        A tuple (start_index, length, value) of the block's properties.
        Returns (None, 0, 0) if no non-zero digits are found.
    """
    start_index = -1
    block_value = 0
    length = 0
    in_block = False

    for i, val in enumerate(data_list):
        if val != 0 and not in_block:  # Found the start of the block
            start_index = i
            block_value = val
            length = 1
            in_block = True
        elif val == block_value and in_block:  # Continuing the block
            length += 1
        elif val != block_value and in_block:  # Found the end of the block (since there's only one)
            break  # Stop searching once the block ends

    if start_index == -1: # No block found at all
        return None, 0, 0
    else:
        return start_index, length, block_value


def transform(input_str):
    """
    Transforms the input string by finding the single non-zero block
    and shifting it left by its own length.

    Args:
        input_str: A string of space-separated single-digit integers.

    Returns:
        A string representing the transformed list, space-separated.
    """
    # --- Input Processing ---
    # Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]
    list_length = len(input_list)

    # --- Core Logic: Find and Shift Block ---
    # 1. Identify the non-zero block's properties using the helper function.
    start_index, block_length, block_value = find_non_zero_block_info(input_list)

    # Handle case where no block is found (return all zeros).
    if start_index is None:
        return " ".join(['0'] * list_length)

    # 2. Calculate the new starting index for the block.
    # The shift amount is equal to the block's length.
    new_start_index = start_index - block_length

    # --- Output Generation ---
    # 3. Create the output list, initialized entirely with zeros.
    output_list = [0] * list_length

    # 4. Place the identified non-zero block into the output list at the new position.
    # Iterate 'block_length' times to copy each digit.
    for i in range(block_length):
        target_index = new_start_index + i
        # Place the block's value at the calculated index.
        # Based on problem constraints, target_index should always be valid.
        if 0 <= target_index < list_length:
             output_list[target_index] = block_value
        # else: # Optional: Error handling if constraints could be violated
             # print(f"Warning: Calculated index {target_index} out of bounds.")


    # 5. Format the output list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str

```
