**Perception of Task Elements:**

The task involves rearranging a sequence of integers. The input consists of a list of integers, containing both zeros and non-zero values. The output is a list of the same length, where all the zero elements from the input are moved to the beginning of the list, and all the non-zero elements are moved to the end, preserving their original relative order.

**Facts:**


```yaml
Input:
  type: sequence
  elements: integers
  properties:
    - contains zeros
    - contains non-zero integers
    - fixed length (e.g., 12 in examples)

Output:
  type: sequence
  elements: integers
  properties:
    - same length as input
    - same multiset of elements as input (same numbers, same counts)
    - structured arrangement

Transformation:
  action: rearrange elements
  rule: partition based on value (zero vs. non-zero)
  constraints:
    - relative order of non-zero elements is preserved
    - all zeros are grouped together at the beginning
    - all non-zeros are grouped together at the end

Relationships:
  - Input element maps to an output element.
  - The position of an element in the output depends on its value (zero or non-zero) and its original position relative to other non-zero elements.
  - The count of zeros in the input equals the count of leading zeros in the output.
  - The sequence of non-zero elements in the input is identical to the sequence of trailing non-zero elements in the output.
```


**Natural Language Program:**

1.  Accept an input sequence of integers.
2.  Create a new, empty sequence to store the non-zero elements, maintaining their original relative order.
3.  Initialize a counter for the number of zero elements to zero.
4.  Iterate through the input sequence:
    a.  If the current element is zero, increment the zero counter.
    b.  If the current element is non-zero, append it to the sequence of non-zero elements.
5.  Construct the final output sequence:
    a.  Start with a sequence consisting of the counted number of zeros.
    b.  Append the sequence of collected non-zero elements to the end of the zero sequence.
6.  Return the constructed output sequence.