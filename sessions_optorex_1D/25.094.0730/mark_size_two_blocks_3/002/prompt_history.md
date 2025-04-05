
## train_1

**input:**
```
1 0 0 0 1 1 0 0 0 0 1 0
```


**output:**
```
1 0 0 3 1 1 3 0 0 0 1 0
```


## train_2

**input:**
```
0 0 0 1 0 0 0 1 0 0 0 0
```


**output:**
```
0 0 0 1 0 0 0 1 0 0 0 0
```


## train_3

**input:**
```
0 0 0 1 1 0 0 0 0 1 0 0
```


**output:**
```
0 0 3 1 1 3 0 0 0 1 0 0
```


## train_4

**input:**
```
0 0 0 1 0 0 0 1 1 1 0 0
```


**output:**
```
0 0 0 1 0 0 0 1 1 1 0 0
```


## train_5

**input:**
```
1 0 0 0 0 0 0 0 1 0 0 0
```


**output:**
```
1 0 0 0 0 0 0 0 1 0 0 0
```


## train_6

**input:**
```
1 1 0 0 0 0 1 0 0 0 1 0
```


**output:**
```
1 1 3 0 0 0 1 0 0 0 1 0
```


## train_7

**input:**
```
0 0 0 1 1 0 0 0 1 0 0 0
```


**output:**
```
0 0 3 1 1 3 0 0 1 0 0 0
```

Okay, let's analyze the transformation.

**Perception of Task Elements:**

The input is a sequence of binary digits (0s and 1s). The output is a sequence of the same length, containing digits 0, 1, and 3. The transformation modifies some of the 0s in the input sequence to 3s in the output sequence, while the 1s remain unchanged. The modification rule for the 0s depends on their context, specifically their neighboring values. By comparing the input and output pairs, a pattern emerges: 0s are changed to 3s only when they are immediately adjacent to a sequence of exactly two consecutive 1s (`1 1`). Sequences of three or more consecutive 1s (`1 1 1`) do not trigger this change in their adjacent 0s.

**Facts:**


```yaml
Input:
  type: list
  element_type: int
  values: [0, 1]
Output:
  type: list
  element_type: int
  values: [0, 1, 3]
  length: Same as input length
Transformation:
  type: Conditional element replacement
  target_element_value: 0
  replacement_value: 3
  condition:
    description: The '0' element must be immediately adjacent (left or right neighbor) to a block of exactly two consecutive '1's.
    pattern_trigger: '1 1'
    pattern_negation: The '1 1' block cannot be part of a longer sequence of '1's (e.g., '1 1 1').
    examples:
      - '0 1 1 0' -> '0 1 1 3' (change right 0)
      - '0 1 1 0' -> '3 1 1 0' (change left 0)
      - '0 1 1 1 0' -> '0 1 1 1 0' (no change)
      - '1 1 0' -> '1 1 3' (change 0)
      - '0 1 1' -> '3 1 1' (change 0)
  unmodified_elements:
    - All '1's from the input remain '1's in the output.
    - '0's not meeting the adjacency condition remain '0's.
```


**Natural Language Program:**

1.  Initialize an output sequence as a copy of the input sequence.
2.  Iterate through each element of the input sequence using its index, `i`.
3.  If the element `input[i]` is `0`:
    *   Check if this `0` is immediately to the right of an isolated `1 1` block: This occurs if `i >= 2`, `input[i-1]` is `1`, `input[i-2]` is `1`, AND (`i == 2` OR `input[i-3]` is not `1`). If these conditions are met, change the element at index `i` in the output sequence to `3`.
    *   Check if this `0` is immediately to the left of an isolated `1 1` block: This occurs if `i <= length(input) - 3`, `input[i+1]` is `1`, `input[i+2]` is `1`, AND (`i == length(input) - 3` OR `input[i+3]` is not `1`). If these conditions are met, change the element at index `i` in the output sequence to `3`.
4.  If the element `input[i]` is `1`, keep the corresponding element in the output sequence as `1`.
5.  Return the modified output sequence.
```python
import math
import collections

"""
Transforms a list of binary digits (0s and 1s) based on the following rule:
A '0' in the input list is changed to a '3' in the output list if and only if 
it is immediately adjacent (either to the left or right) to a sequence of 
exactly two consecutive '1's. '1's and '0's that do not meet this condition 
remain unchanged. Sequences of three or more consecutive '1's do not cause 
adjacent '0's to change.
"""

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of integers (0s and 1s).

    Returns:
        A new list with '0's potentially replaced by '3's according 
        to the adjacency rule with '1 1' sequences.
    """
    # Initialize output_list as a copy of the input
    output_list = list(input_list)
    n = len(input_list)

    # Iterate through the input list with index
    for i in range(n):
        # Check only if the current element is 0
        if input_list[i] == 0:
            # Condition 1: Check if the '0' is to the right of an isolated '1 1'
            # Indices must be valid: i-1 >= 0, i-2 >= 0 => i >= 2
            # Must have '1 1' to the left: input_list[i-1] == 1 and input_list[i-2] == 1
            # Must NOT have a '1' before the '1 1': (i == 2) or (i > 2 and input_list[i-3] == 0)
            is_right_of_isolated_11 = False
            if i >= 2 and input_list[i-1] == 1 and input_list[i-2] == 1:
                if i == 2 or input_list[i-3] == 0:
                    is_right_of_isolated_11 = True

            # Condition 2: Check if the '0' is to the left of an isolated '1 1'
            # Indices must be valid: i+1 < n, i+2 < n => i <= n - 3
            # Must have '1 1' to the right: input_list[i+1] == 1 and input_list[i+2] == 1
            # Must NOT have a '1' after the '1 1': (i == n - 3) or (i < n - 3 and input_list[i+3] == 0)
            is_left_of_isolated_11 = False
            if i <= n - 3 and input_list[i+1] == 1 and input_list[i+2] == 1:
                if i == n - 3 or input_list[i+3] == 0:
                     is_left_of_isolated_11 = True
                     
            # If either condition is met, change the output element to 3
            if is_right_of_isolated_11 or is_left_of_isolated_11:
                output_list[i] = 3
        
        # If input_list[i] is 1, it remains unchanged (already handled by copying)

    return output_list

```
