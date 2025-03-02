
## example 1
*input:*
```
0 7 7
7 7 7
0 7 7
```
*expected output:*
```
0 0 0 0 7 7 0 7 7
0 0 0 7 7 7 7 7 7
0 0 0 0 7 7 0 7 7
0 7 7 0 7 7 0 7 7
7 7 7 7 7 7 7 7 7
0 7 7 0 7 7 0 7 7
0 0 0 0 7 7 0 7 7
0 0 0 7 7 7 7 7 7
0 0 0 0 7 7 0 7 7
```
*transformed output:*
```
0 0 0 7 7 7 7 7 7
0 0 0 7 7 7 7 7 7
0 0 0 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
0 0 0 7 7 7 7 7 7
0 0 0 7 7 7 7 7 7
0 0 0 7 7 7 7 7 7
```
size: True
palette: True
color count: False
pixels off: 14
**FAILED!**

## example 2
*input:*
```
4 0 4
0 0 0
0 4 0
```
*expected output:*
```
4 0 4 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
```
*transformed output:*
```
4 0 4 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0
4 0 4 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0
```
size: True
palette: True
color count: False
pixels off: 9
**FAILED!**

## example 3
*input:*
```
0 0 0
0 0 2
2 0 2
```
*expected output:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2
2 0 2 0 0 0 2 0 2
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 2
2 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
2 0 2 0 0 0 2 0 2
```
size: True
palette: True
color count: True
pixels off: 6
**FAILED!**

## example 4
*input:*
```
6 6 0
6 0 0
0 6 6
```
*expected output:*
```
6 6 0 6 6 0 0 0 0
6 0 0 6 0 0 0 0 0
0 6 6 0 6 6 0 0 0
6 6 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0
0 0 0 6 6 0 6 6 0
0 0 0 6 0 0 6 0 0
0 0 0 0 6 6 0 6 6
```
*transformed output:*
```
6 6 0 6 6 0 0 0 0
6 0 0 6 0 0 0 0 0
0 6 6 0 6 6 0 0 0
6 6 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0
0 0 0 6 6 0 6 6 0
0 0 0 6 0 0 6 0 0
0 0 0 0 6 6 0 6 6
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 5
*input:*
```
2 2 2
0 0 0
0 2 2
```
*expected output:*
```
2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0
0 2 2 0 2 2 0 2 2
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 2 2
```
*transformed output:*
```
2 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0
2 0 2 2 0 2 2 0 2
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 2 0 2
```
size: True
palette: True
color count: False
pixels off: 20
**FAILED!**
