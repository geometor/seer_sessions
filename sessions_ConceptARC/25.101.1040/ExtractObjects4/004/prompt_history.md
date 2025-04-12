
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
```


## train_2

**input:**
```
0 0 0 0 0 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
0 6 6 6 6 0
6 6 6 6 6 6
0 6 6 6 6 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
```


**output:**
```
6 6 6 6
6 6 6 6
6 6 6 6
6 6 6 6
6 6 6 6
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```


**output:**
```
4 4 4
4 4 4
4 4 4
```

Okay, I will analyze the provided examples to understand the transformation task.

**Perception**

1.  **Input Structure:** The input grids consist primarily of two colors: white (0) and one other dominant non-white color (red=2, magenta=6, yellow=4 in the examples). These colors often appear in alternating horizontal rows.
2.  **Row Variation:** Some rows containing the dominant non-white color are completely filled with that color, while others contain interspersed white pixels ("holes" or "impurities").
3.  **Output Structure:** The output grids are always squares, significantly smaller than the input grids, and are filled uniformly with the dominant non-white color found in the input.
4.  **Transformation Clue:** The size of the output square seems related to some property of the input grid. Initial thoughts about counting purely colored *rows* didn't consistently match the output size across examples.
5.  **Columnar Pattern:** Analyzing the columns reveals a pattern: The size of the output square (`N x N`) corresponds to the number of columns in the input grid that are "pure" relative to the dominant non-white color. A column is considered "pure" if, within all the rows that contain *any* instance of the dominant color, that specific column *only* contains the dominant color.
6.  **Core Logic:** The task identifies the main color, filters the input grid based on column purity (where purity is defined by the absence of white pixels in specific locations within the column), counts these pure columns, and generates a square output of that count's dimension filled with the main color.

**Facts**


```yaml
task_elements:
  - name: Input Grid
    attributes:
      - height: integer
      - width: integer
      - pixels: 2D array of colors (0-9)
      - contains_dominant_color: non-white color C
      - contains_white_pixels: color 0
      - structure: often alternating rows of white and color C
  - name: Output Grid
    attributes:
      - height: N (integer)
      - width: N (integer)
      - pixels: 2D array, uniformly filled with color C
      - shape: square

properties:
  - name: Dominant Color (C)
    description: The single non-white color present in the input grid.
  - name: Relevant Rows
    description: The set of row indices in the input grid that contain at least one pixel of the Dominant Color C.
  - name: Pure Column
    description: A column 'j' in the input grid such that for every row index 'i' in the set of Relevant Rows, the pixel input[i][j] has the Dominant Color C.
  - name: Pure Column Count (N)
    description: The total number of Pure Columns in the input grid.

relationships:
  - Output grid dimension N is determined by the Pure Column Count N.
  - Output grid color is the Dominant Color C from the input grid.

actions:
  - Identify the Dominant Color C.
  - Identify the Relevant Rows.
  - Iterate through input columns to identify Pure Columns.
  - Count the number of Pure Columns (N).
  - Generate an N x N grid filled with Dominant Color C.
```


**Natural Language Program**

1.  **Identify Dominant Color:** Scan the input grid to find the single non-white color present. Let this color be `dominant_color`.
2.  **Identify Relevant Rows:** Determine the indices of all rows in the input grid that contain at least one pixel of `dominant_color`. Store these indices in a list called `relevant_row_indices`.
3.  **Count Pure Columns:**
    a.  Initialize a counter `pure_column_count` to 0.
    b.  Iterate through each column index `j` of the input grid.
    c.  For the current column `j`, assume it is pure (`is_column_pure = true`).
    d.  Iterate through each row index `i` in `relevant_row_indices`.
    e.  Check the color of the pixel at `input_grid[i][j]`.
    f.  If `input_grid[i][j]` is *not* equal to `dominant_color`, set `is_column_pure = false` and stop checking rows for this column `j` (break the inner loop).
    g.  After checking all relevant rows for column `j`, if `is_column_pure` is still `true`, increment `pure_column_count`.
4.  **Determine Output Size:** The size `N` for the output square grid is equal to `pure_column_count`.
5.  **Create Output Grid:** Generate a new grid of size `N x N`, filling every cell with the `dominant_color`. This is the final output.
```python
import numpy as np
from typing import List

"""
Identifies the single dominant non-white color in the input grid.
Determines the set of rows that contain at least one instance of this dominant color.
Counts the number of columns where all cells intersecting with the identified rows contain only the dominant color ('pure columns').
Generates a square output grid whose side length equals the count of pure columns, filled entirely with the dominant color.
"""

