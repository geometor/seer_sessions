```python
import collections
import numpy as np # numpy might be useful for more complex array operations if needed later

"""
Transforms the input list by finding the first unique non-zero digit that appears exactly twice. 
If such a digit is found, it fills the elements between its two occurrences with the digit's value. 
If no such digit exists, the original list is returned unchanged.
"""

def find_indices(arr, value):
  """
  Helper function to find all indices of a specific value in a list.

  Args:
    arr: The list to search within.
    value: The value to find indices for.

  Returns:
    A list of indices where the value occurs.
  """
  return [i for i, x in enumerate(arr) if x == value]

def transform(input_list):
  """
  Applies the transformation rule to the input list.

  Args:
    input_list: A list of integers.

  Returns:
    A new list representing the transformed output.
  """
  # Create a copy of the input list to potentially modify
  output_list = list(input_list)

  # Find unique non-zero digits present in the input list
  # Using an ordered dict preserves insertion order which might be important if multiple digits qualify
  # although the prompt implies returning after the first match.
  # A set is simpler if order doesn't matter: non_zero_digits = set(x for x in input_list if x != 0)
  unique_digits = collections.OrderedDict()
  for x in input_list:
      if x != 0:
          unique_digits[x] = None # Store unique non-zero digits in order of appearance

  # Iterate through each unique non-zero digit found
  for digit in unique_digits.keys():
    # Find all indices where this digit appears in the original input list
    indices = find_indices(input_list, digit)

    # Check if the digit occurs exactly twice
    if len(indices) == 2:
      # Get the first and second index
      idx1, idx2 = indices[0], indices[1]

      # Fill the gap in the output_list between the two indices
      # The range starts from the element *after* the first occurrence (idx1 + 1)
      # and goes up to (but does not include) the second occurrence (idx2).
      for i in range(idx1 + 1, idx2):
        output_list[i] = digit

      # According to the natural language program and examples,
      # we return immediately after finding and processing the first valid pair.
      return output_list

  # If the loop completes without finding any digit that occurred exactly twice,
  # it means no transformation should be applied.
  # Return the unmodified copy (which is identical to the input in this case).
  return output_list
```