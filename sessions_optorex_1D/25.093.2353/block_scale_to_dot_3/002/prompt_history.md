
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 9 2
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 2
```


## train_2

**input:**
```
0 0 0 0 2 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 3 3 0 0 0 0 0
```


## train_3

**input:**
```
0 6 6 6 6 6 6 6 0 0 2 0
```


**output:**
```
0 6 6 6 6 6 6 6 6 6 2 0
```


## train_4

**input:**
```
6 6 6 6 6 2 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6 2 0 0 0 0 0 0
```


## train_5

**input:**
```
0 5 5 5 0 0 0 0 0 2 0 0
```


**output:**
```
0 5 5 5 5 5 5 5 5 2 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 0 2 8 8
```


**output:**
```
0 0 0 0 0 0 0 0 0 2 8 8
```


## train_7

**input:**
```
0 2 6 6 6 6 0 0 0 0 0 0
```


**output:**
```
0 2 6 6 6 6 0 0 0 0 0 0
```

**Perception of Elements:**

The task involves processing a list of single-digit integers. The core operation appears to be conditional filling of zeros based on surrounding non-zero numbers, specifically triggered by the presence and position of the number '2'. The transformation focuses on the segment of the list preceding the first occurrence of '2'.

**YAML Facts:**


```yaml
objects:
  - name: list
    type: list of integers
  - name: element
    type: integer (0-9)
  - name: target_element
    value: 2
    property: trigger for transformation
  - name: fill_value
    type: integer (non-zero)
    property: value used to replace zeros
  - name: zero_element
    value: 0
    property: element to be potentially replaced

properties:
  - sequence: contiguous block of identical non-zero numbers
  - position: index of an element in the list

actions:
  - find: locate the first occurrence of the target_element (2)
  - identify: find the last contiguous sequence of identical non-zero numbers before the target_element
  - check: determine if zeros exist between the identified sequence and the target_element
  - replace: change the intervening zero_elements to the fill_value derived from the sequence

relationships:
  - spatial: position of the target_element relative to sequences of non-zero numbers and zero_elements
  - conditional: the replacement action depends on the presence and relative positioning of the target_element, a non-zero sequence, and intervening zeros
```


**Natural Language Program:**

1.  Make a copy of the input list to serve as the potential output.
2.  Find the index of the first occurrence of the number `2` in the list. If `2` is not found, return the original list.
3.  Initialize `last_non_zero_index` to -1 and `fill_value` to -1.
4.  Iterate through the list from the beginning up to (but not including) the index of `2`.
5.  During this iteration, if a non-zero number is encountered:
    *   Check if it's the start of a new contiguous sequence or part of the current one.
    *   Update `last_non_zero_index` to the current index.
    *   Update `fill_value` to the value of the number at the current index.
6.  After iterating up to the index of `2`, check if a `fill_value` (other than -1) was found.
7.  If a `fill_value` was found, iterate from the index immediately following `last_non_zero_index` up to (but not including) the index of `2`.
8.  For each element in this range, if the element is `0`, change its value in the copied list to the `fill_value`.
9.  Return the modified list.
```python
import copy

"""
Identifies the first occurrence of the number 2 in a list of integers. 
If found, it locates the last non-zero number preceding the 2. 
Then, it fills any zeros between that last non-zero number and the 2 with the value of that last non-zero number. 
If 2 is not found, or if there are no non-zero numbers before the 2, the list remains unchanged.
"""

def find_first_occurrence(data_list, target):
    """Finds the index of the first occurrence of target in data_list."""
    try:
        return data_list.index(target)
    except ValueError:
        return -1

def find_last_non_zero_before(data_list, end_index):
    """
    Finds the value and index of the last non-zero element 
    in the list strictly before end_index.
    Returns (value, index) or (None, -1) if none found.
    """
    last_non_zero_val = None
    last_non_zero_idx = -1
    for i in range(end_index - 1, -1, -1):
        if data_list[i] != 0:
            last_non_zero_val = data_list[i]
            last_non_zero_idx = i
            break
    return last_non_zero_val, last_non_zero_idx

def transform(input_list):
    """
    Transforms the input list based on the described rule involving the number 2.

    Args:
        input_list: A list of integers.

    Returns:
        A new list with zeros potentially filled based on the rule, 
        or a copy of the original list if the conditions aren't met.
    """
    # Make a copy to avoid modifying the original input list
    output_list = copy.deepcopy(input_list)
    
    # Define the target element
    target_element = 2
    zero_element = 0

    # 1. Find the index of the first occurrence of the target element (2)
    target_index = find_first_occurrence(output_list, target_element)

    # If the target element is not found, return the original list copy
    if target_index == -1:
        return output_list

    # 2. Find the last non-zero element and its index before the target element
    fill_value, last_non_zero_index = find_last_non_zero_before(output_list, target_index)

    # If no non-zero element was found before the target element, return the list copy
    if fill_value is None:
        return output_list
        
    # 3. Iterate from the position after the last non-zero element up to the target element
    # Replace any zero elements with the fill_value
    for i in range(last_non_zero_index + 1, target_index):
        if output_list[i] == zero_element:
            output_list[i] = fill_value
            
    # 4. Return the modified list
    return output_list
```
