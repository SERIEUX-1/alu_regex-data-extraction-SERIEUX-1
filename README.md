# alu_regex-data-extraction-SERIEUX-1
# Regex Data Extraction

A Python project that uses **regular expressions** to extract eight kinds of
structured data from large blocks of raw text, such as the string responses
returned by a web-aggregation API.

> **Author:** SERIEUX Elias  
> **Course:** African Leadership College of Higher Education(ALCHE)  
> **GitHub:** [@SERIEUX-1](https://github.com/SERIEUX-1)

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Setup Instructions](#setup-instructions)
5. [How to Run](#how-to-run)
6. [Regex Explanations](#regex-explanations)
7. [Sample Input and Output](#sample-input-and-output)
8. [Edge Cases Handled](#edge-cases-handled)
9. [Testing](#testing)
10. [Known Limitations](#known-limitations)

---

## Project Overview

An API aggregates data from across the web and returns hundreds of thousands of
pages of unstructured text. This project scans that text and pulls out the
useful pieces of information using compiled Python regular expressions (`re`).

Each pattern is:
- **documented** with line-by-line comments,
- **tested** with both valid and invalid inputs, and
- **demonstrated** on a realistic sample file that mixes good and bad data.

## Features

All **8 of 8** data types are implemented:

| # | Data type | Examples matched |
|---|-----------|------------------|
| 1 | Email addresses | `user@example.com`, `firstname.lastname@company.co.uk` |
| 2 | URLs | `https://www.example.com`, `https://subdomain.example.org/page` |
| 3 | Phone numbers | `(123) 456-7890`, `123-456-7890`, `123.456.7890` |
| 4 | Credit card numbers | `1234 5678 9012 3456`, `1234-5678-9012-3456` |
| 5 | Time (12h / 24h) | `14:30`, `2:30 PM` |
| 6 | HTML tags | `<p>`, `<div class="example">`, `<img src="image.jpg" alt="description">` |
| 7 | Hashtags | `#example`, `#ThisIsAHashtag` |
| 8 | Currency amounts | `$19.99`, `$1,234.56` |

## Project Structure

```
alu_regex-data-extraction-SERIEUX-1/
├── README.md              # Project documentation (this file)
├── requirements.txt       # Dependencies (pytest)
├── pytest.ini             # Test configuration
├── .gitignore
├── data/
│   └── sample_input.txt   # Sample text with valid AND invalid data
├── output/
│   └── sample_output.txt  # Saved extraction results
├── src/
│   ├── __init__.py
│   ├── patterns.py        # All 8 regex patterns (commented)
│   └── extractor.py       # Runs patterns on text/files, prints a report
└── tests/
    ├── __init__.py
    ├── test_patterns.py   # Valid + invalid cases for every pattern
    └── test_extractor.py  # End-to-end test on the sample file
```

## Setup Instructions

**Requirements:** Python 3.8 or newer.

```bash
# 1. Clone the repository
git clone https://github.com/SERIEUX-1/alu_regex-data-extraction-SERIEUX-1.git
cd alu_regex-data-extraction-SERIEUX-1

# 2. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies (only needed to run the tests)
pip install -r requirements.txt
```

> **Note:** On Ubuntu/Debian you may first need `sudo apt install python3-venv`.
> If the `python` command is not found, use `python3` instead.

The extractor itself uses only the Python standard library.

## How to Run

Run all commands from the **project root** (not from inside `src/`).

```bash
python3 -m src.extractor                                   # run on data/sample_input.txt
python3 -m src.extractor my_file.txt                       # run on your own file
python3 -m src.extractor --json                            # JSON output
python3 -m src.extractor --save output/sample_output.txt   # also save the report
pytest -v                                                  # run the test suite
```

## Regex Explanations

| Type | Key ideas used |
|------|----------------|
| **Email** | Local part `[A-Za-z0-9._%+-]+`, exactly one `@`, domain labels, then a dot and a TLD of 2+ letters. Lookarounds stop matches inside longer words. |
| **URL** | `https?://`, one or more `label.` groups (allows subdomains), TLD, optional port and path. The path cannot **end** with punctuation, so a full stop after a link is not captured. |
| **Phone** | Two alternatives: `(123) 456-7890`, or `123-456-7890` / `123.456.7890`. The back-reference `\1` forces the **same separator** twice. `(?<!\d)` and `(?!\d)` prevent matching part of a longer number. |
| **Credit card** | 4 groups of 4 digits. The separator is captured once (`([ -])`) and reused with `\1`, so mixed separators are rejected. |
| **Time** | The 12-hour alternative (hours `1-12`, minutes `00-59`, AM/PM) is tried **first** so `2:30 PM` is captured whole. The 24-hour alternative allows hours `0-23`. Rejects `25:70`, `14:60`, `13:45 PM` and `12:30:45`. |
| **HTML tag** | `<` or `</`, a tag name starting with a letter, zero or more attributes (double-, single- or un-quoted values), optional `/`, then `>`. An unclosed quote makes the match fail, so broken tags are skipped. |
| **Hashtag** | `#` followed by a letter, then letters/digits/underscores. A lookbehind rejects `page.html#top` and `&#39;`; the letter rule rejects `#123`. |
| **Currency** | `$` then either properly grouped thousands (`1,234`) or plain digits, with optional two-digit cents. A final lookahead rejects malformed tails such as `$1,23.456` and `$19.999`. |

All patterns use `re.VERBOSE`, so every part is commented in
[`src/patterns.py`](src/patterns.py).

## Sample Input and Output

**Input** (`data/sample_input.txt`, excerpt):

```text
Contact us: user@example.com or firstname.lastname@company.co.uk
Invalid: user@  @example.com  user@@example.com  plainaddress

Pay with 1234 5678 9012 3456 or 1234-5678-9012-3456.
Invalid: 1234 5678-9012 3456  1234 5678 9012  12345 6789 0123 4567

Prices: $19.99, $1,234.56, $5 and $1,234,567.89.
Invalid: $1,23.456  $19.999  19.99  $.99
```

**Output** (`python3 -m src.extractor`; the full result is saved in `output/sample_output.txt`):

```text
EMAILS (2 found)
  - user@example.com
  - firstname.lastname@company.co.uk

URLS (2 found)
  - https://www.example.com
  - https://subdomain.example.org/page

PHONE NUMBERS (3 found)
  - (123) 456-7890
  - 123-456-7890
  - 123.456.7890

CREDIT CARDS (2 found)
  - 1234 5678 9012 3456
  - 1234-5678-9012-3456

TIMES (4 found)
  - 14:30
  - 2:30 PM
  - 09:05
  - 11:45 am

HTML TAGS (5 found)
  - <p>
  - <div class="example">
  - <img src="image.jpg" alt="description">
  - </div>
  - <br/>

HASHTAGS (3 found)
  - #example
  - #ThisIsAHashtag
  - #python_3

CURRENCY (4 found)
  - $19.99
  - $1,234.56
  - $5
  - $1,234,567.89
```

Every "Invalid:" item in the sample file is correctly **ignored**.

## Edge Cases Handled

| Type | Rejected (correctly not matched) |
|------|----------------------------------|
| Email | `user@`, `@example.com`, `user@@example.com`, `plainaddress`, `user@example` |
| URL | `htp://broken.com`, `https://nodomain`, `www.example.com`; a trailing `.` or `)` is excluded |
| Phone | `12-3456-7890`, mixed separators `123-456.7890`, too-short numbers, digits inside longer numbers |
| Credit card | Mixed separators, only 3 groups, wrong grouping, 16 digits with no separators |
| Time | `25:70`, `14:60`, `24:00`, `13:45 PM`, `12:30:45` |
| HTML | Unclosed quote `<div class="broken>`, `< p >`, `<3`, `5 < 6 > 4`, `<>` |
| Hashtag | `#123`, lone `#`, `page.html#top`, `&#39;` |
| Currency | `$1,23.456`, `$19.999`, `19.99` (no `$`), `$.99` |

**Multiple formats** are supported for phone numbers (3), credit cards (2),
times (2) and HTML tags (opening, closing and self-closing, with or without
attributes).

## Testing

```bash
pytest -v
```

The suite contains **86 tests** covering valid inputs, invalid inputs, and an
end-to-end check of the sample file. Expected result:

```text
============================== 86 passed in 0.09s ==============================
```

## Known Limitations

Regex is powerful but it is not a full parser. These are the honest limits of
this project:

* **Credit cards** are matched by format only. No Luhn checksum is performed,
  and 16 digits with no separators are not matched (only the two required
  formats). All numbers in this repository are fake test values.
* **Phone numbers** cover North-American style formats only (no `+country` codes).
* **Emails and URLs** follow common real-world shapes, not the full RFC 5322 /
  RFC 3986 grammar. URLs without `http(s)://` are intentionally not matched.
* **HTML** is matched tag by tag. Comments, `<!DOCTYPE>`, and tags whose
  attribute values contain `<` or `>` are not supported. For real HTML parsing,
  use a parser such as Python's `html.parser`.
* **Hashtags** are ASCII only and must start with a letter.
* **Currency** supports the `$` symbol only.

## Author

**SERIEUX Elias**
African Leadership College of Hiher Education (ALCHE)
