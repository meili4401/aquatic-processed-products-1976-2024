import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
PYTHON = Path(r"C:\Users\73596\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe")
NODE = Path(r"C:\Users\73596\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")


def run(command, tolerate_exit=False):
    print("RUN:", " ".join(map(str, command)), flush=True)
    result = subprocess.run([str(x) for x in command])
    if result.returncode and not tolerate_exit:
        raise SystemExit(result.returncode)
    return result.returncode


run([PYTHON, "-B", CODE / "01_scope_and_data.py", "--output", ROOT])
run([PYTHON, "-B", CODE / "analysis_engine.py", "--output", ROOT])
run([PYTHON, "-B", CODE / "03_publication_data.py", "--output", ROOT])
# On the bundled Windows runtime artifact-tool can exit after every requested XLSX
# and preview has already been saved. The next independent validator is authoritative.
run([NODE, CODE / "04_workbooks.mjs", ROOT], tolerate_exit=True)
run([PYTHON, "-B", CODE / "04b_validate_workbooks.py"])
run([PYTHON, "-B", CODE / "05_figures.py", "--output", ROOT])
run([PYTHON, "-B", CODE / "06_reports.py", "--output", ROOT])
run([PYTHON, "-B", CODE / "08_verify_source_rebuild.py"])
run([PYTHON, "-B", CODE / "09_validate_pdf_renders.py"])
run([PYTHON, "-B", CODE / "confirm_visual_qc.py"])
run([PYTHON, "-B", CODE / "07_validate.py"])
run([PYTHON, "-B", CODE / "10_finalize_package.py"])
print("Stage 4.1 rebuild and validation complete: PASS")
