# ChatGPT MCP Connector - URGENT TASK ASSIGNMENT

## TASK FOR CHATGPTCODER
User has assigned you to implement the working ChatGPT MCP connector. The kupn repo has a working implementation that needs to be adapted for the codexs repo.

## CRITICAL ISSUE IDENTIFIED - SSE TUNNEL PROBLEM
**Current Status:** ChatGPT shows "Error creating connector" due to SSE streaming failure through cloudflared tunnel.

**Root Cause Analysis:**
- ✅ SSE endpoint works locally: `curl -N http://localhost:8765/sse` streams events properly
- ❌ SSE endpoint hangs via tunnel: `curl -N https://farmer-thriller-reproduction-cure.trycloudflare.com/sse` times out
- ✅ JSON-RPC endpoints work via tunnel: initialize/tools methods respond correctly
- ❌ ChatGPT validation fails because SSE handshake never completes

**The Fix:** SSE streaming through cloudflared tunnel needs buffering/connection handling fixes.

## WORKING IMPLEMENTATION AVAILABLE
Copy the complete working implementation from `/home/ubuntu/repos/kupn/chatgpt_mac_mcp_server.py` - this file contains:
- ✅ Proper StreamingResponse SSE implementation
- ✅ JSON-RPC 2.0 compliance with MCP protocol version "2025-06-18"
- ✅ HEAD/OPTIONS method support for ChatGPT validation
- ✅ Session management and proper CORS headers
- ✅ Mac system control tools (system_info, run_command, file operations, notifications)

## IMMEDIATE ACTIONS REQUIRED

### 1. Copy Working Implementation
```bash
cp /home/ubuntu/repos/kupn/chatgpt_mac_mcp_server.py ./
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn starlette python-multipart
```

### 3. Test Server
```bash
python chatgpt_mac_mcp_server.py --host 0.0.0.0 --port 8765
```

### 4. Verify SSE Events
```bash
curl -N http://localhost:8765/sse
# Should output properly formatted SSE events without double "data:" prefix
```

### 5. Test JSON-RPC Endpoints
```bash
# Test initialize
curl -X POST http://localhost:8765/message?session_id=test \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"test","method":"initialize","params":{}}'

# Test tools/list
curl -X POST http://localhost:8765/message?session_id=test \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"test","method":"tools/list","params":{}}'
```

## OPENAI MCP DOCUMENTATION REQUIREMENTS
User provided official OpenAI MCP documentation specifying ChatGPT connectors must implement:

### Required Tools for ChatGPT Integration
1. **search tool** - Returns search results from data source
   - Input: `query` string
   - Output: `{"results": [{"id": "doc-1", "title": "...", "url": "..."}]}`
   - Must return JSON-encoded string in MCP content format

2. **fetch tool** - Retrieves full document content
   - Input: document `id` string  
   - Output: `{"id": "doc-1", "title": "...", "text": "full content", "url": "...", "metadata": {...}}`
   - Must return JSON-encoded string in MCP content format

### MCP Content Format
All tool responses must use MCP content array format:
```json
{
  "content": [
    {
      "type": "text", 
      "text": "{\"results\":[...]}" // JSON-encoded string
    }
  ]
}
```

## DEPLOYMENT REQUIREMENTS
- **Current Server:** https://farmer-thriller-reproduction-cure.trycloudflare.com (running but SSE broken)
- Fix SSE streaming through cloudflared tunnel (buffering/connection issue)
- Test ChatGPT connector creation with the public URL
- Verify connector validation completes without timeout

## SUCCESS CRITERIA
- [ ] Server starts without errors
- [ ] SSE endpoint streams properly through cloudflared tunnel (CRITICAL FIX NEEDED)
- [ ] JSON-RPC methods return valid MCP responses (✅ Currently working)
- [ ] Implement search/fetch tools per OpenAI MCP documentation
- [ ] ChatGPT connector creation succeeds without "Error creating connector"
- [ ] Mac system control tools work correctly

## TECHNICAL DETAILS

### Key Fix - SSE Event Format
**WRONG (EventSourceResponse):**
```
data: event: endpoint
data: data: /message?session_id=123
```

**CORRECT (StreamingResponse):**
```
event: endpoint
data: /message?session_id=123
```

### MCP Protocol Compliance
- Protocol version: "2025-06-18"
- Required capabilities: tools, logging, prompts, resources, experimental
- JSON-RPC 2.0 format with proper error handling
- Session-based communication via SSE

### ChatGPT Validation Sequence
1. HEAD request to /sse endpoint
2. HEAD request to /message endpoint  
3. OPTIONS requests for CORS validation
4. GET request to /sse for SSE handshake
5. POST requests to /message for JSON-RPC methods

## CURRENT SERVER STATUS
- **URL:** https://farmer-thriller-reproduction-cure.trycloudflare.com
- **Local Server:** Running on localhost:8765 (works correctly)
- **Tunnel Issue:** SSE streaming hangs through cloudflared, causing ChatGPT validation timeout
- **JSON-RPC:** Working correctly through tunnel

## IMMEDIATE PRIORITY FIXES
1. **Fix SSE streaming through cloudflared tunnel** - This is blocking ChatGPT connector validation
2. **Implement search/fetch tools** per OpenAI MCP documentation requirements
3. **Test connector creation** in ChatGPT to verify "Error creating connector" is resolved

## PRIORITY: IMMEDIATE
User has given up on this project due to repeated failures. This is your chance to deliver a working solution. 

**Key Insight:** The server implementation works locally but SSE streaming fails through the tunnel. Focus on fixing the tunnel SSE streaming issue first, then add the required search/fetch tools.

## CONTACT
Server logs show proper local SSE event generation:
```
DEBUG:__main__:Sending SSE endpoint event: 'event: endpoint\ndata: /message?session_id=...\n\n'
DEBUG:__main__:Sending SSE heartbeat: 'event: heartbeat\ndata: ping-1\n\n'
```

But tunnel access hangs: `curl -N https://farmer-thriller-reproduction-cure.trycloudflare.com/sse` (no output, times out)
