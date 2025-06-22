#!/usr/bin/env python3
"""
BASIC MONITOR - Free Demo Version
For advanced features, contact for premium access
"""

import pyautogui
import time

print("🐭 Basic Activity Monitor (Free Version)")
print("="*40)
print("This is the limited demo.")
print("Premium version includes:")
print("- AI error detection")
print("- Predictive assistance")
print("- Workflow automation")
print("- $1000/month value for $99/month")
print("="*40)

# Just basic tracking
while True:
    pos = pyautogui.position()
    print(f"Mouse at: {pos}")
    time.sleep(5)
