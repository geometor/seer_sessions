import numpy as np

def analyze_example(input_grid, output_grid):
    input_array = np.array(input_grid)
    output_array = np.array(output_grid)

    print(f"Input shape: {input_array.shape}")
    print(f"Output shape: {output_array.shape}")

    for color in range(10):  # Check all possible colors
        input_count = np.sum(input_array == color)
        output_count = np.sum(output_array == color)
        print(f"Color {color}: Input count = {input_count}, Output count = {output_count}")

# Example usage (assuming you have loaded your input/output grids)
# for i in range(len(train_input_grids)):
#    print(f"--- Example {i+1} ---")
#    analyze_example(train_input_grids[i], train_output_grids[i])