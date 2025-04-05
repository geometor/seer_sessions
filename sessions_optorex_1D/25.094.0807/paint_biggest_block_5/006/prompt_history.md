
## train_1

**input:**
```
0 0 6 6 6 6 0 0 0 6 6 0
```


**output:**
```
0 0 1 1 1 1 0 0 0 6 6 0
```


## train_2

**input:**
```
5 5 5 5 0 0 0 5 5 5 0 0
```


**output:**
```
1 1 1 1 0 0 0 5 5 5 0 0
```


## train_3

**input:**
```
0 8 8 8 8 8 0 0 0 0 8 8
```


**output:**
```
0 1 1 1 1 1 0 0 0 0 8 8
```


## train_4

**input:**
```
0 3 3 3 3 0 3 3 3 3 3 3
```


**output:**
```
0 3 3 3 3 0 1 1 1 1 1 1
```


## train_5

**input:**
```
2 2 0 0 0 0 0 0 2 2 2 0
```


**output:**
```
2 2 0 0 0 0 0 0 1 1 1 0
```


## train_6

**input:**
```
6 6 6 6 0 0 0 6 6 6 0 0
```


**output:**
```
1 1 1 1 0 0 0 6 6 6 0 0
```


## train_7

**input:**
```
3 3 0 3 3 3 3 0 0 0 0 0
```


**output:**
```
3 3 0 1 1 1 1 0 0 0 0 0
```

**Perception of Task Elements:**

The task involves transforming a sequence of integers into another sequence of the same length. The core operation appears to be identifying and modifying a specific contiguous subsequence within the input. The modification replaces the original numbers in the identified subsequence with the number `1`. The selection criteria for the subsequence seem to be based on it being composed of identical, non-zero numbers and being the *longest* such subsequence. If multiple subsequences share the maximum length, the one appearing earliest (leftmost) in the sequence is chosen for modification. Other parts of the sequence remain unchanged.

**YAML Facts:**


```yaml
objects:
  - name: input_sequence
    type: List[int]
    description: The sequence of integers provided as input.
  - name: output_sequence
    type: List[int]
    description: The sequence of integers resulting from the transformation.
  - name: subsequence
    type: List[int]
    description: A contiguous part of the input sequence.
    properties:
      - homogeneity: All elements are identical.
      - non_zero: The identical element is not zero.
      - length: The number of elements in the subsequence.
      - start_index: The position where the subsequence begins in the input_sequence.
      - value: The identical non-zero integer value of the elements.

actions:
  - name: identify_subsequences
    description: Find all contiguous subsequences in the input_sequence where all elements are identical and non-zero.
    inputs: input_sequence
    outputs: List[subsequence]
  - name: find_longest_subsequence
    description: Determine the maximum length among the identified subsequences. If multiple subsequences share the maximum length, select the one with the smallest start_index.
    inputs: List[subsequence]
    outputs: subsequence (the target subsequence)
  - name: replace_subsequence
    description: Create the output_sequence by copying the input_sequence, then replace the elements corresponding to the target subsequence with the integer 1.
    inputs:
      - input_sequence
      - target_subsequence
    outputs: output_sequence

relationships:
  - The output_sequence has the same length as the input_sequence.
  - The transformation targets only one specific subsequence within the input_sequence based on length and position.
  - Elements outside the target subsequence remain unchanged between input and output.
```


**Natural Language Program:**

