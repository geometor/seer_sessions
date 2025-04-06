```python
import collections

"""
For each input row (list of integers):
1. Store the value of the first element.
2. Create a new list containing all non-zero elements from the second position 
   to the end of the input row, maintaining their original relative order.
3. Construct the output row by starting with the stored first element.
4. Append the list of non-zero elements (from step 2) immediately after the 
   first element.
5. Append zeros to the end of the output row until its length matches the length
   of the original input row.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms each row of the input grid by moving all non-zero elements 
    (except the first) to the left, immediately following the first element,
    and padding the rest with zeros.
    """
    output_grid = [] # Initialize the output grid

    # Process each row individually
    for input_row in input_grid:
        # Handle empty rows if necessary, though examples don't show them
        if not input_row:
            output_grid.append([])
            continue

        # 1. Store the value of the first element.
        first_element = input_row[0]
        original_length = len(input_row)

        # 2. Create a list containing all non-zero elements from the second 
        #    position onwards, maintaining relative order.
        non_zeros_after_first = [
            element for element in input_row[1:] if element != 0
        ]

        # 3. Construct the output row starting with the stored first element.
        new_row = [first_element]

        # 4. Append the list of non-zero elements.
        new_row.extend(non_zeros_after_first)

        # 5. Append zeros until the length matches the original input row length.
        padding_zeros_count = original_length - len(new_row)
        new_row.extend([0] * padding_zeros_count)

        # Add the transformed row to the output grid
        output_grid.append(new_row)

    return output_grid
```