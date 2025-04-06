```python
import collections
import itertools

"""
Transforms the input grid based on digit frequencies.

1. Calculate the frequency of each digit (0-9) across the entire input grid.
2. Identify 'M', the smallest digit with the highest frequency.
3. Identify 'D2', the smallest digit with the second highest frequency.
4. Create a "stable set" containing only M and D2.
5. Iterate through the input grid:
   - If a digit is in the stable set, keep it.
   - Otherwise, replace it with 7.
"""

def _find_m_d2(input_grid: list[list[int]]) -> tuple[int, int | None]:
    """
    Finds M (smallest digit with highest frequency) and 
    D2 (smallest digit with second highest frequency).

    Args:
        input_grid: The 2D list of integers.

    Returns:
        A tuple (m, d2), where m is the most frequent digit (smallest tie-breaker)
        and d2 is the second most frequent digit (smallest tie-breaker).
        Returns (m, None) if there is only one frequency level.
    """
    # Flatten the grid and count digit frequencies
    all_digits = list(itertools.chain.from_iterable(input_grid))
    if not all_digits:
        return (None, None) # Handle empty grid case
        
    counts = collections.Counter(all_digits)
    
    # Group digits by frequency
    grouped_by_freq = collections.defaultdict(list)
    for digit, freq in counts.items():
        grouped_by_freq[freq].append(digit)
        
    # Sort frequencies in descending order
    sorted_freqs = sorted(grouped_by_freq.keys(), reverse=True)
    
    # Determine M (smallest digit with the highest frequency)
    highest_freq = sorted_freqs[0]
    m = min(grouped_by_freq[highest_freq])
    
    # Determine D2 (smallest digit with the second highest frequency)
    d2 = None
    if len(sorted_freqs) > 1:
        second_highest_freq = sorted_freqs[1]
        d2 = min(grouped_by_freq[second_highest_freq])
        
    # Handle edge case where M might be the only digit type
    # If d2 wasn't found because only one frequency level exists,
    # the logic implicitly handles this as d2 remains None.
    # If the problem guarantees at least two frequency levels or digits,
    # this check might be redundant, but it's safer.
        
    return m, d2


def transform(input_grid: list[list[int]]) -> list[list[int]]:
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
    
    # initialize output_grid with the same dimensions
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # 1-3. Determine M (most frequent) and D2 (second most frequent) digits
    m, d2 = _find_m_d2(input_grid)
    
    # Handle case where grid might be too small or uniform to find M and D2
    if m is None: 
         # If no digits, return empty or copy? Let's return a grid of 7s of same size.
         # Or maybe copy input? Based on rule, if stable set is empty, all become 7.
         return [[7 for _ in range(cols)] for _ in range(rows)]

    # 4. Create the stable set containing M and D2
    stable_set = set()
    stable_set.add(m)
    if d2 is not None:
        stable_set.add(d2)
        
    replacement_value = 7

    # 5. Perform transformations
    for r in range(rows):
        for c in range(cols):
            digit = input_grid[r][c]
            # If the digit is in the stable set, keep it
            if digit in stable_set:
                output_grid[r][c] = digit
            # Otherwise, replace it with 7
            else:
                output_grid[r][c] = replacement_value

    return output_grid
```