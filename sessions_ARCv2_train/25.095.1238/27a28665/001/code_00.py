import numpy as np
from typing import List, Tuple, Set, FrozenSet

"""
Identifies the spatial pattern of non-zero cells within the 3x3 input grid. 
Based on the specific pattern recognized, returns a predetermined integer value.

The mapping between observed patterns (represented as a frozenset of (row, col) coordinates of non-zero cells) and the output integer is derived from the training examples:
- Pattern {(0, 1), (0, 2), (1, 1), (1, 2), (2, 0)} maps to 3. (L-shape)
- Pattern {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)} maps to 6. (Plus-shape)
- Pattern {(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)} maps to 2. (X-shape)
- Pattern {(0, 0), (0, 1), (1, 0), (1, 2), (2, 1)} maps to 1. (Hook-shape)
"""

# Define the known shape patterns based on the coordinates of their non-zero cells
SHAPE_L = frozenset({(0, 1), (0, 2), (1, 1), (1, 2), (2, 0)})
SHAPE_PLUS = frozenset({(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)})
SHAPE_X = frozenset({(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)})
SHAPE_HOOK = frozenset({(0, 0), (0, 1), (1, 0), (1, 2), (2, 1)})

# Map shapes to their corresponding output values
SHAPE_OUTPUT_MAP = {
    SHAPE_L: 3,
    SHAPE_PLUS: 6,
    SHAPE_X: 2,
    SHAPE_HOOK: 1,
}

def get_non_zero_coords(grid: np.ndarray) -> FrozenSet[Tuple[int, int]]:
    """Finds the coordinates of all non-zero cells in the grid."""
    rows, cols = np.where(grid != 0)
    coords = frozenset(zip(rows, cols))
    return coords

def transform(input_grid_list: list[list[int]]) -> int:
    """
    Transforms the input grid based on the spatial pattern of non-zero cells.

    Args:
        input_grid_list: A 3x3 list of lists representing the input grid.

    Returns:
        An integer corresponding to the recognized pattern.
    """
    # Convert list of lists to numpy array for easier processing
    input_grid = np.array(input_grid_list, dtype=int)

    # Find the coordinates of all non-zero cells
    non_zero_coords = get_non_zero_coords(input_grid)

    # Look up the shape in the map
    output_value = SHAPE_OUTPUT_MAP.get(non_zero_coords)

    # Handle unknown shapes (though based on examples, this shouldn't happen)
    if output_value is None:
        # Default or error handling for unknown patterns
        # For this problem, we assume all test cases will match one of the train patterns
        raise ValueError(f"Unknown shape pattern encountered: {non_zero_coords}")

    # Return the corresponding integer value
    return output_value
