
## example 1
*input:*
```
5 1 1 1 1 1 5 0 0 0 0 0 0 0 0 0 0 1 1 0 1 0 0 1 0 0 0 0 1 0
0 1 0 1 0 0 0 1 1 1 1 0 1 1 1 0 0 0 0 1 1 1 0 1 0 1 1 1 1 1
1 1 0 0 0 1 0 1 0 1 1 1 0 1 1 0 0 0 0 1 0 0 1 1 0 0 1 0 0 0
```
*expected output:*
```
5 1 1 1 1 1 5 0 0 0 0 0 0 0 0 0 0 1 1 0 1 0 0 1 0 0 0 0 1 0
0 1 0 1 0 0 0 1 1 1 1 0 1 1 1 6 6 6 6 1 1 1 0 1 0 1 1 1 1 1
1 1 0 0 0 1 0 1 0 1 1 1 0 1 1 6 6 6 6 1 0 0 1 1 0 0 1 0 0 0
```
*transformed output:*
```
5 6 6 6 6 6 5 0 0 0 0 0 0 0 0 0 0 6 6 0 6 0 0 6 0 0 0 0 6 0
0 6 0 6 0 0 0 6 6 6 6 0 6 6 6 0 0 0 0 6 6 6 0 6 0 6 6 6 6 6
6 6 0 0 0 6 0 6 0 6 6 6 0 6 6 0 0 0 0 6 0 0 6 6 0 0 6 0 0 0
```
size: True
palette: True
color count: False
pixels off: 49
**FAILED!**

## example 2
*input:*
```
1 1 1 0 0 1 1 0 1 1 1 1 0 0 0 0 0 1 0 1
1 1 1 0 1 1 0 0 1 0 1 0 1 1 0 0 0 1 1 1
0 0 1 1 1 0 0 1 0 1 0 1 1 0 1 0 1 1 1 0
0 1 0 1 0 0 0 1 1 0 1 1 1 0 0 0 1 1 1 1
```
*expected output:*
```
1 1 1 0 0 1 1 0 1 1 1 1 0 0 6 6 6 1 0 1
1 1 1 0 1 1 0 0 1 0 1 0 1 1 6 6 6 1 1 1
0 0 1 1 1 0 0 1 0 1 0 1 1 0 1 0 1 1 1 0
0 1 0 1 0 0 0 1 1 0 1 1 1 0 0 0 1 1 1 1
```
*transformed output:*
```
6 6 6 0 0 6 6 0 6 6 6 6 0 0 0 0 0 6 0 6
6 6 6 0 6 6 0 0 6 0 6 0 6 6 0 0 0 6 6 6
0 0 6 6 6 0 0 6 0 6 0 6 6 0 6 0 6 6 6 0
0 6 0 6 0 0 0 6 6 0 6 6 6 0 0 0 6 6 6 6
```
size: True
palette: True
color count: False
pixels off: 51
**FAILED!**

## example 3
*input:*
```
1 1 0 0 0 0 0 0 0 1 0 0 1 0 0 1 0 1 0 1
0 1 0 0 0 0 0 1 1 1 1 0 0 1 1 0 0 0 0 0
```
*expected output:*
```
1 1 6 6 6 6 6 0 0 1 0 0 1 0 0 1 0 1 0 1
0 1 6 6 6 6 6 1 1 1 1 0 0 1 1 0 0 0 0 0
```
*transformed output:*
```
6 6 0 0 0 0 0 0 0 6 0 0 6 0 0 6 0 6 0 6
0 6 0 0 0 0 0 6 6 6 6 0 0 6 6 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 24
**FAILED!**

## example 4
*input:*
```
0 0 1 0 0 1 0 0 0 1 1 1 1 1 0 0 0 0 0 0
1 0 0 0 0 1 1 0 0 1 0 0 0 0 0 1 0 0 0 0
1 0 1 1 0 0 1 0 1 0 1 0 1 0 0 0 1 0 0 0
0 0 1 0 0 0 1 1 0 0 1 1 1 1 1 1 1 0 0 1
```
*expected output:*
```
0 0 1 0 0 1 0 0 0 1 1 1 1 1 0 0 0 6 6 6
1 0 0 0 0 1 1 0 0 1 0 0 0 0 0 1 0 6 6 6
1 0 1 1 0 0 1 0 1 0 1 0 1 0 0 0 1 6 6 6
0 0 1 0 0 0 1 1 0 0 1 1 1 1 1 1 1 0 0 1
```
*transformed output:*
```
0 0 6 0 0 6 0 0 0 6 6 6 6 6 0 0 0 0 0 0
6 0 0 0 0 6 6 0 0 6 0 0 0 0 0 6 0 0 0 0
6 0 6 6 0 0 6 0 6 0 6 0 6 0 0 0 6 0 0 0
0 0 6 0 0 0 6 6 0 0 6 6 6 6 6 6 6 0 0 6
```
size: True
palette: True
color count: False
pixels off: 40
**FAILED!**