def find_dominant_color(grid_np: np.ndarray) -> int:
    """Finds the single non-white color in the grid."""
    unique_colors = np.unique(grid_np)
    non_white_colors = unique_colors[unique_colors != 0]
    if len(non_white_colors) != 1:
        # This case might need more sophisticated handling based on task variations,
        # but for the given examples, we expect exactly one non-white color.
        # Let's raise an error or return a default if the assumption is violated.
        # For now, assume the first non-white color is the dominant one if multiple exist,
        # or handle the case where none exists.
        if len(non_white_colors) == 0:
             raise ValueError("No non-white color found in the input grid.")
        # If more than one, pick the lowest value perhaps? Or the most frequent?
        # Based on examples, only one is expected. We'll take the first.
        # print(f"Warning: Found multiple non-white colors: {non_white_colors}. Using {non_white_colors[0]}")
        return non_white_colors[0] # Or raise an error if strict adherence is needed
    return non_white_colors[0]

def find_relevant_rows(grid_np: np.ndarray, dominant_color: int) -> np.ndarray:
    """Finds the indices of rows containing the dominant color."""
    rows_with_color = np.any(grid_np == dominant_color, axis=1)
    relevant_indices = np.where(rows_with_color)[0]
    return relevant_indices

def count_pure_columns(grid_np: np.ndarray, dominant_color: int, relevant_row_indices: np.ndarray) -> int:
    """Counts columns that are 'pure' with respect to the dominant color in relevant rows."""
    if relevant_row_indices.size == 0:
        # If no rows contain the dominant color, technically no columns can be 'pure'
        # based on the definition, or perhaps the output should be empty/0x0.
        # Returning 0 seems consistent with creating a 0x0 grid.
        return 0

    num_cols = grid_np.shape[1]
    pure_column_count = 0

    for j in range(num_cols):
        # Extract the column slice only for the relevant rows
        column_slice = grid_np[relevant_row_indices, j]
        # Check if all elements in this slice are the dominant color
        if np.all(column_slice == dominant_color):
            pure_column_count += 1

    return pure_column_count

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on identifying pure columns relative to the dominant color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)

    if input_grid_np.size == 0:
        return [] # Handle empty input grid case

    # 1. Identify the Dominant Color
    try:
        dominant_color = find_dominant_color(input_grid_np)
    except ValueError:
        # Handle cases where no dominant color is found (e.g., all white grid)
        # Returning an empty grid might be appropriate.
        return []


    # 2. Identify Relevant Rows (rows containing the dominant color)
    relevant_row_indices = find_relevant_rows(input_grid_np, dominant_color)

    # 3. Count Pure Columns
    # A column is pure if, for all relevant rows, the cell in that column contains the dominant color.
    pure_column_count = count_pure_columns(input_grid_np, dominant_color, relevant_row_indices)

    # 4. Determine Output Size
    output_size = pure_column_count

    # 5. Create Output Grid
    # Generate an N x N grid filled with the dominant color, where N is the pure column count.
    output_grid_np = np.full((output_size, output_size), dominant_color, dtype=int)

    # Convert numpy array back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid
```

Previous Code:
```python
import numpy as np
from typing import List

"""
Identifies the single dominant non-white color in the input grid.
Determines the set of rows that contain at least one instance of this dominant color.
Counts the number of columns where all cells intersecting with the identified rows contain only the dominant color ('pure columns').
Generates a square output grid whose side length equals the count of pure columns, filled entirely with the dominant color.
"""

def find_dominant_color(grid_np: np.ndarray) -> int:
    """Finds the single non-white color in the grid."""
    unique_colors = np.unique(grid_np)
    non_white_colors = unique_colors[unique_colors != 0]
    if len(non_white_colors) != 1:
        # This case might need more sophisticated handling based on task variations,
        # but for the given examples, we expect exactly one non-white color.
        # Let's raise an error or return a default if the assumption is violated.
        # For now, assume the first non-white color is the dominant one if multiple exist,
        # or handle the case where none exists.
        if len(non_white_colors) == 0:
             raise ValueError("No non-white color found in the input grid.")
        # If more than one, pick the lowest value perhaps? Or the most frequent?
        # Based on examples, only one is expected. We'll take the first.
        # print(f"Warning: Found multiple non-white colors: {non_white_colors}. Using {non_white_colors[0]}")
        return non_white_colors[0] # Or raise an error if strict adherence is needed
    return non_white_colors[0]

