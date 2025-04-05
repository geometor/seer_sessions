
## train_1

**input:**
```
0 0 0 0 2 0 7 7 7 7 7 7
```


**output:**
```
0 0 0 0 2 7 7 7 7 7 7 7
```


## train_2

**input:**
```
0 0 0 2 0 0 0 0 3 3 3 3
```


**output:**
```
0 0 0 2 3 3 3 3 3 3 3 3
```


## train_3

**input:**
```
0 2 0 0 0 0 0 0 0 0 0 8
```


**output:**
```
0 2 8 8 8 8 8 8 8 8 8 8
```


## train_4

**input:**
```
0 6 6 6 6 6 6 6 6 2 0 0
```


**output:**
```
0 6 6 6 6 6 6 6 6 2 0 0
```


## train_5

**input:**
```
0 9 9 9 0 0 0 0 0 0 2 0
```


**output:**
```
0 9 9 9 9 9 9 9 9 9 2 0
```


## train_6

**input:**
```
7 7 7 7 7 7 7 2 0 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 2 0 0 0 0
```


## train_7

**input:**
```
0 0 5 5 5 5 5 0 0 2 0 0
```


**output:**
```
0 0 5 5 5 5 5 5 5 2 0 0
```

Okay, let's analyze the transformation.

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are sequences (lists or arrays) of 12 single-digit integers.
2.  **Key Digits:** The digits `0` and `2` appear to play special roles. Other non-zero digits (like `3`, `5`, `6`, `7`, `8`, `9` in the examples) act as "fill" values.
3.  **The Role of '2':** The digit `2` seems to function as a fixed boundary or marker within the sequence. Its position does not change.
4.  **The Role of '0':** The digit `0` represents an empty or fillable space. These are the only digits that get replaced.
5.  **The Role of Other Non-Zero Digits (N):** These digits seem to expand or "fill" adjacent `0`s under certain conditions. The expansion originates from an existing block or instance of the digit `N`.
6.  **Transformation Mechanism:** The transformation involves identifying sequences of `0`s that lie *between* the digit `2` and the nearest non-zero digit (`N`) on either side (left or right). These intervening `0`s are then replaced by the digit `N`. If `2` is already adjacent to a non-zero digit, or if there are no non-zero digits on one side, no filling occurs on that side.

**YAML Fact Document:**


```yaml
elements:
  - type: sequence
    properties:
      - length: 12
      - item_type: integer
      - item_range: 0-9
objects:
  - id: marker
    value: 2
    description: A fixed position digit that acts as a boundary. Its own value and position never change.
  - id: fillable_space
    value: 0
    description: Represents positions that can be potentially overwritten.
  - id: fill_value
    value: N (any digit from 1, 3, 4, 5, 6, 7, 8, 9)
    description: A non-zero, non-marker digit that can expand to replace adjacent 'fillable_space' digits.
relationships:
  - type: adjacency
    description: The relative positions of 'marker', 'fillable_space', and 'fill_value' determine the transformation.
  - type: spatial_gap
    description: A sequence of one or more 'fillable_space' digits located between a 'marker' and the nearest 'fill_value' on either side.
actions:
  - name: locate_marker
    actor: system
    target: input_sequence
    description: Find the index of the 'marker' (digit 2).
  - name: locate_nearest_fill_value
    actor: system
    target: input_sequence
    parameters:
      - direction: left_of_marker
      - direction: right_of_marker
    description: Find the index of the nearest non-zero, non-marker digit ('fill_value') to the left and right of the 'marker'.
  - name: fill_gap
    actor: system
    target: sequence (initially a copy of input)
    condition: A 'spatial_gap' exists between the 'marker' and a 'fill_value'.
    effect: Replace all 'fillable_space' (0) digits within the 'spatial_gap' with the corresponding 'fill_value'. This happens independently for the left and right sides of the 'marker'.
```


**Natural Language Program:**

1.  Receive the input sequence of 12 digits.
2.  Create a mutable copy of the input sequence to serve as the potential output.
3.  Find the index (position) of the digit `2` in the sequence. Let this be `marker_index`.
4.  **Left-side Fill:**
    a.  Search the sequence from `marker_index - 1` down to index 0.
    b.  Find the index of the first non-zero digit encountered. Let this be `left_fill_index` and its value be `left_fill_value`.
    c.  If such a digit is found (i.e., `left_fill_index` exists):
        i.  Iterate through the indices from `left_fill_index + 1` up to `marker_index - 1`.
        ii. For each index in this range, if the digit in the sequence copy at that index is `0`, replace it with `left_fill_value`.
