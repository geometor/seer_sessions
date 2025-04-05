
## train_1

**input:**
```
0 0 0 0 0 1 8 8 8 0 0 0
```


**output:**
```
1 1 1 1 1 1 8 8 8 0 0 0
```


## train_2

**input:**
```
0 0 6 8 8 8 8 0 0 0 0 0
```


**output:**
```
6 6 6 8 8 8 8 0 0 0 0 0
```


## train_3

**input:**
```
0 0 1 1 1 1 3 0 0 0 0 0
```


**output:**
```
0 0 1 1 1 1 3 3 3 3 3 3
```


## train_4

**input:**
```
0 0 2 5 5 5 0 0 0 0 0 0
```


**output:**
```
2 2 2 5 5 5 0 0 0 0 0 0
```


## train_5

**input:**
```
9 4 4 4 4 0 0 0 0 0 0 0
```


**output:**
```
9 4 4 4 4 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 8 1 1 1 1 0 0 0 0 0
```


**output:**
```
8 8 8 1 1 1 1 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 7 7 7 2 0 0 0 0
```


**output:**
```
0 0 0 0 7 7 7 2 2 2 2 2
```

*   **Perception of the elements:**
    *   The input and output are lists of single-digit integers.
    *   The core transformation involves conditionally replacing sequences of zeros ('0') at the beginning and/or end of the list.
    *   The replacement value is determined by the non-zero number adjacent to the sequence of zeros.
    *   The replacement only occurs under specific conditions related to the values of the first two distinct non-zero numbers (for the beginning) and the last two distinct non-zero numbers (for the end).

*   **YAML Facts:**
    
```yaml
    objects:
      - input_list:
          type: list
          contains: integers (0-9)
      - output_list:
          type: list
          contains: integers (0-9)
          derivation: modified version of input_list
      - element:
          type: integer
          value_range: 0-9
      - zero_sequence:
          type: sublist
          contains_only: 0
          location: start or end of input_list
      - non_zero_element:
          type: integer
          value_range: 1-9
          properties: [value, index]
      - first_non_zero:
          type: non_zero_element
          relation: earliest non_zero element in the list
      - second_non_zero:
          type: non_zero_element
          relation: second earliest non_zero element in the list (if exists)
      - last_non_zero:
          type: non_zero_element
          relation: latest non_zero element in the list
      - second_last_non_zero:
          type: non_zero_element
          relation: second latest non_zero element in the list (if exists)

    actions:
      - find_non_zeros:
          input: input_list
          output: list of (value, index) pairs for non_zero_elements
      - compare_values:
          input: two non_zero_elements
          output: boolean (equal or not equal)
      - fill_zeros:
          target: section of output_list (start or end)
          condition: comparison result of relevant non-zero elements
          value: value of the adjacent non_zero_element (first_non_zero or last_non_zero)

    relationships:
      - adjacency: A zero_sequence is adjacent to a non_zero_element at the start or end.
      - conditional_fill_start: The zero_sequence at the start is filled if the first_non_zero value differs from the second_non_zero value (or if only one non_zero element exists).
      - conditional_fill_end: The zero_sequence at the end is filled if the last_non_zero value differs from the second_last_non_zero value (or if only one non_zero element exists).
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input list to serve as the initial output list.
    2.  Identify all non-zero elements and their indices in the input list.
    3.  If there are no non-zero elements, return the output list unchanged.
    4.  Determine the first non-zero element (value `v1`, index `i1`) and the last non-zero element (value `vL`, index `iL`).
    5.  **Left Fill Check:**
        a.  Find the second non-zero element (value `v2`, index `i2`) if it exists.
        b.  If only one non-zero element exists OR if `v1` is not equal to `v2`, then replace all elements in the output list from index 0 up to (but not including) index `i1` with the value `v1`.
    6.  **Right Fill Check:**
        a.  Find the second-to-last non-zero element (value `vL-1`, index `iL-1`) if it exists.
        b.  If only one non-zero element exists OR if `vL` is not equal to `vL-1`, then replace all elements in the output list from index `iL + 1` to the end of the list with the value `vL`.
    7.  Return the modified output list.
```python
import math
import re # Using re for potential string parsing if needed, although assuming list input for now

"""
Transforms the input list by conditionally filling leading/trailing zeros.
Zeros at the start are filled with the value of the first non-zero element 
if its value differs from the second non-zero element (or if only one non-zero element exists).
Zeros at the end are filled with the value of the last non-zero element 
if its value differs from the second-to-last non-zero element (or if only one non-zero element exists).
"""

