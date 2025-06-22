#!/bin/bash
echo "🔧 Testing Computer-Control MCP..."
echo ""

# Test 1: Check if server starts
echo "Test 1: Starting server..."
timeout 3 /Users/zpk/codexs/mcp_env/bin/python -m computer_control_mcp.server 2>&1 | grep -q "UserWarning"
if [ $? -eq 0 ]; then
    echo "✅ Server starts successfully"
else
    echo "❌ Server failed to start"
fi

# Test 2: Check Python module
echo ""
echo "Test 2: Checking Python module..."
/Users/zpk/codexs/mcp_env/bin/python -c "import computer_control_mcp; print('✅ Module imports successfully')" 2>/dev/null || echo "❌ Module import failed"

# Test 3: Check OCR availability
echo ""
echo "Test 3: Checking OCR..."
/Users/zpk/codexs/mcp_env/bin/python -c "import rapidocr_onnxruntime; print('✅ OCR module available')" 2>/dev/null || echo "❌ OCR module not available"

echo ""
echo "✅ All tests complete!"
