#!/usr/bin/env bash
set -e

echo "🔧 Installing Computer Control MCP Server..."
echo ""

# Check for Python 3.12
if ! command -v python3.12 &> /dev/null; then
    echo "📦 Python 3.12 not found. Installing..."
    brew install python@3.12
fi

ENV_DIR="mcp_env"

# Remove old environment if it exists
rm -rf "$ENV_DIR"

# Create virtual environment with Python 3.12
python3.12 -m venv "$ENV_DIR"
source "$ENV_DIR/bin/activate"

pip install --upgrade pip

# Install MCP server - let pip resolve compatible versions
echo "📦 Installing computer-control-mcp..."
pip install computer-control-mcp

# Test the imports
echo ""
echo "🧪 Testing imports..."
python - <<'PY'
try:
    import computer_control_mcp
    print('✅ computer_control_mcp imported successfully!')
    
    # Try various RapidOCR imports
    try:
        from rapidocr_paddle import VisRes
        print('✅ rapidocr_paddle.VisRes imported successfully!')
    except ImportError:
        try:
            import rapidocr_paddle
            print(f'⚠️ rapidocr_paddle module loaded but VisRes not found')
            print(f'   Available: {[x for x in dir(rapidocr_paddle) if not x.startswith("_")]}')
        except:
            print('❌ rapidocr_paddle not available')
    
    try:
        import rapidocr_onnxruntime
        print('✅ rapidocr_onnxruntime imported successfully!')
    except:
        print('❌ rapidocr_onnxruntime not available')
        
except Exception as e:
    print(f'❌ Error: {e}')
PY

echo ""
echo "📌 Installation complete!"
echo "🔧 To activate: source $ENV_DIR/bin/activate"
echo "🚀 To run: computer-control-mcp"
echo ""
echo "📊 Installed packages:"
pip list | grep -E "(computer-control|rapidocr|onnx)"
