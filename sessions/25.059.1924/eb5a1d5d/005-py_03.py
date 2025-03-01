def test(task_json):
    """
    Tests the transform function against all training examples in the provided task.
    Prints a detailed comparison of the actual and expected outputs.
    """
    print("Task:", task_json['task_name'])
    correct_count = 0
    total_examples = 0
    
    for example in task_json['train']:
        total_examples += 1
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        transformed_output_grid = transform(input_grid)

        print(f"\nExample {total_examples}:")
        print("Input Grid:")
        print(input_grid)
        print("Expected Output Grid:")
        print(expected_output_grid)
        print("Transformed Output Grid:")
        print(transformed_output_grid)
        
        if np.array_equal(transformed_output_grid, expected_output_grid):
            print("Output: MATCH")
            correct_count +=1
        else:
            print("Output: MISMATCH")
        
        # Detailed pixel-by-pixel comparison
        if not np.array_equal(transformed_output_grid, expected_output_grid):
            print("Pixel-by-pixel comparison:")
            diff = transformed_output_grid == expected_output_grid
            print(diff)
            mismatches = np.where(diff == False)
            for y, x in zip(mismatches[0], mismatches[1]):
                print(f"  Mismatch at ({y}, {x}): Expected {expected_output_grid[y, x]}, Got {transformed_output_grid[y, x]}")
    print(f"\nSummary: {correct_count}/{total_examples} correct")

import json
import numpy as np
# this would normally be provided in a prior or in a separate file
# for now we provide it here
task = {
  "task_name": "6e82a1ae",
  "train": [
    {
      "input": [
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2]
      ],
      "output": [
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 2]
      ]
    },
    {
      "input": [
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3]
      ],
      "output": [
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 3]
      ]
    },
    {
      "input": [
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2]
      ],
      "output": [
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8],
        [8, 8, 8, 8, 2]
      ]
    }
  ]
}
test(task)