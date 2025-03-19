import numpy as np

def analyze_results(task):
    results = {"train": [], "test": []}

    for dataset_type in ["train", "test"]:
        for i, example in enumerate(task[dataset_type]):
            input_grid = np.array(example['input'])
            expected_output = np.array(example['output'])

            yellow_count_input = np.sum(input_grid == 4)
            yellow_count_output = np.sum(expected_output == 4)
            red_count_output = np.sum(expected_output == 2)

            results[dataset_type].append({
                "example_index": i,
                "yellow_input": yellow_count_input,
                "yellow_output": yellow_count_output,
                "red_output": red_count_output,
            })
    return results

task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 2, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ],
  "test": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 4, 4, 4, 4, 4, 0],
        [0, 4, 0, 0, 0, 4, 0],
        [0, 4, 0, 0, 0, 4, 0],
        [0, 4, 4, 4, 4, 4, 0],
        [0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 4, 4, 4, 4, 4, 0],
        [0, 4, 0, 0, 0, 4, 0],
        [0, 4, 0, 0, 0, 4, 0],
        [0, 4, 4, 4, 4, 4, 0],
        [0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}

analysis = analyze_results(task)
print(analysis)