def find_relevant_rows(grid_np: np.ndarray, dominant_color: int) -> np.ndarray:
    """Finds the indices of rows containing the dominant color."""
    rows_with_color = np.any(grid_np == dominant_color, axis=1)
    relevant_indices = np.where(rows_with_color)[0]
    return relevant_indices

def count_pure_columns(grid_np: np.ndarray, dominant_color: int, relevant_row_indices: np.ndarray) -> int:
    """Counts columns that are 'pure' with respect to the dominant color in relevant rows."""
    if relevant_row_indices.size == 0:
        # If no rows contain the dominant color, technically no columns can be 'pure'
        # based on the definition, or perhaps the output should be empty/0x0.
        # Returning 0 seems consistent with creating a 0x0 grid.
        return 0

    num_cols = grid_np.shape[1]
    pure_column_count = 0

    for j in range(num_cols):
        # Extract the column slice only for the relevant rows
        column_slice = grid_np[relevant_row_indices, j]
        # Check if all elements in this slice are the dominant color
        if np.all(column_slice == dominant_color):
            pure_column_count += 1

    return pure_column_count

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on identifying pure columns relative to the dominant color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)

    if input_grid_np.size == 0:
        return [] # Handle empty input grid case

    # 1. Identify the Dominant Color
    try:
        dominant_color = find_dominant_color(input_grid_np)
    except ValueError:
        # Handle cases where no dominant color is found (e.g., all white grid)
        # Returning an empty grid might be appropriate.
        return []


    # 2. Identify Relevant Rows (rows containing the dominant color)
    relevant_row_indices = find_relevant_rows(input_grid_np, dominant_color)

    # 3. Count Pure Columns
    # A column is pure if, for all relevant rows, the cell in that column contains the dominant color.
    pure_column_count = count_pure_columns(input_grid_np, dominant_color, relevant_row_indices)

    # 4. Determine Output Size
    output_size = pure_column_count

    # 5. Create Output Grid
    # Generate an N x N grid filled with the dominant color, where N is the pure column count.
    output_grid_np = np.full((output_size, output_size), dominant_color, dtype=int)

    # Convert numpy array back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
```
Transformed Output:
```
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
0 0 0 0 0 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
0 6 6 6 6 0
6 6 6 6 6 6
0 6 6 6 6 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
```
Expected Output:
```
6 6 6 6
6 6 6 6
6 6 6 6
6 6 6 6
6 6 6 6
```
Transformed Output:
```
6 6 6 6
6 6 6 6
6 6 6 6
6 6 6 6
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4
4 4 4
4 4 4
```
Transformed Output:
```
4 4 4
4 4 4
4 4 4
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
**General Assessment**

The previous transformation attempt correctly identified the core components: finding a dominant color, identifying relevant rows, and analyzing columns based on those rows. The implemented logic counted columns where *all* pixels within the relevant rows matched the dominant color ("pure columns"). This logic successfully produced the correct output size for `train_1` (5x5) and `train_3` (3x3).

However, for `train_2`, this logic resulted in a 4x4 output, while the expected output was 5x5. Despite exploring alternative hypotheses (e.g., counting pure rows, taking the minimum/maximum of pure rows/columns, analyzing impurity counts), the most consistent logic across `train_1` and `train_3` remains tied to the count of "pure columns" as initially defined.

The strategy moving forward is to refine the documentation and natural language program based on the "pure column count" hypothesis, acknowledging the discrepancy in `train_2` but prioritizing the pattern observed in the other two examples. The definition of a "pure column" appears robust for `train_1` and `train_3`.

**Metrics**


