"""
Transforms a 7x7 digit grid into a predefined 3x3 grid (containing only 0s and 8s) based on the input grid's most frequent non-zero digit.

1. Counts the frequency of each non-zero digit (1-9) in the 7x7 input grid.
2. Identifies the non-zero digit with the highest frequency. In case of a tie, the smallest digit among the tied ones is chosen.
3. Selects a specific 3x3 output pattern based on this dominant digit:
   - If the dominant digit is 1, the pattern is [[0,0,8],[8,8,0],[0,8,0]].
   - If the dominant digit is 3, the pattern is [[0,8,8],[0,8,0],[0,8,0]].
   - If the dominant digit is 2, the pattern is [[0,0,0],[8,8,8],[0,0,0]].
4. If no non-zero digits are found, or if the dominant digit is not 1, 2, or 3, a default 3x3 grid of all zeros is returned.
"""

from collections import Counter
import itertools

# --- Helper Functions ---

def count_non_zero_frequencies(grid: list[list[int]]) -> Counter:
    """Counts the frequency of each non-zero digit in the grid."""
    # Flatten the grid into a single list of numbers
    flat_list = list(itertools.chain.from_iterable(grid))
    # Count all numbers
    counts = Counter(flat_list)
    # Remove the count for zero, if it exists
    if 0 in counts:
        del counts[0]
    return counts

def find_dominant_digit(counts: Counter) -> int | None:
    """Finds the most frequent digit, breaking ties by choosing the smallest digit."""
    if not counts:
        return None # No non-zero digits found

    # Find the maximum frequency
    max_freq = 0
    for digit in counts:
        if counts[digit] > max_freq:
            max_freq = counts[digit]

    # Find all digits with the maximum frequency
    dominant_candidates = []
    for digit in counts:
        if counts[digit] == max_freq:
            dominant_candidates.append(digit)

    # Return the smallest digit among the candidates
    return min(dominant_candidates)


# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the most frequent non-zero digit.
    """

    # Define the predefined output patterns
    pattern_map = {
        1: [[0, 0, 8], [8, 8, 0], [0, 8, 0]],
        3: [[0, 8, 8], [0, 8, 0], [0, 8, 0]],
        2: [[0, 0, 0], [8, 8, 8], [0, 0, 0]],
    }
    default_output = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Calculate frequencies of non-zero digits
    frequencies = count_non_zero_frequencies(input_grid)

    # Find the dominant non-zero digit
    dominant_digit = find_dominant_digit(frequencies)

    # Select the output pattern based on the dominant digit
    # If dominant_digit is None (no non-zeros) or not in the map, use default
    output_grid = pattern_map.get(dominant_digit, default_output)

    return output_grid
