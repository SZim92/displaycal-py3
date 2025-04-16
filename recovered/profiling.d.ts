import json
import os
import sys
import tempfile
from contextlib import contextmanager
from os.path import abspath
from os.path import join as pjoin
from subprocess import STDOUT, check_call, check_output

from ._in_process import _in_proc_script_path


def write_json(obj, path, **kwargs):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, **kwargs)


def read_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


class BackendUnavailable(Exception):
    """Will be raised if the backend cannot be imported in the hook process."""
    def __init__(self, traceback):
        self.traceback = traceback


class BackendInvalid(Exception):
    """Will be raised if the backend is invalid."""
    def __init__(self, backend_name, backend_path, message):
        super().__init__(message)
        self.backend_name = backend_name
        self.backend_path = backend_path


class HookMissing(Exception):
    """Will be raised on missing hooks (if a fallback can't be used)."""
    def __init__(self, hook_name):
        super().__init__(hook_name)
        self.hook_name = hook_name


class UnsupportedOperation(Exception):
    """May be raised by build_sdist if the backend indicates that it can't."""
    def __init__(self, traceback):
        self.traceback = traceback


def default_subprocess_runner(cmd, cwd=None, extra_environ=None):
    """The default method of calling the wrapper subprocess.

    This uses :func:`subprocess.check_call` under the hood.
    """
    env = os.environ.copy()
    if extra_environ:
        env.update(extra_environ)

    check_call(cmd, cwd=cwd, env=env)


def quiet_subprocess_runner(cmd, cwd=None, extra_environ=None):
    """Call the subprocess while suppressing output.

    This uses :func:`subprocess.check_output` under the hood.
    """
    env = os.environ.copy()
    if extra_environ:
        env.update(extra_environ)

    check_output(cmd, cwd=cwd, env=env, stderr=STDOUT)


def norm_and_check(source_tree, requested):
    """Nor