#!/usr/bin/env python3
"""
SIMPLE LIVE MONITOR TEST - Fixed image handling
"""

import time
import pyautogui
import pytesseract
from PIL import Image
from datetime import datetime
import io

print("🚀 LIVE MONITOR STARTING...")
print("Press Ctrl+C to stop\n")

# Test OCR first
try:
    # Take screenshot as PIL Image (not bytes)
    screenshot = pyautogui.screenshot()
    
    # OCR directly on PIL Image
    text = pytesseract.image_to_string(screenshot)
    print("✅ OCR WORKING!")
    print(f"Screen has {len(text)} characters")
    print(f"First 100 chars: {text[:100].strip()}\n")
except Exception as e:
    print(f"❌ OCR ERROR: {e}")
    exit(1)

# Main monitoring loop
last_text = ""
error_count = 0
typo_count = 0
check_count = 0

print("Starting continuous monitoring...\n")

while True:
    try:
        check_count += 1
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        
        # Extract text
        current_text = pytesseract.image_to_string(screenshot)
        
        # Check for changes
        if current_text != last_text:
            # Look for common errors
            if "error" in current_text.lower():
                error_count += 1
                print(f"🔴 ERROR DETECTED! (#{error_count})")
                print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
                
            # Look for typos
            typos_found = []
            typo_map = {
                'improt': 'import',
                'pritn': 'print',
                'retrun': 'return',
                'fasle': 'false',
                'defien': 'define',
                'comit': 'commit'
            }
            
            for typo, correct in typo_map.items():
                if typo in current_text:
                    typos_found.append(f"{typo} → {correct}")
                    typo_count += 1
            
            if typos_found:
                print(f"✏️  TYPOS FOUND: {', '.join(typos_found)}")
            
            last_text = current_text
        
        # Status update every 10 checks
        if check_count % 10 == 0:
            print(f"👁️  Still watching... (Checks: {check_count}, Errors: {error_count}, Typos: {typo_count})")
        
        time.sleep(1)  # Check once per second
        
    except KeyboardInterrupt:
        print(f"\n\n✅ MONITOR STOPPED")
        print(f"📊 Final Stats:")
        print(f"   - Total checks: {check_count}")
        print(f"   - Errors found: {error_count}")
        print(f"   - Typos found: {typo_count}")
        break
    except Exception as e:
        print(f"Warning: {e}")
        time.sleep(2)
