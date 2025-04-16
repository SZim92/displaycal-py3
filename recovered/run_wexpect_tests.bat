@echo off
echo Running wexpect tests...
python -m pytest tests/test_wexpect_imports.py tests/test_wexpect_conpty.py::test_wexpect_searcher_string tests/test_wexpect_conpty.py::test_wexpect_searcher_re tests/test_simple_discovery.py -v
echo.
echo Test run complete.
