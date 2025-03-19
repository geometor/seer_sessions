import numpy as np
from collections import Counter

def get_example_metrics(input_grid, output_grid):
    """Calculates metrics for a given input-output pair."""
    
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    metrics = {}
    
    # Check for orange
    metrics['input_contains_orange'] = np.any(input_grid == 7)
    metrics['orange_pixels_input'] = np.sum(input_grid == 7)
    
    # Find most frequent color (excluding orange)
    colors = input_grid.flatten().tolist()
    color_counts = Counter(colors)
    if 7 in color_counts:
        del color_counts[7]  #remove orange
    if len(color_counts) > 0:
      most_common_color = color_counts.most_common(1)[0][0]
      most_common_count = color_counts.most_common(1)[0][1]
      metrics['most_frequent_color_not_orange_input'] = f"{get_color_name(most_common_color)} : {most_common_count}"
      metrics['most_frequent_color_not_orange_count_input'] = most_common_count
    else:
        metrics['most_frequent_color_not_orange_input'] = "None"
        metrics['most_frequent_color_not_orange_count_input'] = 0


    metrics['output_grid'] = output_grid.tolist()
    return metrics

def get_color_name(value):
    color_map = {
    0: "black",
    1: "blue",
    2: "red",
    3: "green",
    4: "yellow",
    5: "gray",
    6: "magenta",
    7: "orange",
    8: "azure",
    9: "maroon"
    }
    return color_map.get(value)
    
example_inputs = [
    [[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 0]],
    [[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 0]],
    [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 7, 1, 1, 1, 7, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 7, 1]],
    [[0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1]],
    [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
]
example_outputs = [
    [[7]],
    [[7]],
    [[7]],
    [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]],
    [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
]

all_metrics = []
for input_grid, output_grid in zip(example_inputs, example_outputs):
  metrics = get_example_metrics(input_grid, output_grid)
  all_metrics.append(metrics)

for i in range(len(all_metrics)):
    print (f"example_{i+1}:")
    for key, value in all_metrics[i].items():
      print (f"  {key}: {value}")
