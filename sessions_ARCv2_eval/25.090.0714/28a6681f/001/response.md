Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np

"""
The transformation operates row by row based on the following rules:

1.  **Identify Boundaries:** For each row, find the index of the first (leftmost) non-white pixel (l) and the last (rightmost) non-white pixel (r) in the original input row.
2.  **Fill White Pixels:** Iterate through the pixels strictly between the boundaries (from column l+1 to r-1). If a pixel is white (0) and its immediate left neighbor (column c-1) and immediate right neighbor (column c+1) in the original input row are both non-white, change this pixel to blue (1) in the output grid.
3.  **Conditional Clear:** After the filling step, check the colors of the original boundary pixels at indices l and r. If both boundary pixels were maroon (9), iterate again through the pixels strictly between the boundaries (from column l+1 to r-1) in the *output* grid. If any pixel in this range is blue (1), change it back to white (0).
4.  **Preservation
---
