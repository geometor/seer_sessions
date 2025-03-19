# 0d3d703e • 017 • refine_coder

---
```python
"""
The transformation performs a direct color substitution on the input grid. The following substitutions are applied:

1.  Gray (5) pixels are replaced with Blue (1) pixels.
2.  Azure (8) pixels are replaced with Maroon (9) pixels.
3.  Magenta (6) pixels are replaced with Red (2) pixels.

All other colors, if present, remain unchanged. The spatial arrangement of pixels is preserved.
"""

import numpy as np
from typing import List, Tuple

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by applying a color substitution cipher.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the input grid (though vectorization would be more efficient).
    #for i in range(output_grid.shape[0]):
    #    for j in range(output_grid.shape[1]):
            # Apply the color mapping.
    output_grid[input_grid == 5] = 1  # Gray to Blue
    output_grid[input_grid == 8] = 9  # Azure to Maroon
    output_grid[input_grid == 6] = 2  # Magenta to Red

    return output_grid
```

