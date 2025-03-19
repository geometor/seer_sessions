import numpy as np

def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a dictionary of differences.

    Args:
        grid1: The first grid (e.g., expected output).
        grid2: The second grid (e.g., actual output from transform).

    Returns:
        A dictionary containing:
        - 'different': True if grids are different, False otherwise.
        - 'height_diff': Difference in height.
        - 'width_diff': Difference in width.
        - 'value_diffs': A list of (y, x, val1, val2) tuples for differing cells.
        - 'grid1_pixels' a count of pixels of each color in grid 1
        - 'grid2_pixels' a count of pixels of each color in grid 2
    """
    array1 = np.array(grid1)
    array2 = np.array(grid2)

    different = not np.array_equal(array1, array2)
    height_diff = array1.shape[0] - array2.shape[0]
    width_diff = array1.shape[1] - array2.shape[1]
    value_diffs = []

    if different:
        for y in range(min(array1.shape[0], array2.shape[0])):
            for x in range(min(array1.shape[1], array2.shape[1])):
                if array1[y, x] != array2[y, x]:
                    value_diffs.append((y, x, int(array1[y, x]), int(array2[y, x])))  # Convert to int
        #check for extra rows
        if array1.shape[0] > array2.shape[0]:
          for y in range(array2.shape[0], array1.shape[0]):
            for x in range(array1.shape[1]):
              value_diffs.append((y,x,int(array1[y,x]), -1))
        #check for extra columns
        if array1.shape[1] > array2.shape[1]:
          for y in range(array1.shape[0]):
            for x in range(array2.shape[1], array1.shape[1]):
              value_diffs.append((y,x,int(array1[y,x]), -1))
    
    #add counts of each color pixel in each array
    grid1_pixels = {}
    grid2_pixels = {}
    for i in range(10):
      grid1_pixels[i] = int(np.sum(array1 == i))
      grid2_pixels[i] = int(np.sum(array2 == i))

    return {
        'different': different,
        'height_diff': height_diff,
        'width_diff': width_diff,
        'value_diffs': value_diffs,
        'grid1_pixels': grid1_pixels,
        'grid2_pixels': grid2_pixels
    }

def show_example_transform(task, example_index):
    input_grid = task['train'][example_index]['input']
    expected_output = task['train'][example_index]['output']
    actual_output = transform(input_grid)
    comparison = compare_grids(expected_output, actual_output)
    print(f"Example {example_index + 1}:")
    print(f"  Input grid dimensions: {np.array(input_grid).shape}")
    print(f"  Expected output dimensions: {np.array(expected_output).shape}")
    print(f"  Actual output dimensions: {np.array(actual_output).shape}")
    print(f"Comparison different: {comparison['different']}")
    print(f"height difference: {comparison['height_diff']}")
    print(f"width difference: {comparison['width_diff']}")
    print(f"value differences: {comparison['value_diffs']}")
    print(f"expected pixel counts: {comparison['grid1_pixels']}")
    print(f"actual pixel counts: {comparison['grid2_pixels']}")
    return comparison

task = {
    "train": [
        {
            "input": [[5, 5, 5], [5, 5, 5], [5, 5, 8]],
            "output": [[5, 5, 5], [5, 5, 5], [5, 5, 8]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 5, 0], [0, 0, 0, 5, 0, 0], [0, 0, 5, 0, 0, 0], [0, 5, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 5, 0], [0, 0, 0, 5, 0, 0], [0, 0, 5, 0, 0, 0], [0, 5, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[1, 0, 0, 2, 0, 0, 3, 0, 0], [0, 1, 0, 0, 2, 0, 0, 3, 0], [0, 0, 1, 0, 0, 2, 0, 0, 3]],
            "output": [[1, 0, 0, 2, 0, 0, 3, 0, 0], [0, 1, 0, 0, 2, 0, 0, 3, 0], [0, 0, 1, 0, 0, 2, 0, 0, 3]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
    ]
}
comparisons = []
for i in range(len(task["train"])):
    comparisons.append(show_example_transform(task, i))
