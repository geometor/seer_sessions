import numpy as np
import math

def analyze_example(input_grid, expected_output, transformed_output, example_name):
    input_np = np.array(input_grid)
    expected_np = np.array(expected_output)
    transformed_np = np.array(transformed_output)

    H_in, W_in = input_np.shape
    H_out, W_out = expected_np.shape # Should be 12x12
    
    scale_h = H_out // H_in if H_in > 0 else 0
    scale_w = W_out // W_in if W_in > 0 else 0
    
    block_shape = (scale_h, scale_w)
    
    match = np.array_equal(expected_np, transformed_np)
    pixels_off = np.sum(expected_np != transformed_np)
    size_correct = (transformed_np.shape == (H_out, W_out))
    
    expected_colors = set(expected_np.flatten())
    transformed_colors = set(transformed_np.flatten())
    palette_correct = (expected_colors == transformed_colors)

    unique_expected, counts_expected = np.unique(expected_np, return_counts=True)
    unique_transformed, counts_transformed = np.unique(transformed_np, return_counts=True)
    count_correct = np.array_equal(unique_expected, unique_transformed) and np.array_equal(counts_expected, counts_transformed)

    print(f"--- {example_name} Analysis ---")
    print(f"Input Shape: {H_in}x{W_in}")
    print(f"Output Shape: {H_out}x{W_out}")
    print(f"Scaling Factors (H, W): ({scale_h}, {scale_w})")
    print(f"Block Shape (scale_h, scale_w): {block_shape}")
    print(f"\nResults of Previous Code Attempt:")
    print(f"Match: {match}")
    print(f"Pixels Off: {pixels_off} / {H_out*W_out}")
    print(f"Size Correct: {size_correct}")
    print(f"Palette Correct: {palette_correct}")
    # print(f"  Expected Colors: {sorted(list(expected_colors))}")
    # print(f"  Transformed Colors: {sorted(list(transformed_colors))}")
    print(f"Color Count Correct: {count_correct}")
    print("-" * 20)

# Example 1 Data (Using corrected expected output based on visual inspection)
input_1 = [[1, 3, 9, 4], [5, 5, 2, 8], [9, 8, 3, 1], [4, 0, 1, 4], [2, 3, 6, 5], [3, 9, 8, 0]]
expected_1 = [[6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5], [6, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 5], [6, 2, 3, 3, 3, 3, 1, 1, 1, 1, 3, 5], [6, 2, 3, 9, 9, 9, 8, 8, 8, 1, 3, 5], [6, 2, 3, 9, 9, 9, 4, 4, 8, 1, 3, 5], [6, 2, 3, 9, 9, 1, 3, 4, 8, 1, 3, 5], [8, 3, 1, 4, 2, 5, 5, 8, 0, 4, 9, 0], [8, 3, 1, 4, 2, 2, 8, 8, 0, 4, 9, 0], [8, 3, 1, 4, 4, 4, 0, 0, 0, 4, 9, 0], [8, 3, 1, 1, 1, 1, 4, 4, 4, 4, 9, 0], [8, 3, 3, 3, 3, 3, 9, 9, 9, 9, 9, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0]]
transformed_1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 2, 5, 2, 8, 2, 8, 0], [0, 1, 3, 1, 3, 9, 3, 9, 4, 9, 4, 0], [0, 9, 8, 9, 8, 3, 8, 3, 1, 3, 1, 0], [0, 5, 5, 5, 5, 2, 5, 2, 8, 2, 8, 0], [0, 4, 0, 4, 0, 1, 0, 1, 4, 1, 4, 0], [0, 9, 8, 9, 8, 3, 8, 3, 1, 3, 1, 0], [0, 2, 3, 2, 3, 6, 3, 6, 5, 6, 5, 0], [0, 4, 0, 4, 0, 1, 0, 1, 4, 1, 4, 0], [0, 3, 9, 3, 9, 8, 9, 8, 0, 8, 0, 0], [0, 2, 3, 2, 3, 6, 3, 6, 5, 6, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
analyze_example(input_1, expected_1, transformed_1, "Example 1")

# Example 2 Data
input_2 = [[9, 1, 1, 7, 7, 9], [2, 0, 7, 7, 0, 3], [2, 8, 7, 7, 2, 1], [5, 3, 9, 7, 7, 8]]
expected_2 = [[2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1], [2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 1], [2, 7, 2, 2, 2, 2, 8, 8, 8, 8, 7, 1], [2, 7, 2, 7, 7, 7, 9, 9, 9, 8, 7, 1], [2, 7, 2, 7, 1, 1, 7, 7, 9, 8, 7, 1], [2, 7, 2, 7, 1, 9, 1, 7, 9, 8, 7, 1], [7, 9, 5, 0, 7, 2, 0, 7, 3, 3, 7, 8], [7, 9, 5, 0, 7, 7, 7, 7, 3, 3, 7, 8], [7, 9, 5, 0, 0, 0, 3, 3, 3, 3, 7, 8], [7, 9, 5, 5, 5, 5, 3, 3, 3, 3, 7, 8], [7, 9, 9, 9, 9, 9, 7, 7, 7, 7, 7, 8], [7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8]]
transformed_2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 9, 1, 1, 7, 1, 7, 7, 9, 7, 0], [0, 0, 2, 7, 0, 7, 7, 0, 7, 3, 0, 0], [0, 1, 9, 1, 1, 7, 1, 7, 7, 9, 7, 0], [0, 0, 2, 7, 0, 7, 7, 0, 7, 3, 0, 0], [0, 8, 2, 7, 8, 7, 7, 2, 7, 1, 2, 0], [0, 0, 2, 7, 0, 7, 7, 0, 7, 3, 0, 0], [0, 8, 2, 7, 8, 7, 7, 2, 7, 1, 2, 0], [0, 3, 5, 9, 3, 7, 9, 7, 7, 8, 7, 0], [0, 8, 2, 7, 8, 7, 7, 2, 7, 1, 2, 0], [0, 3, 5, 9, 3, 7, 9, 7, 7, 8, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
analyze_example(input_2, expected_2, transformed_2, "Example 2")