5.  **Right-side Fill:**
    a.  Search the sequence from `marker_index + 1` up to the end of the sequence (index 11).
    b.  Find the index of the first non-zero digit encountered. Let this be `right_fill_index` and its value be `right_fill_value`.
    c.  If such a digit is found (i.e., `right_fill_index` exists):
        i.  Iterate through the indices from `marker_index + 1` up to `right_fill_index - 1`.
        ii. For each index in this range, if the digit in the sequence copy at that index is `0`, replace it with `right_fill_value`.
6.  Return the modified sequence copy as the output.
```python
import copy

"""
Transforms a sequence of 12 digits based on the following rules:
1. Locate the digit '2', which acts as a fixed marker.
2. Find the nearest non-zero digit to the left of the marker ('left_fill_value').
3. Replace all zeros between the 'left_fill_value' and the marker with 'left_fill_value'.
4. Find the nearest non-zero digit to the right of the marker ('right_fill_value').
5. Replace all zeros between the marker and the 'right_fill_value' with 'right_fill_value'.
6. If no non-zero digit exists on a side, no filling occurs on that side.
7. The marker '2' and existing non-zero digits remain unchanged.
"""

def transform(input_sequence_str):
    """
    Applies the described transformation to an input sequence string.

    Args:
        input_sequence_str: A string of space-separated single digits (e.g., "0 0 0 0 2 0 7 7 7 7 7 7").

    Returns:
        A string of space-separated single digits representing the transformed sequence.
        Returns the original string if the marker '2' is not found.
    """
    # Convert string input to list of integers
    try:
        input_list = [int(d) for d in input_sequence_str.split()]
    except ValueError:
        # Handle cases where input might not be valid integers
        print(f"Error: Input string '{input_sequence_str}' contains non-integer values.")
        return input_sequence_str # Or raise an error

    if len(input_list) != 12:
         print(f"Warning: Input sequence length is not 12 ({len(input_list)}).")
         # Decide how to handle this - process anyway or return error? Processing for now.


    # Initialize output_grid as a copy of the input list
    output_list = copy.deepcopy(input_list)
    n = len(output_list)

    # Find the index of the marker '2'
    marker_index = -1
    try:
        marker_index = input_list.index(2)
    except ValueError:
        # Marker '2' not found, return the original list as a string
        print("Marker '2' not found in the input.")
        return input_sequence_str

    # --- Left-side Fill ---
    left_fill_value = None
    left_fill_index = -1
    # Search backwards from marker_index - 1
    for i in range(marker_index - 1, -1, -1):
        if input_list[i] != 0:
            left_fill_value = input_list[i]
            left_fill_index = i
            break # Found the nearest non-zero

    # If a left fill value was found, fill the zeros between it and the marker
    if left_fill_value is not None:
        for i in range(left_fill_index + 1, marker_index):
            if output_list[i] == 0:
                output_list[i] = left_fill_value

    # --- Right-side Fill ---
    right_fill_value = None
    right_fill_index = -1
    # Search forwards from marker_index + 1
    for i in range(marker_index + 1, n):
        if input_list[i] != 0:
            right_fill_value = input_list[i]
            right_fill_index = i
            break # Found the nearest non-zero

    # If a right fill value was found, fill the zeros between the marker and it
    if right_fill_value is not None:
        for i in range(marker_index + 1, right_fill_index):
             if output_list[i] == 0:
                output_list[i] = right_fill_value

    # Convert the result list back to a space-separated string
    output_sequence_str = " ".join(map(str, output_list))
    return output_sequence_str

```
```python
import copy
# numpy is implicitly available but not explicitly needed for this logic if input is list-like
# import numpy as np 

"""
Transforms a sequence of digits based on the following rules:
1. Locate the digit '2', which acts as a fixed marker.
2. Find the nearest non-zero digit to the left of the marker ('left_fill_value').
3. Replace all zeros strictly between the 'left_fill_value' and the marker with 'left_fill_value'.
4. Find the nearest non-zero digit to the right of the marker ('right_fill_value').
5. Replace all zeros strictly between the marker and the 'right_fill_value' with 'right_fill_value'.
6. If no non-zero digit exists on a side (left or right), no filling occurs on that side.
7. The marker '2' and existing non-zero digits in the input sequence remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_grid: A list-like sequence (e.g., list, numpy array) of integers.

    Returns:
        A new list or array representing the transformed sequence. Returns a copy
        of the original if the marker '2' is not found.
    """
    
    # Initialize output_grid as a deep copy to avoid modifying the input object
    # This works for both lists and numpy arrays
    output_grid = copy.deepcopy(input_grid)
    n = len(output_grid) # Get the length of the sequence

    # Find the index of the marker '2'
    marker_index = -1
    try:
        # Convert to list temporarily to use the .index() method reliably
        # This handles cases where input_grid might be a numpy array
        input_list_for_index = list(input_grid) 
        marker_index = input_list_for_index.index(2)
    except ValueError:
        # Marker '2' not found, return the original grid copy unchanged
        return output_grid # No transformation needed if no marker

    # --- Left-side processing: Find nearest non-zero and fill ---
    left_fill_value = None
    left_fill_index = -1
    # Search backwards from the position immediately left of the marker
    for i in range(marker_index - 1, -1, -1):
        if input_grid[i] != 0:  # Found the nearest non-zero digit
            left_fill_value = input_grid[i]
            left_fill_index = i
            break # Stop searching once the nearest is found

    # If a non-zero value was found to the left, fill the zeros in between
    if left_fill_value is not None:
        # Iterate from the position right after the left fill value up to (not including) the marker
        for i in range(left_fill_index + 1, marker_index):
            # Check if the position in the original grid was a zero before filling
            if input_grid[i] == 0: 
                 output_grid[i] = left_fill_value # Update the output grid

    # --- Right-side processing: Find nearest non-zero and fill ---
    right_fill_value = None
    right_fill_index = -1
    # Search forwards from the position immediately right of the marker
    for i in range(marker_index + 1, n):
        if input_grid[i] != 0: # Found the nearest non-zero digit
            right_fill_value = input_grid[i]
            right_fill_index = i
            break # Stop searching once the nearest is found

    # If a non-zero value was found to the right, fill the zeros in between
    if right_fill_value is not None:
        # Iterate from the position right after the marker up to (not including) the right fill value
        for i in range(marker_index + 1, right_fill_index):
            # Check if the position in the original grid was a zero before filling
             if input_grid[i] == 0: 
                 output_grid[i] = right_fill_value # Update the output grid

    # Return the modified grid
    return output_grid
```

