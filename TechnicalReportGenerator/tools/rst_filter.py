#!/usr/bin/env python

"""
Pandoc filter to convert all regular text to uppercase.

Code, link URLs, etc. are not affected.
"""

import re

from pandocfilters import Image, RawInline, toJSONFilter


def rstFilter(key, value, format, meta):
    """
    Filter datas.

    First part search for latex reference to figure and writes them
    as RawInline thereby backslashes are not escaped.

    Second part search for images and set a label in the description
    in order to be able to make a reference to them.
    """
    if key == 'Str':
        if re.search("\$ref", value):
            # if we find a link, set it as raw link and re-add a
            # backslash before the ref keyword
            return RawInline('latex', value[:1] + "\\" + value[1:])
        elif re.search(".*}\$", value):
            return RawInline('latex', value)

    elif key == 'Image':
        [attrs, caption, src] = value
        new_capt = src[0]
        # add \label{IMAGE_LABEL} to the picture description
        new_desc = "\\" + "label{" + new_capt + "}"
        caption.append(RawInline('latex', new_desc))
        return Image(attrs, caption, src)


if __name__ == "__main__":
    toJSONFilter(rstFilter)