def find_non_zeros(data_list):
    """
    Identifies all non-zero elements and their indices in a list.

    Args:
        data_list: A list of numbers.

    Returns:
        A list of tuples, where each tuple is (value, index) for a non-zero element.
        Returns an empty list if no non-zero elements are found.
    """
    non_zeros = []
    for index, value in enumerate(data_list):
        if value != 0:
            non_zeros.append((value, index))
    return non_zeros

def transform(input_grid: list[int]) -> list[int]:
    """
    Applies the transformation rule to the input list.

    Args:
        input_grid: A list of integers (0-9).

    Returns:
        A new list of integers representing the transformed output.
    """
    # initialize output_grid as a copy of the input
    output_grid = list(input_grid)

    # Find all non-zero elements and their indices
    non_zeros = find_non_zeros(input_grid)

    # If there are no non-zero elements, return the original list
    if not non_zeros:
        return output_grid

    num_non_zeros = len(non_zeros)

    # --- Left Fill Check ---
    # Get the first non-zero element
    v1, i1 = non_zeros[0]
    
    # Determine if the left side (leading zeros) should be filled
    fill_left = False
    if num_non_zeros == 1:
        # If there's only one non-zero number, always fill the left
        fill_left = True
    else:
        # If there are multiple non-zeros, compare the first two
        v2, i2 = non_zeros[1]
        if v1 != v2:
            fill_left = True

    # Perform the left fill if the condition is met
    if fill_left:
        for i in range(i1): # Iterate from index 0 up to (but not including) i1
            if output_grid[i] == 0: # Only fill existing zeros
                 output_grid[i] = v1

    # --- Right Fill Check ---
    # Get the last non-zero element
    vL, iL = non_zeros[-1]

    # Determine if the right side (trailing zeros) should be filled
    fill_right = False
    if num_non_zeros == 1:
         # If there's only one non-zero number, always fill the right
        fill_right = True
    else:
        # If there are multiple non-zeros, compare the last two
        vL_minus_1, iL_minus_1 = non_zeros[-2]
        if vL != vL_minus_1:
            fill_right = True

    # Perform the right fill if the condition is met
    if fill_right:
        for i in range(iL + 1, len(output_grid)): # Iterate from index iL + 1 to the end
             if output_grid[i] == 0: # Only fill existing zeros
                output_grid[i] = vL

    return output_grid

# Example Usage (parsing string input as seen in examples)
def parse_input_string(s: str) -> list[int]:
    return [int(x) for x in s.split()]

def format_output_list(lst: list[int]) -> str:
    return " ".join(map(str, lst))

# Test cases from the problem description
train_examples = [
    ("0 0 0 0 0 1 8 8 8 0 0 0", "1 1 1 1 1 1 8 8 8 0 0 0"),
    ("0 0 6 8 8 8 8 0 0 0 0 0", "6 6 6 8 8 8 8 0 0 0 0 0"),
    ("0 0 1 1 1 1 3 0 0 0 0 0", "0 0 1 1 1 1 3 3 3 3 3 3"),
    ("0 0 2 5 5 5 0 0 0 0 0 0", "2 2 2 5 5 5 0 0 0 0 0 0"),
    ("9 4 4 4 4 0 0 0 0 0 0 0", "9 4 4 4 4 0 0 0 0 0 0 0"), # No change expected here
    ("0 0 8 1 1 1 1 0 0 0 0 0", "8 8 8 1 1 1 1 0 0 0 0 0"),
    ("0 0 0 0 7 7 7 2 0 0 0 0", "0 0 0 0 7 7 7 2 2 2 2 2"),
]

# print("Testing transform function:")
# for i, (input_str, expected_output_str) in enumerate(train_examples):
#     input_list = parse_input_string(input_str)
#     output_list = transform(input_list)
#     output_str = format_output_list(output_list)
#     print(f"Train {i+1}:")
#     print(f"  Input:    {input_str}")
#     print(f"  Output:   {output_str}")
#     print(f"  Expected: {expected_output_str}")
#     print(f"  Match:    {output_str == expected_output_str}")
#     print("-" * 10)
```

Previous Code:
```python
import math
import re # Using re for potential string parsing if needed, although assuming list input for now

"""
Transforms the input list by conditionally filling leading/trailing zeros.
Zeros at the start are filled with the value of the first non-zero element 
if its value differs from the second non-zero element (or if only one non-zero element exists).
Zeros at the end are filled with the value of the last non-zero element 
if its value differs from the second-to-last non-zero element (or if only one non-zero element exists).
"""

