import collections
import itertools

"""
1. Determine the background number, which is the most frequently occurring number in the input grid.
2. Initialize an empty list called `output_list`.
3. Initialize an empty list called `first_seen_order` to store the unique foreground numbers in the order they are first encountered.
4. Initialize an empty dictionary called `foreground_counts` to store the counts of each foreground number.
5. Iterate through each cell of the input grid, row by row from top to bottom, and within each row, column by column from left to right.
6. For each cell value:
    a. Check if the cell value is different from the background number.
    b. If it is different (it's a foreground number):
        i. Increment the count for this number in the `foreground_counts` dictionary (initialize the count to 1 if it's the first time seeing this number).
        ii. Check if this number is already present in the `first_seen_order` list.
        iii. If it is not present, add it to the `first_seen_order` list.
7. Iterate through the numbers in the `first_seen_order` list (maintaining the order).
8. For each number in `first_seen_order`:
    a. Retrieve its count from the `foreground_counts` dictionary.
    b. Append the number to the `output_list` exactly that many times (equal to its count).
9. Return the `output_list`.
"""

def find_background(grid: list[list[int]]) -> int:
    """Finds the most frequent number in the grid."""
    # Flatten the grid into a single list
    flat_list = list(itertools.chain(*grid))
    # Count occurrences of each number
    counts = collections.Counter(flat_list)
    # Find the number with the maximum count
    background_num = counts.most_common(1)[0][0]
    return background_num

def transform(input_grid: list[list[int]]) -> list[int]:
    """
    Extracts foreground numbers from a grid, counts their occurrences,
    and returns a list where each foreground number is repeated by its count,
    ordered by their first appearance in a top-to-bottom, left-to-right scan.
    """

    # 1. Determine the background number
    background_num = find_background(input_grid)

    # 2. Initialize output_list (will be built at the end)
    output_list = []

    # 3. Initialize list to track the order of first appearance
    first_seen_order = []

    # 4. Initialize dictionary to store counts of foreground numbers
    foreground_counts = collections.defaultdict(int)

    # 5. Iterate through the grid to find foreground numbers, count them, and track first appearance
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    for r in range(rows):
        for c in range(cols):
            cell_value = input_grid[r][c]
            # 6a. Check if it's a foreground number
            if cell_value != background_num:
                # 6b.i. Increment count
                foreground_counts[cell_value] += 1
                # 6b.ii & 6b.iii. Add to first_seen_order if not already present
                if cell_value not in first_seen_order:
                    first_seen_order.append(cell_value)

    # 7. & 8. Build the output list based on the order and counts
    for num in first_seen_order:
        count = foreground_counts[num]
        output_list.extend([num] * count) # Append the number 'count' times

    # 9. Return the final list
    return output_list