#!/bin/bash
# LIVE AI ASSISTANT - One-Click Installer
# The $400/month alternative - FREE!

echo "🚀 LIVE AI ASSISTANT INSTALLER"
echo "=============================="
echo "💰 Market price: $400/month"
echo "💻 Our price: FREE (local)"
echo "=============================="
echo

# Check if in codexs directory
if [ ! -f "live_assistant_mcp_server.py" ]; then
    echo "❌ Please run this from the codexs directory!"
    exit 1
fi

# Check Python
echo "✓ Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found! Please install it first."
    exit 1
fi

# Create/activate virtual environment
echo "✓ Setting up environment..."
if [ ! -d "mcp_env" ]; then
    python3 -m venv mcp_env
fi
source mcp_env/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install pyautogui pillow numpy mcp

# Check for tesseract
echo "✓ Checking OCR engine..."
if ! command -v tesseract &> /dev/null; then
    echo "📦 Installing tesseract..."
    if command -v brew &> /dev/null; then
        brew install tesseract
    else
        echo "⚠️  Please install tesseract manually for OCR support"
    fi
fi

# Create launcher script
echo "✓ Creating launcher..."
cat > start_live_assistant.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source mcp_env/bin/activate
echo "🚀 Starting Live AI Assistant..."
echo "This replaces $400/month services!"
python live_assistant_demo.py
EOF
chmod +x start_live_assistant.sh

# Update Claude config
echo "✓ Configuring Claude..."
CONFIG_DIR="$HOME/Library/Application Support/Claude"
mkdir -p "$CONFIG_DIR"

# Backup existing config
if [ -f "$CONFIG_DIR/claude_desktop_config.json" ]; then
    cp "$CONFIG_DIR/claude_desktop_config.json" "$CONFIG_DIR/claude_desktop_config.backup.json"
fi

# Create new config
cat > "$CONFIG_DIR/claude_desktop_config.json" << EOF
{
  "mcpServers": {
    "live-assistant": {
      "command": "$PWD/mcp_env/bin/python",
      "args": ["$PWD/live_assistant_mcp_server.py"]
    },
    "computer-control": {
      "command": "$PWD/mcp_env/bin/python",
      "args": ["-m", "computer_control_mcp"]
    }
  }
}
EOF

echo
echo "✅ INSTALLATION COMPLETE!"
echo
echo "🎯 TO START:"
echo "   ./start_live_assistant.sh"
echo
echo "🤖 IN CLAUDE:"
echo "   Use the 'live-assistant' tools"
echo
echo "💡 FEATURES:"
echo "   - Watches for errors before you see them"
echo "   - Detects typos as you type"
echo "   - Identifies frustration patterns"
echo "   - Suggests help proactively"
echo "   - All running locally!"
echo
echo "💰 You just saved $400/month!"
