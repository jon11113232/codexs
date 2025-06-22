#!/usr/bin/env python3
"""
TEST COMPUTER CONTROL MCP - Direct usage
"""

import time
from datetime import datetime

# Test basic functionality
print("🚀 TESTING COMPUTER-CONTROL MCP...")
print("This will take a screenshot and show what's on screen\n")

try:
    # Import the installed computer-control
    from computer_control_mcp import server
    
    print("✅ Computer-control MCP imported successfully!")
    
    # Try to get screen size
    print("\n📏 Getting screen size...")
    # Note: We'll need to use it through MCP server
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nTrying direct pyautogui test instead...")
    
    import pyautogui
    
    # Get screen size
    width, height = pyautogui.size()
    print(f"✅ Screen size: {width}x{height}")
    
    # Get mouse position
    x, y = pyautogui.position()
    print(f"✅ Mouse at: ({x}, {y})")
    
    print("\n🔍 Monitoring for 10 seconds...")
    print("Move your mouse or type to see detection!\n")
    
    last_pos = (x, y)
    for i in range(10):
        current_pos = pyautogui.position()
        
        if current_pos != last_pos:
            print(f"🖱️  Mouse moved to: {current_pos}")
            last_pos = current_pos
        
        time.sleep(1)
        
    print("\n✅ Test complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
