
Previous Code:
```python
import numpy as np
from collections import Counter

"""
Transformation Rule:

The input grid is composed of repeating 4x4 blocks, each containing a 1-pixel border and a 3x3 inner pattern.
Identify the most frequent 3x3 pattern (Base Pattern) and any other less frequent 3x3 pattern (Variant Pattern).
Iterate through each 4x4 block in the grid.
If a block contains the Base Pattern and is orthogonally adjacent (shares a side, not just a corner) to a block containing the Variant Pattern in the *original input grid*, then replace the 3x3 pattern of the Base Pattern block with the Variant Pattern in the output grid.
The border pixels remain unchanged.
"""

def get_block_pattern(grid, r, c):
    """Extracts the 3x3 inner pattern from a 4x4 block starting at (r, c)."""
    # Assumes block structure is 3x3 pattern + 1 border pixel
    # Pattern is at indices r+1:r+4, c+1:c+4
    return grid[r+1:r+4, c+1:c+4]

def patterns_equal(p1, p2):
    """Checks if two numpy arrays (patterns) are identical."""
    return np.array_equal(p1, p2)

def transform(input_grid):
    """
    Applies the pattern propagation transformation to the input grid.

    Identifies a base pattern and a variant pattern within 4x4 blocks.
    If a base pattern block is adjacent to a variant pattern block in the input,
    the base pattern block is changed to the variant pattern block in the output.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Assuming the grid is composed of 4x4 blocks
    block_size = 4
    pattern_size = 3

    # --- 1. Identify Base and Variant Patterns ---
    patterns = []
    pattern_locations = {} # Store { (r, c): pattern_tuple }

    # Iterate through the grid block by block
    for r in range(0, rows, block_size):
        for c in range(0, cols, block_size):
            # Check if block is within grid bounds (should be for these tasks)
            if r + block_size <= rows and c + block_size <= cols:
                pattern = get_block_pattern(input_np, r, c)
                # Convert pattern to tuple for hashing in Counter
                pattern_tuple = tuple(map(tuple, pattern))
                patterns.append(pattern_tuple)
                pattern_locations[(r, c)] = pattern_tuple

    # Count pattern occurrences
    pattern_counts = Counter(patterns)

    # Find the most frequent (Base) and the other (Variant) pattern
    # Handle cases where there might be only one pattern type
    if len(pattern_counts) < 2:
        return output_grid # No transformation needed if only one pattern type exists

    base_pattern_tuple = pattern_counts.most_common(1)[0][0]
    variant_pattern_tuple = None
    for p_tuple, count in pattern_counts.items():
        if p_tuple != base_pattern_tuple:
            variant_pattern_tuple = p_tuple
            break # Assume only one variant type matters for propagation

    if variant_pattern_tuple is None:
         return output_grid # Should not happen if len > 1, but safe check

    base_pattern_np = np.array(base_pattern_tuple)
    variant_pattern_np = np.array(variant_pattern_tuple)

    # --- 2. Apply Transformation based on Adjacency ---
    # Iterate through blocks again
    for r in range(0, rows, block_size):
        for c in range(0, cols, block_size):
            # Check if the current block contains the Base Pattern in the INPUT grid
            current_pattern_tuple = pattern_locations.get((r,c))
            if current_pattern_tuple == base_pattern_tuple:
                # Check orthogonal neighbors in the INPUT grid
                neighbor_coords = [
                    (r - block_size, c), # Up
                    (r + block_size, c), # Down
                    (r, c - block_size), # Left
                    (r, c + block_size)  # Right
                ]

                is_adjacent_to_variant = False
                for nr, nc in neighbor_coords:
                    # Check if neighbor is within grid bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor_pattern_tuple = pattern_locations.get((nr, nc))
                        if neighbor_pattern_tuple == variant_pattern_tuple:
                            is_adjacent_to_variant = True
                            break # Found an adjacent variant, no need to check others

                # If adjacent to a Variant Pattern, update the OUTPUT grid
                if is_adjacent_to_variant:
                    # Replace the 3x3 area in the output grid
                    output_grid[r+1:r+4, c+1:c+4] = variant_pattern_np

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 3 1 3 2 3 1 3 2 3 1 3 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 3 1 3 2 3 1 3 2 3 1 3 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 3 3 3 2 3 3 3 2 3 3 3 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```
Expected Output:
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 3 1 3 2 4 4 4 2 3 1 3 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 3 1 3 2 4 1 4 2 3 1 3 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 3 3 3 2 4 4 4 2 3 3 3 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 3 1 3 2 4 4 4 2 3 1 3 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 3 1 3 2 4 1 4 2 3 1 3 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 3 3 3 2 4 4 4 2 3 3 3 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 3 1 3 2 3 1 3 2 3 1 3 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 3 1 3 2 3 1 3 2 3 1 3 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 3 3 3 2 3 3 3 2 3 3 3 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```
Transformed Output:
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 3 1 3 2 3 1 3 2 3 1 3 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 3 1 3 2 3 1 3 2 3 1 3 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 3 3 3 2 3 3 3 2 3 3 3 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 3 1 3 2 3 1 3 2 3 1 3 2 3 1 3 2 3 1 3 2 4 4 4 2
2 4 1 4 2 3 1 3 2 3 1 3 2 3 1 3 2 3 1 3 2 3 1 3 2 4 1 4 2
2 4 4 4 2 3 3 3 2 3 3 3 2 3 3 3 2 3 3 3 2 3 3 3 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 3 1 3 2 3 1 3 2 3 1 3 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 3 1 3 2 3 1 3 2 3 1 3 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 3 3 3 2 3 3 3 2 3 3 3 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2
2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2 4 4 4 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```
Match: False
Pixels Off: 64
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 15.219976218787167

