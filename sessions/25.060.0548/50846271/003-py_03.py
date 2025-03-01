# Example 3 analysis.
input_grid = [[2,2,2],[2,0,2],[2,2,2]]
expected_output_grid = [[8,2,8],[8,0,8],[8,2,8]]

actual_output_grid = transform(input_grid)
print(f"Actual: {actual_output_grid}")
print(f"Expect: {expected_output_grid}")
diff = np.array(actual_output_grid) != np.array(expected_output_grid)
print(f"Diff indices: {np.where(diff)}")