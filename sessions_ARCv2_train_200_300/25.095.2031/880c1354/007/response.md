```python
import copy

"""
Transforms an input grid by applying a fixed, cell-wise digit substitution rule.

The rule is determined by analyzing a specific example transformation (in this case, derived from train_1). 
Digits '4' and '7' are always invariant (map to themselves). 
Other digits present in the source example (1, 2, 3, 6 in train_1) undergo a specific permutation:
- 1 maps to 3
- 2 maps to 6
- 3 maps to 2
- 6 maps to 1
Digits not present in the source example's derived map (e.g., 0, 5, 8, 9) are assumed to map to themselves.

This function applies ONLY the train_1 rule and will not produce the correct output for inputs requiring different permutation rules (like train_2 or train_3).
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a fixed cell-wise digit substitution (based on train_1 analysis) to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid of digits.

    Returns:
        A new list of lists representing the transformed grid.
    """

    # 1. Define the substitution map based on the analysis of train_1
    # Invariant digits: 4 -> 4, 7 -> 7
    # Active digits permutation (4-cycle): 1 -> 3 -> 2 -> 6 -> 1
    substitution_map = {
        1: 3,
        2: 6,
        3: 2,
        4: 4,  # Invariant
        6: 1,
        7: 7,  # Invariant
        # Digits not in this map (0, 5, 8, 9) will default to identity mapping via .get()
    }

    # 2. Initialize the output grid with the same dimensions as the input
    # Using list comprehension for efficiency and clarity
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)] # Handle empty columns

    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # 3. Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # 4. Get the input digit value
            input_value = input_grid[r][c]

            # 5. Use the substitution map to find the output value
            # .get(key, default) handles digits not explicitly in the map
            output_value = substitution_map.get(input_value, input_value)

            # 6. Place the output value in the corresponding cell of the output grid
            output_grid[r][c] = output_value

    # 7. Return the completed output grid
    return output_grid
```