def find_non_zeros(data_list):
    """
    Identifies all non-zero elements and their indices in a list.

    Args:
        data_list: A list of numbers.

    Returns:
        A list of tuples, where each tuple is (value, index) for a non-zero element.
        Returns an empty list if no non-zero elements are found.
    """
    non_zeros = []
    for index, value in enumerate(data_list):
        if value != 0:
            non_zeros.append((value, index))
    return non_zeros

def transform(input_grid: list[int]) -> list[int]:
    """
    Applies the transformation rule to the input list.

    Args:
        input_grid: A list of integers (0-9).

    Returns:
        A new list of integers representing the transformed output.
    """
    # initialize output_grid as a copy of the input
    output_grid = list(input_grid)

    # Find all non-zero elements and their indices
    non_zeros = find_non_zeros(input_grid)

    # If there are no non-zero elements, return the original list
    if not non_zeros:
        return output_grid

    num_non_zeros = len(non_zeros)

    # --- Left Fill Check ---
    # Get the first non-zero element
    v1, i1 = non_zeros[0]
    
    # Determine if the left side (leading zeros) should be filled
    fill_left = False
    if num_non_zeros == 1:
        # If there's only one non-zero number, always fill the left
        fill_left = True
    else:
        # If there are multiple non-zeros, compare the first two
        v2, i2 = non_zeros[1]
        if v1 != v2:
            fill_left = True

    # Perform the left fill if the condition is met
    if fill_left:
        for i in range(i1): # Iterate from index 0 up to (but not including) i1
            if output_grid[i] == 0: # Only fill existing zeros
                 output_grid[i] = v1

    # --- Right Fill Check ---
    # Get the last non-zero element
    vL, iL = non_zeros[-1]

    # Determine if the right side (trailing zeros) should be filled
    fill_right = False
    if num_non_zeros == 1:
         # If there's only one non-zero number, always fill the right
        fill_right = True
    else:
        # If there are multiple non-zeros, compare the last two
        vL_minus_1, iL_minus_1 = non_zeros[-2]
        if vL != vL_minus_1:
            fill_right = True

    # Perform the right fill if the condition is met
    if fill_right:
        for i in range(iL + 1, len(output_grid)): # Iterate from index iL + 1 to the end
             if output_grid[i] == 0: # Only fill existing zeros
                output_grid[i] = vL

    return output_grid

# Example Usage (parsing string input as seen in examples)
def parse_input_string(s: str) -> list[int]:
    return [int(x) for x in s.split()]

def format_output_list(lst: list[int]) -> str:
    return " ".join(map(str, lst))

# Test cases from the problem description
train_examples = [
    ("0 0 0 0 0 1 8 8 8 0 0 0", "1 1 1 1 1 1 8 8 8 0 0 0"),
    ("0 0 6 8 8 8 8 0 0 0 0 0", "6 6 6 8 8 8 8 0 0 0 0 0"),
    ("0 0 1 1 1 1 3 0 0 0 0 0", "0 0 1 1 1 1 3 3 3 3 3 3"),
    ("0 0 2 5 5 5 0 0 0 0 0 0", "2 2 2 5 5 5 0 0 0 0 0 0"),
    ("9 4 4 4 4 0 0 0 0 0 0 0", "9 4 4 4 4 0 0 0 0 0 0 0"), # No change expected here
    ("0 0 8 1 1 1 1 0 0 0 0 0", "8 8 8 1 1 1 1 0 0 0 0 0"),
    ("0 0 0 0 7 7 7 2 0 0 0 0", "0 0 0 0 7 7 7 2 2 2 2 2"),
]

# print("Testing transform function:")
# for i, (input_str, expected_output_str) in enumerate(train_examples):
#     input_list = parse_input_string(input_str)
#     output_list = transform(input_list)
#     output_str = format_output_list(output_list)
#     print(f"Train {i+1}:")
#     print(f"  Input:    {input_str}")
#     print(f"  Output:   {output_str}")
#     print(f"  Expected: {expected_output_str}")
#     print(f"  Match:    {output_str == expected_output_str}")
#     print("-" * 10)
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
*   **General Assessment:**
    *   The primary issue identified ("The truth value of an array...") seems related to the execution environment potentially using NumPy arrays instead of standard Python lists, rather than a fundamental flaw in the initial transformation logic derived.
    *   The core logic identified in the previous step (filling leading/trailing zeros based on comparisons of adjacent distinct non-zero elements) appears consistent across all provided training examples.
    *   The strategy is to refine the description of the logic (YAML and Natural Language Program) to be clearer and more robust, ensuring it accurately reflects the observed transformations in all examples, including edge cases like single non-zero elements or non-zeros at the very start/end. We will proceed assuming the inputs/outputs are standard Python lists.

