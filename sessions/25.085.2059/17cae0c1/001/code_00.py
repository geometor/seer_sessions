"""
Transforms a 3x9 input grid composed of white (0) and gray (5) pixels into a 3x9 output grid.
The transformation involves dividing the input grid into three adjacent 3x3 subgrids.
Each input 3x3 subgrid's pattern of gray pixels maps to a specific solid color that fills the corresponding 3x3 block in the output grid.
The output grid is constructed by horizontally concatenating these three 3x3 colored blocks.

The specific pattern-to-color mappings observed are:
- Top row gray ([[5, 5, 5], [0, 0, 0], [0, 0, 0]]) -> Magenta (6)
- U-shape ([[5, 0, 5], [5, 0, 5], [5, 5, 5]]) -> Green (3)
- G-shape ([[5, 5, 5], [5, 0, 5], [5, 5, 5]]) -> Green (3)
- Bottom row gray ([[0, 0, 0], [0, 0, 0], [5, 5, 5]]) -> Blue (1)
- Anti-diagonal gray ([[0, 0, 5], [0, 5, 0], [5, 0, 0]]) -> Maroon (9)
- Center pixel gray ([[0, 0, 0], [0, 5, 0], [0, 0, 0]]) -> Yellow (4)
"""

import numpy as np

def _get_pattern_key(subgrid):
    """Converts a 3x3 numpy subgrid into a hashable tuple key."""
    return tuple(map(tuple, subgrid.tolist()))

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Define the mapping from input 3x3 pattern (represented as tuple of tuples) to output color
    pattern_to_color_map = {
        # train_1
        ((5, 5, 5), (0, 0, 0), (0, 0, 0)): 6, # Magenta
        ((5, 0, 5), (5, 5, 5), (5, 5, 5)): 3, # Green (Note: This looks like the 'G' shape from train_3, but derived from train_1 input)
        ((0, 0, 0), (0, 0, 0), (5, 5, 5)): 1, # Blue
        # train_2
        ((0, 0, 5), (0, 5, 0), (5, 0, 0)): 9, # Maroon
        ((0, 0, 0), (0, 0, 0), (5, 5, 5)): 1, # Blue (Repeated, consistent)
        ((0, 0, 0), (0, 5, 0), (0, 0, 0)): 4, # Yellow
        # train_3
        ((0, 0, 0), (0, 5, 0), (0, 0, 0)): 4, # Yellow (Repeated, consistent)
        ((5, 5, 5), (0, 0, 0), (0, 0, 0)): 6, # Magenta (Repeated, consistent)
        ((5, 5, 5), (5, 0, 5), (5, 5, 5)): 3, # Green ('G' shape)
        # train_4
        ((5, 5, 5), (5, 0, 5), (5, 5, 5)): 3, # Green ('G' shape, repeated, consistent)
        ((0, 0, 0), (0, 5, 0), (0, 0, 0)): 4, # Yellow (Repeated, consistent)
        ((0, 0, 5), (0, 5, 0), (5, 0, 0)): 9, # Maroon (Repeated, consistent)
        # Adding the U-shape from train_1's middle block interpretation from natural language description
        # This pattern was originally interpreted differently above, let's use the one from the NL description
         ((5, 0, 5), (5, 0, 5), (5, 5, 5)): 3, # Green ('U' shape) - Correcting previous interpretation
         # Let's re-evaluate train_1 middle block: [[5, 0, 5], [5, 0, 5], [5, 5, 5]] - yes, U shape
         # Let's re-evaluate train_1 right block: [[0,0,0],[0,0,0],[5,5,5]] - yes, bottom row
         # Need to remove the incorrect one derived from train_1 middle: ((5, 0, 5), (5, 5, 5), (5, 5, 5)): 3,
    }
    # Cleanup map based on re-evaluation and remove duplicates
    pattern_to_color_map = {
        ((5, 5, 5), (0, 0, 0), (0, 0, 0)): 6, # Magenta
        ((5, 0, 5), (5, 0, 5), (5, 5, 5)): 3, # Green (U-shape)
        ((0, 0, 0), (0, 0, 0), (5, 5, 5)): 1, # Blue
        ((0, 0, 5), (0, 5, 0), (5, 0, 0)): 9, # Maroon
        ((0, 0, 0), (0, 5, 0), (0, 0, 0)): 4, # Yellow
        ((5, 5, 5), (5, 0, 5), (5, 5, 5)): 3, # Green (G-shape)
    }


    # Initialize output grid (same size as input)
    output_grid = np.zeros_like(input_np)

    # Process the grid in 3x3 chunks horizontally
    for i in range(0, width, 3):
        # Extract the 3x3 input subgrid
        input_subgrid = input_np[0:3, i:i+3]

        # Get the pattern key for the subgrid
        pattern_key = _get_pattern_key(input_subgrid)

        # Find the corresponding output color from the map
        # Use a default color (e.g., 0/white) if pattern not found, although all should be found based on examples
        output_color = pattern_to_color_map.get(pattern_key, 0)

        # Create the 3x3 output block filled with the determined color
        output_block = np.full((3, 3), output_color, dtype=int)

        # Place the output block into the corresponding position in the output grid
        output_grid[0:3, i:i+3] = output_block

    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
