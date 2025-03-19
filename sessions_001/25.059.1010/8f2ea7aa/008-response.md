# 8f2ea7aa • 008 • refine_coder

---
```python
"""
1.  **Locate Azure Pixel:** Find the single azure (8) pixel within the input grid.
2.  **Identify Target Row:** Determine the row index of the azure pixel.
3.  **Modify Pixels to the Left:** Change all pixels to the *left* of the azure pixel in the target row to black (0).
4. **Preserve Remainder:** Ensure the azure pixel itself and any pixels to its *right* on the row remain unchanged.
"""

import numpy as np
from typing import List, Tuple

def find_pixel(grid_np: np.ndarray, color: int) -> Tuple[int, int] | None:
    """Finds the location of a pixel of the given color.  Assumes only one exists."""
    locations = np.argwhere(grid_np == color)
    if len(locations) > 0:
        return locations[0]  # Return the first location found
    return None

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """Transforms the input grid according to the observed rules."""

    input_np = np.array(input_grid)
    output_np = input_np.copy()  # Start with a copy to preserve original pixels

    # 1. Locate Azure Pixel
    azure_location = find_pixel(input_np, 8)
    if azure_location is None:
        return output_np.tolist()  # No azure pixel, return input unchanged

    # 2. Identify Target Row
    target_row = azure_location[0]
    azure_col = azure_location[1]

    # 3. Modify Pixels to the Left
    for col_index in range(azure_col):  # Iterate up to the azure pixel's column
        output_np[target_row, col_index] = 0

    # 4. Preserve Remainder (Implicitly handled by copying the input and only modifying to the left)

    return output_np.tolist()
```
