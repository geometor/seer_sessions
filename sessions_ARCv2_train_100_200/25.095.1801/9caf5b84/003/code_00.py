import collections
import itertools
from typing import List, Set, Dict, Tuple, Optional

"""
Transforms the input grid based on digit frequencies.

1.  Analyze Frequencies: Scan the entire input grid and count the occurrences of each digit (0 through 9).
2.  Identify Highest Frequency Digits: Determine the highest frequency achieved by any digit. Create a list, `H`, containing all digits that occur with this highest frequency.
3.  Check for Ties: Examine the list `H`.
    *   Case 1: Tie for Highest Frequency (List `H` contains more than one digit): Define the "stable set" `S` as the set containing all digits in `H`.
    *   Case 2: No Tie for Highest Frequency (List `H` contains only one digit, `M`):
        *   Find the second highest frequency present in the grid.
        *   Identify `D2`, the *smallest* digit that occurs with this second highest frequency.
        *   Define the "stable set" `S` as the set containing `M` and `D2`. (If there is no second highest frequency, meaning all digits present have the same frequency, the stable set `S` contains only `M`).
4.  Transform Grid: Create the output grid with the same dimensions as the input grid. Iterate through each cell of the input grid:
    *   If the digit in the input cell is present in the stable set `S`, copy that digit to the corresponding cell in the output grid.
    *   If the digit in the input cell is *not* present in the stable set `S`, place the digit `7` in the corresponding cell in the output grid.
5.  Output: Return the completed output grid.
"""

def _analyze_frequencies(input_grid: List[List[int]]) -> Dict:
    """
    Analyzes the frequency of digits in the grid.

    Args:
        input_grid: The 2D list of integers.

    Returns:
        A dictionary containing frequency analysis results:
        - 'highest_freq': The highest frequency found.
        - 'highest_freq_digits': Sorted list of digits with the highest frequency.
        - 'M': Smallest digit with the highest frequency.
        - 'second_highest_freq': Second highest frequency (or None).
        - 'second_highest_freq_digits': Sorted list of digits with the second highest frequency (or None).
        - 'D2': Smallest digit with the second highest frequency (or None).
    """
    # Flatten the grid to easily count digits
    all_digits = list(itertools.chain.from_iterable(input_grid))
    if not all_digits:
        # Handle empty grid case
        return {
            'highest_freq': 0, 'highest_freq_digits': [], 'M': None,
            'second_highest_freq': None, 'second_highest_freq_digits': None, 'D2': None
        }

    # Count frequency of each digit
    counts = collections.Counter(all_digits)

    # Group digits by their frequency
    grouped_by_freq = collections.defaultdict(list)
    for digit, freq in counts.items():
        grouped_by_freq[freq].append(digit)

    # Sort frequencies in descending order to easily find highest and second highest
    sorted_freqs = sorted(grouped_by_freq.keys(), reverse=True)

    # Determine highest frequency and associated digits
    highest_freq = sorted_freqs[0]
    highest_freq_digits = sorted(grouped_by_freq[highest_freq])
    m = highest_freq_digits[0] # Smallest digit with highest frequency

    # Determine second highest frequency and associated digits (if they exist)
    second_highest_freq = None
    second_highest_freq_digits = None
    d2 = None
    if len(sorted_freqs) > 1:
        second_highest_freq = sorted_freqs[1]
        second_highest_freq_digits = sorted(grouped_by_freq[second_highest_freq])
        d2 = second_highest_freq_digits[0] # Smallest digit with second highest frequency

    return {
        'highest_freq': highest_freq,
        'highest_freq_digits': highest_freq_digits,
        'M': m,
        'second_highest_freq': second_highest_freq,
        'second_highest_freq_digits': second_highest_freq_digits,
        'D2': d2
    }

def _determine_stable_set(freq_analysis: Dict) -> Set[int]:
    """
    Determines the stable set based on frequency analysis results.

    Args:
        freq_analysis: Dictionary returned by _analyze_frequencies.

    Returns:
        A set of integers representing the stable digits.
    """
    highest_freq_digits = freq_analysis['highest_freq_digits']
    m = freq_analysis['M']
    d2 = freq_analysis['D2']

    stable_set = set()

    # Case 1: Tie for the highest frequency
    if len(highest_freq_digits) > 1:
        stable_set = set(highest_freq_digits)
    # Case 2: No tie for the highest frequency
    else:
        # Add M (the unique highest frequency digit)
        if m is not None: # Check needed for potentially empty grids
            stable_set.add(m)
        # Add D2 (the smallest second highest frequency digit) if it exists
        if d2 is not None:
            stable_set.add(d2)
        # If M is not None but D2 is None, the set correctly contains only M

    return stable_set


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule based on digit frequencies.

    Args:
        input_grid: A list of lists representing the input grid of digits.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # 1. & 2. Analyze frequencies and identify key digits/frequencies
    freq_analysis = _analyze_frequencies(input_grid)

    # 3. Determine the stable set based on tie/no-tie rule
    stable_set = _determine_stable_set(freq_analysis)

    # Define the replacement value
    replacement_value = 7

    # 4. Initialize and construct the output grid
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            digit = input_grid[r][c]
            # Check if the digit is stable
            if digit in stable_set:
                output_grid[r][c] = digit # Keep the digit
            else:
                output_grid[r][c] = replacement_value # Replace with 7

    # 5. Return the transformed grid
    return output_grid