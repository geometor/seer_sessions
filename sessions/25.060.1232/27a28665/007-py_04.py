import numpy as np

def analyze_example(input_grid, expected_output):
    """Analyzes a single example and returns relevant metrics."""
    input_array = np.array(input_grid)
    unique, counts = np.unique(input_array, return_counts=True)
    color_counts = dict(zip(unique, counts))
    
    max_count = 0
    dominant_color = None
    for color, count in color_counts.items():
        if count > max_count:
            max_count = count
            dominant_color = color

    sum_other_colors = sum(count for color, count in color_counts.items() if color != dominant_color)
    
    is_dominant = max_count >= sum_other_colors -1

    result = {
        "color_counts": color_counts,
        "dominant_color": dominant_color,
        "max_count": max_count,
        "sum_other_colors": sum_other_colors,
        "is_dominant": is_dominant,
        "output_present": expected_output == [[1]],

    }
    return result

task = {
  "train": [
    {
      "input": [
        [6, 6, 0, 0, 0, 0, 6, 6, 6],
        [6, 6, 6, 6, 0, 0, 0, 6, 6],
        [0, 6, 6, 6, 0, 0, 0, 0, 6],
        [0, 0, 6, 6, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 6, 6, 6, 6, 0],
        [0, 0, 6, 6, 6, 6, 0, 0, 0]
      ],
      "output": [
        [1]
      ]
    },
    {
      "input": [
        [6, 6, 0, 0, 0, 0, 6, 6, 6],
        [6, 6, 6, 6, 0, 0, 0, 6, 6],
        [0, 6, 6, 6, 0, 0, 0, 0, 6],
        [0, 0, 6, 6, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 6, 6, 6, 6, 6],
        [0, 0, 6, 6, 6, 6, 0, 0, 0]
      ],
      "output": [
        [1]
      ]
    },
        {
      "input": [
        [6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6]
      ],
      "output": [
        [1]
      ]
    },
            {
      "input": [
        [2, 2, 8, 2, 2, 2, 2, 8, 2],
        [2, 2, 2, 2, 2, 2, 8, 2, 2],
        [8, 2, 2, 2, 2, 8, 2, 2, 2],
        [2, 2, 2, 2, 8, 2, 2, 2, 2],
        [2, 2, 2, 8, 2, 2, 2, 2, 2],
        [2, 2, 8, 2, 2, 2, 2, 8, 2],
        [2, 2, 2, 2, 2, 2, 8, 2, 2],
        [2, 2, 2, 2, 2, 8, 2, 2, 2],
        [2, 2, 2, 2, 8, 2, 2, 2, 2]
      ],
      "output": [
        [1]
      ]
    },    
    {
      "input": [
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
      ],
      "output": [
        [1]
      ]
    }
  ],
  "test": [
    {
      "input": [
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 7, 7, 7, 0, 0, 0, 0],
        [0, 7, 7, 7, 7, 7, 0, 0, 0],
        [7, 7, 7, 7, 7, 7, 7, 0, 0],
        [0, 7, 7, 7, 7, 7, 0, 0, 0],
        [0, 0, 7, 7, 7, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [1]
      ]
    }
  ]
}

results = []
for example in task["train"]:
  results.append(analyze_example(example["input"], example["output"]))

for result in results:
    print(result)