*   **Metrics and Analysis:**
    We will analyze each example to confirm the non-zero elements and the comparison results that drive the fill logic.
    

*code_execution:*
```python
    import json

    def analyze_example(input_str):
        input_list = [int(x) for x in input_str.split()]
        non_zeros = []
        for index, value in enumerate(input_list):
            if value != 0:
                non_zeros.append({'value': value, 'index': index})

        metrics = {
            'input': input_list,
            'non_zeros': non_zeros,
            'count_non_zeros': len(non_zeros),
            'left_fill_condition': None,
            'right_fill_condition': None,
            'first_non_zero': None,
            'second_non_zero': None,
            'last_non_zero': None,
            'second_last_non_zero': None,
        }

        if not non_zeros:
            metrics['left_fill_condition'] = False
            metrics['right_fill_condition'] = False
            return metrics

        metrics['first_non_zero'] = non_zeros[0]
        metrics['last_non_zero'] = non_zeros[-1]

        # Left Fill Logic
        if len(non_zeros) == 1:
            metrics['left_fill_condition'] = True
        else:
            metrics['second_non_zero'] = non_zeros[1]
            metrics['left_fill_condition'] = (non_zeros[0]['value'] != non_zeros[1]['value'])

        # Right Fill Logic
        if len(non_zeros) == 1:
            metrics['right_fill_condition'] = True
        else:
            metrics['second_last_non_zero'] = non_zeros[-2]
            metrics['right_fill_condition'] = (non_zeros[-1]['value'] != non_zeros[-2]['value'])

        return metrics

    train_inputs = [
        "0 0 0 0 0 1 8 8 8 0 0 0",
        "0 0 6 8 8 8 8 0 0 0 0 0",
        "0 0 1 1 1 1 3 0 0 0 0 0",
        "0 0 2 5 5 5 0 0 0 0 0 0",
        "9 4 4 4 4 0 0 0 0 0 0 0",
        "0 0 8 1 1 1 1 0 0 0 0 0",
        "0 0 0 0 7 7 7 2 0 0 0 0",
    ]

    analysis_results = {}
    for i, input_str in enumerate(train_inputs):
        analysis_results[f"train_{i+1}"] = analyze_example(input_str)

    print(json.dumps(analysis_results, indent=2))
    
```

