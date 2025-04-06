"""
Transforms an input 3x3 grid of digits by identifying the digit that appears most frequently.
If there's a tie in frequency, the largest digit among the tied ones is chosen.
The output grid is a 3x3 grid filled entirely with this chosen digit.
"""

from collections import Counter
import itertools

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Calculates the most frequent digit in the input grid (breaking ties by largest value)
    and returns a new 3x3 grid filled with that digit.

    Args:
        input_grid: A 3x3 list of lists containing single-digit integers.

    Returns:
        A 3x3 list of lists where all cells contain the most frequent digit
        from the input grid (largest value in case of frequency tie).
    """

    # 1. Flatten the input grid into a single list of digits
    flat_list = list(itertools.chain.from_iterable(input_grid))

    # 2. Count the occurrences (frequency) of each unique digit
    #    Using Counter handles this efficiently.
    digit_counts = Counter(flat_list)

    # Handle empty input case gracefully (though not expected based on examples)
    if not digit_counts:
        # Or could return an empty grid, or raise error, depending on spec.
        # For this problem, assume valid 3x3 input.
        # Defaulting to 0 if grid was empty.
        most_frequent_digit = 0
        max_frequency = 0
    else:
        # 3. Determine the maximum frequency
        max_frequency = 0
        for digit in digit_counts:
            if digit_counts[digit] > max_frequency:
                max_frequency = digit_counts[digit]

        # 4. Identify all digits that have the maximum frequency
        candidates = []
        for digit in digit_counts:
            if digit_counts[digit] == max_frequency:
                candidates.append(digit)

        # 5. Select the final digit: the largest among the candidates
        most_frequent_digit = max(candidates)

    # 6. Construct the output 3x3 grid
    #    Get dimensions from input, assuming it's always 3x3 based on examples
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0
    output_grid = [[most_frequent_digit for _ in range(cols)] for _ in range(rows)]

    # 7. Return the newly constructed grid
    return output_grid