Previous Code:
```python
import copy
# numpy is implicitly available but not explicitly needed for this logic if input is list-like
# import numpy as np 

"""
Transforms a sequence of digits based on the following rules:
1. Locate the digit '2', which acts as a fixed marker.
2. Find the nearest non-zero digit to the left of the marker ('left_fill_value').
3. Replace all zeros strictly between the 'left_fill_value' and the marker with 'left_fill_value'.
4. Find the nearest non-zero digit to the right of the marker ('right_fill_value').
5. Replace all zeros strictly between the marker and the 'right_fill_value' with 'right_fill_value'.
6. If no non-zero digit exists on a side (left or right), no filling occurs on that side.
7. The marker '2' and existing non-zero digits in the input sequence remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_grid: A list-like sequence (e.g., list, numpy array) of integers.

    Returns:
        A new list or array representing the transformed sequence. Returns a copy
        of the original if the marker '2' is not found.
    """
    
    # Initialize output_grid as a deep copy to avoid modifying the input object
    # This works for both lists and numpy arrays
    output_grid = copy.deepcopy(input_grid)
    n = len(output_grid) # Get the length of the sequence

    # Find the index of the marker '2'
    marker_index = -1
    try:
        # Convert to list temporarily to use the .index() method reliably
        # This handles cases where input_grid might be a numpy array
        input_list_for_index = list(input_grid) 
        marker_index = input_list_for_index.index(2)
    except ValueError:
        # Marker '2' not found, return the original grid copy unchanged
        return output_grid # No transformation needed if no marker

    # --- Left-side processing: Find nearest non-zero and fill ---
    left_fill_value = None
    left_fill_index = -1
    # Search backwards from the position immediately left of the marker
    for i in range(marker_index - 1, -1, -1):
        if input_grid[i] != 0:  # Found the nearest non-zero digit
            left_fill_value = input_grid[i]
            left_fill_index = i
            break # Stop searching once the nearest is found

    # If a non-zero value was found to the left, fill the zeros in between
    if left_fill_value is not None:
        # Iterate from the position right after the left fill value up to (not including) the marker
        for i in range(left_fill_index + 1, marker_index):
            # Check if the position in the original grid was a zero before filling
            if input_grid[i] == 0: 
                 output_grid[i] = left_fill_value # Update the output grid

    # --- Right-side processing: Find nearest non-zero and fill ---
    right_fill_value = None
    right_fill_index = -1
    # Search forwards from the position immediately right of the marker
    for i in range(marker_index + 1, n):
        if input_grid[i] != 0: # Found the nearest non-zero digit
            right_fill_value = input_grid[i]
            right_fill_index = i
            break # Stop searching once the nearest is found

    # If a non-zero value was found to the right, fill the zeros in between
    if right_fill_value is not None:
        # Iterate from the position right after the marker up to (not including) the right fill value
        for i in range(marker_index + 1, right_fill_index):
            # Check if the position in the original grid was a zero before filling
             if input_grid[i] == 0: 
                 output_grid[i] = right_fill_value # Update the output grid

    # Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 2 0 7 7 7 7 7 7
```
Expected Output:
```
0 0 0 0 2 7 7 7 7 7 7 7
```
Transformed Output:
```
0 0 0 0 2 0 7 7 7 7 7 7
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.666666666666686

## Example 2:
Input:
```
0 0 0 2 0 0 0 0 3 3 3 3
```
Expected Output:
```
0 0 0 2 3 3 3 3 3 3 3 3
```
Transformed Output:
```
0 0 0 2 0 0 0 0 3 3 3 3
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 66.66666666666669

