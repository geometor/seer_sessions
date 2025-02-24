import numpy as np

def describe_grid(grid):
    print(f"  Shape: {grid.shape}")
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    print(f"  Colors: {color_counts}")

def analyze_example(input_grid, output_grid, example_number):
    print(f"Example {example_number}:")
    print("Input:")
    describe_grid(input_grid)
    print("Output:")
    describe_grid(output_grid)

    # Check for rotation (quick check, might not be the full story)
    rotated_input = np.rot90(input_grid, k=-1)
    if np.array_equal(rotated_input, output_grid):
        print("  Rotation: 90 degrees clockwise")
    else:
        print("  Rotation: Not a simple 90-degree rotation")

    # Magenta pixel analysis
    input_magenta_indices = np.where(input_grid == 6)
    output_magenta_indices = np.where(output_grid == 6)

    print(f"  Input Magenta Indices: {list(zip(input_magenta_indices[0], input_magenta_indices[1]))}")
    print(f"  Output Magenta Indices: {list(zip(output_magenta_indices[0], output_magenta_indices[1]))}")
    
    # Check overall difference between the input and output
    diff = input_grid - output_grid
    print(f"  Difference: {np.unique(diff, return_counts=True)}")
    print("-----")

# Load the example grids (replace with actual data loading)
# Assume task_data contains the loaded JSON data
examples = task_data['train']  # Assuming 'train' key holds the examples

for i, example in enumerate(examples):
    analyze_example(np.array(example['input']), np.array(example['output']), i + 1)