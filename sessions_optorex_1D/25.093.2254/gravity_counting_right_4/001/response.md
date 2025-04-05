```python
import re # Needed for splitting the string

"""
Counts the number of non-zero integers in the input sequence and generates an output sequence consisting of that many '1's followed by '0's to fill the remaining length (total length 12).
"""

def count_non_zeros(input_list):
  """Counts the number of non-zero elements in a list."""
  count = 0
  for num in input_list:
    if num != 0:
      count += 1
  return count

def transform(input_str):
  """
  Transforms an input string of 12 space-separated digits into an output string
  of 12 binary digits based on the count of non-zero digits in the input.
  """
  # 1. Accept an input sequence of 12 integers (as a string).
  # Parse the input string into a list of integers.
  input_list = [int(x) for x in input_str.split()]

  # 2. Initialize a counter variable non_zero_count to zero.
  # 3. Iterate through each integer in the input sequence.
  # 4. For each integer, if it is not equal to 0, increment non_zero_count.
  non_zero_count = count_non_zeros(input_list)

  # 5. Create a new output sequence.
  output_list = []

  # 6. Append the integer '1' to the output sequence non_zero_count times.
  for _ in range(non_zero_count):
    output_list.append(1)

  # 7. Calculate the number of zeros needed: zero_count = 12 - non_zero_count.
  zero_count = 12 - non_zero_count

  # 8. Append the integer '0' to the output sequence zero_count times.
  for _ in range(zero_count):
    output_list.append(0)

  # 9. Return the generated output sequence (formatted as a string).
  output_str = " ".join(map(str, output_list))
  return output_str

```