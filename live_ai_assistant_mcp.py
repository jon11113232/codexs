#!/usr/bin/env python3
"""
LIVE AI ASSISTANT MCP - The $400/month killer
Watches your screen continuously and helps in real-time
"""

import asyncio
import numpy as np
from PIL import Image
import pyautogui
from mcp.server.fastmcp import FastMCP
import time
from datetime import datetime
import difflib

mcp = FastMCP("Live AI Assistant")

# Global state
monitoring_active = False
last_screen = None
context_history = []
error_patterns = []
last_alert_time = 0

@mcp.tool()
async def start_live_monitoring(check_interval: float = 1.0) -> str:
    """
    Start continuous screen monitoring
    Args:
        check_interval: How often to check screen (seconds)
    """
    global monitoring_active
    monitoring_active = True
    
    # Start background monitoring
    asyncio.create_task(continuous_monitor(check_interval))
    
    return f"Live monitoring started! Checking every {check_interval} seconds"

async def continuous_monitor(interval: float):
    """Background task that monitors continuously"""
    global last_screen, context_history
    
    while monitoring_active:
        try:
            # Capture current screen
            screenshot = pyautogui.screenshot()
            current_screen = np.array(screenshot)
            
            # Detect what's happening
            changes = await detect_changes(current_screen)
            
            if changes['significant']:
                # AI analyzes what user is doing
                context = await analyze_context(changes)
                
                # Proactive help based on context
                if context['needs_help']:
                    await provide_live_assistance(context)
            
            last_screen = current_screen
            await asyncio.sleep(interval)
            
        except Exception as e:
            print(f"Monitor error: {e}")
            await asyncio.sleep(interval)

async def detect_changes(current_screen) -> dict:
    """Detect what changed on screen"""
    global last_screen
    
    if last_screen is None:
        return {'significant': False, 'first_frame': True}
    
    # Calculate difference
    diff = np.abs(current_screen.astype(float) - last_screen.astype(float))
    change_amount = np.mean(diff)
    
    # Detect specific patterns
    detected = {
        'significant': change_amount > 10,
        'change_amount': float(change_amount),
        'error_dialog': False,  # Check for error patterns
        'new_window': False,    # Check for new windows
        'typing': False,        # Detect if user is typing
        'idle': change_amount < 1
    }
    
    return detected

async def analyze_context(changes: dict) -> dict:
    """AI understands what user is doing"""
    context = {
        'needs_help': False,
        'activity': 'unknown',
        'suggestions': []
    }
    
    # Smart detection patterns
    if changes.get('error_dialog'):
        context['needs_help'] = True
        context['activity'] = 'error_encountered'
        context['suggestions'].append("I see an error - let me help fix it")
    
    elif changes.get('typing') and changes['change_amount'] > 50:
        context['activity'] = 'coding'
        # Could detect syntax errors, suggest completions
    
    elif changes.get('idle'):
        context['activity'] = 'idle'
        # Could suggest next tasks
    
    return context

@mcp.tool()
async def get_live_status() -> dict:
    """Get current monitoring status and insights"""
    global monitoring_active, context_history
    
    return {
        'monitoring': monitoring_active,
        'recent_activities': context_history[-10:],
        'current_context': await analyze_current_screen()
    }

async def analyze_current_screen() -> dict:
    """Deep analysis of current screen"""
    # This is where the magic happens
    # - OCR to read text
    # - Pattern matching
    # - Context understanding
    return {
        'application': 'detected_app',
        'activity': 'what_user_doing',
        'suggestions': ['helpful_tip_1', 'helpful_tip_2']
    }

@mcp.tool()
async def set_help_patterns(patterns: list[str]) -> str:
    """
    Tell AI what to watch for
    Examples:
        - "error messages"
        - "terminal commands"
        - "code compilation"
        - "stuck on same screen"
    """
    global error_patterns
    error_patterns = patterns
    return f"Now watching for: {', '.join(patterns)}"

@mcp.tool()
async def stop_monitoring() -> str:
    """Stop live monitoring"""
    global monitoring_active
    monitoring_active = False
    return "Live monitoring stopped"

async def provide_live_assistance(context: dict):
    """Proactively help user"""
    global last_alert_time
    
    # Don't spam alerts
    current_time = time.time()
    if current_time - last_alert_time < 5:  # 5 second cooldown
        return
    
    # Smart assistance based on context
    if context['activity'] == 'error_encountered':
        # Could trigger notification
        # Or update a status file Claude watches
        print(f"🚨 HELP NEEDED: {context['suggestions'][0]}")
    
    last_alert_time = current_time

# Run the server
if __name__ == "__main__":
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as streams:
            await mcp.run(streams)
    
    asyncio.run(main())
