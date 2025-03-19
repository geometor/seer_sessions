def get_metrics(input_grid, output_grid):
    metrics = {}
    metrics['input_dims'] = input_grid.shape
    metrics['output_dims'] = output_grid.shape
    metrics['input_red_pixels'] = np.argwhere(input_grid == 2).tolist()
    metrics['input_blue_pixels'] = np.argwhere(input_grid == 1).tolist()
    metrics['output_blue_pixels'] = np.argwhere(output_grid == 1).tolist()
    metrics['output_red_pixels'] = np.argwhere(output_grid == 2).tolist()

    diff = input_grid != output_grid
    metrics['changed_pixels'] = np.argwhere(diff).tolist()
    if (len(metrics['changed_pixels']) > 0):
      metrics['input_changed_pixels_value'] = [input_grid[x,y] for x,y in metrics['changed_pixels']]
      metrics['output_changed_pixels_value'] = [output_grid[x,y] for x,y in metrics['changed_pixels']]

    return metrics

import numpy as np
task_data = json.loads(task_json)

# task_data = {"train": ...., "test": ....}

train_examples = task_data['train']
test_examples = task_data['test']

all_metrics = []

for i, example in enumerate(train_examples):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    metrics = get_metrics(input_grid, output_grid)
    all_metrics.append({'example': i, 'metrics': metrics})

print(json.dumps(all_metrics, indent=2))