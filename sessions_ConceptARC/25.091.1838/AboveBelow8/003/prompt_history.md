
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 8 8 3 3 3 3 3 3 3 3 0
0 3 3 8 3 3 3 3 3 3 3 3 0
0 6 6 8 6 6 6 6 6 6 6 6 0
0 6 6 8 6 6 6 6 6 6 6 6 0
0 7 7 8 8 8 7 7 7 7 7 7 0
0 7 7 7 7 8 7 7 7 7 7 7 0
0 4 4 4 4 8 8 4 4 4 4 4 0
0 4 4 4 4 4 8 8 8 8 4 4 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0
```


## train_2

**input:**
```
3 3 3 3 8 8 8 8 8 8 3
3 3 3 3 8 3 3 3 3 3 3
2 2 2 2 8 8 8 8 2 2 2
2 2 2 2 2 2 2 8 2 2 2
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 8 8 8 8 7 7 7
9 9 9 8 8 9 9 9 9 9 9
1 1 1 8 1 1 1 1 1 1 1
1 1 1 8 8 1 1 1 1 1 1
1 1 1 1 8 8 8 1 1 1 1
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 8 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 8 8 8 3 3 3 3 0
0 3 3 3 8 3 3 3 3 0
0 3 8 8 8 3 3 3 3 0
0 3 8 3 3 3 3 3 3 0
0 3 8 3 3 3 3 3 3 0
0 1 8 8 1 1 1 1 1 0
0 1 1 8 1 1 1 1 1 0
0 1 1 8 8 8 8 1 1 0
0 1 1 1 1 1 8 1 1 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception**: The task involves filtering the input grid based on pixel color. Each input grid contains various colored pixels, including a significant number of azure (8) pixels, often interspersed within or forming patterns across other colored regions. The corresponding output grid retains only the azure (8) pixels in their original positions, while all other pixels are replaced with the background color, white (0). The dimensions of the grid remain unchanged. The transformation acts as a selective filter, isolating the azure pixels against a uniform white background.

*   **YAML Facts**:
    
```yaml
    task_context:
      grid_dimensions: Consistent between input and output.
      background_color_input: Variable (white (0) in examples 1 and 3, none explicit in example 2).
      background_color_output: Consistently white (0).
    objects:
      - type: pixel_groups
        properties:
          - color: Various colors present in input (e.g., green-3, magenta-6, orange-7, yellow-4, red-2, maroon-9, blue-1, azure-8, white-0).
          - special_color: Azure (8) is the key color.
    relationships:
      - type: positional_invariance
        description: The azure (8) pixels maintain their exact (row, column) coordinates from the input to the output grid.
    actions:
      - type: filter
        input: Input grid
        output: Output grid
        rule: Keep only pixels with azure (8) color.
      - type: replace
        target_pixels: All pixels that are NOT azure (8).
        replacement_color: White (0).
        condition: Apply to all non-azure pixels in the input grid to produce the output grid.

    ```


*   **Natural Language Program**:
    1.  Initialize an output grid with the same dimensions as the input grid, filling it entirely with the white (0) color.
    2.  Iterate through each pixel of the input grid at every row and column position.
    3.  Check the color of the current pixel in the input grid.
    4.  If the color of the input pixel is azure (8), set the color of the pixel at the corresponding position in the output grid to azure (8).
    5.  If the color of the input pixel is any color other than azure (8), leave the corresponding pixel in the output grid as white (0).
    6.  Return the completed output grid.
```python
"""
Create an output grid of the same dimensions as the input grid, initialized with the background color white (0). Iterate through each pixel of the input grid. If a pixel's color is azure (8), copy its color to the corresponding position in the output grid. Otherwise, leave the output grid pixel as white (0). Return the final output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Filters the input grid to keep only azure (8) pixels, replacing all others with white (0).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid with only azure pixels preserved.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize an output grid of the same dimensions with white (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Identify the locations of azure (8) pixels in the input grid
    azure_pixels = (input_grid == 8)

    # Set the corresponding locations in the output grid to azure (8)
    output_grid[azure_pixels] = 8

    return output_grid
```

