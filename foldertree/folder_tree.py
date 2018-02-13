"""Explore a directory and print its structure as graphviz graph."""
import os
import sys

import pygraphviz as pgv
from PIL import ImageFont

from nodes import Node

EXCLUDE = ['.git', '__pycache__']

SHARED_ATTRIBUTES = ", style=filled, colorscheme=ylgnbu"
GRAPHVIZ_DPI = 60.
FONT_SIZE = 14


class FileNode(Node):
    """FileNode class."""

    type = 'File'
    attributes = "[shape=note" + SHARED_ATTRIBUTES

    def __init__(self, color_scheme, *args, **kwargs):
        """Init Node."""
        self.attributes += str(color_scheme)
        super().__init__(*args, **kwargs)


class DirectoryNode(Node):
    """DirectoryNode class."""

    type = 'Directory'
    attributes = "[shape=folder" + SHARED_ATTRIBUTES
    default_icon = "file-directory"

    def __init__(self, color_scheme, *args, **kwargs):
        """Init Node."""
        self.children = []
        self.file_children = []
        self.directory_children = []
        self.attributes += str(color_scheme)
        super().__init__(*args, **kwargs)

    def add(self, node):
        """Add node to tree."""
        if isinstance(node, FileNode):
            self.file_children.append(node)
        elif isinstance(node, DirectoryNode):
            self.directory_children.append(node)

        self.children = self.file_children + self.directory_children
        node.parent(self)


class EmptyNode(Node):
    """EmptyNode."""

    type = 'Empty'
    attributes = "[shape=\"point\", width=0, height=0]"

    def __init__(self, *args, **kwargs):
        """Init Node."""
        self.children = ""
        super().__init__(*args, **kwargs)

    def add(self, node):
        """Add node to tree."""
        self.children = node
        node.parent(self)

    def print_for_graphviz(self):
        """Represent node for graphviz layout."""
        representation = "\t" + self.id() + " "
        representation += self.attributes + "\n"
        return representation


def write_to_file(filename, content, mode='a'):
    """Write content to file."""
    with open(filename, mode) as f:
        f.write(content)


def open_graph(filename):
    """Open graphviz graph."""
    graph = "strict digraph projetcStructure { \n"
    graph += "\tgraph [overlap=false, splines=ortho, ranksep=0.05]\n"
    graph += "\tedge[arrowhead=none, color=black]\n"
    graph += f'\tnode[fontname=\"DejaVu Sans Mono\", fontsize={FONT_SIZE}]\n'
    write_to_file(filename, graph, 'w')


def close_graph(filename):
    """Close graph."""
    write_to_file(filename, "\n}")


def print_tree(root):
    """Print folder tree."""
    nodes = ""
    invisible_edges = ""
    edges = ""
    temp_nodes = ""
    temp_edges = ""

    nodes += root.print_for_graphviz()
    curr_invisible = root
    try:
        rank_visible = "\t{rank=same; "
        rank_invisible = rank_visible
        for child in root.children:
            (t_nodes, t_edges) = print_tree(child)
            temp_nodes += t_nodes
            temp_edges += t_edges

            nodes += child.print_for_graphviz()

            empty = EmptyNode("empty" + child.name, child.depth)
            nodes += empty.print_for_graphviz()

            invisible_edges += curr_invisible.id() + " -> " + empty.id() + "\n"
            edges += empty.id() + " -> " + child.id() + "\n"

            rank_invisible += " " + empty.id()
            rank_visible += " " + child.id()

            curr_invisible = empty

        if len(root.children) is 0:
            rank_visible = ""
            rank_invisible = ""
        else:
            rank_visible += "}\n"
            rank_invisible += "}\n"

        nodes += temp_nodes
        edges = rank_invisible + invisible_edges + rank_visible + edges
        edges += temp_edges
    except AttributeError:
        pass
    return (nodes, edges)


def walk_dir(root, depth, color_scheme):
    """Explore directory and build graph until depth."""
    directory = root.complete_path
    content = os.listdir(directory)
    node = None
    font = ImageFont.truetype('DejaVuSansMono.ttf', FONT_SIZE)
    width = 0
    if depth > 0:
        for c in content:
            if c not in EXCLUDE:
                fname = directory + c
                if os.path.isfile(fname):
                    node = FileNode(color_scheme,
                                    c,
                                    depth,
                                    complete_path=fname)
                else:
                    node = DirectoryNode(
                        color_scheme, c, depth, complete_path=fname)
                    node = walk_dir(node, depth - 1, color_scheme)
                root.add(node)

                width = max(width, font.getsize(node.name)[0])

        root.children_width = width / GRAPHVIZ_DPI + ((1 / 72) * 20 * 2)
    return root


def build_tree(output, td_name, target_dir, depth):
    """Build tree from target_dir and write it to output file."""
    if depth < 3:
        color_scheme = 3
    else:
        color_scheme = depth + 1

    try:
        print('Building tree...')
        output += '.dot'
        open_graph(output)

        root = DirectoryNode(color_scheme, td_name, depth +
                             1, complete_path=target_dir)
        root = walk_dir(root, depth, color_scheme)

        (nodes, edges) = print_tree(root)

        write_to_file(output, nodes + edges)
        close_graph(output)
    except FileNotFoundError as e:
        exit(f'Error:\t{e.strerror}: {output}\nExiting...')


def main(target_dir=".", depth=2):
    """Catch main function."""
    td_name = os.getcwd().split("/")[-1] if target_dir is "." else target_dir

    directory = 'generated/'

    if not os.path.exists(directory):
        os.makedirs(directory)

    output = directory + 'folder-tree-for-' + \
        td_name.replace("/", "-")

    while os.path.isfile(f'{output}.dot'):
        output += "0"

    build_tree(output, td_name, target_dir, depth)

    print(f'Wrote folder tree as [{output}.dot]\nComputing pdf...')
    g = pgv.AGraph(f'{output}.dot')
    g.draw(f'{output}.pdf', prog="dot", args='-Grankdir=LR')
    print(f'Wrote pdf as [{output}.pdf]')


if __name__ == "__main__":

    if len(sys.argv) < 2:
        exit("Il est nécessaire de spécifier sur \
             quel répertoire effectuer la recherche")

    target_dir = str(sys.argv[1])
    depth = int(sys.argv[2]) if len(sys.argv) > 2 else 2

    main(target_dir, depth)
