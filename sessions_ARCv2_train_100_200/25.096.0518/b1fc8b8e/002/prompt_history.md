
## train_1

**input:**
```
8 8 8 8 0 0
8 8 8 8 8 8
0 8 8 0 8 8
0 8 8 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
8 8 0 8 8
8 8 0 8 8
0 0 0 0 0
8 8 0 8 8
8 8 0 8 8
```


## train_2

**input:**
```
0 0 8 8 0 0
8 8 8 8 0 0
8 8 8 8 8 8
0 0 8 8 8 8
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
8 8 0 8 8
8 8 0 8 8
0 0 0 0 0
8 8 0 8 8
8 8 0 8 8
```


## train_3

**input:**
```
0 0 0 8 0 0
0 8 8 8 0 0
8 8 8 0 8 0
0 8 8 8 8 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 8 0 0 8
8 8 0 8 8
0 0 0 0 0
0 8 0 0 8
8 8 0 8 8
```


## train_4

**input:**
```
0 0 0 8 0 0
0 8 8 8 8 0
8 8 8 8 8 0
0 8 8 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 8 0 0 8
8 8 0 8 8
0 0 0 0 0
0 8 0 0 8
8 8 0 8 8
```


## train_5

**input:**
```
0 0 0 8 0 0
0 0 8 8 8 0
0 8 0 8 8 0
8 8 8 0 0 0
0 8 8 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 8 0 0 8
8 8 0 8 8
0 0 0 0 0
0 8 0 0 8
8 8 0 8 8
```

## Perception

1.  **Input/Output Format:** The input is a 6x6 grid of integers (0 and 8). The output is a 5x5 grid of integers (0 and 8).
2.  **Color Palette:** Only two distinct numbers (colors) are used: 0 (representing perhaps black or background) and 8 (representing perhaps red or foreground).
3.  **Dimensionality Change:** The grid size reduces from 6x6 to 5x5.
4.  **Output Structure:** The output grids exhibit distinct, highly structured patterns. There appear to be two primary patterns for the output grid, determined by the content of the input grid.
5.  **Row Patterns:** The output grids are constructed from a small set of predefined 1x5 row patterns. Let's identify them:
    *   `P0 = 0 0 0 0 0` (Zero row)
    *   `P1 = 8 8 0 8 8`
    *   `P2 = 0 8 0 0 8`
6.  **Conditional Output Generation:** The specific arrangement of these row patterns (P0, P1, P2) in the 5x5 output depends on a condition evaluated on the input grid.
    *   **Output Pattern 1:** Observed in `train_1` and `train_2`. The structure is `P1, P1, P0, P1, P1`.
    *   **Output Pattern 2:** Observed in `train_3`, `train_4`, and `train_5`. The structure is `P2, P1, P0, P2, P1`.
7.  **Trigger Condition:** The switch between Output Pattern 1 and Output Pattern 2 seems to depend on the presence of a specific 3x3 pattern within the 6x6 input grid. The pattern that triggers Output Pattern 1 appears to be a 3x3 subgrid where the top two rows consist entirely of 8s (`[[8, 8, 8], [8, 8, 8], [*, *, *]]`, where '*' can be 0 or 8). If this pattern is found anywhere in the input, Output Pattern 1 is generated; otherwise, Output Pattern 2 is generated.

## YAML Facts


