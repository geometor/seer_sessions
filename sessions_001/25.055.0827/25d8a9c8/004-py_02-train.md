
## example 1
*input:*
```
4 4 4
2 3 2
2 3 3
```
*expected output:*
```
5 5 5
0 0 0
0 0 0
```
*transformed output:*
```
5 5 5
0 0 0
0 0 0
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 2
*input:*
```
7 3 3
6 6 6
3 7 7
```
*expected output:*
```
0 0 0
5 5 5
0 0 0
```
*transformed output:*
```
5 5 5
0 0 0
0 0 0
```
size: True
palette: True
color count: True
pixels off: 6
**FAILED!**

## example 3
*input:*
```
2 9 2
4 4 4
9 9 9
```
*expected output:*
```
0 0 0
5 5 5
5 5 5
```
*transformed output:*
```
5 5 5
0 0 0
0 0 0
```
size: True
palette: True
color count: False
pixels off: 9
**FAILED!**

## example 4
*input:*
```
2 2 4
2 2 4
1 1 1
```
*expected output:*
```
0 0 0
0 0 0
5 5 5
```
*transformed output:*
```
5 5 5
0 0 0
0 0 0
```
size: True
palette: True
color count: True
pixels off: 6
**FAILED!**
