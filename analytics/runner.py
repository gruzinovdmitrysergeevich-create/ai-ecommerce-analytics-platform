#!/usr/bin/env python3
import sys
import io
import traceback

def run_code_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    allowed_globals = {
        '__name__': '__main__',
        '__file__': filepath,
        'pd': __import__('pandas'),
        'np': __import__('numpy'),
        'scipy': __import__('scipy'),
        'lifetimes': __import__('lifetimes'),
        'uncertainties': __import__('uncertainties'),
        'npf': __import__('numpy_financial'),
        'requests': __import__('requests'),
        'os': __import__('os'),
        'json': __import__('json'),
        'datetime': __import__('datetime'),
    }

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        exec(code, allowed_globals)
        stdout = sys.stdout.getvalue()
        stderr = sys.stderr.getvalue()
        return 0, stdout, stderr
    except Exception:
        stderr = traceback.format_exc()
        return 1, "", stderr
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: runner.py <script.py>")
        sys.exit(1)
    retcode, stdout, stderr = run_code_file(sys.argv[1])
    if stdout:
        print("STDOUT:")
        print(stdout)
    if stderr:
        print("STDERR:", file=sys.stderr)
        print(stderr, file=sys.stderr)
    sys.exit(retcode)
