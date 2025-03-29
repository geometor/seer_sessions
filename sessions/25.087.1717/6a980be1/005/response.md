Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np

"""
Transformation Rule:

1.  Identify the border color (`border_color`) from the input grid's top-left corner (`input_grid[0, 0]`). Handle empty grids.
2.  Initialize an output grid with the same dimensions as the input grid, filled with White (0).
3.  Iterate through each row `r` of the input grid (from index 0 to height-1).
4.  For the current input row `r`:
    a. Check if the input row consists entirely of the `border_color`. If yes, leave the corresponding output row `r` as White (0) and skip to the next row.
    b. Check if the input row `r` contains any Red pixels (color code 2).
    c. Determine the background color (`row_bg_color`) for the corresponding output row `r`:
        i.  Default background is White (0).
        ii. If the input row contains Red:
            - If the `border_color` is Yellow (4),
---
