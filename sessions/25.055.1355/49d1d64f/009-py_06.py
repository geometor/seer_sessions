import numpy as np

def compare_grids(expected, actual):
    """Compares two grids and returns a report."""
    if expected.shape != actual.shape:
        return {
            "shape_match": False,
            "pixel_match": False,
            "differences": "Shapes differ",
            "expected_shape": expected.shape,
            "actual_shape": actual.shape
        }

    diff = expected != actual
    diff_indices = np.where(diff)
    num_diffs = len(diff_indices[0])
    diff_coords = list(zip(diff_indices[0], diff_indices[1]))

    return {
        "shape_match": True,
        "pixel_match": num_diffs == 0,
        "differences": diff_coords,
        "num_differences": num_diffs,
        "expected_shape": expected.shape,
        "actual_shape": actual.shape
    }
def test_transform(transform_function, examples):
    results = []
    for task_name, pairs in examples.items():
        task_results = []
        for i, pair in enumerate(pairs):
            input_grid = np.array(pair['input'])
            expected_output = np.array(pair['output'])
            actual_output = transform_function(input_grid)
            comparison = compare_grids(expected_output, actual_output)
            task_results.append({
                "example_index": i,
                "comparison": comparison
            })
        results.append({"task_name": task_name, "results": task_results})
    return results
#Placeholder examples
examples = {
  "task_1": [
    {'input': [[1, 2], [3, 4]], 'output': [[1, 2, 2], [1, 2, 2], [3, 4, 4], [3, 4, 4]]},
    {'input': [[5, 6, 7]], 'output': [[5, 6, 7, 7], [5, 6, 7, 7]]},
    {'input': [[8],[9]], 'output': [[8,8],[8,8],[9,9],[9,9]]}
  ]
}

results = test_transform(transform, examples)
for task_result in results:
    print(f"Task: {task_result['task_name']}")
    for example_result in task_result['results']:
        print(f"  Example {example_result['example_index']}:")
        print(f"    Shape Match: {example_result['comparison']['shape_match']}")
        print(f"    Pixel Match: {example_result['comparison']['pixel_match']}")
        if not example_result['comparison']['pixel_match']:
            print(f"    Differences: {example_result['comparison']['differences']}")
            print(f"   Expected Shape: {example_result['comparison']['expected_shape']}")
            print(f"   Actual Shape: {example_result['comparison']['actual_shape']}")
