```python
import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Given a 5x5 input grid:
    1. Extract four 2x2 subgrids (quadrants) from the corners, ignoring the middle row and column:
        - Top-Left (TL): Rows 0-1, Columns 0-1
        - Top-Right (TR): Rows 0-1, Columns 3-4
        - Bottom-Left (BL): Rows 3-4, Columns 0-1
        - Bottom-Right (BR): Rows 3-4, Columns 3-4
    2. Compare the four quadrants.
    3. Identify the single quadrant that is different from the other three.
    4. Return this unique quadrant as the 2x2 output grid.
    """

    # Convert input_grid to numpy array for easier slicing
    grid = np.array(input_grid)

    # Extract the four 2x2 quadrants
    quadrants = [
        grid[0:2, 0:2],  # Top-Left
        grid[0:2, 3:5],  # Top-Right
        grid[3:5, 0:2],  # Bottom-Left
        grid[3:5, 3:5]   # Bottom-Right
    ]

    # Convert numpy arrays to tuples of tuples to make them hashable for counting
    quadrant_tuples = [tuple(map(tuple, q)) for q in quadrants]

    # Count the occurrences of each unique quadrant pattern
    counts = Counter(quadrant_tuples)

    # Find the tuple pattern that occurs only once (the unique one)
    unique_tuple = None
    for q_tuple, count in counts.items():
        if count == 1:
            unique_tuple = q_tuple
            break

    # Find the original numpy quadrant that corresponds to the unique tuple
    output_grid = None
    for i, q_tuple in enumerate(quadrant_tuples):
        if q_tuple == unique_tuple:
            output_grid = quadrants[i]
            break
            
    # Ensure an output was found (should always happen based on task description)
    if output_grid is None:
        # Fallback or error handling, though based on examples, one should always be unique.
        # For robustness, maybe return the first quadrant or raise an error.
        # Let's return the first quadrant as a default if the pattern fails.
        print("Warning: Could not find a unique quadrant. Returning Top-Left.")
        output_grid = quadrants[0]


    return output_grid.tolist() # Return as list of lists per ARC standard
```