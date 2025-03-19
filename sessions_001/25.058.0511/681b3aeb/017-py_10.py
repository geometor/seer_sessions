import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    in_height, in_width = input_grid.shape
    out_height, out_width = output_grid.shape
    match = np.array_equal(input_grid[:out_height, :out_width], output_grid)

    print(f"  Input dims: {in_height}x{in_width}")
    print(f"  Output dims: {out_height}x{out_width}")
    print(f"  Upper-left match: {match}")

    # Check for subgrid matches anywhere in the input
    subgrid_found = False
    for i in range(in_height - out_height + 1):
        for j in range(in_width - out_width + 1):
            if np.array_equal(input_grid[i:i+out_height, j:j+out_width], output_grid):
                print(f"  Subgrid match found at: ({i}, {j})")
                subgrid_found = True
                break  # Stop after first match for simplicity, may need modification
        if subgrid_found:
            break
    if not subgrid_found:
        print("  No subgrid match found.")

examples = [
    ([[5, 5, 5], [5, 5, 5], [5, 5, 5]], [[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
    ([[0, 5, 5, 5, 0], [0, 5, 5, 5, 0], [0, 5, 5, 5, 0], [0, 0, 0, 0, 0]], [[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
    ([[8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8]], [[8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8]]),
    ([[5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5]], [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[7, 7, 7], [7, 7, 7], [7, 7, 7]]),
]

for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)