
## train_1

**input:**
```
0 2 2 0 0 0 0 0 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 2 0 2 2
```


## train_2

**input:**
```
7 7 7 7 0 0 7 0 0 7 7 0
```


**output:**
```
0 0 0 7 7 7 7 0 7 7 0 7
```


## train_3

**input:**
```
0 2 2 0 0 0 0 0 2 2 2 2
```


**output:**
```
0 0 0 0 0 2 2 2 2 0 2 2
```


## train_4

**input:**
```
0 0 0 0 9 9 9 9 0 0 0 9
```


**output:**
```
0 0 0 0 0 0 9 9 9 9 0 9
```


## train_5

**input:**
```
0 4 0 0 0 4 4 4 4 0 0 0
```


**output:**
```
0 0 0 0 0 0 4 4 4 4 0 4
```


## train_6

**input:**
```
0 0 0 0 0 6 0 0 0 6 6 0
```


**output:**
```
0 0 0 0 0 0 0 0 6 6 0 6
```


## train_7

**input:**
```
1 1 1 0 0 0 0 0 0 0 0 1
```


**output:**
```
0 0 0 0 0 0 0 1 1 1 0 1
```

Okay, analyzing the provided examples, here's my perception of the task:

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are sequences (lists) of single-digit non-negative integers. All examples have a fixed length of 12.
2.  **Key Entities:** The primary entities are the numbers within the sequence. They can be categorized into:
    *   Zeros (0)
    *   Non-zero numbers (e.g., 1, 2, 4, 6, 7, 9)
3.  **Structure:** The non-zero numbers often appear in contiguous groups or "blocks", separated by one or more zeros. Zeros also appear at the beginning and end of the sequence.
4.  **Transformation Goal:** The transformation rearranges the sequence. The non-zero blocks are moved towards the right end of the sequence. The number of zeros and non-zeros remains the same between input and output.
5.  **Core Action:** The core action is identifying these non-zero blocks, potentially reordering them based on a specific condition, and then packing them together at the right end, separated by single zeros, with leading zeros filling the remaining space.
6.  **Order Preservation/Reversal:** The relative order of the non-zero blocks from the input is generally preserved in the output *except* under a specific condition: if there are exactly two blocks and the first block consists of only a single number, the order of these two blocks is reversed in the output.
7.  **Separators:** When the blocks are placed in the output, they are separated by exactly one zero, regardless of how many zeros separated them in the input.

**YAML Facts:**


```yaml
task_description: Rearrange a sequence of numbers by consolidating non-zero blocks to the right end.
elements:
  - type: sequence
    properties:
      - content: single-digit non-negative integers
      - length: 12 (in examples)
  - type: number
    properties:
      - value: 0 (zero)
        role: separator, padding
      - value: non-zero (1-9)
        role: content_element
objects:
  - name: non_zero_block
    description: A contiguous subsequence of one or more non-zero numbers.
    properties:
      - length: number of elements in the block
      - content: sequence of non-zero numbers
      - original_position: order of appearance in the input sequence (1st, 2nd, etc.)
relationships:
  - type: separation
    between: non_zero_block
    by: one or more zeros in the input
    transformed_to: single zero separator in the output (if multiple blocks exist)
  - type: ordering
    of: non_zero_block
    in_output: Generally preserves original relative order, BUT reverses if exactly two blocks exist AND the first block has length 1.
actions:
  - name: identify_blocks
    input: input_sequence
    output: list of non_zero_blocks
  - name: determine_order
    input: list of non_zero_blocks
    output: ordered list of non_zero_blocks (potentially reversed)
    condition_for_reversal: count(blocks) == 2 AND length(first_block) == 1
  - name: construct_output
    input:
      - ordered list of non_zero_blocks
      - original_sequence_length
    output: output_sequence
    steps:
      - Concatenate blocks with single zero separators in between.
      - Calculate required padding zeros (original_length - length(concatenated_blocks_and_separators)).
      - Prepend padding zeros to the concatenated sequence.

```


**Natural Language Program:**

