Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from scipy.ndimage import label, binary_dilation, generate_binary_structure

"""
Transformation Rule:

The primary transformation identifies connected components of gray pixels (color 5) using 8-way connectivity (including diagonals). 
For each distinct gray component found in the input grid:
1. Find all pixels that are orthogonally or diagonally adjacent (8-way neighbors) to any pixel within that gray component.
2. Check if any of these adjacent pixels in the input grid has the color orange (7).
3. If at least one adjacent pixel is orange, then *all* pixels belonging to that specific gray component are changed to orange (7) in the output grid.
4. If a gray component has no adjacent orange pixels, it remains unchanged in the output grid.
5. All other pixels (background, borders, other colors) retain their original color from the input grid.

Note: This implementation focuses solely on the color interaction rule described above. It does not account for the object/region movements observed in the examples, which likely represent a separate or combined transformation step needed for a complete solution. The test cases may fail due to the absence of this movement logic.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the gray-to-orange transformation based on adjacency to orange pixels.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    
    # Initialize output_grid as a copy of the input
    # The transformation will modify this grid directly where needed.
    output_grid = np.copy(input_grid)
    
    # Define 8-way connectivity structure for component labeling and dilation
    # This considers pixels as connected if they touch sides or corners.
    conn_8 = generate_binary_structure(rank=2, connectivity=2) # Returns a 3x3 array of True

    # Create a boolean mask identifying all gray pixels (color 5)
    gray_mask = (input_grid == 5)

    # Check if there are any gray pixels to process
    if not np.any(gray_mask):
        return output_grid # No gray pixels, return the original grid copy

    # Label connected components of gray pixels using 8-way connectivity
    # `labeled_array` assigns a unique integer ID to each connected component.
    # `num_features` is the total count of distinct gray components found.
    labeled_array, num_features = label
---
