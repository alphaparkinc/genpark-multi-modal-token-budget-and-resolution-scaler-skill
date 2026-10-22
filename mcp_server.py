"""MCP server for Multi-Modal Token Budget & Resolution Scaler."""
import sys
import json
from client import MultiModalResolutionScaler

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "scale_multimodal_resolution",
                "description": "Calculates scaled image dimensions to satisfy vision LLM token limits",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "orig_width": {"type": "integer"},
                        "orig_height": {"type": "integer"},
                        "max_tokens": {"type": "integer"}
                    },
                    "required": ["orig_width", "orig_height"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "scale_multimodal_resolution":
            args = params.get("arguments", {})
            res = MultiModalResolutionScaler.scale_dimensions(
                int(args.get("orig_width", 1024)),
                int(args.get("orig_height", 768)),
                int(args.get("max_tokens", 1000))
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
