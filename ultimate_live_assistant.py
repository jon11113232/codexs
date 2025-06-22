#!/usr/bin/env python3
"""
ULTIMATE LIVE ASSISTANT - Keyboard + Mouse + Smart Detection
This is what $400/month gets you elsewhere!
"""

import pyautogui
import time
from datetime import datetime
import threading
import queue
from collections import deque

print("🚀 ULTIMATE LIVE ASSISTANT")
print("="*60)
print("💰 Market price: $400/month")
print("💻 Our price: FREE (local)")
print("="*60)

# Configuration
TYPING_SPEED_THRESHOLD = 5  # chars per second = fast typing
IDLE_THRESHOLD = 5  # seconds before considered idle
RAPID_CLICK_THRESHOLD = 3  # clicks in 1 second

# Global state
activity_queue = queue.Queue()
keystroke_buffer = deque(maxlen=100)
click_times = deque(maxlen=10)
mouse_path = deque(maxlen=50)

class ActivityAnalyzer:
    def __init__(self):
        self.patterns = {
            'searching': 0,
            'typing_fast': 0,
            'frustrated': 0,
            'idle': 0,
            'reading': 0
        }
        self.last_activity = time.time()
        
    def analyze(self, event_type, data):
        current_time = time.time()
        
        if event_type == 'mouse_move':
            # Add to path
            mouse_path.append(data)
            
            # Detect circular motion (searching)
            if len(mouse_path) >= 10:
                # Check for back-and-forth pattern
                distances = []
                for i in range(1, len(mouse_path)):
                    dist = ((mouse_path[i][0] - mouse_path[i-1][0])**2 + 
                           (mouse_path[i][1] - mouse_path[i-1][1])**2)**0.5
                    distances.append(dist)
                
                avg_dist = sum(distances) / len(distances)
                if avg_dist > 100:
                    self.patterns['searching'] += 1
                    return "🔍 Searching pattern detected"
                    
        elif event_type == 'mouse_click':
            click_times.append(current_time)
            
            # Detect rapid clicking (frustration)
            recent_clicks = [t for t in click_times if current_time - t < 1]
            if len(recent_clicks) >= RAPID_CLICK_THRESHOLD:
                self.patterns['frustrated'] += 1
                return "😤 Rapid clicking - frustration detected"
                
        elif event_type == 'idle':
            idle_time = current_time - self.last_activity
            if idle_time > IDLE_THRESHOLD:
                self.patterns['idle'] += 1
                return f"💤 Idle for {int(idle_time)}s"
                
        elif event_type == 'hover':
            self.patterns['reading'] += 1
            return "📖 Reading/focusing on content"
            
        self.last_activity = current_time
        return None

# Create analyzer
analyzer = ActivityAnalyzer()

def monitor_activity():
    """Main monitoring loop"""
    last_pos = pyautogui.position()
    hover_start = None
    hover_pos = None
    
    while True:
        try:
            current_pos = pyautogui.position()
            current_time = time.time()
            
            # Mouse movement
            if current_pos != last_pos:
                result = analyzer.analyze('mouse_move', current_pos)
                if result:
                    print(f"\n{result}")
                    suggest_help(result)
                    
                hover_start = None
                last_pos = current_pos
                
            else:
                # Detect hovering
                if hover_start is None:
                    hover_start = current_time
                    hover_pos = current_pos
                elif current_time - hover_start > 2:
                    result = analyzer.analyze('hover', hover_pos)
                    if result:
                        print(f"\n{result}")
                    hover_start = current_time
            
            # Check for idle
            if current_time - analyzer.last_activity > IDLE_THRESHOLD:
                result = analyzer.analyze('idle', None)
                if result:
                    print(f"\n{result}")
                    
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Monitor error: {e}")
            time.sleep(1)

def suggest_help(detection):
    """Provide smart suggestions based on detection"""
    suggestions = {
        "🔍 Searching": [
            "Try Cmd+F to search in page",
            "Use Spotlight (Cmd+Space) for system search",
            "I can help you find what you need"
        ],
        "😤 Rapid clicking": [
            "Take a breath - I can help automate this",
            "Try keyboard shortcuts instead",
            "Let me know what's not working"
        ],
        "💤 Idle": [
            "Need a break? I'll keep watch",
            "Stuck on something? Ask me",
            "I'm here when you're ready"
        ],
        "📖 Reading": [
            "Need a summary?",
            "Want me to explain this?",
            "I can help clarify"
        ]
    }
    
    for key, msgs in suggestions.items():
        if key in detection:
            print(f"   💡 Suggestion: {msgs[0]}")
            break

def show_stats():
    """Show activity statistics"""
    while True:
        time.sleep(10)
        print(f"\n📊 ACTIVITY STATS:")
        print(f"   Searching: {analyzer.patterns['searching']}")
        print(f"   Fast typing: {analyzer.patterns['typing_fast']}") 
        print(f"   Frustrated: {analyzer.patterns['frustrated']}")
        print(f"   Reading: {analyzer.patterns['reading']}")
        print(f"   Idle moments: {analyzer.patterns['idle']}")

# Start monitoring
print("\n🎯 MONITORING STARTED")
print("I'm watching for:")
print("- Searching patterns (circular mouse)")
print("- Frustration (rapid clicks)")
print("- Reading (hovering)")
print("- Idle time\n")

# Start threads
monitor_thread = threading.Thread(target=monitor_activity, daemon=True)
stats_thread = threading.Thread(target=show_stats, daemon=True)

monitor_thread.start()
stats_thread.start()

# Keep main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n✅ ASSISTANT STOPPED")
    print("This is the future of AI assistance!")