Previous Code:
```python
"""
Create an output grid of the same dimensions as the input grid, initialized with the background color white (0). Iterate through each pixel of the input grid. If a pixel's color is azure (8), copy its color to the corresponding position in the output grid. Otherwise, leave the output grid pixel as white (0). Return the final output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Filters the input grid to keep only azure (8) pixels, replacing all others with white (0).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid with only azure pixels preserved.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize an output grid of the same dimensions with white (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Identify the locations of azure (8) pixels in the input grid
    azure_pixels = (input_grid == 8)

    # Set the corresponding locations in the output grid to azure (8)
    output_grid[azure_pixels] = 8

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 8 8 3 3 3 3 3 3 3 3 0
0 3 3 8 3 3 3 3 3 3 3 3 0
0 6 6 8 6 6 6 6 6 6 6 6 0
0 6 6 8 6 6 6 6 6 6 6 6 0
0 7 7 8 8 8 7 7 7 7 7 7 0
0 7 7 7 7 8 7 7 7 7 7 7 0
0 4 4 4 4 8 8 4 4 4 4 4 0
0 4 4 4 4 4 8 8 8 8 4 4 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 4.195804195804186

## Example 2:
Input:
```
3 3 3 3 8 8 8 8 8 8 3
3 3 3 3 8 3 3 3 3 3 3
2 2 2 2 8 8 8 8 2 2 2
2 2 2 2 2 2 2 8 2 2 2
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 8 8 8 8 7 7 7
9 9 9 8 8 9 9 9 9 9 9
1 1 1 8 1 1 1 1 1 1 1
1 1 1 8 8 1 1 1 1 1 1
1 1 1 1 8 8 8 1 1 1 1
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 8 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0
```
Transformed Output:
```
0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 8 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 11.570247933884303

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 3 8 8 8 3 3 3 3 0
0 3 3 3 8 3 3 3 3 0
0 3 8 8 8 3 3 3 3 0
0 3 8 3 3 3 3 3 3 0
0 3 8 3 3 3 3 3 3 0
0 1 8 8 1 1 1 1 1 0
0 1 1 8 1 1 1 1 1 0
0 1 1 8 8 8 8 1 1 0
0 1 1 1 1 1 8 1 1 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.363636363636346
**General Assessment**

The initial analysis based only on the first example led to an overly simplistic hypothesis: keep all azure (8) pixels and discard others. Testing this against all training examples revealed inconsistencies. The key insight gained from analyzing the failures is that the retention of azure (8) pixels is conditional and depends on the context of the *row* in which they appear. Specifically, azure pixels are discarded if the predominant color within their row (excluding white (0) and azure (8)) is green (3). Otherwise, they are kept. The strategy is to refine the transformation rule to incorporate this row-based conditional filtering.

**Metrics**

To verify the row-based filtering hypothesis, the dominant color (excluding white (0) and azure (8)) for each relevant row in each example was determined:


