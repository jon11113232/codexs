#!/usr/bin/env python3
"""
Motion Detection MCP - Works without video permissions!
Uses rapid screenshots instead of video stream
"""

import asyncio
import numpy as np
from PIL import Image
import pyautogui
from mcp.server.fastmcp import FastMCP
import time

mcp = FastMCP("Motion Detection MCP")

# Store previous frame
previous_frame = None
motion_threshold = 30  # Adjust sensitivity

@mcp.tool()
async def start_motion_detection(sensitivity: int = 30) -> str:
    """Start detecting motion using screenshots"""
    global motion_threshold
    motion_threshold = sensitivity
    return f"Motion detection started with sensitivity {sensitivity}"

@mcp.tool()
async def check_for_motion() -> dict:
    """Check if motion detected between frames"""
    global previous_frame
    
    # Take screenshot
    current = pyautogui.screenshot()
    current_array = np.array(current)
    
    if previous_frame is None:
        previous_frame = current_array
        return {"motion": False, "first_frame": True}
    
    # Calculate difference
    diff = np.abs(current_array - previous_frame)
    motion_amount = np.mean(diff)
    
    # Update previous frame
    previous_frame = current_array
    
    motion_detected = motion_amount > motion_threshold
    
    return {
        "motion": motion_detected,
        "amount": float(motion_amount),
        "threshold": motion_threshold
    }

@mcp.tool()
async def monitor_area(x: int, y: int, width: int, height: int, seconds: int = 10) -> list:
    """Monitor specific area for motion"""
    events = []
    start_time = time.time()
    
    while time.time() - start_time < seconds:
        # Take screenshot of specific area
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        
        # Check for changes
        # Add logic here
        
        await asyncio.sleep(0.5)  # Check twice per second
    
    return events

# Run it
if __name__ == "__main__":
    import sys
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as streams:
            await mcp.run(streams)
    
    asyncio.run(main())
