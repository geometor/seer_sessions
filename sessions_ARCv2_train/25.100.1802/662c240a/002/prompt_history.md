
## train_1

**input:**
```
2 2 2
2 2 3
2 3 3
5 7 7
7 5 5
7 5 5
8 8 1
1 8 1
1 8 1
```


**output:**
```
8 8 1
1 8 1
1 8 1
```


## train_2

**input:**
```
1 5 5
5 1 1
5 1 1
3 3 3
3 6 3
3 6 6
7 7 7
7 2 2
7 2 2
```


**output:**
```
3 3 3
3 6 3
3 6 6
```


## train_3

**input:**
```
8 8 4
4 4 4
4 4 8
1 1 3
1 3 3
3 3 1
6 2 2
2 2 2
2 2 6
```


**output:**
```
8 8 4
4 4 4
4 4 8
```


## train_4

**input:**
```
8 9 8
9 8 8
8 8 8
2 2 1
2 2 1
1 1 2
4 4 4
4 4 3
3 3 3
```


**output:**
```
4 4 4
4 4 3
3 3 3
```

*   **Perception of Task Elements:**
    *   The input data consists of 9 lines, each containing three space-separated integers.
    *   The input can be conceptually divided into three contiguous blocks of 3 lines each (Lines 1-3, 4-6, 7-9).
    *   The output data consists of exactly one of these 3-line blocks.
    *   Each 3-line block in the input appears to be constructed using only two distinct integer values among the nine integers present in that block.
    *   The core task is to identify which of the three input blocks should be selected as the output.
    *   The selection logic seems based on the frequency distribution of the two unique integers within each block. Specifically, the target block has one integer appearing 5 times and the other 4 times.
    *   A tie-breaking rule is necessary when multiple blocks satisfy this frequency condition. The tie-breaker appears to involve the sum of the two unique integers characterising the block.

*   **YAML Facts:**
    
```yaml
    Objects:
      - Input:
          Properties:
            - Lines: A list of 9 text lines.
            - Blocks: A list of 3 Blocks, derived by grouping Lines.
      - Line:
          Properties:
            - Integers: A list of 3 integers.
      - Block:
          Properties:
            - Lines: A list of 3 Lines.
            - AllIntegers: A list of 9 integers (concatenated from its Lines).
            - UniqueIntegers: A set of 2 distinct integers present in AllIntegers.
            - FrequencyCounts: A mapping of each UniqueInteger to its count in AllIntegers.
            - IsTargetFrequency: A boolean indicating if FrequencyCounts are {5, 4}.
            - UniqueIntegerSum: The sum of the 2 UniqueIntegers.
      - Output:
          Properties:
            - Lines: A list of 3 text lines, identical to the Lines of the selected Block.

    Relationships:
      - An Input is composed of 9 Lines.
      - An Input is divided into 3 Blocks.
      - A Block is composed of 3 Lines.
      - A Block contains 9 Integers derived from its Lines.
      - A Block is characterized by 2 UniqueIntegers and their FrequencyCounts.
      - The Output corresponds to exactly one Block from the Input.

    Actions:
      - Parse: Convert input text lines into lists of integers.
      - Group: Divide the 9 input Lines into 3 Blocks.
      - Analyze Block:
          - Identify the 2 UniqueIntegers within a Block's 9 integers.
          - Calculate the FrequencyCounts for these UniqueIntegers.
          - Determine if FrequencyCounts match the target pattern {5, 4}.
          - Calculate the UniqueIntegerSum for the block.
      - Filter: Identify all Blocks where IsTargetFrequency is true.
      - Select:
          - If only one Block is filtered, choose it.
          - If multiple Blocks are filtered, choose the one with the maximum UniqueIntegerSum.
      - Format Output: Present the Lines of the selected Block as the final output.
    ```


*   **Natural Language Program:**
    1.  Divide the 9 input lines into three blocks: Block 1 (lines 1-3), Block 2 (lines 4-6), and Block 3 (lines 7-9).
    2.  For each block, determine the two unique integer values present across its three lines (total 9 integers).
    3.  For each block, count the occurrences of each of its two unique integers.
    4.  Identify all blocks where one unique integer appears exactly 5 times and the other unique integer appears exactly 4 times.
    5.  If exactly one block satisfies condition (4), select that block.
    6.  If multiple blocks satisfy condition (4), calculate the sum of the two unique integers for each of these blocks. Select the block for which this sum is the largest.
    7.  Output the three lines corresponding to the selected block.