*code_execution:*
```python
import numpy as np
from collections import Counter

def get_dominant_color(row):
    """Finds the most common color in a row, excluding white (0) and azure (8)."""
    filtered_row = [pixel for pixel in row if pixel != 0 and pixel != 8]
    if not filtered_row:
        return None
    counts = Counter(filtered_row)
    dominant_color, _ = counts.most_common(1)[0]
    # Ensure the returned type is a standard Python int if it's a numpy int type
    if isinstance(dominant_color, np.integer):
        dominant_color = int(dominant_color)
    return dominant_color

# --- Example Inputs ---
# Example 1 Input
input_1 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 0], [0, 3, 3, 8, 3, 3, 3, 3, 3, 3, 3, 3, 0], [0, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6, 0],
    [0, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6, 0], [0, 7, 7, 8, 8, 8, 7, 7, 7, 7, 7, 7, 0], [0, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 0],
    [0, 4, 4, 4, 4, 8, 8, 4, 4, 4, 4, 4, 0], [0, 4, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 0]
])
# Example 2 Input
input_2 = np.array([
    [3, 3, 3, 3, 8, 8, 8, 8, 8, 8, 3], [3, 3, 3, 3, 8, 3, 3, 3, 3, 3, 3], [2, 2, 2, 2, 8, 8, 8, 8, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 8, 2, 2, 2], [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7],
    [7, 7, 7, 7, 8, 8, 8, 8, 7, 7, 7], [9, 9, 9, 8, 8, 9, 9, 9, 9, 9, 9], [1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 8, 8, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 8, 8, 8, 1, 1, 1, 1]
])
# Example 3 Input
input_3 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 8, 8, 8, 3, 3, 3, 3, 0], [0, 3, 3, 3, 8, 3, 3, 3, 3, 0],
    [0, 3, 8, 8, 8, 3, 3, 3, 3, 0], [0, 3, 8, 3, 3, 3, 3, 3, 3, 0], [0, 3, 8, 3, 3, 3, 3, 3, 3, 0],
    [0, 1, 8, 8, 1, 1, 1, 1, 1, 0], [0, 1, 1, 8, 1, 1, 1, 1, 1, 0], [0, 1, 1, 8, 8, 8, 8, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 8, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# --- Expected Outputs (for checking the hypothesis) ---
# Expected Output 1
output_1 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,8,0,0,0,0,0,0,0,0,0],
    [0,0,0,8,0,0,0,0,0,0,0,0,0],[0,0,0,8,8,8,0,0,0,0,0,0,0],[0,0,0,0,0,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,8,8,0,0,0,0,0,0],[0,0,0,0,0,0,8,8,8,8,0,0,0]
])
# Expected Output 2
output_2 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,8,8,8,8,0,0,0],
    [0,0,0,0,0,0,0,8,0,0,0],[0,0,0,0,0,0,0,8,0,0,0],[0,0,0,0,0,0,0,8,0,0,0],
    [0,0,0,0,8,8,8,8,0,0,0],[0,0,0,8,8,0,0,0,0,0,0],[0,0,0,8,0,0,0,0,0,0,0],
    [0,0,0,8,8,0,0,0,0,0,0],[0,0,0,0,8,8,8,0,0,0,0]
])
# Expected Output 3
output_3 = np.array([
    [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
    [0,0,8,8,0,0,0,0,0,0],[0,0,0,8,0,0,0,0,0,0],[0,0,0,8,8,8,8,0,0,0],
    [0,0,0,0,0,0,8,0,0,0],[0,0,0,0,0,0,0,0,0,0]
])

inputs = [input_1, input_2, input_3]
expected_outputs = [output_1, output_2, output_3]
results = {}

for i, input_grid in enumerate(inputs):
    height, width = input_grid.shape
    transformed_output = np.zeros((height, width), dtype=int)
    row_dominant_colors = {}
    rows_to_discard_8s = set()

    # Step 1: Determine dominant color for each row and identify rows where 8s should be discarded
    for r in range(height):
        dominant_color = get_dominant_color(input_grid[r])
        row_dominant_colors[r] = dominant_color
        if dominant_color == 3: # Green
            rows_to_discard_8s.add(r)

    # Step 2: Build the output grid based on the rule
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 8: # If pixel is azure
                if r not in rows_to_discard_8s: # And row dominant color is not green
                    transformed_output[r, c] = 8 # Keep the azure pixel

    # Check if the transformed output matches the expected output
    match = np.array_equal(transformed_output, expected_outputs[i])
    results[f"Example {i+1}"] = {
        "Row Dominant Colors": row_dominant_colors,
        "Rows Discarding 8s (Color=3)": sorted(list(rows_to_discard_8s)),
        "Hypothesis Output Matches Expected": match
    }

print(results)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
{'Example 1': {'Row Dominant Colors': {0: None, 1: None, 2: None, 3: 3, 4: 3, 5: 6, 6: 6, 7: 7, 8: 7, 9: 4, 10: 4}, 'Rows Discarding 8s (Color=3)': [3, 4], 'Hypothesis Output Matches Expected': True}, 'Example 2': {'Row Dominant Colors': {0: 3, 1: 3, 2: 2, 3: 2, 4: 7, 5: 7, 6: 7, 7: 9, 8: 1, 9: 1, 10: 1}, 'Rows Discarding 8s (Color=3)': [0, 1], 'Hypothesis Output Matches Expected': True}, 'Example 3': {'Row Dominant Colors': {0: None, 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 1, 7: 1, 8: 1, 9: 1, 10: None}, 'Rows Discarding 8s (Color=3)': [1, 2, 3, 4, 5], 'Hypothesis Output Matches Expected': True}}

```
The metrics confirm the hypothesis:
-   **Example 1**: Rows 3 and 4 have green (3) as the dominant color (excluding white/azure). Azure (8) pixels in these rows are discarded. All other rows with azure pixels have non-green dominant colors (magenta-6, orange-7, yellow-4), and their azure pixels are kept. The generated output matches the expected output.
-   **Example 2**: Rows 0 and 1 have green (3) as the dominant color. Azure (8) pixels in these rows are discarded. All other rows with azure pixels have non-green dominant colors (red-2, orange-7, maroon-9, blue-1), and their azure pixels are kept. The generated output matches the expected output.
-   **Example 3**: Rows 1 through 5 have green (3) as the dominant color. Azure (8) pixels in these rows are discarded. Rows 6 through 9 have blue (1) as the dominant color, and their azure pixels are kept. The generated output matches the expected output.

