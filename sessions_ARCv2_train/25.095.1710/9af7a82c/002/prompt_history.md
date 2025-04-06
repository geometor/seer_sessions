
## train_1

**input:**
```
8 8 2
3 8 8
3 3 4
3 3 4
```


**output:**
```
3 8 4 2
3 8 4 0
3 8 0 0
3 8 0 0
3 0 0 0
```


## train_2

**input:**
```
3 1 1 4
2 2 2 4
4 4 4 4
```


**output:**
```
4 2 1 3
4 2 1 0
4 2 0 0
4 0 0 0
4 0 0 0
4 0 0 0
```


## train_3

**input:**
```
1 1 1
2 2 1
2 8 1
2 8 1
```


**output:**
```
1 2 8
1 2 8
1 2 0
1 2 0
1 0 0
1 0 0
```


## train_4

**input:**
```
2 2 1
2 3 1
1 1 1
```


**output:**
```
1 2 3
1 2 0
1 2 0
1 0 0
1 0 0
```

Okay, let's break down the transformation.

**Perception of Task Elements**

The input is a grid of integers. The output is also a grid of integers, but typically with different dimensions than the input. The transformation seems to involve analyzing the frequency of non-zero numbers in the input grid and using this frequency information to construct the output grid.

1.  **Input Analysis:** The core operation involves identifying all unique non-zero numbers present in the entire input grid and counting how many times each appears.
2.  **Ordering:** The unique non-zero numbers seem to determine the columns of the output grid. Their order in the output columns is based on their frequency (count) in the input grid, arranged from most frequent to least frequent.
3.  **Output Grid Construction:**
    *   The number of columns in the output grid equals the number of unique non-zero integers found in the input.
    *   The number of rows in the output grid depends on the maximum frequency of any single number and potentially the dimensions of the input grid.
    *   Each column in the output corresponds to one of the unique non-zero input numbers (ordered by frequency). The column is populated vertically with that number, repeating it a number of times equal to its frequency count (with a potential modification in one specific case related to input dimensions). The remaining rows in that column are filled with zeros.
4.  **Special Conditions:** There appear to be adjustments based on the input grid's dimensions:
    *   The count for the *smallest* unique non-zero number is incremented if the input grid has more columns than rows.
    *   The total number of rows in the output grid seems to be `max_count + 1`, unless the input grid has 4 columns, in which case it's `max_count + 2`.

**Facts (YAML)**


```python
import collections
import itertools

"""
Transforms an input grid of integers into an output grid based on the frequency of non-zero numbers in the input.

1.  **Count Frequencies:** Count the occurrences of each unique non-zero integer in the entire input grid.
2.  **Determine Column Order:** Identify the unique non-zero integers. Sort these integers in descending order based on their frequency count. This sorted list determines the order of columns in the output grid.
3.  **Adjust Counts (Conditional):**
    *   If the input grid has more columns than rows, find the smallest unique non-zero integer present in the input and increment its frequency count by 1.
4.  **Determine Output Dimensions:**
    *   The number of columns in the output grid is equal to the number of unique non-zero integers found in the input.
    *   Calculate the maximum frequency count among all unique non-zero integers (after potential adjustment).
    *   The number of rows in the output grid is `max_count + 1`, unless the input grid has exactly 4 columns, in which case the number of rows is `max_count + 2`.
5.  **Construct Output Grid:**
    *   Initialize an output grid with the calculated dimensions, filled with zeros.
    *   Iterate through the sorted unique non-zero integers (from step 2). For each integer:
        *   Fill the corresponding column in the output grid from top to bottom with that integer.
        *   The number of times the integer is placed in the column is equal to its (potentially adjusted) frequency count.
        *   The remaining cells in that column below the filled integers remain zero.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on non-zero integer frequencies.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A list of lists representing the transformed output grid.
    """
    if not input_grid or not input_grid[0]:
        return [] # Handle empty input

    num_input_rows = len(input_grid)
    num_input_cols = len(input_grid[0])

    # 1. Count Frequencies
    # Flatten the grid and count non-zero elements
    all_elements = list(itertools.chain.from_iterable(input_grid))
    counts = collections.Counter(el for el in all_elements if el != 0)

    if not counts:
        # Handle input grid with only zeros or empty
         # Determine output rows based on rules even if counts are zero initially
        max_count = 0
        num_output_rows = max_count + 1
        if num_input_cols == 4:
            num_output_rows = max_count + 2
        # If no non-zeros, output should likely be empty columns or based on row count?
        # Based on examples, seems like columns require non-zeros. Return empty grid.
        return []


    # 2. Determine Column Order (Sort by frequency descending, then number ascending for ties)
    # Get unique non-zero numbers sorted primarily by count (desc) and secondarily by value (asc)
    sorted_unique_numbers = sorted(counts.keys(), key=lambda x: (-counts[x], x))

    # 3. Adjust Counts (Conditional)
    if num_input_cols > num_input_rows:
        # Find the smallest unique non-zero number
        if sorted_unique_numbers: # Ensure there are non-zero numbers
             min_num = min(counts.keys())
             counts[min_num] += 1 # Increment its count


    # 4. Determine Output Dimensions
    # Recalculate max_count after potential adjustment
    max_count = 0
    if counts:
         max_count = max(counts.values())

    num_output_rows = max_count + 1
    # Special case for input with 4 columns
    if num_input_cols == 4:
        num_output_rows = max_count + 2

    num_output_cols = len(sorted_unique_numbers)

    # 5. Construct Output Grid
    # Initialize output grid with zeros
    output_grid = [[0] * num_output_cols for _ in range(num_output_rows)]

    # Fill the output grid column by column based on sorted numbers and their counts
    for col_index, number in enumerate(sorted_unique_numbers):
        count = counts[number]
        for row_index in range(count):
             # Ensure we don't write past the allocated rows
             if row_index < num_output_rows:
                output_grid[row_index][col_index] = number

    return output_grid
```
