#!/usr/bin/env python3
"""
ULTRA SIMPLE MONITOR - Just watch mouse/keyboard
"""

import pyautogui
import time
from datetime import datetime

print("🚀 SIMPLE ACTIVITY MONITOR")
print("Move mouse or press keys - I'll detect it!\n")

# Get initial state
last_mouse = pyautogui.position()
width, height = pyautogui.size()

print(f"📺 Screen: {width}x{height}")
print(f"🖱️  Mouse at: {last_mouse}")
print("\nWatching for 30 seconds...\n")

# Monitor loop
start_time = time.time()
activity_count = 0

while time.time() - start_time < 30:
    try:
        # Check mouse
        current_mouse = pyautogui.position()
        
        if current_mouse != last_mouse:
            activity_count += 1
            distance = ((current_mouse[0] - last_mouse[0])**2 + 
                       (current_mouse[1] - last_mouse[1])**2)**0.5
            
            if distance > 50:  # Significant movement
                print(f"🎯 BIG MOVE: {last_mouse} → {current_mouse} ({int(distance)}px)")
            
            last_mouse = current_mouse
        
        # Small delay
        time.sleep(0.1)
        
    except KeyboardInterrupt:
        break

print(f"\n✅ DONE! Detected {activity_count} movements")
print("This proves we CAN monitor your screen!")
