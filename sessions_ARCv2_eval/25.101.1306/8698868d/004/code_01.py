import numpy as np

def analyze_example(input_grid_list, expected_output_list, transformed_output_list):
    input_grid = np.array(input_grid_list)
    expected_output = np.array(expected_output_list)
    # Handle cases where transformed output might be malformed or empty
    try:
        transformed_output = np.array(transformed_output_list)
        if transformed_output.size == 0 and expected_output.size != 0 :
             # Treat empty transformed output as completely wrong if expected is not empty
             transformed_output_dims = (0, 0)
             size_match = False
             pixel_diff = expected_output.size
             palette_match = False
             count_match = False
        elif transformed_output.size == 0 and expected_output.size == 0:
             transformed_output_dims = (0, 0)
             size_match = True
             pixel_diff = 0
             palette_match = True
             count_match = True
        else:
            transformed_output_dims = transformed_output.shape
            size_match = (expected_output.shape == transformed_output.shape)
            if size_match:
                pixel_diff = int(np.sum(expected_output != transformed_output))
                expected_palette, expected_counts = np.unique(expected_output, return_counts=True)
                transformed_palette, transformed_counts = np.unique(transformed_output, return_counts=True)
                palette_match = set(expected_palette) == set(transformed_palette)
                # Check count match only if palettes match
                if palette_match:
                    expected_dict = dict(zip(expected_palette, expected_counts))
                    transformed_dict = dict(zip(transformed_palette, transformed_counts))
                    count_match = expected_dict == transformed_dict
                else:
                    count_match = False
            else:
                # Cannot compare pixels/palettes/counts if sizes differ
                pixel_diff = expected_output.size # Max difference
                palette_match = False
                count_match = False

    except Exception: # Catch potential errors during np.array conversion
        transformed_output_dims = "Error"
        size_match = False
        pixel_diff = expected_output.size
        palette_match = False
        count_match = False


    metrics = {}
    metrics['input_dims'] = input_grid.shape
    metrics['expected_output_dims'] = expected_output.shape
    metrics['transformed_output_dims'] = transformed_output_dims
    metrics['size_match'] = size_match
    metrics['pixel_diff'] = pixel_diff
    metrics['palette_match'] = palette_match
    metrics['count_match'] = count_match
    # Add context from analysis (Separator=8 for Ex1, 2 for Ex2)
    # Frame/Content sizes deduced from rule (N vs N-2)
    metrics['context'] = {}
    if expected_output.shape == (6, 12): # Example 1 signature
        metrics['context']['separator'] = 8
        metrics['context']['frame_size'] = (6, 6)
        metrics['context']['content_size'] = (4, 4)
        metrics['context']['num_pairs'] = 2
    elif expected_output.shape == (16, 16): # Example 2 signature
        metrics['context']['separator'] = 2
        metrics['context']['frame_size'] = (8, 8)
        metrics['context']['content_size'] = (6, 6)
        metrics['context']['num_pairs'] = 4
    else: # Default/Unknown
        metrics['context']['separator'] = 'unknown'
        metrics['context']['frame_size'] = 'unknown'
        metrics['context']['content_size'] = 'unknown'
        metrics['context']['num_pairs'] = 'unknown'


    return metrics

# Example 1 Data (Using transformed output from prompt run 1)
input_1 = [[1,1,1,1,1,1,4,4,4,4,4,4,8,8,8],[1,1,1,1,1,1,4,8,4,4,4,4,8,8,8],[1,1,1,1,1,1,4,4,4,4,4,4,8,8,8],[1,1,1,1,1,1,4,4,4,4,4,4,8,8,8],[1,1,1,1,8,1,4,4,4,4,8,4,8,8,8],[1,1,1,1,1,1,4,4,4,4,4,4,8,8,8],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],[8,8,2,2,2,2,8,8,8,8,8,8,8,8,8],[8,8,2,8,8,2,8,8,8,8,8,8,8,8,8],[8,8,2,8,8,2,8,8,8,8,8,8,8,8,8],[8,8,2,2,2,2,8,8,8,8,8,8,8,8,8],[8,8,8,8,8,8,8,3,3,3,3,8,8,8,8],[8,8,8,8,8,8,8,3,3,8,3,8,8,8,8],[8,8,8,8,8,8,8,3,8,3,3,8,8,8,8],[8,8,8,8,8,8,8,3,3,3,3,8,8,8,8],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]]
expected_1 = [[1,1,1,1,1,1,4,4,4,4,4,4],[1,2,2,2,2,1,4,3,3,3,3,4],[1,2,1,1,2,1,4,3,3,4,3,4],[1,2,1,1,2,1,4,3,4,3,3,4],[1,2,2,2,2,1,4,3,3,3,3,4],[1,1,1,1,1,1,4,4,4,4,4,4]]
transformed_1 = [[1,1,1,1,1,1,4,4,4,4,4,4],[1,0,0,0,0,1,4,0,0,0,0,4],[1,0,0,0,0,1,4,0,0,0,0,4],[1,0,0,0,0,1,4,0,0,0,0,4],[1,0,0,0,0,1,4,0,0,0,0,4],[1,1,1,1,1,1,4,4,4,4,4,4]]

