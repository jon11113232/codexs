#!/bin/bash
# EMERGENCY: Convert to private advantage

echo "🔒 CONVERTING TO PRIVATE ADVANTAGE..."
echo

# Create private version
echo "📁 Creating private fork..."
mkdir -p ~/private_codexs
cp -r *.py ~/private_codexs/
cp -r mcp_env ~/private_codexs/

# Remove sensitive files from public
echo "🗑️ Removing the good stuff from public..."
rm -f live_assistant_mcp_server.py
rm -f advanced_live_assistant.py
rm -f ultimate_live_ai.py

# Create decoy files
echo "🎭 Creating decoy versions..."

cat > live_assistant_mcp_server.py << 'EOF'
# This is a placeholder
# The real magic is in the private version
print("Basic monitoring only - contact for premium version")
EOF

cat > README.md << 'EOF'
# codexs - AI Assistant Framework

Basic monitoring tools for development.

For advanced features, contact directly.

## Features
- Basic mouse tracking
- Simple pattern detection

Premium version includes:
- Advanced AI
- Predictive features  
- $1000/month value

Contact for access.
EOF

echo "✅ Public version nerfed!"
echo "🔐 Private version saved to ~/private_codexs"
echo
echo "NEXT STEPS:"
echo "1. Push these changes to make repo look basic"
echo "2. Keep the real version private"
echo "3. Maybe sell access for $100/month?"
