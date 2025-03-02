
## example 1
*input:*
```
4 4 0 0 0 0 5 0
4 4 0 0 0 0 0 0
0 0 4 0 0 0 5 0
0 4 0 0 5 5 0 0
0 0 6 0 0 0 9 0
6 6 6 0 0 0 0 9
6 0 6 6 9 9 0 0
0 6 6 0 9 0 0 0
```
*expected output:*
```
4 4 5 0
6 6 6 9
6 9 5 6
5 5 6 0
```
*transformed output:*
```
4 0 0 0
0 0 5 0
6 6 0 9
6 6 9 0
```
size: True
palette: True
color count: False
pixels off: 12
**FAILED!**

## example 2
*input:*
```
4 0 0 4 5 5 0 0
0 0 0 0 0 0 5 5
4 4 0 4 0 5 0 0
4 0 4 4 0 5 5 5
0 0 0 6 0 9 0 9
0 0 6 0 0 9 0 0
6 0 0 6 0 9 0 9
0 0 6 6 0 0 0 9
```
*expected output:*
```
5 5 0 6
0 9 5 5
6 5 0 6
4 5 5 5
```
*transformed output:*
```
0 0 5 5
4 4 5 5
0 6 9 0
0 6 0 9
```
size: True
palette: True
color count: False
pixels off: 14
**FAILED!**

## example 3
*input:*
```
0 0 0 4 5 0 0 0
4 0 0 0 0 5 0 0
0 0 0 4 0 0 5 0
0 4 0 4 0 0 5 0
6 0 0 0 0 9 9 0
6 0 0 0 0 9 0 9
6 0 6 0 9 9 9 0
6 0 6 0 0 0 0 0
```
*expected output:*
```
5 9 9 4
6 5 0 9
6 9 5 4
6 4 5 4
```
*transformed output:*
```
0 0 5 0
0 4 0 5
6 0 9 9
6 6 9 0
```
size: True
palette: True
color count: False
pixels off: 13
**FAILED!**

## example 4
*input:*
```
4 0 0 4 0 5 0 5
0 0 4 0 5 0 0 5
0 0 4 4 0 0 5 5
4 0 0 0 5 0 0 5
6 6 6 0 9 0 9 9
6 6 6 0 0 9 9 9
6 0 0 6 9 9 0 9
6 6 0 6 9 0 9 9
```
*expected output:*
```
6 5 6 5
5 6 6 5
6 9 5 5
5 6 9 5
```
*transformed output:*
```
0 4 5 5
0 4 0 5
6 6 9 9
6 6 9 9
```
size: True
palette: False
color count: False
pixels off: 11
**FAILED!**

## example 5
*input:*
```
0 4 4 4 0 5 5 5
0 0 4 0 5 5 0 5
0 0 0 0 5 0 0 0
4 0 0 0 5 0 0 0
6 6 0 6 0 0 9 9
0 0 0 6 9 0 9 0
0 0 0 6 9 0 9 9
6 6 0 6 0 9 0 9
```
*expected output:*
```
6 5 5 5
5 5 9 5
5 0 9 6
5 6 0 6
```
*transformed output:*
```
0 4 5 5
0 0 5 0
6 6 0 9
6 6 9 9
```
size: True
palette: False
color count: False
pixels off: 13
**FAILED!**
