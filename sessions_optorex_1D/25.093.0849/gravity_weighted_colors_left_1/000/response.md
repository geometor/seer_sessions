**Perception of Elements:**

The input consists of a sequence of numbers (specifically, the digits 0, 1, and 2) presented as a space-separated string. The output is also a sequence of the same digits, also presented as a space-separated string, and always having the same length as the input sequence. The key observation across all examples is that the digits in the output sequence are the same as the digits in the input sequence, but they are arranged in ascending numerical order. The count of each digit (0s, 1s, and 2s) remains the same from input to output.

**Facts:**


```yaml
Input:
  Type: String
  Format: Space-separated digits
  Content: Sequence of digits (0, 1, 2)
  Length: Constant (12 digits in examples)
Output:
  Type: String
  Format: Space-separated digits
  Content: Sequence of digits (0, 1, 2)
  Length: Same as input
Transformation:
  Action: Sorting
  Object: The sequence of digits from the input
  Rule: Arrange digits in non-decreasing (ascending) numerical order
  Property_Preserved: Count of each distinct digit (0, 1, 2)
Relationship:
  - The output sequence is a reordering of the input sequence.
  - The output sequence is the sorted version of the input sequence.
```


**Natural Language Program:**

1.  Parse the input string into a list of individual digits.
2.  Sort the list of digits in ascending numerical order.
3.  Format the sorted list of digits back into a space-separated string.
4.  Return the formatted string as the output.