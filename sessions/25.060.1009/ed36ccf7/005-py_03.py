import numpy as np

def get_subgrids(grid, size=2):
    """Extracts all possible subgrids of a given size."""
    subgrids = []
    for r in range(grid.shape[0] - size + 1):
        for c in range(grid.shape[1] - size + 1):
            subgrids.append(grid[r:r+size, c:c+size])
    return subgrids

def analyze_examples(examples):
    """Analyzes input/output pairs to identify the rotating subgrid."""
    results = []
    for i, (input_grid, output_grid) in enumerate(examples):
        input_grid = np.array(input_grid)
        output_grid = np.array(output_grid)

        input_subgrids = get_subgrids(input_grid)
        rotated_input_subgrids = [np.rot90(sg, k=-1) for sg in input_subgrids]  # Clockwise rotation

        match_found = False
        for j, rotated_sg in enumerate(rotated_input_subgrids):
            # Find where the rotated subgrid appears in the output
            for r in range(output_grid.shape[0] - 1):
                for c in range(output_grid.shape[1] - 1):
                    if np.array_equal(rotated_sg, output_grid[r:r+2, c:c+2]):
                        results.append({
                            "example": i + 1,
                            "input_subgrid_coords": (j // (input_grid.shape[1]-1), j % (input_grid.shape[1]-1)), #original subgrid coordinates
                            "output_subgrid_coords": (r,c),
                            "subgrid_colors": [int(x) for x in input_subgrids[j].flatten()], #flattened list of colors

                        })
                        match_found = True
                        break  # Found in output, move to next subgrid
                if match_found:
                    break
        if not match_found:
            results.append({
                "example": i+1,
                "error": "No matching rotated subgrid found."
            })

    return results
examples = [
    ([[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]], [[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]]),
    ([[8, 5, 5, 8], [5, 5, 8, 5], [5, 5, 5, 5], [5, 5, 5, 5]], [[8, 5, 5, 8], [5, 8, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]),
    ([[8, 5, 5, 8, 5], [5, 5, 8, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 8]], [[8, 5, 5, 8, 5], [5, 8, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 8]]),
]

analysis = analyze_examples(examples)
for item in analysis:
    print(item)
