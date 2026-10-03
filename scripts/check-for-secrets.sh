#!/usr/bin/env bash
set -euo pipefail

# Heuristic pre-commit check. Review findings manually.
grep -RInE --exclude-dir=.git --exclude='*.example' '(PRIVATE_KEY|API_KEY|PASSWORD|TOKEN|SECRET|Authorization:|oauth|cookie)' . || true
