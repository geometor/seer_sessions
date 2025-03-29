Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np

"""
Transforms an input grid based on patterns and a color key defined in the top-left corner.

1.  Identifies a 3x2 color key map in the top-left corner (rows 0-2, cols 0-1).
    This maps pattern colors (col 0) to border colors (col 1). White (0) is ignored as a pattern color.
2.  Finds unique non-white pattern colors and their locations in the grid, excluding the key map area.
3.  For each pattern color:
    a. Determines the corresponding border color using the key map. If a pattern color isn't in the key, it's ignored.
    b. Calculates the minimal bounding box enclosing all pixels of that pattern color.
4.  Sorts the identified patterns based on the minimum column index (leftmost position) of their bounding boxes. This determines the drawing order.
5.  Initializes an output grid of the same size as the input, filled with white (0).
6.  Iterates through the sorted patterns and draws rectangles onto the output grid according to these rules:
    a. For each cell (r, c) within the pattern's bounding box:
    b. If (r, c) lies on the border of the bounding box, the output cell is set to the pattern's border color. This overwrites any previous color in the output grid.
    c. If (r, c) is in the interior of the bounding box:
        i. If the original color in the input grid at (r, c) was the current pattern's color, the output cell is set to that pattern color. This overwrites any previous color.
        ii. If the original color in the input grid at (r, c) was white (0), the output cell is set to the current pattern's border color. This overwrites any previous color.
        iii. If the original color in the input grid at (r, c) was a *different* non-white color, the output cell retains whatever value it had *before* processing the current pattern (it might have been set by a previously drawn overlapping pattern, or still be
---
