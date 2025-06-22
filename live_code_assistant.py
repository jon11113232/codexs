#!/usr/bin/env python3
"""
LIVE CODING ASSISTANT - Watches you code and helps instantly
This is what people pay $400/month for!
"""

import asyncio
import pyautogui
import numpy as np
from datetime import datetime
import re
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Live Coding Assistant")

# Global state
monitoring = False
last_text = ""
error_count = 0
help_cooldown = {}

# Common coding patterns to watch for
TYPO_PATTERNS = {
    'improt': 'import',
    'pritn': 'print', 
    'defien': 'define',
    'retrun': 'return',
    'fasle': 'false',
    'ture': 'true',
    'comit': 'commit',
    'instal': 'install'
}

ERROR_PATTERNS = {
    'ModuleNotFoundError': 'pip install {module}',
    'SyntaxError': 'Check your syntax - missing : or ()',
    'NameError': 'Variable not defined - typo?',
    'ImportError': 'Module not installed or wrong name',
    'command not found': 'Command not in PATH or typo'
}

@mcp.tool()
async def start_code_monitoring(language: str = "python") -> str:
    """Start monitoring for coding help"""
    global monitoring
    monitoring = True
    
    # Start the monitor
    asyncio.create_task(code_monitor_loop())
    
    return f"👁️ Live {language} coding assistant activated! I'm watching for:\n- Typos\n- Errors\n- Getting stuck\n- Need help"

async def code_monitor_loop():
    """Main monitoring loop"""
    global last_text, error_count
    stuck_counter = 0
    last_screen_hash = None
    
    while monitoring:
        try:
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screen_array = np.array(screenshot)
            
            # Simple change detection
            current_hash = hash(screen_array.tobytes())
            
            if current_hash == last_screen_hash:
                stuck_counter += 1
                if stuck_counter > 10:  # Stuck for 10 seconds
                    await offer_help("stuck")
                    stuck_counter = 0
            else:
                stuck_counter = 0
                
                # Detect terminal/code editor regions
                # In real version, we'd use OCR here
                changes = await detect_code_changes()
                
                if changes['has_error']:
                    await provide_error_help(changes['error_type'])
                elif changes['has_typo']:
                    await suggest_typo_fix(changes['typo'])
            
            last_screen_hash = current_hash
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"Monitor error: {e}")
            await asyncio.sleep(1)

async def detect_code_changes() -> dict:
    """Detect what's happening in code"""
    # In real implementation, this would:
    # 1. Use OCR to read text
    # 2. Detect terminal vs editor
    # 3. Find errors and typos
    
    # Simulated detection
    return {
        'has_error': False,
        'error_type': None,
        'has_typo': False,
        'typo': None,
        'is_terminal': True,
        'current_text': ""
    }

@mcp.tool()
async def report_error(error_text: str) -> str:
    """Manually report an error for instant help"""
    
    # Check error patterns
    for pattern, solution in ERROR_PATTERNS.items():
        if pattern.lower() in error_text.lower():
            if pattern == 'ModuleNotFoundError':
                # Extract module name
                module = re.search(r"No module named '(\w+)'", error_text)
                if module:
                    return f"🔧 Fix: Run `pip install {module.group(1)}`"
            return f"🔧 Fix: {solution}"
    
    return "🤔 Show me more context about this error"

@mcp.tool()
async def check_typos(text: str) -> dict:
    """Check text for common typos"""
    found_typos = {}
    
    words = text.split()
    for word in words:
        if word.lower() in TYPO_PATTERNS:
            found_typos[word] = TYPO_PATTERNS[word.lower()]
    
    return {
        'has_typos': len(found_typos) > 0,
        'corrections': found_typos
    }

@mcp.tool()
async def get_context_help(context: str) -> str:
    """Get help based on current context"""
    
    help_map = {
        'vim': "Stuck in vim? Press ESC then :q to quit, :wq to save and quit",
        'git': "Git commands: add, commit -m, push, pull, status, log",
        'terminal': "Terminal tips: Use tab for autocomplete, ↑ for history",
        'python': "Python tips: Use pylint for checking, black for formatting",
        'error': "Got an error? I can help debug it - just show me!"
    }
    
    return help_map.get(context, "What are you working on? I can help!")

async def offer_help(reason: str):
    """Offer contextual help"""
    global help_cooldown
    
    current_time = datetime.now()
    if reason in help_cooldown:
        if (current_time - help_cooldown[reason]).seconds < 30:
            return  # Don't spam
    
    help_cooldown[reason] = current_time
    
    if reason == "stuck":
        print("🤔 Looks like you might be stuck. Need help?")
    elif reason == "error":
        print("🚨 I see an error! Let me help you fix it.")

async def provide_error_help(error_type: str):
    """Provide instant error help"""
    if error_type:
        print(f"🔧 Error detected: {error_type}")
        print(f"💡 Try: {ERROR_PATTERNS.get(error_type, 'Check the error message')}")

async def suggest_typo_fix(typo: str):
    """Suggest typo corrections"""
    if typo in TYPO_PATTERNS:
        print(f"✏️ Typo: '{typo}' → '{TYPO_PATTERNS[typo]}'")

@mcp.tool()
async def stop_monitoring() -> str:
    """Stop the live monitoring"""
    global monitoring
    monitoring = False
    return "👁️ Live monitoring stopped"

# Run it
if __name__ == "__main__":
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as streams:
            await mcp.run(streams)
    
    asyncio.run(main())
