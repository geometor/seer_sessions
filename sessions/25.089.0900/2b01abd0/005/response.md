Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np

# Define the color swapping pairs
COLOR_SWAP_MAP = {
    8: 4, 4: 8,  # Azure <-> Yellow
    2: 3, 3: 2,  # Red <-> Green
    5: 6, 6: 5,  # Gray <-> Magenta
    # Identity mappings for other colors (should not be strictly necessary if
    # only processing non-zero, non-axis pixels, but good for completeness)
    0: 0, 1: 1, 7: 7, 9: 9
}

def find_reflection_axis(grid):
    """
    Finds the primary reflection axis in the grid.
    The axis is defined as a horizontal or vertical line composed entirely of 
    blue (1) and white (0) pixels, containing at least one blue pixel.
    If multiple such lines exist, the one with the most blue pixels is chosen.
    If there's a tie in blue pixel count, a horizontal axis is preferred over 
    a vertical one.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (
---
