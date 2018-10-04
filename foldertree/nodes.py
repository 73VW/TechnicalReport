"""Nodes used in printing directory structure."""
import datetime
import hashlib
import os
import re

EXTENSIONS_TO_ICON = {
    r'.+\.sh': 'terminal',
    r'.+\.pdf': 'file-pdf',
    r'.+\.py': 'python',
    r'(license)': 'book',
    r'(\.gitignore)': 'git-merge',
    r'(^\.travis.*)': 'travis',
    r'(\.github)': 'mark-github',
    r'.+\.cfg': 'settings',
    r'(^\..*)': 'gear',
    r'(.+\.md)': 'markdown',
    r'(.+\.dot)': 'kebab-horizontal',
    r'(.+\.rst)': 'note',
    r'(.+\.(png|svg|jpe?g|bmp))': 'file-media'
}

ICON_FOLDER = 'octicons/'


class bcolors:
    """
    Colors used to render in console.

    Source: https://stackoverflow.com/a/287944
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Node():
    """Node class."""

    type = "Node"
    attributes = ""
    default_icon = "file"

    def __init__(self, name, depth=0, parent=None, complete_path=""):
        """Init Node."""
        self.name = name
        self.depth = depth
        self.identifier = self.make_identifier(name)
        self.parent_node = parent
        self.complete_path = complete_path + "/"
        self.children_width = 0

    def make_identifier(self, name):
        """Make a unique identifier."""
        identifier = str(datetime.datetime.now().timestamp())
        identifier += name
        hash_object = hashlib.md5(identifier.encode())
        return hash_object.hexdigest()

    def __repr__(self):
        """Represent obj."""
        return str(self)

    def __str__(self):
        """Stringify node."""
        string = bcolors.FAIL
        string += f'Node {self.type}:\n'
        string += bcolors.ENDC

        string += bcolors.HEADER
        string += f'\tName: {self.name}\n'
        string += bcolors.ENDC

        string += bcolors.OKBLUE
        string += '\tParent: '
        if self.parent_node is not None:
            string += self.parent_node.name + '\n'
        else:
            string += "None\n"
        string += bcolors.ENDC

        string += bcolors.OKGREEN
        string += '\tChildren:\n'
        try:
            for child in self.children:
                string += f'\t\t{child.name}\n'
        except TypeError:
            string += f'\t\t{self.children.name}\n'
        except AttributeError:
            pass

        string += bcolors.ENDC

        return string

    def id(self):
        """Get node identifier with quotes."""
        return "\"" + self.identifier + "\""

    def recursive_print(self, depth=0):
        """Stringify node recursively."""
        string = bcolors.HEADER
        string += '\t' * depth
        string += f'{self.name}\n'
        string += bcolors.ENDC
        try:
            for child in self.children:
                string += '\t' * depth
                string += child.recursive_print(depth + 1) + "\n"
        except TypeError:
            string += '\t' * depth
            string += self.children.recursive_print(depth) + "\n"
        except AttributeError:
            pass

        return string

    def parent(self, parent):
        """Add parent node to self."""
        self.parent_node = parent

    def print_for_graphviz(self):
        """Represent node for graphviz layout."""
        label = self.label()
        representation = "\t" + self.id() + " "
        representation += self.attributes
        if self.parent_node:
            representation += ", width=" + str(self.parent_node.children_width)
        representation += f', label={label}, color={self.depth}]\n'
        return representation

    def label(self):
        """Get html label for node."""
        icon_path = self.get_icon_path()
        lab = '<<TABLE><TR><TD WIDTH="20" HEIGHT="20" FIXEDSIZE="TRUE">'
        lab += f'<IMG SRC="{icon_path}" SCALE="TRUE"/></TD>'
        lab += f'<TD>{self.name}</TD></TR></TABLE>>'
        return lab

    def get_icon_path(self):
        """Get icon path according to icon name."""
        icon_name = self.get_icon_name()
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        return f'{curr_dir}/{ICON_FOLDER}{icon_name}.png'

    def get_icon_name(self):
        """Get icon name according to filename."""
        for reg in EXTENSIONS_TO_ICON:
            p = re.compile(reg, re.IGNORECASE)
            if p.match(self.name):
                return EXTENSIONS_TO_ICON[reg]
        return self.default_icon
