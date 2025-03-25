```python
"""
1.  **Examine the Input Grid:** Analyze the 3x3 input grid and count the occurrences of each digit.
2.  **Determine the Most Frequent Digit:** Identify the digit that appears most frequently in the input grid.
3.  **Construct the Output Grid:** Create a new 3x3 grid. Fill every cell of this new grid with the most frequent digit identified in step 2.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Count digit occurrences
    digit_counts = Counter(input_grid.flatten())

    # Find the most frequent digit
    most_frequent_digit = digit_counts.most_common(1)[0][0]

    # change output pixels
    output_grid[:] = most_frequent_digit

    return output_grid
```