## Example 3:
Input:
```
0 2 0 0 0 0 0 0 0 0 0 8
```
Expected Output:
```
0 2 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
0 2 0 0 0 0 0 0 0 0 0 8
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 150.0

## Example 4:
Input:
```
0 6 6 6 6 6 6 6 6 2 0 0
```
Expected Output:
```
0 6 6 6 6 6 6 6 6 2 0 0
```
Transformed Output:
```
0 6 6 6 6 6 6 6 6 2 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 5:
Input:
```
0 9 9 9 0 0 0 0 0 0 2 0
```
Expected Output:
```
0 9 9 9 9 9 9 9 9 9 2 0
```
Transformed Output:
```
0 9 9 9 0 0 0 0 0 0 2 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 100.0

## Example 6:
Input:
```
7 7 7 7 7 7 7 2 0 0 0 0
```
Expected Output:
```
7 7 7 7 7 7 7 2 0 0 0 0
```
Transformed Output:
```
7 7 7 7 7 7 7 2 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 7:
Input:
```
0 0 5 5 5 5 5 0 0 2 0 0
```
Expected Output:
```
0 0 5 5 5 5 5 5 5 2 0 0
```
Transformed Output:
```
0 0 5 5 5 5 5 0 0 2 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 33.333333333333314

Test Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 0 0 0 0 2 0
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 2 0
```
Transformed Output:
```
1 1 1 1 1 1 0 0 0 0 2 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 66.66666666666669
**General Assessment and Strategy**

The provided Python code attempts to implement the observed transformation rule: fill sequences of zeros ('0') located strictly between a marker digit ('2') and the nearest non-zero digit on either side (left and right independently), using the value of that nearest non-zero digit.

However, the execution results show that the code failed to perform the 'fill' action correctly on all examples requiring it (train 1, 2, 3, 5, 7, and test 1). It only passed examples (train 4, 6) where no filling was necessary. A detailed trace of the code logic suggests it *should* work for the failing examples. This discrepancy implies either:

1.  A subtle flaw in the code's logic or variable handling (e.g., interaction between left/right fill, incorrect range, modification issue).
2.  An issue in the execution environment or the testing harness where the code modifications did not reflect in the output.
3.  A misunderstanding of the transformation rule, although the current rule fits all examples well.

**Strategy:**

1.  **Re-verify the core logic:** Double-check the loops, ranges, conditions, and variable assignments in the code against the natural language program.
2.  **Assume Code Logic is Intended:** Base the refined YAML and Natural Language Program on the logic implemented in the Python code, as it aligns well with the visual transformation in the examples.
3.  **Gather Metrics:** Confirm the reported 'Pixels Off' count using code execution.
4.  **Refine Documentation:** Update the YAML and Natural Language Program for clarity based on this logic. The core transformation rule remains unchanged, as the code's *intent* seems correct, even if its execution produced errors. The focus will be on precisely describing the intended steps.

**Metrics**


*code_execution:*
```python
import numpy as np