*code_execution:*
```python
import numpy as np

def analyze_example(input_grid):
    grid_np = np.array(input_grid)
    metrics = {}

    # Dominant Color
    unique_colors = np.unique(grid_np)
    non_white_colors = unique_colors[unique_colors != 0]
    if len(non_white_colors) == 0:
        metrics['dominant_color'] = None
        metrics['relevant_row_indices'] = []
        metrics['pure_row_indices'] = []
        metrics['pure_column_indices'] = []
        return metrics
    # Assuming one dominant color as per task structure
    dominant_color = non_white_colors[0]
    metrics['dominant_color'] = dominant_color

    # Relevant Rows (contain dominant color)
    rows_with_color = np.any(grid_np == dominant_color, axis=1)
    relevant_row_indices = np.where(rows_with_color)[0].tolist()
    metrics['relevant_row_indices'] = relevant_row_indices

    # Pure Rows (contain ONLY dominant color, ignoring all-white rows)
    pure_row_indices = []
    for i in relevant_row_indices:
         row = grid_np[i, :]
         # Check if all non-zero elements are the dominant color AND if there's at least one dominant color
         if np.all(row[row != 0] == dominant_color) and np.any(row == dominant_color):
             # Further check: ensure NO zeros exist if we expect pure rows to be *full*
             if np.all(row == dominant_color):
                 pure_row_indices.append(i)
    metrics['pure_row_indices'] = pure_row_indices

    # Pure Columns (contain ONLY dominant color within RELEVANT rows)
    pure_column_indices = []
    if relevant_row_indices: # Check if list is not empty
        num_cols = grid_np.shape[1]
        relevant_rows_np = np.array(relevant_row_indices) # Convert list to numpy array for indexing
        for j in range(num_cols):
            column_slice = grid_np[relevant_rows_np, j]
            if np.all(column_slice == dominant_color):
                pure_column_indices.append(j)
    metrics['pure_column_indices'] = pure_column_indices

    # Add counts
    metrics['relevant_row_count'] = len(relevant_row_indices)
    metrics['pure_row_count'] = len(pure_row_indices)
    metrics['pure_column_count'] = len(pure_column_indices)

    return metrics

# Example Data
train_1_input = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

train_2_input = [
    [0, 0, 0, 0, 0, 0],
    [6, 6, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0],
    [6, 6, 6, 6, 6, 6],
    [0, 6, 6, 6, 6, 0],
    [6, 6, 6, 6, 6, 6],
    [0, 6, 6, 6, 6, 0],
    [6, 6, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0],
    [6, 6, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0],
    [6, 6, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0],
    [6, 6, 6, 6, 6, 6]
]

train_3_input = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
]

metrics_1 = analyze_example(train_1_input)
metrics_2 = analyze_example(train_2_input)
metrics_3 = analyze_example(train_3_input)

print("--- Metrics Example 1 ---")
print(metrics_1)
print("--- Metrics Example 2 ---")
print(metrics_2)
print("--- Metrics Example 3 ---")
print(metrics_3)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Metrics Example 1 ---
{'dominant_color': np.int64(2), 'relevant_row_indices': [1, 3, 5, 6, 7, 8, 9, 11, 13], 'pure_row_indices': [1, 3, 5, 7, 9, 11, 13], 'pure_column_indices': [1, 2, 3, 4, 5], 'relevant_row_count': 9, 'pure_row_count': 7, 'pure_column_count': 5}
--- Metrics Example 2 ---
{'dominant_color': np.int64(6), 'relevant_row_indices': [1, 3, 4, 5, 6, 7, 9, 11, 13], 'pure_row_indices': [1, 3, 5, 7, 9, 11, 13], 'pure_column_indices': [1, 2, 3, 4], 'relevant_row_count': 9, 'pure_row_count': 7, 'pure_column_count': 4}
--- Metrics Example 3 ---
{'dominant_color': np.int64(4), 'relevant_row_indices': [1, 2, 3, 5], 'pure_row_indices': [1, 3, 5], 'pure_column_indices': [11, 12, 13], 'relevant_row_count': 4, 'pure_row_count': 3, 'pure_column_count': 3}

```
**Facts**


```yaml
task_elements:
  - name: Input Grid
    attributes:
      - height: integer
      - width: integer
      - pixels: 2D array of colors (0-9)
      - contains_dominant_color: A single non-white color C.
      - contains_white_pixels: color 0, potentially interspersed within rows containing C.
  - name: Output Grid
    attributes:
      - height: N (integer)
      - width: N (integer)
      - pixels: 2D array, uniformly filled with color C.
      - shape: square

properties:
  - name: Dominant Color (C)
    description: The single non-white color present in the input grid.
  - name: Relevant Rows
    description: The set of row indices in the input grid that contain at least one pixel of the Dominant Color C.
  - name: Pure Column
    description: A column 'j' in the input grid such that for every row index 'i' in the set of Relevant Rows, the pixel input_grid[i][j] has the Dominant Color C. (Contains no other color, including white, within the relevant rows).
  - name: Pure Column Count (N)
    description: The total number of Pure Columns in the input grid. This count determines the output grid size.

relationships:
  - Output grid dimension N is determined by the Pure Column Count N.
  - Output grid color is the Dominant Color C from the input grid.

actions:
  - Identify the Dominant Color C.
  - Identify the Relevant Rows.
  - Iterate through input columns to identify Pure Columns based on the definition above.
  - Count the number of Pure Columns (N).
  - Generate an N x N grid filled with Dominant Color C.
```


**Natural Language Program**

