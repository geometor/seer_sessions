
## example 1
*input:*
```
1 1 1 1 1 1 1
1 2 2 1 1 1 1
1 2 2 3 1 1 1
1 1 1 2 1 1 1
1 1 1 1 1 1 1
```
*expected output:*
```
2 2 0
2 2 3
0 0 2
```
*transformed output:*
```
[2 2 0] [2 2 3] [0 0 2]
```
**ERROR**: Could not save image: 'NoneType' object has no attribute 'to_image'

## example 2
*input:*
```
1 1 1 1 1 1 1
1 1 3 1 2 1 1
1 1 3 1 2 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
```
*expected output:*
```
3 0 2
3 0 2
```
*transformed output:*
```
[3] [3]
[2] [2]
```
**ERROR**: Could not save image: 'NoneType' object has no attribute 'to_image'

## example 3
*input:*
```
1 1 1 1 1 1
1 1 1 1 1 1
1 5 5 1 1 1
1 5 5 1 1 1
1 6 6 1 1 1
1 1 1 1 1 1
1 1 1 1 1 1
```
*expected output:*
```
5 5
5 5
6 6
```
*transformed output:*
```
[5 5] [5 5] [6 6]
```
**ERROR**: Could not save image: 'NoneType' object has no attribute 'to_image'
