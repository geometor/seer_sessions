# eb281b96 • 002 • example_2 • investigate_coder

---
```python
"""
The input grid's pattern is replicated vertically and horizontally to create a larger output grid. The spatial arrangement of non-zero digits is maintained. The output grid's dimensions are integer multiples of the input grid's dimensions.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)
    input_height, input_width = input_array.shape

    # Determine replication factors. For this specific case it appears to always
    # replicate by factor of 3 vertically and 1 horizontally, then add
    # vertically to the original
    height_replication_factor = 3
    width_replication_factor = 1
    
    # initialize and build output in steps to clarify process
    output_array = np.tile(input_array, (height_replication_factor, width_replication_factor))
    output_array = np.concatenate((input_array, output_array), axis=0)


    return output_array.tolist()
```