```python
import collections
from typing import List, Tuple, Dict, Any

"""
The transformation rule selects one of three contiguous 3x3 blocks from a 9x3 input grid. 
The selection criteria are based on the frequency distribution of the two unique integer values within each block.

1.  Divide the 9x3 input grid into three 3x3 blocks (rows 1-3, 4-6, 7-9).
2.  For each 3x3 block:
    a.  Identify the two unique integer values present among its 9 integers.
    b.  Count the occurrences of each unique integer.
    c.  Determine if one integer appears exactly 5 times and the other appears exactly 4 times. Mark this block as a "candidate" if it meets this frequency condition.
    d.  Calculate the sum of the two unique integers for the block.
3.  Identify all candidate blocks from step 2c.
4.  If there is only one candidate block, select it as the output.
5.  If there are multiple candidate blocks, select the candidate block where the sum of its two unique integers (calculated in step 2d) is the largest.
6.  Return the selected 3x3 block.
"""

def analyze_block(block: List[List[int]]) -> Dict[str, Any]:
    """
    Analyzes a 3x3 block to find unique integers, their counts, sum, and qualifying status.

    Args:
        block: A list of 3 lists, each containing 3 integers (a 3x3 block).

    Returns:
        A dictionary containing analysis results:
        - 'block': The original input block.
        - 'is_qualifying': Boolean, true if counts are {4, 5}.
        - 'unique_sum': The sum of the two unique integers (0 if not qualifying or not exactly 2 unique).
        - 'unique_integers': Tuple of the two unique integers, or None.
        - 'counts': Dictionary mapping unique integers to their counts, or None.
    """
    # Flatten the block into a single list of 9 integers
    all_integers = [num for row in block for num in row]

    # Count the frequency of each integer
    counts = collections.Counter(all_integers)
    unique_integers = list(counts.keys())

    # Initialize results
    is_qualifying = False
    unique_sum = 0
    result_unique_integers = None
    result_counts = None

    # Check if there are exactly two unique integers
    if len(unique_integers) == 2:
        # Get the two unique integers and their counts
        val1, val2 = unique_integers
        count1, count2 = counts[val1], counts[val2]
        result_unique_integers = tuple(sorted(unique_integers)) # Store consistently
        result_counts = dict(counts)

        # Check if the counts are 4 and 5 (in any order)
        if {count1, count2} == {4, 5}:
            is_qualifying = True
            unique_sum = val1 + val2

    return {
        'block': block,
        'is_qualifying': is_qualifying,
        'unique_sum': unique_sum,
        'unique_integers': result_unique_integers,
        'counts': result_counts
    }


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Selects a 3x3 block from the 9x3 input grid based on unique integer frequencies.

    Args:
        input_grid: A list of 9 lists, each containing 3 integers.

    Returns:
        A list of 3 lists, each containing 3 integers, representing the selected block.
        Returns an empty list if no qualifying block is found or input is invalid.
    """
    # Ensure input grid has the correct dimensions
    if len(input_grid) != 9 or not all(len(row) == 3 for row in input_grid):
        # Or raise an error, depending on desired behavior for invalid input
        print("Warning: Input grid dimensions are not 9x3.")
        return [] 

    # 1. Divide the input grid into three 3x3 blocks
    blocks = [
        input_grid[0:3],
        input_grid[3:6],
        input_grid[6:9]
    ]

    # 2. Analyze each block
    analysis_results = [analyze_block(block) for block in blocks]

    # 3. Filter for candidate blocks (those meeting the frequency condition)
    candidate_blocks = [result for result in analysis_results if result['is_qualifying']]

    # Handle cases based on the number of candidate blocks
    if not candidate_blocks:
        # No block qualifies - return empty or handle as error
        print("Warning: No qualifying block found.")
        return [] # Or raise ValueError("No qualifying block found")
    elif len(candidate_blocks) == 1:
        # 4. If exactly one candidate block, select it
        selected_block_result = candidate_blocks[0]
    else:
        # 5. If multiple candidates, select the one with the maximum unique integer sum
        selected_block_result = max(candidate_blocks, key=lambda r: r['unique_sum'])

    # 6. Return the selected 3x3 block
    return selected_block_result['block']

```
