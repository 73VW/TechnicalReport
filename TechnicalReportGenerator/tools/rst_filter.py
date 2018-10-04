#!/usr/bin/env python

"""
Pandoc filter to convert all regular text to uppercase.

Code, link URLs, etc. are not affected.
"""

import re

from pandocfilters import Image
from pandocfilters import LineBreak
from pandocfilters import RawInline
from pandocfilters import toJSONFilter


def rstFilter(key, value, format, meta):
    """
    Filter datas.

    First part search for latex reference to figure and writes them
    as RawInline thereby backslashes are not escaped.

    Second part search for images and set a label in the description
    in order to be able to make a reference to them.
    """
    if key == 'Str':
        if re.search("@fig:", value):
            p = re.compile(r'@fig:((?:\w+\/?)*\w+\.\w+)')
            results = p.findall(value)
            return RawInline('latex', "\\ref{" + results[0] + "}")

        if re.search(r'@cite:', value):
            p = re.compile(r'@cite:(\w+)')
            result = p.findall(value)[0]
            return RawInline('latex', "\\cite{" + result + "}")

        if re.search("@bib:", value):
            result = value.split(":", 1)[1]
            inline = "\\begin{thebibliography}{50}\section{"
            inline += result + "}\label{" + result + "}"
            return RawInline('latex', inline)

        if re.search("@endbib", value):
            return RawInline('latex', "\\end{thebibliography}")

        if re.search("@bibitem", value):
            title, desc, date, url = value.split(":", 1)[1].split(", ")
            inline = "\\bibitem{"+title+"} "+desc+" \\textsl{"+date+"}."
            inline2 = 'latex', "\\url{"+url+"}"
            type_ = 'latex'
            return [RawInline(type_, inline), LineBreak(), RawInline(inline2)]

    elif key == 'Image':
        [attrs, caption, src] = value
        new_capt = src[0]
        # add \label{IMAGE_LABEL} to the picture description
        new_desc = "\\" + "label{" + new_capt + "}"
        caption.append(RawInline('latex', new_desc))
        return Image(attrs, caption, src)


if __name__ == "__main__":
    toJSONFilter(rstFilter)
