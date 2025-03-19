def get_cluster_metrics(grid, color):
    clusters = find_clusters(grid, color)
    metrics = []
    for cluster in clusters:
        min_row, min_col, max_row, max_col = get_bounding_box(cluster)
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        area = width * height
        metrics.append(
            {
                "top_left": (min_row, min_col),
                "bottom_right": (max_row, max_col),
                "width": width,
                "height": height,
                "area": area,
                "num_pixels": len(cluster),
            }
        )
    return metrics

def compare_grids(grid1, grid2):
    return np.array_equal(grid1, grid2)

def analyze_example(example):
  input_grid = np.array(example['input'])
  output_grid = np.array(example['output'])
  predicted = transform(input_grid)
  match = compare_grids(predicted, output_grid)
  print(f"Example: {example_index}")
  print(f"Input:\n{input_grid}\nOutput:\n{output_grid}\nPredicted:\n{predicted}")
  print(f"Match with expected: {match}")
  print("Red Cluster Metrics (Input):")
  metrics = get_cluster_metrics(input_grid, 2)
  for i, metric in enumerate(metrics):
    print(f"  Cluster {i + 1}: {metric}")
  output_metrics = get_cluster_metrics(output_grid, 2)
  if not output_metrics:
      output_metrics = "No Red Clusters"
  print(f"Red Cluster Metrics: (output):\n{output_metrics}")
  print("-" * 20)
  return match

train_success = []
for example_index, example in enumerate(task["train"]):
  match = analyze_example(example)
  train_success.append(match)

print(f"Transformation Success of all training examples: {all(train_success)}")
