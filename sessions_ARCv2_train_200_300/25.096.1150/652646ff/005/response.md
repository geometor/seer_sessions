```python
import numpy as np
from collections import Counter

"""
Transforms an input grid based on identifying signal digits and generating fixed patterns.
1. Determine the background digit (most frequent).
2. Identify signal digits: non-background digits with at least one adjacent (including diagonal) neighbor of the same digit.
3. Sort signal digits numerically.
4. For each sorted signal digit, create a standard 6x6 pattern using it as foreground and the background digit. The pattern is a fixed frame shape.
5. Stack these 6x6 patterns vertically in the sorted order of signal digits.
6. Return the resulting stacked grid. If no signal digits are found, return an empty grid.
"""

def _get_background_digit(grid: np.ndarray) -> int:
    """Finds the most frequent digit in the grid."""
    if grid.size == 0:
        # Should ideally not happen based on task constraints, but good practice.
        raise ValueError("Input grid cannot be empty") 
    counts = Counter(grid.flatten())
    # Find the digit with the highest count
    background_digit = counts.most_common(1)[0][0]
    # Ensure standard Python int type, numpy ints can sometimes cause issues
    return int(background_digit) 

def _find_signal_digits(grid: np.ndarray, background_digit: int) -> list[int]:
    """Identifies signal digits based on self-adjacency (including diagonals)."""
    rows, cols = grid.shape
    unique_digits = np.unique(grid)
    # Consider only digits that are not the background
    candidate_digits = [int(d) for d in unique_digits if d != background_digit] 
    signal_digits = set()

    # Define offsets for 8 neighbors (including diagonals)
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 ( 0, -1),          ( 0, 1),
                 ( 1, -1), ( 1, 0), ( 1, 1)]

    # Iterate through each potential signal digit
    for digit in candidate_digits:
        # Find all locations (coordinates) of the current candidate digit
        locations = np.argwhere(grid == digit)
        is_signal = False
        # Check neighbors for each location of the digit
        for r, c in locations:
            for dr, dc in neighbors:
                nr, nc = r + dr, c + dc
                # Check if the neighbor coordinate is within the grid bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if the neighbor has the same digit
                    if grid[nr, nc] == digit:
                        # Found adjacency, mark this digit as signal and stop checking for it
                        signal_digits.add(digit)
                        is_signal = True
                        break # Stop checking neighbors for this location
            if is_signal:
                break # Stop checking locations for this digit

    # Return the unique signal digits, sorted numerically
    return sorted(list(signal_digits))

def _create_pattern_grid(foreground_digit: int, background_digit: int) -> np.ndarray:
    """Creates a standard 6x6 grid with the specified foreground/background pattern."""
    # Initialize a 6x6 grid filled with the background digit
    pattern = np.full((6, 6), background_digit, dtype=int)
    
    # Define the coordinates for the foreground digit (the frame)
    # Rows 0 & 5
    pattern[0, [0, 2, 3, 5]] = foreground_digit
    pattern[5, [0, 2, 3, 5]] = foreground_digit
    # Rows 1 & 4
    pattern[1, [0, 1, 4, 5]] = foreground_digit
    pattern[4, [0, 1, 4, 5]] = foreground_digit
    # Rows 2 & 3
    pattern[2, [0, 5]] = foreground_digit
    pattern[3, [0, 5]] = foreground_digit
    
    return pattern

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)

    # Handle empty input grid case
    if input_array.size == 0:
        return [] 

    # Step 1: Identify the background digit (most frequent)
    background_digit = _get_background_digit(input_array)

    # Step 2 & 3: Identify and sort signal digits (non-background, self-adjacent)
    signal_digits = _find_signal_digits(input_array, background_digit)

    # Step 4 & 5: Generate patterns for each signal digit and prepare for stacking
    output_patterns = []
    if not signal_digits:
        # If no signal digits are found, return an empty list
        return [] 

    for fg_digit in signal_digits:
        # Create the standard 6x6 pattern for the current signal digit
        pattern_grid = _create_pattern_grid(fg_digit, background_digit)
        output_patterns.append(pattern_grid)

    # Step 6: Stack the generated patterns vertically
    # vstack requires at least one array, handled by the check for empty signal_digits
    output_grid_np = np.vstack(output_patterns)

    # Step 7: Convert the final numpy array back to a list of lists for the expected output format
    return output_grid_np.tolist()
```