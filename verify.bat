@echo off
call conda run --no-capture-output -n shared_calendar python -s scripts/verify.py --mode all
