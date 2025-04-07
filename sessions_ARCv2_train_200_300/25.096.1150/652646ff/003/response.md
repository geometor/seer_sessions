```python
import numpy as np
from collections import Counter

"""
Identify the background digit (most frequent) in the input grid. Then, identify 
'signal' digits, which are non-background digits where at least one instance 
is adjacent (horizontally, vertically, or diagonally) to another instance of 
the same digit. Sort these signal digits numerically. For each sorted signal 
digit, construct a standard 6x6 pattern using the signal digit as foreground 
and the identified background digit. The pattern has a fixed frame structure 
with 8 foreground cells. Finally, stack these generated 6x6 patterns vertically 
in the sorted order to create the output grid.
"""

def _get_background_digit(grid: np.ndarray) -> int:
    """Finds the most frequent digit in the grid."""
    if grid.size == 0:
        # Handle empty input grid case if necessary, though constraints likely prevent this.
        # Returning a default or raising an error might be appropriate.
        # For now, assuming non-empty grids based on examples.
        raise ValueError("Input grid cannot be empty")
    counts = Counter(grid.flatten())
    # Find the digit with the highest count
    background_digit = counts.most_common(1)[0][0]
    return int(background_digit) # Ensure it's a standard int

def _find_signal_digits(grid: np.ndarray, background_digit: int) -> list[int]:
    """Identifies signal digits based on self-adjacency."""
    rows, cols = grid.shape
    unique_digits = np.unique(grid)
    candidate_digits = [d for d in unique_digits if d != background_digit]
    signal_digits = set()

    # Define offsets for 8 neighbors (including diagonals)
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 ( 0, -1),          ( 0, 1),
                 ( 1, -1), ( 1, 0), ( 1, 1)]

    # Iterate through each candidate digit
    for digit in candidate_digits:
        # Find all locations of the current candidate digit
        locations = np.argwhere(grid == digit)
        is_signal = False
        # Check neighbors for each location
        for r, c in locations:
            for dr, dc in neighbors:
                nr, nc = r + dr, c + dc
                # Check if neighbor is within bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if neighbor has the same digit
                    if grid[nr, nc] == digit:
                        signal_digits.add(digit)
                        is_signal = True
                        break # Found adjacency for this location, move to next location
            if is_signal:
                break # Found adjacency for this digit, move to next digit

    return sorted(list(signal_digits))


def _create_pattern_grid(foreground_digit: int, background_digit: int) -> np.ndarray:
    """Creates a standard 6x6 grid with the specified foreground/background pattern."""
    pattern = np.full((6, 6), background_digit, dtype=int)
    # Set foreground digits based on the defined pattern structure
    # Rows 0 & 5: F B F F B F --> indices 0, 2, 3, 5
    pattern[[0, 5], [0, 2, 3, 5]] = foreground_digit
    # Rows 1 & 4: F F B B F F --> indices 0, 1, 4, 5
    pattern[[1, 4], [0, 1, 4, 5]] = foreground_digit
    # Rows 2 & 3: F B B B B F --> indices 0, 5
    pattern[[2, 3], [0, 5]] = foreground_digit
    return pattern

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying signal digits based on adjacency,
    generating standard 6x6 patterns for them, and stacking these patterns.
    """
    # Convert input to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)

    if input_array.size == 0:
        return [] # Handle empty input

    # Step 1: Identify the background digit
    background_digit = _get_background_digit(input_array)

    # Step 2 & 3: Identify Candidate Digits and Filter for Signal Digits
    signal_digits = _find_signal_digits(input_array, background_digit)

    # Step 4: Sort Signal Digits (already sorted by _find_signal_digits)
    # signal_digits are sorted

    # Step 5 & 6: Construct Output Patterns and Stack
    output_patterns = []
    if not signal_digits:
        return [] # Return empty list if no signal digits found

    for fg_digit in signal_digits:
        # Create the standard 6x6 pattern for the current signal digit
        pattern_grid = _create_pattern_grid(fg_digit, background_digit)
        output_patterns.append(pattern_grid)

    # Stack the found patterns vertically
    output_grid_np = np.vstack(output_patterns)

    # Step 7: Return Result as list of lists
    return output_grid_np.tolist()
```