# Example usage of tools (imaginary execution)
import numpy as np

# Assume tools are available:
# - compare_grids(grid1, grid2) -> prints element-wise comparison of two numpy arrays

task_examples = [
  {
     "input": np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,2,3,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,4,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]),
     "output": np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,3,3,0,0,0],[0,0,0,0,0,0,0,0],[4,0,0,0,0,0,0,4],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]])
  },
  {
    "input": np.array([[0,0,0,0,0,0,0],[0,0,0,0,2,0,0],[0,0,0,0,0,0,0],[0,0,4,0,0,0,0],[0,0,0,0,0,0,0],[0,3,0,0,0,0,0],[0,0,0,0,0,0,0]]),
    "output": np.array([[0,0,0,0,2,0,0],[0,0,0,0,2,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,3,0,0,0,0,0],[0,0,0,0,0,0,0]])
  },
  {
        "input": np.array([[0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,2,1,3,0,0,0],[0,0,0,0,0,0,0,0],[0,0,4,4,0,4,4,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]),
        "output": np.array([[0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,3,3,3,0,0,0],[0,0,0,0,0,0,0,0],[4,4,4,4,0,4,4,4],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]])
  }
]
predicted_outputs = []
for ex in task_examples:
   predicted_outputs.append(transform(ex["input"]))
print("Example 1 Comparison:")
compare_grids(predicted_outputs[0], task_examples[0]['output'])

print("\nExample 2 Comparison:")
compare_grids(predicted_outputs[1], task_examples[1]['output'])

print("\nExample 3 Comparison:")
compare_grids(predicted_outputs[2], task_examples[2]['output'])