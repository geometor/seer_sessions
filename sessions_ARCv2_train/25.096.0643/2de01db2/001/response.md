```python
import collections

"""
For each row in the input grid:
1. Identify the 'primary' non-zero number. This is the non-zero number that appears most frequently in the row.
2. If there is a tie for the most frequent non-zero number, the smallest value among the tied numbers is chosen as the primary number.
3. Create a corresponding output row based on the following rules applied to each element of the input row:
    a. If the element is 0, replace it with the primary number.
    b. If the element is the primary number, replace it with 0.
    c. If the element is a non-zero number different from the primary number, replace it with the primary number.
4. Collect the transformed rows to form the output grid.
"""

def find_primary_number(row: list[int]) -> int | None:
    """
    Finds the primary non-zero number in a row based on frequency.
    Handles ties by selecting the smallest value among the most frequent.
    Returns None if the row contains no non-zero numbers.
    """
    # Filter out zeros and count frequencies of non-zero numbers
    non_zero_counts = collections.Counter(num for num in row if num != 0)

    if not non_zero_counts:
        # Handle rows with only zeros (or empty rows)
        return None # Or decide on a default behavior if needed

    # Find the maximum frequency
    max_freq = 0
    for num in non_zero_counts:
        if non_zero_counts[num] > max_freq:
            max_freq = non_zero_counts[num]

    # Find all numbers with the maximum frequency
    most_frequent_numbers = []
    for num in non_zero_counts:
        if non_zero_counts[num] == max_freq:
            most_frequent_numbers.append(num)

    # Determine the primary number (smallest value in case of a tie)
    primary_num = min(most_frequent_numbers)
    
    return primary_num

def transform_row(row: list[int], primary_num: int | None) -> list[int]:
    """Transforms a single row based on the primary number."""
    output_row = []
    # If no primary number was found (e.g., all zeros), return the row unchanged or as all zeros.
    # Based on the examples, it seems a primary number always exists. 
    # If it didn't, the transformation is undefined by the examples. Let's assume it always exists.
    if primary_num is None:
        # Assuming input rows always have non-zeros based on examples. 
        # If a row could be all zeros, this might need adjustment.
        # Perhaps return a row of zeros matching the input length?
        # For now, let's raise an error or return the row as is, though the logic below implicitly handles it if used.
         return [0] * len(row) # Default to zeros if no primary found

    for num in row:
        if num == 0:
            output_row.append(primary_num)
        elif num == primary_num:
            output_row.append(0)
        else: # Non-zero number different from the primary number
            output_row.append(primary_num)
    return output_row

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid row by row based on identifying and using a 'primary' number for each row.
    The primary number is the most frequent non-zero number (smallest value wins ties).
    Zeros are replaced by the primary number, the primary number is replaced by zero, 
    and other non-zeros are replaced by the primary number.
    """
    output_grid = [] # Initialize the output grid

    # Process each row independently
    for input_row in input_grid:
        # Find the primary number for the current row
        primary_num = find_primary_number(input_row)
        
        # Transform the row using the identified primary number
        # Note: Added handling in transform_row in case primary_num is None, 
        # although examples suggest it's always found.
        output_row = transform_row(input_row, primary_num)
        
        # Add the transformed row to the output grid
        output_grid.append(output_row)

    return output_grid

```