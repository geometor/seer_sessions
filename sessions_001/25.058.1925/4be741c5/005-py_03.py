import numpy as np
from collections import Counter

def get_dominant_color(grid_section):
    color_counts = Counter(grid_section.flatten())
    dominant_color = color_counts.most_common(1)[0][0]
    return dominant_color

def calculate_accuracy(predicted_output, expected_output):
    """Calculates the accuracy of the prediction."""
    if predicted_output.shape != expected_output.shape:
        return 0.0
    return np.mean(predicted_output == expected_output)

def analyze_example(input_grid, expected_output, transform_func):
    """Analyzes a single example."""
    predicted_output = transform_func(input_grid)
    accuracy = calculate_accuracy(predicted_output, expected_output)
    
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    section_width = input_width // 3

    section_dominant_colors = []
    for i in range(3):
        start_col = i * section_width
        end_col = (i+1) * section_width
        if i == 2:
          end_col = input_width #handle remainder
        section = input_grid[:, start_col:end_col]  #Using numpy slicing
        section_dominant_colors.append(get_dominant_color(section))


    analysis = {
        'input_shape': input_grid.shape,
        'output_shape': predicted_output.shape,
        'expected_output_shape': expected_output.shape,
        'accuracy': accuracy,
        'section_dominant_colors': section_dominant_colors,
        'predicted_output': predicted_output.tolist(),
        'expected_output': expected_output.tolist()
    }
    return analysis

def test():
  task_data = {
      'train': [
          {
              'input': [[5, 5, 5, 0, 0, 0, 5, 5, 5], [5, 5, 5, 0, 0, 0, 5, 5, 5], [5, 5, 5, 0, 0, 0, 5, 5, 5]],
              'output': [[5, 0, 5]]
          },
          {
              'input': [[5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5], [5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5], [5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5], [5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5]],
              'output': [[5, 0, 5]]
          },
          {
              'input': [[5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5]],
              'output': [[5, 0, 5]]
          },
          {
              'input': [[1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1]],
              'output': [[1, 0, 1]]
          },
          {
              'input': [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
              'output': [[6, 1]]
          }
      ]
  }

  results = []
  for example in task_data['train']:
    input_grid = np.array(example['input'])
    expected_output = np.array(example['output'])
    analysis = analyze_example(input_grid, expected_output, transform)
    results.append(analysis)

  for i, r in enumerate(results):
      print (f"Example {i+1}:")
      print (r)

test()