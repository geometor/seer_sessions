# 6150a2bd • 012 • refine_coder

---
```python
"""
Reflect the input grid horizontally.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting it horizontally.
    """
    # Convert input_grid to a NumPy array
    input_array = np.array(input_grid)
    
    # Reflect the array horizontally
    output_array = np.fliplr(input_array)
            
    return output_array.tolist()
```