**YAML Facts**


```yaml
task_context:
  grid_dimensions: Consistent between input and output.
  background_color_input: Variable (often includes white-0).
  background_color_output: Consistently white (0).
objects:
  - type: pixel
    properties:
      - color: Specific value from 0-9 (white, blue, red, green, yellow, gray, magenta, orange, azure, maroon).
      - is_target: Azure (8) pixels are the primary focus.
      - is_filter_condition: Green (3) pixels determine filtering logic within a row.
      - is_background: White (0) pixels act as background/empty space.
  - type: row
    properties:
      - content: Contains a mix of pixels, often one dominant color alongside azure (8) and white (0).
      - dominant_color_excluding_special: The most frequent color in the row, ignoring white (0) and azure (8). This property is crucial for the transformation rule.
relationships:
  - type: positional_invariance
    description: Kept azure (8) pixels maintain their exact (row, column) coordinates from the input to the output grid.
  - type: row_based_condition
    description: The decision to keep or discard an azure (8) pixel depends on the properties of the row it resides in.
actions:
  - type: determine_row_property
    input: Each row of the input grid.
    output: The dominant color excluding white (0) and azure (8) for that row.
    computation: Count pixel frequencies per row, ignoring 0 and 8, find the maximum.
  - type: filter_and_replace
    input: Input grid.
    output: Output grid.
    rule: |
      1. Initialize output grid with white (0).
      2. For each row `r`: Determine its dominant color `d` (ignoring 0 and 8).
      3. For each pixel at `(r, c)` in the input:
         - If the pixel is azure (8) AND the dominant color `d` of row `r` is NOT green (3):
           Copy azure (8) to the output grid at `(r, c)`.
         - Otherwise:
           The corresponding output pixel remains white (0).

```


**Natural Language Program**

1.  Create a new grid (output grid) with the same dimensions as the input grid, and fill it entirely with the background color white (0).
2.  For each row `r` in the input grid:
    a.  Identify all pixel colors present in the row, excluding white (0) and azure (8).
    b.  Determine the most frequent color among these remaining colors. This is the "dominant row color". If no such colors exist in the row, consider the condition for keeping azure pixels met by default (i.e., the dominant color is not green).
    c.  Check if this dominant row color is green (3).
3.  Iterate through each pixel of the input grid at position `(r, c)`:
    a.  If the input pixel at `(r, c)` is azure (8):
        i.  Retrieve the result from step 2c for row `r`.
        ii. If the dominant row color for row `r` was *not* green (3), set the pixel at `(r, c)` in the output grid to azure (8).
    b.  If the input pixel is not azure (8), or if it is azure (8) but the dominant color of its row is green (3), leave the corresponding pixel in the output grid as white (0).
4.  Return the completed output grid.
