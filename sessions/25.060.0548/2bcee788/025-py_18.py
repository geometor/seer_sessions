import numpy as np

def get_object_metrics(grid, color):
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return {
            "exists": False,
            "min_row": None,
            "max_row": None,
            "min_col": None,
            "max_col": None,
            "height": 0,
            "width": 0,
            "count": 0
        }
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    count = len(coords)
    return {
        "exists": True,
        "min_row": min_row,
        "max_row": max_row,
        "min_col": min_col,
        "max_col": max_col,
        "height": height,
        "width": width,
        "count": count,
    }

def analyze_examples(task_data):
  example_data = []
  for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)
        
        input_metrics = get_object_metrics(input_grid, 8)  # 8 is for azure
        output_metrics = get_object_metrics(output_grid, 8)
        predicted_metrics = get_object_metrics(predicted_output, 8)

        example_data.append({
          "input": input_metrics,
          "output": output_metrics,
          "predicted": predicted_metrics,
          "correct": np.array_equal(output_grid, predicted_output)
        })
  return example_data

# the following is example data from the prompt - replace with actual task
task_data = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0],
                   [0, 0, 8, 8, 8, 0],
                   [0, 0, 0, 0, 0, 0],
                   [0, 2, 0, 0, 0, 0]],
         'output': [[3, 3, 3, 3, 3, 3],
                    [3, 3, 8, 8, 8, 3],
                    [3, 3, 3, 8, 3, 3],
                    [3, 3, 3, 8, 3, 3]]},

        {'input': [[0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 8, 8, 8, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 2, 0, 0]],
         'output': [[3, 3, 3, 3, 3, 3, 3],
                    [3, 3, 3, 8, 8, 8, 3],
                    [3, 3, 3, 3, 8, 3, 3],
                    [3, 3, 3, 3, 8, 3, 3]]},

        {'input': [[0, 0, 0, 0, 0, 0],
                   [0, 8, 8, 8, 0, 0],
                   [0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 2, 0, 0]],
         'output': [[3, 3, 3, 3, 3, 3],
                    [3, 8, 8, 8, 3, 3],
                    [3, 3, 8, 3, 3, 3],
                    [3, 3, 8, 3, 3, 3]]},
    ]
}

analysis = analyze_examples(task_data)

for i, example in enumerate(analysis):
  print (f"Example {i+1}:")
  print (f"  Input Azure: exists={example['input']['exists']}, height={example['input']['height']}, width={example['input']['width']}, count={example['input']['count']}")
  print (f"  Output Azure: exists={example['output']['exists']}, height={example['output']['height']}, width={example['output']['width']}, count={example['output']['count']}")
  print (f"  Predicted Azure: exists={example['predicted']['exists']}, height={example['predicted']['height']}, width={example['predicted']['width']}, count={example['predicted']['count']}")
  print (f"  Correct Prediction: {example['correct']}")