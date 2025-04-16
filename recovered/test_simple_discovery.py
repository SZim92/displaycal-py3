"""Simple test file to verify test discovery in VSCode."""

import pytest


def test_simple_addition():
    """Simple test to check test discovery."""
    assert 1 + 1 == 2, "Basic addition should work"


def test_simple_subtraction():
    """Another simple test to check test discovery."""
    assert 5 - 3 == 2, "Basic subtraction should work"


class TestSimpleClass:
    """Test class to verify class-based test discovery."""

    def test_multiplication(self):
        """Test multiplication."""
        assert 2 * 3 == 6, "Basic multiplication should work"

    def test_division(self):
        """Test division."""
        assert 10 / 2 == 5, "Basic division should work"
