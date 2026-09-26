import re
import os

PORTAL_BUILDER = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/build_full_portal.py"

with open(PORTAL_BUILDER, 'r', encoding='utf-8') as f:
    code = f.read()

# Verify that build_full_portal.py exists and can be loaded
print("Successfully verified build_full_portal.py, size:", len(code))
