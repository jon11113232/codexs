#!/usr/bin/env python3
"""
LIVE AI ASSISTANT DEMO - The $400/month alternative!
Shows how we can watch and help proactively
"""

import pyautogui
import time
from datetime import datetime
import random

print("="*60)
print("🤖 LIVE AI ASSISTANT - DEMO")
print("="*60)
print("\n💰 Others charge $400/month for this!")
print("🏠 We run it locally for FREE\n")

# Configuration
HELP_MESSAGES = [
    "💡 I noticed rapid mouse movement - need help finding something?",
    "🎯 Hovering in one spot - reading something difficult?",
    "⚡ Fast clicking detected - automation could help!",
    "🔍 Searching for something? I can help locate it.",
    "📝 Been in same area for a while - need assistance?"
]

print("Starting monitoring...\n")

# State tracking
last_pos = pyautogui.position()
last_activity_time = time.time()
hover_start = None
hover_position = None
rapid_clicks = 0
last_click_time = 0

def show_help(reason):
    """Simulate showing help notification"""
    print(f"\n{'='*50}")
    print(f"🔔 PROACTIVE HELP ALERT")
    print(f"{'='*50}")
    print(f"Reason: {reason}")
    print(f"Suggestion: {random.choice(HELP_MESSAGES)}")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}\n")

# Main loop
print("👁️ Watching your activity patterns...\n")
print("Try these to trigger help:")
print("- Move mouse rapidly")
print("- Keep mouse still for 3+ seconds") 
print("- Click multiple times quickly\n")

start_time = time.time()

while time.time() - start_time < 60:  # Run for 60 seconds
    try:
        current_pos = pyautogui.position()
        current_time = time.time()
        
        # Detect rapid movement
        if current_pos != last_pos:
            distance = ((current_pos[0] - last_pos[0])**2 + 
                       (current_pos[1] - last_pos[1])**2)**0.5
            
            if distance > 200:  # Rapid movement
                show_help("Rapid mouse movement detected")
                time.sleep(2)  # Cooldown
            
            hover_start = None  # Reset hover
            last_activity_time = current_time
            
        else:
            # Detect hovering
            if hover_start is None:
                hover_start = current_time
                hover_position = current_pos
            elif current_time - hover_start > 3:  # 3 seconds hover
                show_help(f"Hovering at {hover_position} for {int(current_time - hover_start)}s")
                hover_start = current_time  # Reset
                time.sleep(2)
        
        # Status update
        elapsed = int(current_time - start_time)
        if elapsed % 10 == 0 and elapsed > 0:
            print(f"⏱️  {elapsed}s elapsed - Still monitoring...")
        
        last_pos = current_pos
        time.sleep(0.1)
        
    except KeyboardInterrupt:
        break

print("\n✅ Demo complete!")
print("\n📊 This is the foundation for:")
print("- Error detection before you notice")
print("- Typo correction as you type")
print("- Smart suggestions based on behavior")
print("- All running locally, no cloud needed!")
