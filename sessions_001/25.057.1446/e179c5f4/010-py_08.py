import numpy as np

def analyze_examples(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        results.append({
            'input_dims': input_grid.shape,
            'output_dims': output_grid.shape,
        })
    return results

task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [1, 8, 1, 8, 1, 8, 1, 8, 1, 8],
        [8, 1, 8, 1, 8, 1, 8, 1, 8, 1],
        [1, 8, 1, 8, 1, 8, 1, 8, 1, 8],
        [8, 1, 8, 1, 8, 1, 8, 1, 8, 1],
        [1, 8, 1, 8, 1, 8, 1, 8, 1, 8],
        [8, 1, 8, 1, 8, 1, 8, 1, 8, 1],
        [1, 8, 1, 8, 1, 8, 1, 8, 1, 8],
        [8, 1, 8, 1, 8, 1, 8, 1, 8, 1],
        [1, 8, 1, 8, 1, 8, 1, 8, 1, 8],
        [8, 1, 8, 1, 8, 1, 8, 1, 8, 1]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [8, 1, 8, 1, 8, 1],
        [1, 8, 1, 8, 1, 8],
        [8, 1, 8, 1, 8, 1],
        [1, 8, 1, 8, 1, 8],
        [8, 1, 8, 1, 8, 1],
        [1, 8, 1, 8, 1, 8]
      ]
    },
      {
      "input": [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0]
      ],
      "output": [
        [1,8,1,8],
        [8,1,8,1],
        [1,8,1,8],
        [8,1,8,1],
      ]
    }
  ]
}

analysis_results = analyze_examples(task)
print(analysis_results)