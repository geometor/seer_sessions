import numpy as np

def analyze_example(input_grid, output_grid):
    """Analyzes a single input/output pair and returns relevant information."""
    input_yellow_coords = np.argwhere(input_grid == 4)
    input_red_coords = np.argwhere(input_grid == 2)
    output_red_coords = np.argwhere(output_grid == 2)

    # Find the highest row of the yellow structure in the input
    highest_yellow_row_input = np.min(input_yellow_coords[:, 0]) if len(input_yellow_coords) > 0 else None
    
    #get the x,y of existing and new red
    existing_red = []
    if (len(input_red_coords) > 0):
        existing_red = input_red_coords
    
    new_red = []
    if (len(output_red_coords) > 0):
        for coord in output_red_coords:
            if not any(np.array_equal(coord, input_coord) for input_coord in input_red_coords):
                new_red.append(coord)

    return {
        'input_yellow_highest_row': highest_yellow_row_input,
        'existing_red': existing_red.tolist(),
        'new_red': new_red
    }

# Example usage (replace with actual input/output grids)
examples = [
    (
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0],
            [0, 0, 0, 0, 4, 2, 2, 4, 0, 0, 0],
            [0, 0, 0, 0, 4, 2, 2, 4, 0, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        np.array([
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0],
            [0, 0, 0, 0, 4, 2, 2, 4, 0, 0, 0],
            [0, 0, 0, 0, 4, 2, 2, 4, 0, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
    ),
     (
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0],
            [0, 0, 0, 0, 4, 2, 2, 4, 4, 0, 0],
            [0, 0, 0, 0, 4, 2, 2, 4, 4, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        np.array([
            [0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0],
            [0, 0, 0, 0, 4, 2, 2, 4, 4, 0, 0],
            [0, 0, 0, 0, 4, 2, 2, 4, 4, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
    ),
        (
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 4, 4, 0, 0, 0],
            [0, 0, 0, 4, 2, 4, 0, 0, 0],
            [0, 0, 0, 4, 4, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        np.array([
            [2, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 4, 4, 4, 0, 0, 0],
            [0, 0, 0, 4, 2, 4, 0, 0, 0],
            [0, 0, 0, 4, 4, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
    )
]

results = [analyze_example(input_grid, output_grid) for input_grid, output_grid in examples]
for i, r in enumerate(results):
    print (f"example {i}:")
    print (r)
