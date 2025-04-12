"""
1. Examine the input list of integers (represented as the first row of the input grid).
2. Calculate the frequency of each distinct integer in the list.
3. Determine the minimum frequency among all occurring integers.
4. Create a new list containing only those integers from the input that appear with this minimum frequency.
5. Sort this new list in ascending order.
6. If the sorted list contains only one integer, the output is that integer.
7. If the sorted list contains more than one integer, the output is the second integer in the sorted list (the second smallest).
8. The final output is a 1x1 grid containing this selected integer.
"""

import collections

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the frequency of numbers in the first row.

    Args:
        input_grid: A list of lists of integers representing the input grid.
                    Expected to have at least one row.

    Returns:
        A 1x1 grid containing the selected integer based on frequency rules.
    """

    # Extract the sequence from the first row of the input grid
    if not input_grid or not input_grid[0]:
        # Handle empty input if necessary, though ARC examples usually don't have this.
        # Returning an empty grid or raising an error might be options.
        # For now, let's assume valid input as per examples.
        return [[]] 
        
    sequence = input_grid[0]

    # Calculate the frequency of each integer in the sequence
    # Example: [8, 3, 3, 3, 7, 3, 3, 3, 4] -> {8: 1, 3: 6, 7: 1, 4: 1}
    counts = collections.Counter(sequence)

    # Check if there are any counts (handles empty sequence case if not caught above)
    if not counts:
        return [[]]

    # Determine the minimum frequency
    # Example: min(1, 6, 1, 1) -> 1
    min_frequency = min(counts.values())

    # Create a list of integers that appear with the minimum frequency
    # Example: [num for num, count in counts.items() if count == 1] -> [8, 7, 4]
    min_freq_numbers = [num for num, count in counts.items() if count == min_frequency]

    # Sort this list in ascending order
    # Example: sorted([8, 7, 4]) -> [4, 7, 8]
    min_freq_numbers.sort()

    # Select the output number based on the size of the sorted list
    output_number = -1 # Default or error value
    if len(min_freq_numbers) == 1:
        # If only one number has the minimum frequency, it's the output
        # Example: if list was [1], output_number = 1
        output_number = min_freq_numbers[0]
    elif len(min_freq_numbers) > 1:
        # If multiple numbers share the minimum frequency, the output is the second smallest
        # Example: [4, 7, 8] -> output_number = 7 (the second element)
        output_number = min_freq_numbers[1]
    # Note: The case where min_freq_numbers is empty shouldn't happen if sequence is not empty.

    # Format the output as a 1x1 grid
    output_grid = [[output_number]]

    return output_grid
