import numpy as np

def grid_to_string(grid):
    return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

def analyze_example(input_grid, expected_output, result_grid):
    input_str = grid_to_string(input_grid)
    expected_str = grid_to_string(expected_output)
    result_str = grid_to_string(result_grid)

    input_objects = find_objects(input_grid)
    expected_objects = find_objects(expected_output)
    result_objects = find_objects(result_grid)

    print(f"Input Grid:\n{input_str}\n")
    print(f"  Objects: {input_objects}\n")
    print(f"Expected Output:\n{expected_str}\n")
    print(f"  Objects: {expected_objects}\n")
    print(f"Result Output:\n{result_str}\n")
    print(f"  Objects: {result_objects}\n")

    #try to find the correct plus sign:
    target = None
    for obj_list in input_objects.get(4,[]):
        h, w = get_plus_extent(obj_list)
        if h == w and h%2 == 1:
            if target is None or h > get_plus_extent(target)[0]:
                target = obj_list

    if target is not None:
        target_h, target_w = get_plus_extent(target)
        print(f"Target Object (Yellow Plus) Height: {target_h}, Width: {target_w}")
        expected_h, expected_w = expected_output.shape
        print(f"Expected Output Height: {expected_h}, Width: {expected_w}")
    else:
        print("No Target Object Found.")

    diff = result_grid == expected_output
    total_pixels = diff.size
    correct_pixels = np.sum(diff)
    accuracy_percentage = (correct_pixels / total_pixels) * 100
    print(f"Prediction Accuracy: {correct_pixels}/{total_pixels} ({accuracy_percentage:.2f}%)")


task = {
'train': [
        {'input': [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 4, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 4, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]], 'output': [[8, 8, 8, 8, 8], [8, 8, 4, 8, 8], [8, 4, 4, 4, 8], [8, 8, 4, 8, 8], [8, 8, 8, 8, 8]]},
        {'input': [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 4, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 4, 4, 4, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 4, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]], 'output': [[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 4, 8, 8, 8, 8], [8, 8, 8, 4, 4, 4, 8, 8, 8], [8, 8, 8, 8, 4, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]]},
        {'input': [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]], 'output': [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 4, 5, 5, 5], [5, 5, 4, 4, 4, 5, 5], [5, 5, 5, 4, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5]]}
    ]
}

for i, example in enumerate(task['train']):
  print(f"Example {i+1}:")
  analyze_example(np.array(example['input']), np.array(example['output']), transform(np.array(example['input'])))
  print("-" * 40)