1.  **Scan** the input sequence to identify all contiguous subsequences composed of identical, non-zero integer values. Record their value, length, and starting index.
2.  **Determine** the maximum length found among these identified subsequences.
3.  **Select** the subsequence that matches this maximum length. If there are multiple subsequences with the same maximum length, choose the one that appears first (i.e., has the lowest starting index).
4.  **Initialize** the output sequence as a copy of the input sequence.
5.  **Modify** the output sequence by replacing the elements corresponding to the selected subsequence (using its starting index and length) with the integer `1`.
6.  **Return** the modified sequence as the output.
```python
import math
from typing import List, Dict, Tuple, Optional

"""
Transforms an input sequence of integers by identifying all contiguous subsequences 
composed of identical, non-zero values. Among these subsequences, it finds the one(s) 
with the maximum length. If multiple subsequences share the maximum length, it selects 
the one that appears earliest (leftmost) in the original sequence. The elements of this 
selected subsequence are then replaced with the integer 1 in the output sequence, while 
all other elements remain unchanged.
"""

def find_all_homogeneous_nonzero_subsequences(sequence: List[int]) -> List[Dict]:
    """
    Finds all contiguous subsequences of identical, non-zero values.

    Args:
        sequence: The input list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a subsequence
        and contains 'value', 'start_index', and 'length'. Returns an empty
        list if no such subsequences are found.
    """
    subsequences = []
    if not sequence:
        return subsequences

    n = len(sequence)
    i = 0
    while i < n:
        current_val = sequence[i]
        # Skip zeros or start of a new potential subsequence
        if current_val == 0:
            i += 1
            continue

        # Found a non-zero value, start checking for a homogeneous subsequence
        start_index = i
        j = i + 1
        while j < n and sequence[j] == current_val:
            j += 1

        # Length of the subsequence found
        length = j - start_index

        # Record the subsequence if its length is >= 1 (it always will be here)
        if length >= 1:
             subsequences.append({
                 'value': current_val,
                 'start_index': start_index,
                 'length': length
             })

        # Move the main pointer past the subsequence we just processed
        i = j

    return subsequences


def transform(input_list: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: The sequence of integers provided as input.

    Returns:
        The sequence of integers resulting from the transformation.
    """
    # 1. Scan the input sequence to identify all contiguous subsequences
    #    composed of identical, non-zero integer values.
    identified_subsequences = find_all_homogeneous_nonzero_subsequences(input_list)

    # If no such subsequences exist, return the original list
    if not identified_subsequences:
        return list(input_list) # Return a copy

    # 2. Determine the maximum length found among these identified subsequences.
    max_length = 0
    for sub in identified_subsequences:
        if sub['length'] > max_length:
            max_length = sub['length']

    # 3. Select the subsequence that matches this maximum length.
    #    If there are multiple, choose the one with the lowest starting index.
    longest_subsequences = []
    for sub in identified_subsequences:
        if sub['length'] == max_length:
            longest_subsequences.append(sub)

    # Sort by start_index to easily find the first one
    longest_subsequences.sort(key=lambda x: x['start_index'])
    target_subsequence = longest_subsequences[0]

    # 4. Initialize the output sequence as a copy of the input sequence.
    output_list = list(input_list)

    # 5. Modify the output sequence by replacing the elements corresponding
    #    to the selected subsequence with the integer 1.
    start = target_subsequence['start_index']
    length = target_subsequence['length']
    for i in range(start, start + length):
        output_list[i] = 1

    # 6. Return the modified sequence as the output.
    return output_list

```
```python
import math
from typing import List, Dict, Tuple, Optional

"""
Transforms an input sequence of integers by performing the following steps:
1.  Identify Candidates: Scan the input sequence from left to right. Find all contiguous subsequences where every element is the same non-zero integer. For each such subsequence found, record its value, its starting index, and its length.
2.  Check for Candidates: If no such subsequences were found in step 1, the transformation is complete, and the output sequence is identical to the input sequence. Proceed to step 6.
3.  Find Max Length: Determine the maximum length among all the candidate subsequences identified in step 1.
4.  Select Target: Filter the candidate subsequences to keep only those that have the maximum length determined in step 3. From this filtered list, select the single subsequence that has the smallest starting index (i.e., the one that appears earliest in the original input sequence). This is the *target* subsequence.
5.  Transform Sequence: Create the output sequence by starting with a copy of the input sequence. Then, modify this copied sequence by replacing the elements corresponding to the *target* subsequence (identified by its start index and length) with the integer `1`.
6.  Return Output: Return the resulting sequence (either the modified sequence from step 5 or the original sequence if no candidates were found in step 2).
"""

def find_all_homogeneous_nonzero_subsequences(sequence: List[int]) -> List[Dict]:
    """
    Finds all contiguous subsequences of identical, non-zero values.

    Args:
        sequence: The input list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a subsequence
        and contains 'value', 'start_index', and 'length'. Returns an empty
        list if no such subsequences are found.
    """
    subsequences = []
    if not sequence:
        return subsequences

    n = len(sequence)
    i = 0
    while i < n:
        current_val = sequence[i]
        # Skip zeros or start of a new potential subsequence
        if current_val == 0:
            i += 1
            continue

        # Found a non-zero value, start checking for a homogeneous subsequence
        start_index = i
        j = i + 1
        while j < n and sequence[j] == current_val:
            j += 1

        # Length of the subsequence found
        length = j - start_index

        # Record the subsequence
        subsequences.append({
            'value': current_val,
            'start_index': start_index,
            'length': length
        })

        # Move the main pointer past the subsequence we just processed
        i = j

    return subsequences


def transform(input_list: List[int]) -> List[int]:
    # 1. Identify Candidates: Scan the input sequence and find all contiguous
    #    subsequences where every element is the same non-zero integer.
    candidate_subsequences = find_all_homogeneous_nonzero_subsequences(input_list)

    # 2. Check for Candidates: If no such subsequences were found, return a copy
    #    of the original list.
    if not candidate_subsequences:
        return list(input_list) # Return a copy

    # 3. Find Max Length: Determine the maximum length among candidates.
    max_length = 0
    for sub in candidate_subsequences:
        if sub['length'] > max_length:
            max_length = sub['length']

    # 4. Select Target: Filter candidates to keep only those with max length,
    #    then select the one with the smallest start index.
    longest_subsequences = []
    for sub in candidate_subsequences:
        if sub['length'] == max_length:
            longest_subsequences.append(sub)

    # Sort by start_index to easily find the earliest one
    longest_subsequences.sort(key=lambda x: x['start_index'])
    target_subsequence = longest_subsequences[0] # The target is the first after sorting

    # 5. Transform Sequence: Create the output sequence by copying the input,
    #    then modify the target subsequence elements to 1.
    output_list = list(input_list) # Start with a copy

    start = target_subsequence['start_index']
    length = target_subsequence['length']
    for i in range(start, start + length):
        output_list[i] = 1

    # 6. Return Output: Return the modified sequence.
    return output_list

```
```python
import math
from typing import List, Dict, Tuple, Optional

"""
Transforms an input sequence of integers by performing the following steps:
1.  Identify Candidates: Scan the input sequence from left to right. Find all contiguous subsequences where every element is the same non-zero integer. For each such subsequence found, record its value, its starting index, and its length.
2.  Check for Candidates: If no such subsequences were found in step 1, the transformation is complete, and the output sequence is identical to the input sequence. Proceed to step 6.
3.  Find Max Length: Determine the maximum length among all the candidate subsequences identified in step 1.
4.  Select Target: Filter the candidate subsequences to keep only those that have the maximum length determined in step 3. From this filtered list, select the single subsequence that has the smallest starting index (i.e., the one that appears earliest in the original input sequence). This is the *target* subsequence.
5.  Transform Sequence: Create the output sequence by starting with a copy of the input sequence. Then, modify this copied sequence by replacing the elements corresponding to the *target* subsequence (identified by its start index and length) with the integer `1`.
6.  Return Output: Return the resulting sequence (either the modified sequence from step 5 or the original sequence if no candidates were found in step 2).
"""

def find_all_homogeneous_nonzero_subsequences(sequence: List[int]) -> List[Dict]:
    """
    Helper function: Finds all contiguous subsequences of identical, non-zero values.

    Args:
        sequence: The input list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a subsequence
        and contains 'value', 'start_index', and 'length'. Returns an empty
        list if no such subsequences are found.
    """
    subsequences = []
    if not sequence:
        return subsequences

    n = len(sequence)
    i = 0
    while i < n:
        current_val = sequence[i]
        # Skip zeros
        if current_val == 0:
            i += 1
            continue

        # Found a non-zero value, start checking for a homogeneous subsequence
        start_index = i
        j = i + 1
        while j < n and sequence[j] == current_val:
            j += 1

        # Length of the subsequence found
        length = j - start_index

        # Record the subsequence
        subsequences.append({
            'value': current_val,
            'start_index': start_index,
            'length': length
        })

        # Move the main pointer past the subsequence we just processed
        i = j

    return subsequences


def transform(input_list: List[int]) -> List[int]:
    # 1. Identify Candidates: Scan the input sequence and find all contiguous
    #    subsequences where every element is the same non-zero integer.
    candidate_subsequences = find_all_homogeneous_nonzero_subsequences(input_list)

    # 2. Check for Candidates: If no such subsequences were found, return a copy
    #    of the original list. (Step 6 is reached directly)
    if not candidate_subsequences:
        return list(input_list) # Return a copy

    # 3. Find Max Length: Determine the maximum length among candidates.
    max_length = 0
    for sub in candidate_subsequences:
        if sub['length'] > max_length:
            max_length = sub['length']
    
    # Alternative using max() for conciseness:
    # max_length = max(sub['length'] for sub in candidate_subsequences)

    # 4. Select Target: Filter candidates to keep only those with max length,
    #    then select the one with the smallest start index.
    longest_subsequences = []
    for sub in candidate_subsequences:
        if sub['length'] == max_length:
            longest_subsequences.append(sub)

    # Sort by start_index to easily find the earliest one
    # If only one exists, sorting doesn't change the outcome.
    longest_subsequences.sort(key=lambda x: x['start_index'])
    target_subsequence = longest_subsequences[0] # The target is the first after sorting

    # 5. Transform Sequence: Create the output sequence by copying the input,
    #    then modify the target subsequence elements to 1.
    output_list = list(input_list) # Start with a copy

    start = target_subsequence['start_index']
    length = target_subsequence['length']
    for i in range(start, start + length):
        output_list[i] = 1

    # 6. Return Output: Return the modified sequence.
    return output_list

```
