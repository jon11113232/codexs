#!/usr/bin/env python3
"""
OCR LIVE MONITOR - Real-time text detection!
"""

import pyautogui
import pytesseract
from PIL import Image
import time
import numpy as np
from datetime import datetime

print("🔥 OCR LIVE MONITOR - WATCHING YOUR SCREEN")
print("="*50)

# Fix for OCR
pyautogui.screenshot().save('/tmp/test_screen.png')
test_img = Image.open('/tmp/test_screen.png')
test_text = pytesseract.image_to_string(test_img)
print(f"✅ OCR TEST: Found {len(test_text)} chars on screen\n")

# Error patterns to catch
ERROR_PATTERNS = [
    'error', 'failed', 'exception', 'warning', 
    'undefined', 'null', 'cannot', 'invalid'
]

# Code typos to fix
TYPO_FIX = {
    'improt': 'import',
    'pritn': 'print',
    'retrun': 'return',
    'fasle': 'false',
    'ture': 'true',
    'fucntion': 'function',
    'cosnt': 'const',
    'lgo': 'log'
}

print("🎯 WATCHING FOR:")
print("- Errors before you see them")
print("- Typos as you type")
print("- Problems in real-time\n")

last_screen_text = ""
error_count = 0
typo_count = 0
check_count = 0

while True:
    try:
        # Screenshot region (faster than full screen)
        # Focus on center where coding happens
        width, height = pyautogui.size()
        region = (width//4, height//4, width//2, height//2)
        
        # Capture and OCR
        screenshot = pyautogui.screenshot(region=region)
        current_text = pytesseract.image_to_string(screenshot)
        
        if current_text != last_screen_text:
            # Check for new errors
            for error in ERROR_PATTERNS:
                if error in current_text.lower() and error not in last_screen_text.lower():
                    error_count += 1
                    print(f"\n🚨 ERROR DETECTED: '{error}' found!")
                    print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
                    print(f"   Total errors: {error_count}")
            
            # Check for typos
            for typo, correct in TYPO_FIX.items():
                if typo in current_text and typo not in last_screen_text:
                    typo_count += 1
                    print(f"\n✏️  TYPO ALERT: '{typo}' → '{correct}'")
                    print(f"   Fix it quickly!")
            
            last_screen_text = current_text
        
        check_count += 1
        if check_count % 20 == 0:
            print(f"👁️  Scan #{check_count} - Errors: {error_count}, Typos: {typo_count}")
        
        time.sleep(0.5)  # 2 checks per second
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Minor issue: {e}")
        time.sleep(1)

print(f"\n📊 FINAL STATS:")
print(f"- Scans: {check_count}")
print(f"- Errors caught: {error_count}")
print(f"- Typos found: {typo_count}")