*code_execution_result:*
outcome: OUTCOME_OK
```
{
  "train_1": {
    "input": [
      0,
      0,
      0,
      0,
      0,
      1,
      8,
      8,
      8,
      0,
      0,
      0
    ],
    "non_zeros": [
      {
        "value": 1,
        "index": 5
      },
      {
        "value": 8,
        "index": 6
      },
      {
        "value": 8,
        "index": 7
      },
      {
        "value": 8,
        "index": 8
      }
    ],
    "count_non_zeros": 4,
    "left_fill_condition": true,
    "right_fill_condition": false,
    "first_non_zero": {
      "value": 1,
      "index": 5
    },
    "second_non_zero": {
      "value": 8,
      "index": 6
    },
    "last_non_zero": {
      "value": 8,
      "index": 8
    },
    "second_last_non_zero": {
      "value": 8,
      "index": 7
    }
  },
  "train_2": {
    "input": [
      0,
      0,
      6,
      8,
      8,
      8,
      8,
      0,
      0,
      0,
      0,
      0
    ],
    "non_zeros": [
      {
        "value": 6,
        "index": 2
      },
      {
        "value": 8,
        "index": 3
      },
      {
        "value": 8,
        "index": 4
      },
      {
        "value": 8,
        "index": 5
      },
      {
        "value": 8,
        "index": 6
      }
    ],
    "count_non_zeros": 5,
    "left_fill_condition": true,
    "right_fill_condition": false,
    "first_non_zero": {
      "value": 6,
      "index": 2
    },
    "second_non_zero": {
      "value": 8,
      "index": 3
    },
    "last_non_zero": {
      "value": 8,
      "index": 6
    },
    "second_last_non_zero": {
      "value": 8,
      "index": 5
    }
  },
  "train_3": {
    "input": [
      0,
      0,
      1,
      1,
      1,
      1,
      3,
      0,
      0,
      0,
      0,
      0
    ],
    "non_zeros": [
      {
        "value": 1,
        "index": 2
      },
      {
        "value": 1,
        "index": 3
      },
      {
        "value": 1,
        "index": 4
      },
      {
        "value": 1,
        "index": 5
      },
      {
        "value": 3,
        "index": 6
      }
    ],
    "count_non_zeros": 5,
    "left_fill_condition": false,
    "right_fill_condition": true,
    "first_non_zero": {
      "value": 1,
      "index": 2
    },
    "second_non_zero": {
      "value": 1,
      "index": 3
    },
    "last_non_zero": {
      "value": 3,
      "index": 6
    },
    "second_last_non_zero": {
      "value": 1,
      "index": 5
    }
  },
  "train_4": {
    "input": [
      0,
      0,
      2,
      5,
      5,
      5,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "non_zeros": [
      {
        "value": 2,
        "index": 2
      },
      {
        "value": 5,
        "index": 3
      },
      {
        "value": 5,
        "index": 4
      },
      {
        "value": 5,
        "index": 5
      }
    ],
    "count_non_zeros": 4,
    "left_fill_condition": true,
    "right_fill_condition": false,
    "first_non_zero": {
      "value": 2,
      "index": 2
    },
    "second_non_zero": {
      "value": 5,
      "index": 3
    },
    "last_non_zero": {
      "value": 5,
      "index": 5
    },
    "second_last_non_zero": {
      "value": 5,
      "index": 4
    }
  },
  "train_5": {
    "input": [
      9,
      4,
      4,
      4,
      4,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "non_zeros": [
      {
        "value": 9,
        "index": 0
      },
      {
        "value": 4,
        "index": 1
      },
      {
        "value": 4,
        "index": 2
      },
      {
        "value": 4,
        "index": 3
      },
      {
        "value": 4,
        "index": 4
      }
    ],
    "count_non_zeros": 5,
    "left_fill_condition": true,
    "right_fill_condition": false,
    "first_non_zero": {
      "value": 9,
      "index": 0
    },
    "second_non_zero": {
      "value": 4,
      "index": 1
    },
    "last_non_zero": {
      "value": 4,
      "index": 4
    },
    "second_last_non_zero": {
      "value": 4,
      "index": 3
    }
  },
  "train_6": {
    "input": [
      0,
      0,
      8,
      1,
      1,
      1,
      1,
      0,
      0,
      0,
      0,
      0
    ],
    "non_zeros": [
      {
        "value": 8,
        "index": 2
      },
      {
        "value": 1,
        "index": 3
      },
      {
        "value": 1,
        "index": 4
      },
      {
        "value": 1,
        "index": 5
      },
      {
        "value": 1,
        "index": 6
      }
    ],
    "count_non_zeros": 5,
    "left_fill_condition": true,
    "right_fill_condition": false,
    "first_non_zero": {
      "value": 8,
      "index": 2
    },
    "second_non_zero": {
      "value": 1,
      "index": 3
    },
    "last_non_zero": {
      "value": 1,
      "index": 6
    },
    "second_last_non_zero": {
      "value": 1,
      "index": 5
    }
  },
  "train_7": {
    "input": [
      0,
      0,
      0,
      0,
      7,
      7,
      7,
      2,
      0,
      0,
      0,
      0
    ],
    "non_zeros": [
      {
        "value": 7,
        "index": 4
      },
      {
        "value": 7,
        "index": 5
      },
      {
        "value": 7,
        "index": 6
      },
      {
        "value": 2,
        "index": 7
      }
    ],
    "count_non_zeros": 4,
    "left_fill_condition": false,
    "right_fill_condition": true,
    "first_non_zero": {
      "value": 7,
      "index": 4
    },
    "second_non_zero": {
      "value": 7,
      "index": 5
    },
    "last_non_zero": {
      "value": 2,
      "index": 7
    },
    "second_last_non_zero": {
      "value": 7,
      "index": 6
    }
  }
}

```
    *   **Analysis Summary:** The code execution confirms the fill conditions derived from visual inspection:
        *   `train_1`: Fill left (1 != 8), Don't fill right (8 == 8). Matches output.
        *   `train_2`: Fill left (6 != 8), Don't fill right (8 == 8). Matches output.
        *   `train_3`: Don't fill left (1 == 1), Fill right (3 != 1). Matches output.
        *   `train_4`: Fill left (2 != 5), Don't fill right (5 == 5). Matches output.
        *   `train_5`: Fill left rule `(9 != 4)` is true, but `i1=0`, so no leading zeros to fill. Don't fill right (4 == 4). Matches output.
        *   `train_6`: Fill left (8 != 1), Don't fill right (1 == 1). Matches output.
        *   `train_7`: Don't fill left (7 == 7), Fill right (2 != 7). Matches output.
    *   The logic appears sound and consistent across all examples. The case where only one non-zero element exists implicitly leads to filling both left and right sides as per the logic (`len(non_zeros) == 1` makes both `left_fill_condition` and `right_fill_condition` true).

