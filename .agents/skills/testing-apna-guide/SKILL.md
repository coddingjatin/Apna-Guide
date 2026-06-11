---
name: testing-apna-guide
description: Test the Apna Guide TSP solver app end-to-end. Use when verifying GUI, error handling, or path computation changes.
---

# Testing Apna Guide

## Environment Setup

The app is a Tkinter GUI application. The pyenv Python may not have `_tkinter` compiled in. Use system Python instead:

```bash
# System Python has tkinter support
/usr/bin/python3 -m pip install --user networkx matplotlib Pillow
```

If `apt-get install python3-tk` fails, run `sudo apt-get update` first.

## Running the App

```bash
cd /path/to/Apna-Guide
/usr/bin/python3 AGTSP.py
```

Requires a display (`:0` on Linux). The app opens a 600x400 window.

## Key Test Scenarios

### Input Validation
- **Empty input + Show Path**: Should show "Please enter a city name."
- **Empty input + Guide**: Should show "Please enter a destination city."
- **Invalid city (e.g. "London")**: Should show "Invalid city! Choose from: Mumbai, Pune, Thane, Delhi"
- Valid cities: `Mumbai`, `Pune`, `Thane`, `Delhi`

### Happy Path
- Type "Pune" → Click "Show Path" → Graph window opens showing `Mumbai → Thane → Pune | Distance: 105 km`
- Type "Delhi" → Click "Show Path" → Shows path through the graph

### Error Propagation
- **Missing `fl.jpg`**: Rename/remove it, launch app → messagebox "Missing Resource" with full file path, then clean exit
- **Dead-end in TSP path**: Would raise ValueError (hard to trigger with current graph since it's fully connected)

## Tips
- The messagebox for missing image may appear BEHIND the main window. Use Alt+Tab to find it.
- Repeated "Show Path" clicks may accumulate matplotlib state (known minor issue). Each click opens a new graph window.
- The app window is 600x400, so long error messages may be truncated in the label. This is cosmetic, not a bug.

## Devin Secrets Needed
None required for testing this app.
