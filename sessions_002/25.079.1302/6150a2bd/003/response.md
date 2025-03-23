```python
"""
The input grid is rotated 90 degrees clockwise, then mirrored vertically, and finally, the rows of the resulting grid are sorted in decreasing order based on the sum of elements in each row.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the input grid 90 degrees clockwise
    rotated_array = np.rot90(input_array, k=-1)

    # Mirror/Flip the rotated grid vertically
    mirrored_array = np.flipud(rotated_array)
    
    # Sort rows based on the sum of elements in each row
    # Create a list of tuples where each tuple is (row_sum, row)
    row_data = []
    for row in mirrored_array:
        row_data.append((np.sum(row), row))

    # Sort rows in descending order of their sums
    row_data.sort(key=lambda x: x[0], reverse=True)
    sorted_rows = [row for row_sum, row in row_data]
    
    # Convert back to numpy array
    output_array = np.array(sorted_rows)

    return output_array.tolist()
```