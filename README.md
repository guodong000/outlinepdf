PDF 目录生成器 (PDF Outline Writer)
====

```
usage: main.py [-h] -t OUTLINE [-s OFFSET] pdf

PDF 目录生成器

positional arguments:
  pdf                   pdf 文件

options:
  -h, --help            show this help message and exit
  -t OUTLINE, --outline OUTLINE
                        目录文件。每一行表示一个目录项，缩进表示级别关系。目录项格式: [缩进][title] [页码]
  -s OFFSET, --offset OFFSET
                        页码偏移
```

## Outline File Example

Line Format: `[Indent][Title] [PageNumber]`

```
Chapter 1: First 1
    1.1 Hello 1
    1.2 World 2
Chapter 2: Second 3
Chapter 3: Third 4
```