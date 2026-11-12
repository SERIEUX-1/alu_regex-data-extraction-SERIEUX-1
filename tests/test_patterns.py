#!/usr/bin/env python3
"""
Unit tests for every regex in src/patterns.py.

For each data type we test:
  * VALID inputs   - must match completely (fullmatch)
  * INVALID inputs - must produce no match at all (edge cases / malformed data)

Run with:  pytest -v
"""

import pytest

from src.patterns import (
    CREDIT_CARD, CURRENCY, EMAIL, HASHTAG, HTML_TAG, PHONE, TIME, URL,
)


def find_all(pattern, text):
    """Return every full match of ``pattern`` found in ``text``."""
    return [m.group(0) for m in pattern.finditer(text)]


# --------------------------------------------------------------------------- #
# Emails
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text", [
    "user@example.com",
    "firstname.lastname@company.co.uk",
    "first_last+tag@sub.domain.org",
])
def test_email_valid(text):
    assert EMAIL.fullmatch(text)


@pytest.mark.parametrize("text", [
    "user@", "@example.com", "user@@example.com",
    "plainaddress", "user@example", "user@example.c",
])
def test_email_invalid(text):
    assert find_all(EMAIL, text) == []


def test_email_in_sentence_excludes_trailing_period():
    assert find_all(EMAIL, "Write to user@example.com.") == ["user@example.com"]


# --------------------------------------------------------------------------- #
# URLs
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text", [
    "https://www.example.com",
    "https://subdomain.example.org/page",
    "http://example.com:8080/a/b?x=1&y=2",
])
def test_url_valid(text):
    assert URL.fullmatch(text)


@pytest.mark.parametrize("text", [
    "htp://broken.com", "https://nodomain", "www.example.com", "ftp://example.com",
])
def test_url_invalid(text):
    assert find_all(URL, text) == []


def test_url_excludes_trailing_punctuation():
    assert find_all(URL, "See https://subdomain.example.org/page.") == [
        "https://subdomain.example.org/page"]
    assert find_all(URL, "(https://www.example.com/a)") == ["https://www.example.com/a"]


# --------------------------------------------------------------------------- #
# Phone numbers
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text", [
    "(123) 456-7890", "(123)456-7890", "123-456-7890", "123.456.7890",
])
def test_phone_valid(text):
    assert PHONE.fullmatch(text)


@pytest.mark.parametrize("text", [
    "12-3456-7890", "123-456.7890", "1234567", "123-45-67890", "(12) 456-7890",
])
def test_phone_invalid(text):
    assert find_all(PHONE, text) == []


def test_phone_not_matched_inside_longer_number():
    assert find_all(PHONE, "9123-456-78901") == []


# --------------------------------------------------------------------------- #
# Credit cards
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text", ["1234 5678 9012 3456", "1234-5678-9012-3456"])
def test_card_valid(text):
    assert CREDIT_CARD.fullmatch(text)


@pytest.mark.parametrize("text", [
    "1234 5678-9012 3456",        # mixed separators
    "1234 5678 9012",             # too short
    "12345 6789 0123 4567",       # wrong grouping
    "1234567890123456",           # no separators
])
def test_card_invalid(text):
    assert find_all(CREDIT_CARD, text) == []


# --------------------------------------------------------------------------- #
# Time
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text", [
    "14:30", "2:30 PM", "09:05", "11:45 am", "12:00 PM", "0:00", "23:59",
])
def test_time_valid(text):
    assert TIME.fullmatch(text)


@pytest.mark.parametrize("text", ["25:70", "14:60", "13:45 PM", "12:30:45", "24:00"])
def test_time_invalid(text):
    assert find_all(TIME, text) == []


def test_time_12h_captured_whole():
    assert find_all(TIME, "at 2:30 PM sharp") == ["2:30 PM"]


# --------------------------------------------------------------------------- #
# HTML tags
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text", [
    "<p>", "</p>", '<div class="example">', "<br/>", "<br />",
    '<img src="image.jpg" alt="description">',
    "<input disabled>", "<a href='x.html'>",
])
def test_html_valid(text):
    assert HTML_TAG.fullmatch(text)


@pytest.mark.parametrize("text", ['<div class="broken>', "< p >", "<3", "5 < 6 > 4", "<>"])
def test_html_invalid(text):
    assert find_all(HTML_TAG, text) == []


def test_html_multiple_tags_in_one_line():
    text = '<p>Hi</p><img src="a.png">'
    assert find_all(HTML_TAG, text) == ["<p>", "</p>", '<img src="a.png">']


# --------------------------------------------------------------------------- #
# Hashtags
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text", ["#example", "#ThisIsAHashtag", "#python_3"])
def test_hashtag_valid(text):
    assert HASHTAG.fullmatch(text)


@pytest.mark.parametrize("text", ["#123", "#", "page.html#top", "&#39;", "# space"])
def test_hashtag_invalid(text):
    assert find_all(HASHTAG, text) == []


def test_hashtag_multiple():
    assert find_all(HASHTAG, "Love #python and #Regex!") == ["#python", "#Regex"]


# --------------------------------------------------------------------------- #
# Currency
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text", [
    "$19.99", "$1,234.56", "$5", "$1,234,567.89", "$0.99", "$1234.50",
])
def test_currency_valid(text):
    assert CURRENCY.fullmatch(text)


@pytest.mark.parametrize("text", ["$1,23.456", "$19.999", "19.99", "$.99", "$", "$1,23"])
def test_currency_invalid(text):
    assert find_all(CURRENCY, text) == []


def test_currency_excludes_sentence_period():
    assert find_all(CURRENCY, "It costs $19.99.") == ["$19.99"]
