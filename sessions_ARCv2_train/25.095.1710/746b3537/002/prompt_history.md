
## train_1

**input:**
```
2 2
6 6
8 8
8 8
```


**output:**
```
2
6
8
```


## train_2

**input:**
```
3 4 6
3 4 6
3 4 6
```


**output:**
```
3 4 6
```


## train_3

**input:**
```
2 3 3 8 1
2 3 3 8 1
2 3 3 8 1
```


**output:**
```
2 3 8 1
```


## train_4

**input:**
```
4 4 4 4
4 4 4 4
2 2 2 2
2 2 2 2
8 8 8 8
3 3 3 3
```


**output:**
```
4
2
8
3
```


## train_5

**input:**
```
1 1 1
2 2 2
1 1 1
```


**output:**
```
1
2
1
```

Okay, let's break down the task based on the provided examples.

**Perception of Task Elements:**

1.  **Input Structure:** The input consists of multiple lines of text. Each line contains one or more space-separated integers.
2.  **Output Structure:** The output also consists of multiple lines of text. Each output line corresponds directly to an input line. Each output line contains space-separated integers.
3.  **Transformation:** The core transformation appears to operate on each line independently. Within each line, duplicate numbers are removed. The order of the *first* appearance of each unique number is preserved.
4.  **Example Walkthrough (train_3):**
    *   Input line: `2 3 3 8 1`
    *   Process:
        *   See `2`. Keep it. Seen: `{2}`. Result: `[2]`
        *   See `3`. Keep it. Seen: `{2, 3}`. Result: `[2, 3]`
        *   See `3`. It's already seen. Ignore it. Seen: `{2, 3}`. Result: `[2, 3]`
        *   See `8`. Keep it. Seen: `{2, 3, 8}`. Result: `[2, 3, 8]`
        *   See `1`. Keep it. Seen: `{2, 3, 8, 1}`. Result: `[2, 3, 8, 1]`
    *   Output line: `2 3 8 1`

**YAML Facts:**


```yaml
task_description: "Remove duplicate numbers within each line while preserving the order of the first occurrence."
input_format:
  type: multiline_text
  line_content: space_separated_integers
output_format:
  type: multiline_text
  line_content: space_separated_integers
processing_granularity: line_by_line
line_transformation:
  action: deduplicate_ordered
  elements: integers
  details: "Iterate through numbers in the input line. Keep a number only if it hasn't been seen before in that specific line. Maintain the original relative order of the kept numbers."
relationship: "Each output line is the deduplicated version of the corresponding input line."
```


**Natural Language Program:**


```
1. Read the input line by line.
2. For each input line:
   a. Initialize an empty list called `unique_numbers_in_order`.
   b. Initialize an empty set called `seen_numbers`.
   c. Split the input line into a sequence of individual numbers.
   d. Iterate through this sequence of numbers.
   e. For each number encountered:
      i. Check if this number is present in the `seen_numbers` set.
      ii. If the number is NOT in `seen_numbers`:
          - Add the number to the `unique_numbers_in_order` list.
          - Add the number to the `seen_numbers` set.
   f. Join the numbers in the `unique_numbers_in_order` list back together with single spaces to form the output line string.
   g. Record this output line string.
3. Combine all the recorded output line strings, ensuring each is on a new line, to produce the final output.
```
```python
import collections

"""
Processes a grid of numbers (represented as a list of lists) by removing duplicate numbers within each inner list (row) while preserving the original order of the first occurrence of each number.
"""

def deduplicate_ordered_list(data_list: list[int]) -> list[int]:
    """
    Removes duplicate integers from a list while preserving the order of the first occurrence.

    Args:
        data_list: A list of integers.

    Returns:
        A new list containing only the unique integers from the input list,
        in the order they first appeared.
    """
    seen = set()
    result = []
    # Iterate through the input list
    for item in data_list:
        # Check if the item has been seen before in this list
        if item not in seen:
            # If not seen, add it to the result list
            result.append(item)
            # Mark the item as seen
            seen.add(item)
    return result

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by applying ordered deduplication to each row.

    Args:
        input_grid: A list of lists, where each inner list contains integers.
                    Represents the input lines, pre-parsed into numbers.

    Returns:
        A list of lists, where each inner list is the ordered, deduplicated
        version of the corresponding input row.
    """
    # Initialize the output grid which will store the processed rows
    output_grid = []

    # Iterate through each row (inner list) in the input grid
    for row in input_grid:
        # Apply the ordered deduplication logic to the current row
        # using the helper function
        deduplicated_row = deduplicate_ordered_list(row)
        # Add the processed row to the output grid
        output_grid.append(deduplicated_row)

    # Return the grid containing all the processed rows
    return output_grid

```