# Example 2 Data (Using transformed output from prompt run 2)
input_2 = [[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[4,4,2,4,4,2,4,4,3,3,3,3,3,2,3,3,2,2,2,9,9,9,9,9,9,2,2,2,2,2],[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,2,2,2,9,2,2,9,2,9,2,2,2,2,2],[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,2,2,2,9,2,2,9,2,9,2,2,2,2,2],[4,4,2,4,4,4,4,4,3,3,2,3,3,3,3,3,2,2,2,9,9,9,9,2,9,2,2,2,2,2],[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,2,2,2,9,2,2,9,2,9,2,2,2,2,2],[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,2,2,2,9,9,9,9,9,9,2,2,2,2,2],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[8,8,8,8,8,2,8,8,1,1,2,1,1,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[8,8,8,8,8,8,8,8,1,1,2,1,1,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,5,5,5,5,5,5,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,5,2,2,5,2,5,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,5,2,2,5,2,5,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,5,5,5,5,5,5,2,2,2,2,2],[2,2,2,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,5,2,2,5,2,5,2,2,2,2,2],[2,2,2,1,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,5,5,5,5,5,5,2,2,2,2,2],[2,2,2,1,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,1,2,2,2,2,1,2,2,2,2,7,7,7,7,7,7,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,1,2,2,2,2,1,2,2,2,2,7,2,7,7,7,7,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,1,1,1,1,1,1,2,2,2,2,7,7,7,7,7,7,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,7,2,7,7,7,7,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,7,2,7,7,7,7,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,7,7,7,7,7,7,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]]
expected_2 = [[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3],[4,9,9,9,9,9,9,4,3,7,7,7,7,7,7,3],[4,9,4,4,9,4,9,4,3,7,3,7,7,7,7,3],[4,9,4,4,9,4,9,4,3,7,7,7,7,7,7,3],[4,9,9,9,9,4,9,4,3,7,3,7,7,7,7,3],[4,9,4,4,9,4,9,4,3,7,3,7,7,7,7,3],[4,9,9,9,9,9,9,4,3,7,7,7,7,7,7,3],[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1],[8,1,1,1,1,1,1,8,1,5,5,5,5,5,5,1],[8,1,8,8,8,8,1,8,1,5,1,1,5,1,5,1],[8,1,8,8,8,8,1,8,1,5,1,1,5,1,5,1],[8,1,8,8,8,8,1,8,1,5,5,5,5,5,5,1],[8,1,8,8,8,8,1,8,1,5,1,1,5,1,5,1],[8,1,1,1,1,1,1,8,1,5,5,5,5,5,5,1],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1]]
# Transformed output for Example 2 from the SECOND code run in the prompt
transformed_2 = [[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3],[4,9,9,9,9,9,9,4,3,5,5,5,5,5,5,3],[4,9,4,4,9,4,9,4,3,5,3,3,5,3,5,3],[4,9,4,4,9,4,9,4,3,5,3,3,5,3,5,3],[4,9,9,9,9,4,9,4,3,5,5,5,5,5,5,3],[4,9,4,4,9,4,9,4,3,5,3,3,5,3,5,3],[4,9,9,9,9,9,9,4,3,5,5,5,5,5,5,3],[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1],[8,1,1,1,1,1,1,8,1,7,7,7,7,7,7,1],[8,1,8,8,8,8,1,8,1,7,1,7,7,7,7,1],[8,1,8,8,8,8,1,8,1,7,7,7,7,7,7,1],[8,1,8,8,8,8,1,8,1,7,1,7,7,7,7,1],[8,1,8,8,8,8,1,8,1,7,1,7,7,7,7,1],[8,1,1,1,1,1,1,8,1,7,7,7,7,7,7,1],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1]]

metrics_1 = analyze_example(input_1, expected_1, transformed_1)
metrics_2 = analyze_example(input_2, expected_2, transformed_2)


print("--- Metrics Example 1 (Prompt Run 1) ---")
print(metrics_1)
print("\n--- Metrics Example 2 (Prompt Run 2) ---")
print(metrics_2)

# Calculate metrics for the *correct* expected output for Example 1, assuming code worked
correct_transformed_1 = [[1,1,1,1,1,1,4,4,4,4,4,4],[1,2,2,2,2,1,4,3,3,3,3,4],[1,2,1,1,2,1,4,3,3,4,3,4],[1,2,1,1,2,1,4,3,4,3,3,4],[1,2,2,2,2,1,4,3,3,3,3,4],[1,1,1,1,1,1,4,4,4,4,4,4]]
metrics_1_correct = analyze_example(input_1, expected_1, correct_transformed_1)
print("\n--- Metrics Example 1 (Correct Output) ---")
print(metrics_1_correct)

# Calculate metrics for the *correct* expected output for Example 2, assuming code worked
correct_transformed_2 = [[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3],[4,9,9,9,9,9,9,4,3,7,7,7,7,7,7,3],[4,9,4,4,9,4,9,4,3,7,3,7,7,7,7,3],[4,9,4,4,9,4,9,4,3,7,7,7,7,7,7,3],[4,9,9,9,9,4,9,4,3,7,3,7,7,7,7,3],[4,9,4,4,9,4,9,4,3,7,3,7,7,7,7,3],[4,9,9,9,9,9,9,4,3,7,7,7,7,7,7,3],[4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1],[8,1,1,1,1,1,1,8,1,5,5,5,5,5,5,1],[8,1,8,8,8,8,1,8,1,5,1,1,5,1,5,1],[8,1,8,8,8,8,1,8,1,5,1,1,5,1,5,1],[8,1,8,8,8,8,1,8,1,5,5,5,5,5,5,1],[8,1,8,8,8,8,1,8,1,5,1,1,5,1,5,1],[8,1,1,1,1,1,1,8,1,5,5,5,5,5,5,1],[8,8,8,8,8,8,8,8,1,1,1,1,1,1,1,1]]
metrics_2_correct = analyze_example(input_2, expected_2, correct_transformed_2)
print("\n--- Metrics Example 2 (Correct Output) ---")
print(metrics_2_correct)
