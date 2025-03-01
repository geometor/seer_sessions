import numpy as np

def analyze_results(examples, transform_function):
    results = []
    for i, (input_grid, expected_output) in enumerate(examples):
        input_grid = np.array(input_grid)
        expected_output = np.array(expected_output)
        predicted_output = transform_function(input_grid)
        diff_pixels = np.where(predicted_output != expected_output)
        diff_coordinates = list(zip(diff_pixels[0], diff_pixels[1]))

        # Find azure region
        azure_region = find_contiguous_region(input_grid, 8)
        if azure_region:
          min_row = min(r for r, _ in azure_region)
          max_row = max(r for r, _ in azure_region)
          min_col = min(c for _, c in azure_region)
          max_col = max(c for _, c in azure_region)
          azure_region_shape = (max_row - min_row + 1, max_col - min_col + 1)
        else:
          azure_region_shape = (0,0)

        results.append({
            "example_index": i,
            "input_shape": input_grid.shape,
            "output_shape": expected_output.shape,
            "azure_region_shape": azure_region_shape,
            "diff_coordinates": diff_coordinates,
        })
    return results

#Assuming 'train' contains the list of input/output pairs.
# results = analyze_results(train, transform)
# print(results)
# Example usage (assuming 'train' is defined as in the ARC task)

train = [
    ([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 8, 8, 0, 0],
    [0, 0, 0, 8, 8, 8, 0, 0],
    [0, 0, 0, 8, 8, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
], [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 2, 8, 0, 0],
    [0, 0, 0, 8, 8, 8, 0, 0],
    [0, 0, 0, 8, 8, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]),
([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
[
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 8, 2, 8, 8, 8, 2, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]),
([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
[
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 2, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]),
([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 8, 8, 8, 0, 0],
    [0, 0, 8, 8, 8, 8, 0, 0],
    [0, 0, 8, 8, 8, 8, 0, 0],
    [0, 0, 8, 8, 8, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
],
[
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 8, 8, 8, 0, 0],
    [0, 0, 8, 2, 2, 8, 0, 0],
    [0, 0, 8, 8, 8, 8, 0, 0],
    [0, 0, 8, 8, 8, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]),
([
    [8, 8, 8, 8],
    [8, 8, 8, 8],
    [8, 8, 8, 8],
    [8, 8, 8, 8]
],
[
    [8, 8, 8, 8],
    [8, 2, 2, 8],
    [8, 8, 8, 8],
    [8, 8, 8, 8]
])
]

results = analyze_results(train, transform)
print(results)