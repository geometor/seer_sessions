import numpy as np

def code_execution(input_grid, output_grid, predicted_grid):
    """Executes targeted code snippets and reports observations."""

    # 1. Check if the correct color is targeted.
    input_objects = find_objects(input_grid)
    red_objects = [obj for obj in input_objects if any(input_grid[r, c] == 2 for r, c in obj)]
    largest_red_object = max(red_objects, key=len, default=[])
    
    correct_color_targeted = False
    if largest_red_object:
        top_left, _ = bounding_box(largest_red_object)
        # Check a predicted green pixel
        if predicted_grid[top_left[0], top_left[1]] == 3:
            correct_color_targeted = True
            

    # 2. compare predicted output with actual output
    comparison = predicted_grid == output_grid
    all_match = np.all(comparison)

    print(f"Correct Red Object Targeted: {correct_color_targeted}")
    print(f"Output grids match: {all_match}")
    if not all_match:
        print(f"Differences: {np.sum(~comparison)} pixels")
        
# load first example to demonstrate the approach
examples = task["train"]
for i, example in enumerate(examples):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_grid = transform(input_grid)
    print(f"--- Example {i+1} ---")
    code_execution(input_grid, output_grid, predicted_grid)
