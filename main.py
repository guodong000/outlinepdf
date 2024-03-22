import re
import argparse
import pathlib
import pypdf


class OutlineItem:
    def __init__(self, title=None, page_number=None, indent_length=0):
        self.title = title
        self.page_number = page_number
        self.indent_length = indent_length
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        
    def remove_child(self, child):
        self.children.remove(child)


parser = argparse.ArgumentParser(description='PDF 目录生成器')
parser.add_argument('-t', '--outline', type=argparse.FileType('r', encoding='utf-8'), required=True,
                    help='''目录文件。每一行表示一个目录项，缩进表示级别关系。目录项格式: [缩进][title] [页码]''')
parser.add_argument('-s', '--offset', help='页码偏移', type=int, default=0)
parser.add_argument('pdf', type=pathlib.Path, help='pdf 文件')


def parse_outline_tree(fp):
    tree = OutlineItem(indent_length=-1)
    parents = [tree]
    last_item = None
    line = fp.readline()
    while line:
        m = re.match(r'^( *?)(\S.*?)\s+(\d+?)\s*$', line)
        indent, title, page = m.groups()
        item = OutlineItem(title, int(page), len(indent))

        last_indent_len = last_item.indent_length if last_item else 0
        if item.indent_length > last_indent_len:
            parents.append(last_item)
        elif item.indent_length < last_indent_len:
            while parents[-1].indent_length >= item.indent_length:
                parents.pop()
        
        parents[-1].add_child(item)
        last_item = item
        line = fp.readline()
    return tree


def print_outline(item: OutlineItem, offset=0, indent=''):
    print(f'{indent}{item.title} [{item.page_number} - {item.page_number+offset}]')
    for child in item.children:
        print_outline(child, offset, indent+'  ')


def add_outline(writer: pypdf.PdfWriter, item: OutlineItem, offset=0, parent=None):
    obj = writer.add_outline_item(item.title, item.page_number+offset-1, parent)
    for child in item.children:
        add_outline(writer, child, offset, obj)


if __name__ == '__main__':
    args = parser.parse_args()
    pdf_path = args.pdf
    out_path = pdf_path.with_stem(pdf_path.stem + '.out')

    tree = parse_outline_tree(args.outline)

    with open(args.pdf, 'rb') as ifp:
        pdf_writer = pypdf.PdfWriter(clone_from=ifp)
        for child in tree.children:
            # print_outline(child, args.offset)
            add_outline(pdf_writer, child, args.offset)
        with open(out_path, 'wb') as ofp:
            pdf_writer.write(ofp)
            