## Example 2:
Input:
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 1 8 1 2 1 8 1 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 1 1 1 2 1 1 1 2 1 1 1 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 1 8 1 2 1 8 1 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```
Expected Output:
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 1 8 1 2 8 8 8 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 1 1 1 2 3 8 3 2 1 1 1 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 1 8 1 2 8 8 8 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 1 8 1 2 1 8 1 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 1 1 1 2 1 1 1 2 1 1 1 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 1 8 1 2 1 8 1 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 1 8 1 2 8 8 8 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 1 1 1 2 3 8 3 2 1 1 1 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 1 8 1 2 8 8 8 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```
Transformed Output:
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 1 8 1 2 1 8 1 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 1 1 1 2 1 1 1 2 1 1 1 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 1 8 1 2 1 8 1 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 1 8 1 2 1 8 1 2 1 8 1 2 1 8 1 2 1 8 1 2 8 8 8 2 8 8 8 2
2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 3 8 3 2 3 8 3 2
2 1 8 1 2 1 8 1 2 1 8 1 2 1 8 1 2 1 8 1 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 1 8 1 2 1 8 1 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 1 1 1 2 1 1 1 2 1 1 1 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 1 8 1 2 1 8 1 2 1 8 1 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2 3 8 3 2
2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2 8 8 8 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```
Match: False
Pixels Off: 28
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 6.658739595719396

## Example 3:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 8 4 1 4 8 4 1 4 8 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 8 8 8 1 8 8 8 1 8 8 8 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 8 4 8 1 8 4 8 1 8 4 8 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 8 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 8 8 8 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 8 4 8 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 8 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 8 8 8 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 8 4 8 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 8 4 1 4 8 4 1 4 8 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 8 8 8 1 8 8 8 1 8 8 8 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 8 4 8 1 8 4 8 1 8 4 8 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 8 4 1 4 2 4 1 4 8 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 8 8 8 1 2 4 2 1 8 8 8 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 8 4 8 1 4 2 4 1 8 4 8 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 8 4 1 4 8 4 1 4 8 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 8 8 8 1 8 8 8 1 8 8 8 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 8 4 8 1 8 4 8 1 8 4 8 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 8 4 1 4 8 4 1 4 8 4 1 4 8 4 1 4 8 4 1 4 2 4 1 4 2 4 1
1 8 8 8 1 8 8 8 1 8 8 8 1 8 8 8 1 8 8 8 1 2 4 2 1 2 4 2 1
1 8 4 8 1 8 4 8 1 8 4 8 1 8 4 8 1 8 4 8 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 8 4 1 4 8 4 1 4 8 4 1 4 8 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 8 8 8 1 8 8 8 1 8 8 8 1 8 8 8 1 2 4 2 1 2 4 2 1 2 4 2 1
1 8 4 8 1 8 4 8 1 8 4 8 1 8 4 8 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 8 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 8 8 8 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 8 4 8 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1 2 4 2 1
1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1 4 2 4 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Match: False
Pixels Off: 49
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 11.65279429250893
