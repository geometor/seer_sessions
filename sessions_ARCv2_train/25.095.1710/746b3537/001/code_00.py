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
