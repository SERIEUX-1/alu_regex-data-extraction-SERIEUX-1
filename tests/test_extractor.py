#!/usr/bin/env python3
"""Integration tests: run the full extractor against data/sample_input.txt."""

from pathlib import Path

from src.extractor import extract_all, extract_from_file, format_report

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "sample_input.txt"


def test_sample_file_expected_results():
    results = extract_from_file(SAMPLE)
    assert results["emails"] == ["user@example.com", "firstname.lastname@company.co.uk"]
    assert results["urls"] == ["https://www.example.com", "https://subdomain.example.org/page"]
    assert results["phone_numbers"] == ["(123) 456-7890", "123-456-7890", "123.456.7890"]
    assert results["credit_cards"] == ["1234 5678 9012 3456", "1234-5678-9012-3456"]
    assert results["times"] == ["14:30", "2:30 PM", "09:05", "11:45 am"]
    assert results["html_tags"] == [
        "<p>", '<div class="example">', '<img src="image.jpg" alt="description">',
        "</div>", "<br/>",
    ]
    assert results["hashtags"] == ["#example", "#ThisIsAHashtag", "#python_3"]
    assert results["currency"] == ["$19.99", "$1,234.56", "$5", "$1,234,567.89"]


def test_empty_text_returns_empty_lists():
    results = extract_all("")
    assert len(results) == 8
    assert all(matches == [] for matches in results.values())


def test_report_contains_counts():
    report = format_report(extract_all("user@example.com #hello"))
    assert "EMAILS (1 found)" in report
    assert "HASHTAGS (1 found)" in report
