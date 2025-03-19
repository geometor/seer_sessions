import numpy as np

def report(task, transform):
    print(f"Task: {task['name']}")
    correct_count = 0
    for i, example in enumerate(task['train']):
        input_grid = example['input']
        expected_output = example['output']
        predicted_output = transform(input_grid)
        if np.array_equal(predicted_output, np.array(expected_output)):
            correct_count += 1
            print(f"  Example {i + 1}: Correct")
        else:
            print(f"  Example {i + 1}: Incorrect")
            print(f"    Input:\n{np.array(input_grid)}")
            print(f"    Expected Output:\n{np.array(expected_output)}")
            print(f"    Predicted Output:\n{np.array(predicted_output)}")
    print(f"Correct Examples: {correct_count} / {len(task['train'])} ")

#mock task - replace later with provided task info
task = {
  "name": "Task Name",
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 2, 2, 0, 0],
        [0, 0, 1, 1, 2, 2, 0, 0],
        [0, 0, 4, 4, 3, 3, 0, 0],
        [0, 0, 4, 4, 3, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [1, 2],
        [4, 3]
      ]
    },
     {
      "input": [
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 8, 8, 8, 8, 8, 0, 0],
       [0, 0, 8, 8, 8, 8, 8, 0, 0],
       [0, 0, 8, 8, 8, 8, 8, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
       [8]
      ]
    },
        {
      "input": [
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 0, 0, 7, 7, 7, 0],
       [0, 0, 0, 5, 5, 5, 0, 0, 7, 7, 7, 0],
       [0, 0, 0, 5, 5, 5, 0, 0, 7, 7, 7, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
       [5, 7]
      ]
    },
     {
      "input":[
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0],
       [0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0],
       [0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
       [6]
      ]
    }

  ]
}

report(task, transform)
