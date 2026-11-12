#!/usr/bin/env python3
"""
patterns.py
===========

Compiled regular expressions for extracting eight kinds of structured data
from raw text (for example, API responses containing hundreds of pages).

Every pattern is a ``re.Pattern`` object stored in the ``PATTERNS`` dictionary
at the bottom of the file, so other modules can loop over all of them.

Design notes
------------
* Raw strings (``r"..."``) are used everywhere so backslashes are not
  interpreted by Python.
* ``re.VERBOSE`` is used so each part of a pattern can carry a comment.
  (In verbose mode, a literal space must be written ``[ ]`` or ``\\ ``.)
* Lookarounds such as ``(?<!\\d)`` and ``(?!\\d)`` stop a pattern from matching
  a *piece* of a longer number or word.
"""

import re

# --------------------------------------------------------------------------- #
# 1. EMAIL ADDRESSES
#    user@example.com | firstname.lastname@company.co.uk
# --------------------------------------------------------------------------- #
EMAIL = re.compile(
    r"""
    (?<![\w.%+-])                 # not in the middle of a longer word
    [A-Za-z0-9._%+-]+             # local part: letters, digits, . _ % + -
    @                             # exactly one @ symbol
    [A-Za-z0-9-]+                 # first domain label (example, company)
    (?:\.[A-Za-z0-9-]+)*          # optional extra labels (.co, .mail ...)
    \.[A-Za-z]{2,}                # final dot + TLD of 2+ letters (.com, .uk)
    (?![\w-])                     # not followed by more word characters
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
# 2. URLS
#    https://www.example.com | https://subdomain.example.org/page
# --------------------------------------------------------------------------- #
URL = re.compile(
    r"""
    https?://                     # scheme: http or https
    (?:[A-Za-z0-9-]+\.)+          # one or more labels, each ending in a dot
    [A-Za-z]{2,}                  # top-level domain
    (?::\d{1,5})?                 # optional port, e.g. :8080
    (?:                           # optional path / query / fragment
        /
        (?:[^\s<>"']*             #   any URL characters ...
           [^\s<>"'.,;:!?)]       #   ... but never END on punctuation, so a
        )?                        #   full stop after the URL is not captured
    )?
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #

# 3. PHONE NUMBERS
#    (123) 456-7890 | 123-456-7890 | 123.456.7890
# --------------------------------------------------------------------------- #
PHONE = re.compile(
    r"""
    (?<!\d)                       # not preceded by a digit
    (?:
        \(\d{3}\)[ ]?\d{3}[-.]\d{4}      # (123) 456-7890
      |
        \d{3}([-.])\d{3}\1\d{4}          # 123-456-7890 or 123.456.7890
    )                             # \1 forces the SAME separator both times
    (?!\d)                        # not followed by a digit
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
# 4. CREDIT CARD NUMBERS
#    1234 5678 9012 3456 | 1234-5678-9012-3456
# --------------------------------------------------------------------------- #
CREDIT_CARD = re.compile(
    r"""
    (?<!\d)                       # not preceded by a digit
    \d{4}                         # group 1
    ([ -])                        # separator: a space or a dash (captured)
    \d{4}\1                       # group 2 + SAME separator
    \d{4}\1                       # group 3 + SAME separator
    \d{4}                         # group 4
    (?!\d)                        # not followed by a digit
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
# 5. TIME (12-hour and 24-hour)
#    14:30 | 2:30 PM
# --------------------------------------------------------------------------- #
TIME = re.compile(
    r"""
    \b
    (?:
        # 12-hour clock: hour 1-12, minutes 00-59, AM/PM (listed FIRST so
        # "2:30 PM" is captured whole rather than just "2:30")
        (?:0?[1-9]|1[0-2]):[0-5]\d[ ]?[AaPp][Mm]
      |
        # 24-hour clock: hour 0-23, minutes 00-59 (and not followed by AM/PM)
        (?:[01]?\d|2[0-3]):[0-5]\d(?![ ]?[AaPp][Mm])
    )
    \b
    (?!:\d)                       # reject 12:30:45 style (seconds)
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
# 6. HTML TAGS
#    <p> | <div class="example"> | <img src="image.jpg" alt="description">
# --------------------------------------------------------------------------- #
HTML_TAG = re.compile(
    r"""
    </?                           # "<" or "</" (closing tag)
    [A-Za-z][A-Za-z0-9]*          # tag name: must start with a letter
    (?:                           # zero or more attributes
        \s+                       #   whitespace before each attribute
        [A-Za-z_:][\w:.-]*        #   attribute name
        (?:                       #   optional value
            \s*=\s*
            (?:"[^"<>]*"          #     double-quoted value
              |'[^'<>]*'          #     single-quoted value
              |[^\s"'=<>`]+       #     unquoted value
            )
        )?
    )*
    \s*/?>                        # optional self-closing slash, then ">"
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