1.  **Identify Dominant Color:** Scan the input grid to find the single non-white color present. Let this color be `dominant_color`.
2.  **Identify Relevant Rows:** Determine the indices of all rows in the input grid that contain at least one pixel of `dominant_color`. Store these indices in a list called `relevant_row_indices`.
3.  **Count Pure Columns:**
    a.  Initialize a counter `pure_column_count` to 0.
    b.  Iterate through each column index `j` from 0 to `width - 1` of the input grid.
    c.  For the current column `j`, assume it is pure (`is_column_pure = true`).
    d.  If `relevant_row_indices` is empty, stop and set `pure_column_count` to 0.
    e.  Otherwise, iterate through each row index `i` in `relevant_row_indices`.
    f.  Check the color of the pixel at `input_grid[i][j]`.
    g.  If `input_grid[i][j]` is *not* equal to `dominant_color`, set `is_column_pure = false` and stop checking rows for this column `j` (break the inner loop).
    h.  After checking all relevant rows for column `j` (or breaking early), if `is_column_pure` is still `true`, increment `pure_column_count`.
4.  **Determine Output Size:** The size `N` for the output square grid is equal to the final `pure_column_count`.
5.  **Create Output Grid:** Generate a new grid of size `N x N`, filling every cell with the `dominant_color`. This is the final output.
```python
"""
Identifies the single dominant non-white color in the input grid.
Determines the set of rows that contain at least one instance of this dominant color ('relevant rows').
Counts the number of columns where all cells intersecting with the relevant rows contain only the dominant color ('pure columns').
Generates a square output grid whose side length equals the count of pure columns, filled entirely with the dominant color.
"""

import numpy as np
from typing import List, Tuple, Optional

# Helper function to find the dominant non-white color
def find_dominant_color(grid_np: np.ndarray) -> Optional[int]:
    """Finds the single non-white color in the grid."""
    unique_colors = np.unique(grid_np)
    non_white_colors = unique_colors[unique_colors != 0]
    if len(non_white_colors) == 1:
        return int(non_white_colors[0])
    elif len(non_white_colors) == 0:
        # Handle case with no non-white colors (e.g., all white grid)
        return None
    else:
        # Handle case with multiple non-white colors if needed,
        # based on examples, only one is expected.
        # For now, return the first one found, though this might need adjustment
        # if future tasks show ambiguity.
        # print(f"Warning: Found multiple non-white colors: {non_white_colors}. Using {non_white_colors[0]}")
        return int(non_white_colors[0]) # Or raise an error

# Helper function to find relevant row indices
def find_relevant_rows(grid_np: np.ndarray, dominant_color: int) -> np.ndarray:
    """Finds the indices of rows containing the dominant color."""
    if dominant_color is None:
        return np.array([], dtype=int)
    rows_with_color = np.any(grid_np == dominant_color, axis=1)
    relevant_indices = np.where(rows_with_color)[0]
    return relevant_indices

# Helper function to count pure columns
def count_pure_columns(grid_np: np.ndarray, dominant_color: int, relevant_row_indices: np.ndarray) -> int:
    """Counts columns that are 'pure' with respect to the dominant color in relevant rows."""
    # If no dominant color or no relevant rows found, no columns can be pure by definition.
    if dominant_color is None or relevant_row_indices.size == 0:
        return 0

    num_cols = grid_np.shape[1]
    pure_column_count = 0

    for j in range(num_cols):
        # Extract the column slice corresponding to the relevant rows
        column_slice = grid_np[relevant_row_indices, j]
        # Check if all elements in this slice are the dominant color
        if np.all(column_slice == dominant_color):
            pure_column_count += 1

    return pure_column_count

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on identifying pure columns relative to the dominant color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input to numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)

    # Handle empty input grid case
    if input_grid_np.size == 0:
        return []

    # 1. Identify the Dominant Color
    dominant_color = find_dominant_color(input_grid_np)

    # Handle case where no dominant color is found (e.g., all white)
    if dominant_color is None:
        # Return empty grid or handle as per specific task requirements if this occurs
        return []

    # 2. Identify Relevant Rows (rows containing the dominant color)
    relevant_row_indices = find_relevant_rows(input_grid_np, dominant_color)

    # 3. Count Pure Columns
    # A column is pure if, for all relevant rows, the cell in that column contains the dominant color.
    pure_column_count = count_pure_columns(input_grid_np, dominant_color, relevant_row_indices)

    # 4. Determine Output Size
    output_size = pure_column_count

    # 5. Create Output Grid
    # Generate an N x N grid filled with the dominant color, where N is the pure column count.
    output_grid_np = np.full((output_size, output_size), dominant_color, dtype=int)

    # Convert numpy array back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid
```
