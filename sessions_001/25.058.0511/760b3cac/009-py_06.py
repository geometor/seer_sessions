# this example has no errors
# compare(example['input'], example['output'], transform)

# Example 1:
#   - Input: [[0, 0, 0], [0, 8, 0], [0, 0, 0]]
#   - Output: [[0, 0, 0], [0, 8, 8], [0, 0, 0]]
#   - Comparison Result: No errors found.

# Example 2:
example = task.train[1]
compare(example['input'], example['output'], transform)

# Example 2:
#   - Input: [[0, 0, 8, 0, 0], [0, 0, 8, 0, 0], [0, 0, 8, 0, 0], [0, 0, 8, 0, 0], [0, 0, 8, 0, 0]]
#   - Output: [[0, 0, 8, 8, 8], [0, 0, 8, 8, 8], [0, 0, 8, 8, 8], [0, 0, 8, 8, 8], [0, 0, 8, 8, 8]]
#   - Comparison Result: No errors found.

example = task.train[2]
compare(example['input'], example['output'], transform)
# Example 3:
#   - Input: [[0, 0, 0, 0, 0], [0, 8, 0, 8, 0], [0, 0, 0, 0, 0], [0, 8, 0, 8, 0], [0, 0, 0, 0, 0]]
#   - Output: [[0, 0, 0, 0, 0], [0, 8, 8, 8, 8], [0, 0, 0, 0, 0], [0, 8, 8, 8, 8], [0, 0, 0, 0, 0]]
#   - Comparison Result: No errors found.
