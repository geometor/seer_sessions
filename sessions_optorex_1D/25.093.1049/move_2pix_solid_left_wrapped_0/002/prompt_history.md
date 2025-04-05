
## train_1

**input:**
```
1 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 1 0
```


## train_2

**input:**
```
5 5 5 0 0 5 5 5 5 5 5 5
```


**output:**
```
5 0 0 5 5 5 5 5 5 5 5 5
```


## train_3

**input:**
```
1 1 1 1 1 1 1 1 1 1 0 1
```


**output:**
```
1 1 1 1 1 1 1 1 0 1 1 1
```


## train_4

**input:**
```
3 0 0 0 0 0 0 0 0 0 0 3
```


**output:**
```
0 0 0 0 0 0 0 0 0 3 3 0
```


## train_5

**input:**
```
3 3 0 3 3 3 3 3 3 3 3 3
```


**output:**
```
0 3 3 3 3 3 3 3 3 3 3 3
```


## train_6

**input:**
```
0 0 0 0 0 0 4 4 4 4 4 4
```


**output:**
```
0 0 0 0 4 4 4 4 4 4 0 0
```


## train_7

**input:**
```
2 2 2 2 2 0 0 0 2 2 2 2
```


**output:**
```
2 2 2 0 0 0 2 2 2 2 2 2
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of the Elements**

1.  **Input/Output Structure:** Both input and output are sequences (lists) of 12 single-digit integers.
2.  **Element Types:** The sequences contain integers, with '0' being a prominent element alongside other digits (1, 2, 3, 4, 5 in the examples).
3.  **Core Transformation:** The primary change between input and output appears to be the rearrangement of elements. Specifically, the positions of the '0' digits seem to be systematically shifted.
4.  **Pattern Recognition:** Comparing the indices of the '0's in the input and output reveals a consistent pattern across examples: the index of each '0' in the output is 2 less than its index in the input, calculated modulo 12 (wrapping around from the beginning if the result is negative).
5.  **Handling Non-Zeros:** The non-zero elements from the input fill the positions in the output list that are *not* occupied by the shifted '0's. Importantly, the relative order of these non-zero elements is preserved from the input to the output.

**YAML Facts**


```yaml
objects:
  - name: input_list
    properties:
      - type: list
      - element_type: integer (digit)
      - length: 12
  - name: output_list
    properties:
      - type: list
      - element_type: integer (digit)
      - length: 12
  - name: zero_element
    properties:
      - value: 0
      - role: undergoes positional shift
  - name: non_zero_element
    properties:
      - value: integer > 0
      - role: fills remaining positions, preserves relative order

actions:
  - name: identify_zero_indices
    actor: transformation_process
    input: input_list
    output: list of indices where input_list element is 0
  - name: calculate_target_indices
    actor: transformation_process
    input: list of zero indices
    operation: (index - 2) mod 12 for each index
    output: list of target indices for zeros in output_list
  - name: collect_non_zero_elements
    actor: transformation_process
    input: input_list
    output: ordered list of non-zero elements
  - name: construct_output_list
    actor: transformation_process
    steps:
      - Initialize output_list (size 12, e.g., with placeholders).
      - Place 0 at each calculated target index.
      - Fill remaining placeholder positions sequentially with collected non-zero elements.

relationships:
  - type: positional_mapping
    source: zero_element in input_list at index `i`
    target: zero_element in output_list at index `(i - 2) mod 12`
  - type: order_preservation
    elements: non_zero_element
    description: The relative order of non_zero_elements in input_list is maintained in output_list.
  - type: complementary_placement
    description: Non-zero elements fill the positions not occupied by the shifted zero elements.
```


**Natural Language Program**

1.  Create a new list, `output_list`, of length 12, initially empty or filled with placeholders.
2.  Create an empty list called `non_zero_elements` to store the non-zero digits from the input in order.
3.  Create an empty list called `zero_target_indices` to store the calculated destination indices for the zeros.
4.  Iterate through the `input_list` from index `i = 0` to `11`:
    *   If the element at `input_list[i]` is 0, calculate its target index `j = (i - 2) % 12`. Add `j` to the `zero_target_indices` list.
    *   If the element at `input_list[i]` is not 0, append this element to the `non_zero_elements` list.
5.  Iterate through the `zero_target_indices` list. For each target index `j` in the list, set `output_list[j] = 0`.
6.  Initialize a counter `k = 0` for the `non_zero_elements` list.
7.  Iterate through the `output_list` from index `i = 0` to `11`:
    *   If `output_list[i]` is still empty or a placeholder (i.e., not yet assigned a 0), set `output_list[i]` to the element `non_zero_elements[k]`, and increment `k` by 1.
8.  Return the fully constructed `output_list`.
```python
import collections

"""
Transforms an input list of 12 digits by shifting the positions of all '0' elements two steps to the left (with wrap-around) 
and filling the remaining positions with the non-zero elements from the input list, preserving their original relative order.
"""

def transform(input_list_str: str) -> str:
    """
    Applies the described transformation to the input list string.

    Args:
        input_list_str: A string representing the input list of 12 digits, space-separated.

    Returns:
        A string representing the transformed list of 12 digits, space-separated.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_list_str.split()]
    list_length = 12

    # Initialize the output list with placeholders (e.g., None)
    output_list = [None] * list_length

    # Store non-zero elements in their original order
    non_zero_elements = []
    # Store the target indices for the zero elements
    zero_target_indices = []

    # First pass: Identify non-zero elements and calculate target indices for zeros
    for i, element in enumerate(input_list):
        if element == 0:
            # Calculate the target index for the zero, shifting left by 2 with wrap-around
            target_index = (i - 2) % list_length
            zero_target_indices.append(target_index)
        else:
            # Collect non-zero elements
            non_zero_elements.append(element)

    # Second pass: Place the zeros in their calculated target positions in the output list
    for index in zero_target_indices:
        output_list[index] = 0

    # Third pass: Fill the remaining placeholder positions with the non-zero elements
    non_zero_iter = iter(non_zero_elements) # Use an iterator for sequential filling
    for i in range(list_length):
        if output_list[i] is None: # If the position is not filled by a zero
            try:
                output_list[i] = next(non_zero_iter)
            except StopIteration:
                # This should not happen if the input length and logic are correct
                print("Error: Ran out of non-zero elements unexpectedly.")
                break # Or handle error appropriately

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))
    return output_str

```
