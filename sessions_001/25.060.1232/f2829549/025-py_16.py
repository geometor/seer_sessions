import numpy as np

#from previous interactions
task_id = '08ed6ac7'
examples = task_data[task_id]['train']

widths = []
for i, example in enumerate(examples):
    expected_output_grid = np.array(example['output'])
    widths.append(expected_output_grid.shape[1])

print(widths)
