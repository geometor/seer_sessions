```python
"""
Examine the input grid. Identify all pixels with non-zero values. Count the occurrences of the identified non zero values. Create the output by concatenating horizontally the identified non-zero value for the amount of times of it's occurrence.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Identify all non-zero values.
    non_zero_values = input_array[input_array != 0]
    
    # Count the occurrences of non-zero values, using a unique sorted version of the non zero values
    unique_non_zero_values = np.unique(non_zero_values)

    output_list = []
    for value in unique_non_zero_values:
        count = np.count_nonzero(non_zero_values == value)
        output_list.extend([value] * count)


    # Convert to a numpy array
    output_array = np.array(output_list)

    return output_array.tolist()
```