1.  Scan the input sequence from left to right.
2.  Identify all contiguous blocks (subsequences) consisting only of non-zero numbers. Keep track of these blocks and their original order of appearance.
3.  Determine the final order for placing these blocks in the output:
    *   Check if there are exactly two blocks identified in step 2.
    *   If yes, check if the first block (the one that appeared earliest in the input) contains only one number (has a length of 1).
    *   If both conditions are true (exactly two blocks AND the first block has length 1), reverse the order of the two blocks.
    *   Otherwise (if there are not exactly two blocks, or if the first of the two blocks has length greater than 1), maintain the original relative order of the blocks.
4.  Construct the core part of the output sequence by concatenating the blocks in the order determined in step 3. Insert a single zero between each consecutive block. (If there's only one block, no zeros are inserted here).
5.  Calculate the number of leading zeros needed: subtract the total length of the core part (blocks + separating zeros) from the total length of the original input sequence.
6.  Create the final output sequence by prepending the calculated number of leading zeros to the core part constructed in step 4.
```python
import math
import collections

# Helper function to identify non-zero blocks
def _identify_non_zero_blocks(sequence):
    """
    Identifies contiguous blocks of non-zero numbers in a sequence.

    Args:
        sequence: A list of numbers.

    Returns:
        A list of lists, where each inner list is a non-zero block.
    """
    blocks = []
    current_block = []
    in_block = False
    for num in sequence:
        if num != 0:
            if not in_block:
                in_block = True
                current_block = [num]
            else:
                current_block.append(num)
        else:
            if in_block:
                blocks.append(current_block)
                in_block = False
                current_block = []
    # Add the last block if the sequence ends with non-zeros
    if in_block:
        blocks.append(current_block)
    return blocks

def transform(input_sequence_str):
    """
    Rearranges a sequence of numbers by consolidating non-zero blocks to the 
    right end, separated by single zeros. The order of blocks is reversed 
    if there are exactly two blocks and the first block has a length of 1; 
    otherwise, the original relative order is maintained. Leading zeros 
    are used for padding.
    """
    # Convert input string to list of integers
    input_sequence = [int(x) for x in input_sequence_str.split()]
    original_length = len(input_sequence)

    # 1. & 2. Identify all contiguous blocks of non-zero numbers and their original order.
    blocks = _identify_non_zero_blocks(input_sequence)

    # 3. Determine the final order for placing these blocks.
    ordered_blocks = blocks
    if len(blocks) == 2 and len(blocks[0]) == 1:
        # Reverse the order of the two blocks
        ordered_blocks = blocks[::-1] # Slicing creates a reversed copy

    # 4. Construct the core part of the output sequence.
    core_output = []
    for i, block in enumerate(ordered_blocks):
        core_output.extend(block)
        # Add a single zero separator if this is not the last block
        if i < len(ordered_blocks) - 1:
            core_output.append(0)

    # 5. Calculate the number of leading zeros needed.
    core_length = len(core_output)
    padding_zeros_count = original_length - core_length

    # 6. Create the final output sequence.
    output_sequence = [0] * padding_zeros_count + core_output

    # Convert back to string format for output
    output_str = " ".join(map(str, output_sequence))
    
    return output_str

```
```python
"""
Rearranges a sequence of numbers (provided as a NumPy array) by consolidating 
contiguous non-zero blocks to the right end. The blocks are sorted by their 
length in descending order (stable sort) before being placed. Single zeros 
are used to separate the blocks in the output. Leading zeros are added to 
pad the sequence to match the original input length.
"""
import numpy as np

# Helper function to identify non-zero blocks
def _identify_non_zero_blocks(sequence):
    """
    Identifies contiguous blocks of non-zero numbers in a sequence.

    Args:
        sequence: A list or 1D NumPy array of numbers.

    Returns:
        A list of lists, where each inner list is a non-zero block.
    """
    # Convert numpy array to list for easier processing if needed
    if isinstance(sequence, np.ndarray):
        sequence = sequence.tolist()
        
    blocks = []
    current_block = []
    in_block = False
    for num in sequence:
        if num != 0:
            # Start or continue a block
            if not in_block:
                in_block = True
                current_block = [num]
            else:
                current_block.append(num)
        else:
            # End of a block (if currently in one)
            if in_block:
                blocks.append(current_block)
                in_block = False
                current_block = []
                
    # Add the last block if the sequence ends with non-zeros
    if in_block:
        blocks.append(current_block)
        
    return blocks

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input sequence according to the specified rules.
    """
    # 1. Receive input and determine original length
    input_sequence = input_grid # input is already a numpy array
    original_length = len(input_sequence)

    # 2. Identify all contiguous blocks of non-zero numbers
    blocks = _identify_non_zero_blocks(input_sequence)

    # 3. Sort the identified blocks by length in descending order (stable sort)
    # Python's sorted() is stable
    sorted_blocks = sorted(blocks, key=len, reverse=True)

    # 4. Construct the core part of the output sequence (blocks + separators)
    core_output = []
    num_blocks = len(sorted_blocks)
    for i, block in enumerate(sorted_blocks):
        core_output.extend(block)
        # Add a single zero separator if this is not the last block
        if i < num_blocks - 1:
            core_output.append(0)

    # 5. Calculate the number of leading zeros needed for padding
    core_length = len(core_output)
    padding_zeros_count = original_length - core_length

    # 6. Create the final output sequence by prepending padding zeros
    output_sequence = [0] * padding_zeros_count + core_output

    # 7. Return the final sequence as a NumPy array
    return np.array(output_sequence)

```
```python
"""
Rearranges a sequence of numbers (provided as a NumPy array) by consolidating 
contiguous non-zero blocks to the right end. The blocks are sorted by their 
length in descending order (stable sort) before being placed. Single zeros 
are used to separate the blocks in the output. Leading zeros are added to 
pad the sequence to match the original input length.
"""
import numpy as np

# Helper function to identify non-zero blocks
def _identify_non_zero_blocks(sequence):
    """
    Identifies contiguous blocks of non-zero numbers in a sequence.

    Args:
        sequence: A list or 1D NumPy array of numbers.

    Returns:
        A list of lists, where each inner list is a non-zero block.
    """
    # Convert numpy array to list for easier processing if needed
    if isinstance(sequence, np.ndarray):
        sequence = sequence.tolist()
        
    blocks = []
    current_block = []
    in_block = False
    for num in sequence:
        if num != 0:
            # Start or continue a block
            if not in_block:
                in_block = True
                current_block = [num]
            else:
                current_block.append(num)
        else:
            # End of a block (if currently in one)
            if in_block:
                blocks.append(current_block)
                in_block = False
                current_block = []
                
    # Add the last block if the sequence ends with non-zeros
    if in_block:
        blocks.append(current_block)
        
    return blocks

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input sequence according to the specified rules.
    """
    # 1. Receive input (already a NumPy array) and determine original length
    input_sequence = input_grid 
    original_length = len(input_sequence)

    # 2. Identify all contiguous blocks of non-zero numbers
    # The helper function preserves the content of each block.
    blocks = _identify_non_zero_blocks(input_sequence)

    # 3. Sort the identified blocks by length in descending order (stable sort)
    # Python's sorted() is stable, preserving relative order for equal lengths.
    sorted_blocks = sorted(blocks, key=len, reverse=True)

    # 4. Construct the core part of the output sequence (blocks + separators)
    core_output = []
    num_blocks = len(sorted_blocks)
    # Iterate through the sorted blocks.
    for i, block in enumerate(sorted_blocks):
        # Append the elements of the current block.
        core_output.extend(block)
        # If it's not the last block, append a single zero separator.
        if i < num_blocks - 1:
            core_output.append(0)

    # 5. Calculate the number of leading zeros needed for padding
    core_length = len(core_output)
    padding_zeros_count = original_length - core_length
    
    # Ensure padding count is not negative (e.g., if input was all zeros)
    padding_zeros_count = max(0, padding_zeros_count)

    # 6. Create the final output sequence by prepending padding zeros
    output_sequence = [0] * padding_zeros_count + core_output

    # 7. Return the final sequence as a NumPy array
    return np.array(output_sequence)
```

Previous Code:
```python
"""
Rearranges a sequence of numbers (provided as a NumPy array) by consolidating 
contiguous non-zero blocks to the right end. The blocks are sorted by their 
length in descending order (stable sort) before being placed. Single zeros 
are used to separate the blocks in the output. Leading zeros are added to 
pad the sequence to match the original input length.
"""
import numpy as np

# Helper function to identify non-zero blocks
def _identify_non_zero_blocks(sequence):
    """
    Identifies contiguous blocks of non-zero numbers in a sequence.

    Args:
        sequence: A list or 1D NumPy array of numbers.

    Returns:
        A list of lists, where each inner list is a non-zero block.
    """
    # Convert numpy array to list for easier processing if needed
    if isinstance(sequence, np.ndarray):
        sequence = sequence.tolist()
        
    blocks = []
    current_block = []
    in_block = False
    for num in sequence:
        if num != 0:
            # Start or continue a block
            if not in_block:
                in_block = True
                current_block = [num]
            else:
                current_block.append(num)
        else:
            # End of a block (if currently in one)
            if in_block:
                blocks.append(current_block)
                in_block = False
                current_block = []
                
    # Add the last block if the sequence ends with non-zeros
    if in_block:
        blocks.append(current_block)
        
    return blocks

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input sequence according to the specified rules.
    """
    # 1. Receive input (already a NumPy array) and determine original length
    input_sequence = input_grid 
    original_length = len(input_sequence)

    # 2. Identify all contiguous blocks of non-zero numbers
    # The helper function preserves the content of each block.
    blocks = _identify_non_zero_blocks(input_sequence)

    # 3. Sort the identified blocks by length in descending order (stable sort)
    # Python's sorted() is stable, preserving relative order for equal lengths.
    sorted_blocks = sorted(blocks, key=len, reverse=True)

    # 4. Construct the core part of the output sequence (blocks + separators)
    core_output = []
    num_blocks = len(sorted_blocks)
    # Iterate through the sorted blocks.
    for i, block in enumerate(sorted_blocks):
        # Append the elements of the current block.
        core_output.extend(block)
        # If it's not the last block, append a single zero separator.
        if i < num_blocks - 1:
            core_output.append(0)

    # 5. Calculate the number of leading zeros needed for padding
    core_length = len(core_output)
    padding_zeros_count = original_length - core_length
    
    # Ensure padding count is not negative (e.g., if input was all zeros)
    padding_zeros_count = max(0, padding_zeros_count)

    # 6. Create the final output sequence by prepending padding zeros
    output_sequence = [0] * padding_zeros_count + core_output

    # 7. Return the final sequence as a NumPy array
    return np.array(output_sequence)
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 2 2 0 0 0 0 0 2 2 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 2 2 0 2 2
```
Transformed Output:
```
0 2 2 0 0 0 0 0 2 2 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 50.0

## Example 2:
Input:
```
7 7 7 7 0 0 7 0 0 7 7 0
```
Expected Output:
```
0 0 0 7 7 7 7 0 7 7 0 7
```
Transformed Output:
```
7 7 7 7 0 0 7 0 0 7 7 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 66.66666666666667

## Example 3:
Input:
```
0 2 2 0 0 0 0 0 2 2 2 2
```
Expected Output:
```
0 0 0 0 0 2 2 2 2 0 2 2
```
Transformed Output:
```
0 2 2 0 0 0 0 0 2 2 2 2
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 50.0

## Example 4:
Input:
```
0 0 0 0 9 9 9 9 0 0 0 9
```
Expected Output:
```
0 0 0 0 0 0 9 9 9 9 0 9
```
Transformed Output:
```
0 0 0 0 9 9 9 9 0 0 0 9
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 33.33333333333334

## Example 5:
Input:
```
0 4 0 0 0 4 4 4 4 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 4 4 4 4 0 4
```
Transformed Output:
```
0 4 0 0 0 4 4 4 4 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 33.33333333333334

## Example 6:
Input:
```
0 0 0 0 0 6 0 0 0 6 6 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 6 6 0 6
```
Transformed Output:
```
0 0 0 0 0 6 0 0 0 6 6 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 33.33333333333334

## Example 7:
Input:
```
1 1 1 0 0 0 0 0 0 0 0 1
```
Expected Output:
```
0 0 0 0 0 0 0 1 1 1 0 1
```
Transformed Output:
```
1 1 1 0 0 0 0 0 0 0 0 1
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 50.0

Test Set Results:

## Example 1:
Input:
```
0 2 2 2 2 0 0 0 0 2 2 0
```
Expected Output:
```
0 0 0 0 0 2 2 2 2 0 2 2
```
Transformed Output:
```
0 2 2 2 2 0 0 0 0 2 2 0
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 83.33333333333334
**General Assessment and Strategy**

The previous execution attempt failed because the implemented code did not correctly reflect the transformation logic derived from the examples. The results showed the input was returned unchanged, indicating a flaw in the implementation of the rearrangement, likely related to using the wrong transformation hypothesis (sorting by length) or a bug preventing the modification.

Re-examining the input/output pairs reveals a consistent pattern:
1.  Identify contiguous blocks of non-zero numbers.
2.  Sort these blocks based on their length in descending order. A stable sort is crucial for blocks of equal length (preserving their original relative order).
3.  Reconstruct the sequence by placing the sorted blocks at the right end, separated by single zeros.
4.  Pad the beginning with the necessary number of zeros to match the original sequence length.

The strategy is to:
1.  Correctly implement the logic described above: block identification, stable sorting by length (descending), and reconstruction with zero separators and padding.
2.  Update the descriptive documents (YAML, natural language program) to accurately reflect this sorting-based transformation.
3.  Use code execution to gather metrics and verify the updated logic against all examples.

**Metrics Gathering**


*code_execution:*
```python
import collections
import numpy as np

def analyze_sequence(input_str, expected_output_str):
    """
    Identifies non-zero blocks, their lengths, counts, performs stable sort by length desc,
    reconstructs the output, and compares with the expected output.
    """
    # Use numpy for consistency with the expected final function signature
    sequence = np.array([int(x) for x in input_str.split()], dtype=int)
    expected_output = np.array([int(x) for x in expected_output_str.split()], dtype=int)
    original_length = len(sequence)

    # Identify blocks
    blocks = []
    current_block = []
    in_block = False
    indices = [] # Store start index for stability tie-breaking
    start_index = -1

    for i, num in enumerate(sequence):
        if num != 0:
            if not in_block:
                in_block = True
                current_block = [num]
                start_index = i
            else:
                current_block.append(num)
        else:
            if in_block:
                blocks.append(list(current_block)) # Store as list
                indices.append(start_index)
                in_block = False
                current_block = []
                start_index = -1
                
    if in_block:
        blocks.append(list(current_block)) # Store as list
        indices.append(start_index)

    block_lengths = [len(b) for b in blocks]
    block_count = len(blocks)
    
    # Combine blocks with their original start index for stable sorting
    indexed_blocks = list(zip(indices, blocks))
    
    # Stable sort: primary key = length (desc), secondary key = index (asc)
    sorted_indexed_blocks = sorted(indexed_blocks, key=lambda x: (-len(x[1]), x[0]))
    
    # Extract sorted blocks
    sorted_blocks = [block for index, block in sorted_indexed_blocks]
    
    # Reconstruct
    core_output = []
    num_sorted_blocks = len(sorted_blocks)
    for i, block in enumerate(sorted_blocks):
        core_output.extend(block)
        if i < num_sorted_blocks - 1:
            core_output.append(0) # Single zero separator

    padding_zeros_count = max(0, original_length - len(core_output))
    reconstructed_output_list = [0] * padding_zeros_count + core_output
    reconstructed_output = np.array(reconstructed_output_list, dtype=int)

    match = np.array_equal(reconstructed_output, expected_output)
    
    return {
        "input": input_str,
        "expected_output": expected_output_str,
        "blocks": blocks,
        "block_lengths": block_lengths,
        "block_count": block_count,
        "sorted_blocks_by_length_desc": sorted_blocks, # Content of blocks after sorting
        "reconstructed_output": " ".join(map(str, reconstructed_output)),
        "match": match
    }

# Analyze each training example
examples = [
    ("0 2 2 0 0 0 0 0 2 2 0 0", "0 0 0 0 0 0 0 2 2 0 2 2"),
    ("7 7 7 7 0 0 7 0 0 7 7 0", "0 0 0 7 7 7 7 0 7 7 0 7"),
    ("0 2 2 0 0 0 0 0 2 2 2 2", "0 0 0 0 0 2 2 2 2 0 2 2"),
    ("0 0 0 0 9 9 9 9 0 0 0 9", "0 0 0 0 0 0 9 9 9 9 0 9"),
    ("0 4 0 0 0 4 4 4 4 0 0 0", "0 0 0 0 0 0 4 4 4 4 0 4"),
    ("0 0 0 0 0 6 0 0 0 6 6 0", "0 0 0 0 0 0 0 0 6 6 0 6"),
    ("1 1 1 0 0 0 0 0 0 0 0 1", "0 0 0 0 0 0 0 1 1 1 0 1"),
]

analysis_results = []
print("--- Metrics Analysis ---")
for i, (inp, outp) in enumerate(examples):
    result = analyze_sequence(inp, outp)
    analysis_results.append(result)
    print(f"\nExample {i+1}:")
    print(f"  Input: {result['input']}")
    print(f"  Blocks: {result['blocks']}")
    print(f"  Block Lengths: {result['block_lengths']}")
    print(f"  Block Count: {result['block_count']}")
    print(f"  Sorted Blocks (len desc): {result['sorted_blocks_by_length_desc']}")
    print(f"  Reconstructed Output: {result['reconstructed_output']}")
    print(f"  Expected Output:      {result['expected_output']}")
    print(f"  Match: {result['match']}")

# Overall check
all_match = all(r['match'] for r in analysis_results)
print("\n--- Overall ---")
print(f"All examples match the 'stable sort by length desc' logic: {all_match}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Metrics Analysis ---

Example 1:
  Input: 0 2 2 0 0 0 0 0 2 2 0 0
  Blocks: [[np.int64(2), np.int64(2)], [np.int64(2), np.int64(2)]]
  Block Lengths: [2, 2]
  Block Count: 2
  Sorted Blocks (len desc): [[np.int64(2), np.int64(2)], [np.int64(2), np.int64(2)]]
  Reconstructed Output: 0 0 0 0 0 0 0 2 2 0 2 2
  Expected Output:      0 0 0 0 0 0 0 2 2 0 2 2
  Match: True

Example 2:
  Input: 7 7 7 7 0 0 7 0 0 7 7 0
  Blocks: [[np.int64(7), np.int64(7), np.int64(7), np.int64(7)], [np.int64(7)], [np.int64(7), np.int64(7)]]
  Block Lengths: [4, 1, 2]
  Block Count: 3
  Sorted Blocks (len desc): [[np.int64(7), np.int64(7), np.int64(7), np.int64(7)], [np.int64(7), np.int64(7)], [np.int64(7)]]
  Reconstructed Output: 0 0 0 7 7 7 7 0 7 7 0 7
  Expected Output:      0 0 0 7 7 7 7 0 7 7 0 7
  Match: True

Example 3:
  Input: 0 2 2 0 0 0 0 0 2 2 2 2
  Blocks: [[np.int64(2), np.int64(2)], [np.int64(2), np.int64(2), np.int64(2), np.int64(2)]]
  Block Lengths: [2, 4]
  Block Count: 2
  Sorted Blocks (len desc): [[np.int64(2), np.int64(2), np.int64(2), np.int64(2)], [np.int64(2), np.int64(2)]]
  Reconstructed Output: 0 0 0 0 0 2 2 2 2 0 2 2
  Expected Output:      0 0 0 0 0 2 2 2 2 0 2 2
  Match: True

Example 4:
  Input: 0 0 0 0 9 9 9 9 0 0 0 9
  Blocks: [[np.int64(9), np.int64(9), np.int64(9), np.int64(9)], [np.int64(9)]]
  Block Lengths: [4, 1]
  Block Count: 2
  Sorted Blocks (len desc): [[np.int64(9), np.int64(9), np.int64(9), np.int64(9)], [np.int64(9)]]
  Reconstructed Output: 0 0 0 0 0 0 9 9 9 9 0 9
  Expected Output:      0 0 0 0 0 0 9 9 9 9 0 9
  Match: True

Example 5:
  Input: 0 4 0 0 0 4 4 4 4 0 0 0
  Blocks: [[np.int64(4)], [np.int64(4), np.int64(4), np.int64(4), np.int64(4)]]
  Block Lengths: [1, 4]
  Block Count: 2
  Sorted Blocks (len desc): [[np.int64(4), np.int64(4), np.int64(4), np.int64(4)], [np.int64(4)]]
  Reconstructed Output: 0 0 0 0 0 0 4 4 4 4 0 4
  Expected Output:      0 0 0 0 0 0 4 4 4 4 0 4
  Match: True

Example 6:
  Input: 0 0 0 0 0 6 0 0 0 6 6 0
  Blocks: [[np.int64(6)], [np.int64(6), np.int64(6)]]
  Block Lengths: [1, 2]
  Block Count: 2
  Sorted Blocks (len desc): [[np.int64(6), np.int64(6)], [np.int64(6)]]
  Reconstructed Output: 0 0 0 0 0 0 0 0 6 6 0 6
  Expected Output:      0 0 0 0 0 0 0 0 6 6 0 6
  Match: True

Example 7:
  Input: 1 1 1 0 0 0 0 0 0 0 0 1
  Blocks: [[np.int64(1), np.int64(1), np.int64(1)], [np.int64(1)]]
  Block Lengths: [3, 1]
  Block Count: 2
  Sorted Blocks (len desc): [[np.int64(1), np.int64(1), np.int64(1)], [np.int64(1)]]
  Reconstructed Output: 0 0 0 0 0 0 0 1 1 1 0 1
  Expected Output:      0 0 0 0 0 0 0 1 1 1 0 1
  Match: True

--- Overall ---
All examples match the 'stable sort by length desc' logic: True

```
**YAML Facts**


```yaml
task_description: Rearrange a sequence of numbers by consolidating non-zero blocks to the right end, sorting them by length.
elements:
  - type: sequence
    properties:
      - content: single-digit non-negative integers
      - length: variable (12 in examples)
  - type: number
    properties:
      - value: 0 (zero)
        role: separator, padding
      - value: non-zero (1-9)
        role: content_element
objects:
  - name: non_zero_block
    description: A contiguous subsequence of one or more non-zero numbers.
    properties:
      - length: number of elements in the block
      - content: sequence of non-zero numbers
      - original_position: implicit start index or order of appearance in the input sequence
relationships:
  - type: separation
    between: non_zero_block
    by: one or more zeros in the input
    transformed_to: single zero separator in the output (only between blocks)
  - type: ordering
    of: non_zero_block
    in_output: Blocks are ordered based on their length in descending order. If blocks have the same length, their relative order from the input is preserved (stable sort).
actions:
  - name: identify_blocks
    input: input_sequence
    output: list of non_zero_blocks (preserving content and implicit original order)
  - name: sort_blocks
    input: list of non_zero_blocks
    output: ordered list of non_zero_blocks
    method: Stable sort by block length in descending order.
  - name: construct_output
    input:
      - sorted list of non_zero_blocks
      - original_sequence_length
    output: output_sequence
    steps:
      - Initialize an empty core list.
      - Iterate through the sorted blocks. Append each block's content to the core list.
      - If it is not the last block, append a single zero to the core list as a separator.
      - Calculate required padding zeros: original_length - length(core_list).
      - Prepend the padding zeros to the core list to create the final output sequence.

```


**Natural Language Program**

1.  Receive the input sequence of numbers. Note its total length.
2.  Scan the input sequence from left to right to identify all contiguous blocks (subsequences) consisting solely of non-zero numbers. Store these blocks, preserving the numbers within each block and implicitly noting their original relative order.
3.  Sort the identified blocks based on their length (number of elements) in descending order. If two or more blocks have the same length, maintain their original relative order (perform a stable sort).
4.  Create a new list, initially empty, to build the core part of the output.
5.  Iterate through the sorted blocks. For each block:
    *   Append all numbers from the current block to the core list.
    *   If this is not the last block in the sorted list, append a single zero (0) to the core list as a separator.
6.  Calculate the number of padding zeros required: subtract the length of the core list (containing sorted blocks and separators) from the original total length of the input sequence.
7.  Construct the final output sequence by creating a list of the calculated number of padding zeros and concatenating the core list to it.
8.  Return the final output sequence.