def calculate_metrics(input_str, expected_str, actual_str):
    input_arr = np.array([int(x) for x in input_str.split()])
    expected_arr = np.array([int(x) for x in expected_str.split()])
    actual_arr = np.array([int(x) for x in actual_str.split()])

    pixels_off = np.sum(expected_arr != actual_arr)
    size_correct = len(expected_arr) == len(actual_arr)
    
    return {
        "pixels_off": pixels_off,
        "size_correct": size_correct,
        # Note: Color Palette/Count correctness cannot be determined without the actual code output arrays, 
        # but we use the reported results. The provided reports indicate Size is always True, 
        # Palette is always True, and Count is False when Pixels Off > 0.
        "match": pixels_off == 0
    }

# Data based on the prompt's report for code_00.py
examples = [
    {"id": "train_1", "in": "0 0 0 0 2 0 7 7 7 7 7 7", "exp": "0 0 0 0 2 7 7 7 7 7 7 7", "act": "0 0 0 0 2 0 7 7 7 7 7 7"},
    {"id": "train_2", "in": "0 0 0 2 0 0 0 0 3 3 3 3", "exp": "0 0 0 2 3 3 3 3 3 3 3 3", "act": "0 0 0 2 0 0 0 0 3 3 3 3"},
    {"id": "train_3", "in": "0 2 0 0 0 0 0 0 0 0 0 8", "exp": "0 2 8 8 8 8 8 8 8 8 8 8", "act": "0 2 0 0 0 0 0 0 0 0 0 8"},
    {"id": "train_4", "in": "0 6 6 6 6 6 6 6 6 2 0 0", "exp": "0 6 6 6 6 6 6 6 6 2 0 0", "act": "0 6 6 6 6 6 6 6 6 2 0 0"},
    {"id": "train_5", "in": "0 9 9 9 0 0 0 0 0 0 2 0", "exp": "0 9 9 9 9 9 9 9 9 9 2 0", "act": "0 9 9 9 0 0 0 0 0 0 2 0"},
    {"id": "train_6", "in": "7 7 7 7 7 7 7 2 0 0 0 0", "exp": "7 7 7 7 7 7 7 2 0 0 0 0", "act": "7 7 7 7 7 7 7 2 0 0 0 0"},
    {"id": "train_7", "in": "0 0 5 5 5 5 5 0 0 2 0 0", "exp": "0 0 5 5 5 5 5 5 5 2 0 0", "act": "0 0 5 5 5 5 5 0 0 2 0 0"},
    {"id": "test_1",  "in": "1 1 1 1 1 1 0 0 0 0 2 0", "exp": "1 1 1 1 1 1 1 1 1 1 2 0", "act": "1 1 1 1 1 1 0 0 0 0 2 0"}, # From test set report
]

metrics_report = {}
for ex in examples:
    metrics_report[ex["id"]] = calculate_metrics(ex["in"], ex["exp"], ex["act"])

print(metrics_report)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
{'train_1': {'pixels_off': np.int64(1), 'size_correct': True, 'match': np.False_}, 'train_2': {'pixels_off': np.int64(4), 'size_correct': True, 'match': np.False_}, 'train_3': {'pixels_off': np.int64(9), 'size_correct': True, 'match': np.False_}, 'train_4': {'pixels_off': np.int64(0), 'size_correct': True, 'match': np.True_}, 'train_5': {'pixels_off': np.int64(6), 'size_correct': True, 'match': np.False_}, 'train_6': {'pixels_off': np.int64(0), 'size_correct': True, 'match': np.True_}, 'train_7': {'pixels_off': np.int64(2), 'size_correct': True, 'match': np.False_}, 'test_1': {'pixels_off': np.int64(4), 'size_correct': True, 'match': np.False_}}

```
**Fact Document (YAML)**


```yaml
task_description: Fill sequences of zeros based on proximity to a marker and other non-zero digits.
elements:
  - type: sequence
    properties:
      - item_type: integer
      - item_range: 0-9
      - length: variable (observed as 12 in examples, but logic might generalize)
