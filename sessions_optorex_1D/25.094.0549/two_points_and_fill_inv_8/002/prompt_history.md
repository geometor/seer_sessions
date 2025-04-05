
## train_1

**input:**
```
0 0 0 0 0 0 1 1 1 0 0 0
```


**output:**
```
0 0 0 0 0 0 1 0 1 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 2 2 2 2 2 2 2
```


**output:**
```
0 0 0 0 0 2 0 0 0 0 0 2
```


## train_3

**input:**
```
0 6 6 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 4 4 4 4 0 0 0 0 0 0 0
```


**output:**
```
0 4 0 0 4 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 4 4 4 4 4 4 4 4 4 4 4
```


**output:**
```
0 4 0 0 0 0 0 0 0 0 0 4
```


## train_6

**input:**
```
0 0 0 0 2 2 2 2 2 2 0 0
```


**output:**
```
0 0 0 0 2 0 0 0 0 2 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 7 7 7 0 0 0
```


**output:**
```
0 0 0 0 0 0 7 0 7 0 0 0
```

Okay, let's analyze the input-output pairs to understand the transformation.

**Perception of Elements and Transformation:**

1.  **Input/Output Structure:** Both inputs and outputs are sequences (lists or arrays) of single-digit integers. The length of the output sequence is always the same as the length of the input sequence.
2.  **Key Element:** The core transformation seems to operate on contiguous blocks (runs) of identical non-zero numbers.
3.  **Role of Zeros:** Zeroes (`0`) appear to act as delimiters or background elements. They generally remain unchanged unless they are part of the transformation applied to a non-zero block. However, based on the examples, the transformation specifically targets the *interior* of non-zero blocks, leaving the surrounding zeros untouched.
4.  **Transformation Logic:**
    *   Identify contiguous runs of the *same* non-zero digit. Let's call the digit `d` (where `d > 0`) and the length of the run `L`.
    *   If `L` is 1 or 2, the run remains unchanged in the output. (See train\_3: `[6, 6]` -> `[6, 6]`).
    *   If `L` is greater than 2, the first and last elements of the run remain `d`, but all elements *between* the first and the last are changed to `0`. (See train\_1: `[1, 1, 1]` -> `[1, 0, 1]`; train\_4: `[4, 4, 4, 4]` -> `[4, 0, 0, 4]`; train\_2: `[2, 2, 2, 2, 2, 2, 2]` -> `[2, 0, 0, 0, 0, 0, 2]`).
5.  **Multiple Runs:** The transformation applies independently to each distinct run of non-zero digits within the sequence.

**YAML Facts:**


```yaml
task_description: Modifying interior elements of contiguous non-zero runs in a sequence.
elements:
  - name: sequence
    type: list of integers (0-9)
    role: input and output structure
  - name: non_zero_run
    type: contiguous sub-sequence
    properties:
      - all elements are the same non-zero digit
      - bounded by zeros or sequence ends
    role: primary object of transformation
  - name: zero_element
    type: integer
    value: 0
    role: delimiter, generally preserved
  - name: run_length
    type: integer
    role: property determining the action on a non_zero_run
actions:
  - name: identify_runs
    input: input_sequence
    output: list of non_zero_runs (with start/end indices and value)
  - name: modify_run
    input: non_zero_run
    condition: run_length > 2
    effect: change all elements except the first and last to 0
  - name: preserve_run
    input: non_zero_run
    condition: run_length <= 2
    effect: keep the run unchanged
  - name: preserve_zeros
    input: zero_elements in input_sequence
    effect: keep zero elements unchanged in the output sequence
relationships:
  - input sequence length equals output sequence length
  - transformation is applied independently to each non_zero_run
  - output sequence is constructed by applying modifications/preservations to runs and preserving original zeros
```


**Natural Language Program:**

1.  Initialize an output sequence as a copy of the input sequence.
2.  Iterate through the input sequence to identify the start and end indices of each contiguous run of identical non-zero digits.
3.  For each identified run:
    a.  Determine the length of the run.
    b.  If the length of the run is greater than 2:
        i.  Iterate through the indices from the second element (`start_index + 1`) up to, but not including, the last element (`end_index`).
        ii. For each index in this range, set the corresponding element in the *output* sequence to 0.
4.  Return the final output sequence.
```python
import copy

def transform(input_sequence):
    """
    Modifies a sequence of integers by identifying contiguous runs of the same 
    non-zero digit. If a run has a length greater than 2, all elements 
    between the first and last element of the run are changed to 0. Runs of 
    length 1 or 2, and all zero elements, remain unchanged.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    
    # Initialize output_sequence as a copy of the input to preserve original zeros 
    # and runs that don't meet the length criteria.
    output_sequence = copy.deepcopy(input_sequence)
    n = len(input_sequence)
    i = 0
    
    # Iterate through the sequence to find runs of non-zero numbers
    while i < n:
        # Skip over zeros or start of a potential run
        if input_sequence[i] == 0:
            i += 1
            continue
        
        # Found a non-zero number, mark the start of a potential run
        start_index = i
        current_value = input_sequence[i]
        
        # Find the end of the contiguous run of the same non-zero number
        j = i + 1
        while j < n and input_sequence[j] == current_value:
            j += 1
            
        # The run ends at index j-1
        end_index = j - 1
        run_length = end_index - start_index + 1
        
        # Check if the run length is greater than 2
        if run_length > 2:
            # Modify the output sequence: set interior elements of the run to 0
            for k in range(start_index + 1, end_index):
                output_sequence[k] = 0
                
        # Move the main iterator past the processed run
        i = j 
        
    # Return the modified sequence
    return output_sequence

```
