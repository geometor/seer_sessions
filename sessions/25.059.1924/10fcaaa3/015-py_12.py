import numpy as np

def analyze_grid(grid):
    grid = np.array(grid)
    height, width = grid.shape
    yellow_pixels = np.argwhere(grid == 4)
    num_yellow = len(yellow_pixels)
    first_yellow = yellow_pixels[0] if num_yellow > 0 else None
    white_pixels = np.argwhere(grid == 0)
    num_white = len(white_pixels)

    return {
        'height': height,
        'width': width,
        'num_yellow': num_yellow,
        'first_yellow': first_yellow,
        'num_white': num_white,
    }

def analyze_example(example):
    input_analysis = analyze_grid(example['input'])
    output_analysis = analyze_grid(example['output'])
    return {
        'input': input_analysis,
        'output': output_analysis,
    }
def summarize(task, results):
    print(f"TASK: {task['name']}")
    for i,result in enumerate(results):
      print(f"  Example: {i}")
      if 'error' in result:
          print(f"    Error: {result['error']}")
      else:
          match = np.array_equal(result['actual_output'], result['expected_output'])
          print(f"    Match: {match}")
          if not match:
            print("actual != expected")
            #print(f"  Expected:\n{result['expected_output']}")
            #print(f"  Actual:\n{result['actual_output']}")

task = {
  "name": "Task c59eb8ac",
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0]
      ],
      "output": [
        [8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
        [0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8],
        [8, 0, 8, 0, 8, 0, 4, 4, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
        [0, 8, 0, 8, 0, 8, 4, 4, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8],
        [8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
        [0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
        [0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8],
        [8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
        [0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 4]
      ],
      "output": [
        [8, 0, 8, 0, 8, 0, 8, 0, 4, 4],
        [0, 8, 0, 8, 0, 8, 0, 8, 4, 4]
      ]
    },
    {
      "input": [
        [4, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [4, 4, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
        [4, 4, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8]
      ]
    }
  ],
      "test": [
        {
            "input": [
                [0, 0, 0, 0, 4, 0, 0, 0, 0]
            ],
            "output": [
                [8, 0, 8, 0, 4, 4, 8, 0, 8, 0],
                [0, 8, 0, 8, 4, 4, 0, 8, 0, 8]
            ]
        }
    ]

}

results = []
for example in task["train"]:
  expected = example['output']
  actual = transform(example['input'])
  results.append({'expected_output': example['output'], 'actual_output': actual})

summarize(task, results)

for i, example in enumerate(task["train"]):
    analysis = analyze_example(example)
    print(f"Example {i+1}:")
    print(f"  Input:  Height={analysis['input']['height']}, Width={analysis['input']['width']}, Yellow Pixels={analysis['input']['num_yellow']}, White Pixels: {analysis['input']['num_white']}")
    print(f"  Output: Height={analysis['output']['height']}, Width={analysis['output']['width']}, Yellow Pixels={analysis['output']['num_yellow']}, White Pixels: {analysis['output']['num_white']}")