*   **YAML Facts:**
    
```yaml
    objects:
      - input_list:
          type: list
          contains: integers (0-9)
          description: The initial sequence of numbers.
      - output_list:
          type: list
          contains: integers (0-9)
          derivation: A modified copy of input_list.
      - element:
          type: integer
          value_range: 0-9
      - non_zero_element:
          type: object
          properties:
            - value: integer (1-9)
            - index: integer (position in the list)
      - non_zero_sequence:
          type: list
          contains: non_zero_element objects
          derivation: Extracted from input_list, ordered by index.
          properties: [count]
      - leading_zeros:
          type: sublist
          contains_only: 0
          location: Start of the list, up to the index of the first non_zero_element. Can be empty.
      - trailing_zeros:
          type: sublist
          contains_only: 0
          location: End of the list, starting from the index after the last non_zero_element. Can be empty.

    actions:
      - find_all_non_zeros:
          input: input_list
          output: non_zero_sequence (list of {'value': v, 'index': i} dictionaries/objects)
      - get_element_by_position:
          input: non_zero_sequence, position (e.g., first, second, last, second-last)
          output: non_zero_element object (or null/error if position doesn't exist)
      - compare_values:
          input: two non_zero_element objects
          output: boolean (true if values are different, false if equal)
      - fill_sublist:
          target: a sublist within output_list (identified by start and end index)
          value: integer (the fill value)
          action: Replace all elements within the target sublist with the specified value.

    relationships_and_conditions:
      - left_fill_rule:
          condition: True if count of non_zero_sequence is 1, OR if the value of the first non_zero_element is different from the value of the second non_zero_element.
          action_if_true: fill_sublist targeting leading_zeros with the value of the first non_zero_element.
          index_range: 0 to index of first_non_zero_element (exclusive).
      - right_fill_rule:
          condition: True if count of non_zero_sequence is 1, OR if the value of the last non_zero_element is different from the value of the second-last non_zero_element.
          action_if_true: fill_sublist targeting trailing_zeros with the value of the last non_zero_element.
          index_range: index of last_non_zero_element + 1 to end of list.
    ```


*   **Natural Language Program:**
    1.  Initialize the `output_list` as a direct copy of the `input_list`.
    2.  Find all non-zero elements in the `input_list` and store them along with their original indices in an ordered list called `non_zero_sequence`. Let `n` be the count of elements in `non_zero_sequence`.
    3.  If `n` is 0 (no non-zero elements), return the `output_list` as is.
    4.  Identify the first non-zero element (`first_nz = non_zero_sequence[0]`) and the last non-zero element (`last_nz = non_zero_sequence[n-1]`).
    5.  **Evaluate Left Fill Condition:**
        a.  Determine if the leading zeros should be filled. This condition (`fill_left`) is TRUE if:
            *   `n` is equal to 1 (only one non-zero element exists).
            *   OR `n` is greater than 1 AND the value of `first_nz` is different from the value of the second non-zero element (`non_zero_sequence[1]`).
        b.  If `fill_left` is TRUE, iterate from index 0 up to (but not including) `first_nz.index`. For each index `i` in this range, set `output_list[i]` to `first_nz.value`.
    6.  **Evaluate Right Fill Condition:**
        a.  Determine if the trailing zeros should be filled. This condition (`fill_right`) is TRUE if:
            *   `n` is equal to 1 (only one non-zero element exists).
            *   OR `n` is greater than 1 AND the value of `last_nz` is different from the value of the second-to-last non-zero element (`non_zero_sequence[n-2]`).
        b.  If `fill_right` is TRUE, iterate from index `last_nz.index + 1` to the end of the `output_list`. For each index `i` in this range, set `output_list[i]` to `last_nz.value`.
    7.  Return the modified `output_list`.
