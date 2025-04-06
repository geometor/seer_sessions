import collections # Note: collections is not strictly needed for this implementation, but kept from previous iteration.

"""
Processes a list of lists of integers. First, removes duplicates within each 
inner list (row) while preserving the order of the first occurrence. Second, 
filters these processed lists, keeping only those whose corresponding original 
input list was different from the immediately preceding original input list.
"""

def _deduplicate_ordered_list(data_list: list[int]) -> list[int]:
    """
    Removes duplicate integers from a list while preserving the order of the 
    first occurrence. Helper function for the main transform.

    Args:
        data_list: A list of integers (representing a row).

    Returns:
        A new list containing only the unique integers from the input list,
        in the order they first appeared.
    """
    seen = set()
    result = []
    # Iterate through the input list of numbers
    for item in data_list:
        # Check if the number has been seen before in this specific list
        if item not in seen:
            # If not seen, add it to the result list
            result.append(item)
            # Mark the number as seen for this list
            seen.add(item)
    return result

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a two-step transformation to the input grid:
    1. Intra-list deduplication: Removes duplicate numbers within each list, 
       preserving order.
    2. Inter-list filtering: Removes processed lists if their corresponding 
       original input list was identical to the immediately preceding 
       original input list.

    Args:
        input_grid: A list of lists, where each inner list contains integers.

    Returns:
        A list of lists, containing the transformed and filtered lists.
    """

    # Step 1: Process each input row (inner list) to remove duplicates
    # while preserving order. Store these processed rows.
    processed_grid = []
    for input_row in input_grid:
        deduplicated_row = _deduplicate_ordered_list(input_row)
        processed_grid.append(deduplicated_row)

    # Step 2: Filter the processed rows based on consecutive identical *original* rows.
    final_output_grid = []
    # Keep track of the previous *original* input row to detect consecutive duplicates
    previous_input_row = None

    # Iterate through the original input grid along with its index
    for i, current_input_row in enumerate(input_grid):
        # Get the corresponding processed row from the results of Step 1
        current_processed_row = processed_grid[i]

        # Determine if this processed row should be kept:
        # Keep if it's the very first row (index 0) OR
        # if the current *original* row is different from the previous *original* row.
        if i == 0 or current_input_row != previous_input_row:
            # If the condition is met, add the processed row to the final output
            final_output_grid.append(current_processed_row)

        # Update the 'previous_input_row' for the next iteration's comparison
        # Always store the current *original* row
        previous_input_row = current_input_row

    # Return the grid containing the filtered, processed rows
    return final_output_grid