```yaml
task_elements:
  - element: grid
    properties:
      - type: input
      - dimensions: 6x6
      - cells: integer
      - values: [0, 8]
  - element: grid
    properties:
      - type: output
      - dimensions: 5x5
      - cells: integer
      - values: [0, 8]
transformation:
  - operation: pattern_detection
    description: Check the input grid for a specific 3x3 pattern.
    details:
      - pattern_name: TriggerPattern
      - pattern_definition: A 3x3 subgrid where the first row is [8, 8, 8] and the second row is [8, 8, 8]. The third row can contain any combination of 0s and 8s.
      - input: input grid (6x6)
      - output: boolean (true if found, false otherwise)
  - operation: define_patterns
    description: Define fixed 1x5 row patterns used to construct the output.
    details:
      - pattern_name: P0
        value: [0, 0, 0, 0, 0]
      - pattern_name: P1
        value: [8, 8, 0, 8, 8]
      - pattern_name: P2
        value: [0, 8, 0, 0, 8]
  - operation: conditional_assembly
    description: Assemble the 5x5 output grid based on the result of the pattern detection.
    details:
      - condition: TriggerPattern found in input grid
        output_assembly:
          - row_1: P1
          - row_2: P1
          - row_3: P0
          - row_4: P1
          - row_5: P1
      - condition: TriggerPattern not found in input grid
        output_assembly:
          - row_1: P2
          - row_2: P1
          - row_3: P0
          - row_4: P2
          - row_5: P1
relationships:
  - type: conditional_dependency
    from: presence of TriggerPattern in input grid
    to: structure of the output grid
```


## Natural Language Program

1.  Define three constant row patterns of size 1x5:
    *   `P0` = `[0, 0, 0, 0, 0]`
    *   `P1` = `[8, 8, 0, 8, 8]`
    *   `P2` = `[0, 8, 0, 0, 8]`
2.  Search the input 6x6 grid for any occurrence of a 3x3 subgrid where the top row is `[8, 8, 8]` and the second row is `[8, 8, 8]` (the third row can be anything). Let's call this the "Trigger Pattern".
3.  If the Trigger Pattern is found anywhere in the input grid:
    *   Construct the 5x5 output grid by stacking the rows in the following order: `P1`, `P1`, `P0`, `P1`, `P1`.
4.  If the Trigger Pattern is *not* found anywhere in the input grid:
    *   Construct the 5x5 output grid by stacking the rows in the following order: `P2`, `P1`, `P0`, `P2`, `P1`.
5.  Return the constructed 5x5 grid as the output.
```python
import numpy as np

def find_trigger_pattern(grid: list[list[int]]) -> bool:
    """
    Searches a 6x6 grid for a 3x3 subgrid where the first two rows are [8, 8, 8].

    Args:
        grid: The input 6x6 grid represented as a list of lists.

    Returns:
        True if the pattern is found, False otherwise.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # The pattern requires at least 3 rows and 3 columns in the grid
    if rows < 3 or cols < 3:
        return False

    # Iterate through all possible top-left corners of a 3x3 subgrid
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Check if the first row of the 3x3 subgrid matches [8, 8, 8]
            row1_match = (grid[r][c] == 8 and
                          grid[r][c+1] == 8 and
                          grid[r][c+2] == 8)
            # Check if the second row of the 3x3 subgrid matches [8, 8, 8]
            row2_match = (grid[r+1][c] == 8 and
                          grid[r+1][c+1] == 8 and
                          grid[r+1][c+2] == 8)

            if row1_match and row2_match:
                return True  # Pattern found

    return False # Pattern not found after checking all positions

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 6x6 input grid into a 5x5 output grid based on the presence
    of a specific 3x3 pattern ([ [8, 8, 8], [8, 8, 8], [*, *, *] ]) in the input.

    If the pattern is found, a specific 5x5 grid (Pattern A) is returned.
    If the pattern is not found, a different 5x5 grid (Pattern B) is returned.
    """

    # Define the constant 1x5 row patterns
    P0 = [0, 0, 0, 0, 0]
    P1 = [8, 8, 0, 8, 8]
    P2 = [0, 8, 0, 0, 8]

    # Define the two possible output patterns
    output_pattern_A = [P1, P1, P0, P1, P1] # Used when trigger pattern is found
    output_pattern_B = [P2, P1, P0, P2, P1] # Used when trigger pattern is NOT found

    # Search for the trigger pattern in the input grid
    trigger_found = find_trigger_pattern(input_grid)

    # Select the appropriate output pattern based on whether the trigger was found
    if trigger_found:
        output_grid = output_pattern_A
    else:
        output_grid = output_pattern_B

    return output_grid
```