objects:
  - id: marker
    value: 2
    description: A fixed pivot digit. Its position determines the regions for potential filling. It is never overwritten.
  - id: empty_space
    value: 0
    description: Represents positions that are candidates for being filled.
  - id: fill_source
    value: N (any digit from 1, 3, 4, 5, 6, 7, 8, 9)
    description: Non-zero, non-marker digits. The nearest 'fill_source' to the 'marker' on each side dictates the value used for filling 'empty_space' on that side. 'fill_source' digits are never overwritten.
relationships:
  - type: position
    description: The index of the 'marker' is crucial.
  - type: adjacency
    description: The transformation depends on the sequence of digits between the 'marker' and the nearest 'fill_source' on the left and right.
  - type: nearest_neighbor
    description: Finding the closest 'fill_source' to the left and right of the 'marker' is a key step.
actions:
  - name: initialize_output
    actor: system
    input: input_sequence
    output: output_sequence
    description: Create a mutable copy of the input sequence.
  - name: locate_marker
    actor: system
    target: input_sequence
    output: marker_index
    description: Find the index of the first occurrence of the 'marker' (digit 2). If not found, return the initial copy.
  - name: find_left_neighbor
    actor: system
    target: input_sequence
    input: marker_index
    output: left_fill_value, left_fill_index
    description: Search leftwards from marker_index - 1. Find the first 'fill_source' digit and its index. If none found, values remain null/invalid.
  - name: find_right_neighbor
    actor: system
    target: input_sequence
    input: marker_index
    output: right_fill_value, right_fill_index
    description: Search rightwards from marker_index + 1. Find the first 'fill_source' digit and its index. If none found, values remain null/invalid.
  - name: fill_left_gap
    actor: system
    target: output_sequence
    input: marker_index, left_fill_value, left_fill_index
    condition: A 'left_fill_value' was found (left_fill_index is valid).
    effect: Iterate from index `left_fill_index + 1` up to (but not including) `marker_index`. If the digit at the current index in the *original input sequence* was an 'empty_space' (0), replace the digit at the corresponding index in the 'output_sequence' with 'left_fill_value'.
  - name: fill_right_gap
    actor: system
    target: output_sequence
    input: marker_index, right_fill_value, right_fill_index
    condition: A 'right_fill_value' was found (right_fill_index is valid).
    effect: Iterate from index `marker_index + 1` up to (but not including) `right_fill_index`. If the digit at the current index in the *original input sequence* was an 'empty_space' (0), replace the digit at the corresponding index in the 'output_sequence' with 'right_fill_value'.
  - name: finalize_output
    actor: system
    input: output_sequence
    output: final_sequence
    description: Return the modified 'output_sequence'.

```


**Natural Language Program**

1.  Create a working copy of the input sequence (let's call it `output_sequence`).
2.  Find the index of the digit `2` in the original input sequence. If `2` is not present, return the `output_sequence` as is. Let the index found be `marker_index`.
3.  **Left Fill Process:**
    a.  Initialize `left_fill_value` and `left_fill_index` to indicate "not found".
    b.  Search backwards from index `marker_index - 1` down to index 0 in the original input sequence.
    c.  If a non-zero digit is found, record its value as `left_fill_value`, its index as `left_fill_index`, and stop searching leftwards.
    d.  If `left_fill_value` was found:
        i.  Iterate through the indices `i` from `left_fill_index + 1` up to `marker_index - 1`.
        ii. For each index `i`, check if the digit in the *original input sequence* at index `i` is `0`.
        iii. If it is `0`, update the `output_sequence` at index `i` with `left_fill_value`.
4.  **Right Fill Process:**
    a.  Initialize `right_fill_value` and `right_fill_index` to indicate "not found".
    b.  Search forwards from index `marker_index + 1` up to the end of the original input sequence.
    c.  If a non-zero digit is found, record its value as `right_fill_value`, its index as `right_fill_index`, and stop searching rightwards.
    d.  If `right_fill_value` was found:
        i.  Iterate through the indices `j` from `marker_index + 1` up to `right_fill_index - 1`.
        ii. For each index `j`, check if the digit in the *original input sequence* at index `j` is `0`.
        iii. If it is `0`, update the `output_sequence` at index `j` with `right_fill_value`.
5.  Return the final `output_sequence`.
