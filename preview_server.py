#!/usr/bin/env python3
"""
Markdown Preview Server for Interview Syllabus
Run: python3 preview_server.py
Then open: http://localhost:8765
"""

import os
import json
import threading
import time
import subprocess
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote

SYLLABUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "syllabus")
UI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preview_ui")
PORT = 20328

# Global state for Git updates
git_status = {
    "last_check": time.time(),
    "status": "idle",  # idle, checking, pulling, updated, error
    "message": "Up to date",
    "last_commit": ""
}


def get_all_files():
    """Recursively collect all .md files under SYLLABUS_DIR."""
    result = []
    for root, dirs, files in os.walk(SYLLABUS_DIR):
        # Sort directories for consistent ordering
        dirs.sort()
        for fname in sorted(files):
            if fname.endswith(".md"):
                full_path = os.path.join(root, fname)
                rel_path = os.path.relpath(full_path, SYLLABUS_DIR)
                result.append({"label": rel_path, "path": full_path})
    return result


def git_update_worker():
    """Background thread to check and pull git updates."""
    global git_status
    while True:
        try:
            git_status["status"] = "checking"
            git_status["last_check"] = time.time()
            
            # Fetch remote
            subprocess.run(["git", "fetch"], check=True, capture_output=True)
            
            # Check if we are behind
            local = subprocess.check_output(["git", "rev-parse", "@"], text=True).strip()
            remote = subprocess.check_output(["git", "rev-parse", "@{u}"], text=True).strip()
            base = subprocess.check_output(["git", "merge-base", "@", "@{u}"], text=True).strip()
            
            git_status["last_commit"] = local[:7]

            if local == remote:
                git_status["status"] = "idle"
                git_status["message"] = f"Up to date ({git_status['last_commit']})"
            elif local == base:
                git_status["status"] = "pulling"
                git_status["message"] = "Pulling updates..."
                subprocess.run(["git", "pull"], check=True, capture_output=True)
                git_status["status"] = "updated"
                git_status["message"] = "Updated! Refreshing..."
            else:
                git_status["status"] = "idle"
                git_status["message"] = "Diverged (manual intervention needed)"
                
        except Exception as e:
            git_status["status"] = "error"
            git_status["message"] = f"Git Error: {str(e)}"
        
        # Check every 600 seconds
        time.sleep(600)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress access logs

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # ── API Endpoints ──
        if path == "/files":
            files = get_all_files()
            body = json.dumps(files).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
            return

        elif path == "/status":
            body = json.dumps(git_status).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
            return

        elif path == "/file":
            from urllib.parse import parse_qs
            params = parse_qs(parsed.query)
            file_path = unquote(params.get("path", [""])[0])
            # Security: must be under SYLLABUS_DIR
            real = os.path.realpath(file_path)
            if not real.startswith(os.path.realpath(SYLLABUS_DIR)):
                self.send_response(403)
                self.end_headers()
                return
            try:
                with open(real, "r", encoding="utf-8") as f:
                    content = f.read()
                body = content.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(body)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
            return

        # ── Static File Serving ──
        if path == "/" or path == "/index.html":
            filename = "index.html"
        else:
            filename = path.lstrip("/")

        file_to_serve = os.path.join(UI_DIR, filename)
        
        if os.path.exists(file_to_serve) and os.path.isfile(file_to_serve):
            # Security: must be under UI_DIR
            if not os.path.realpath(file_to_serve).startswith(os.path.realpath(UI_DIR)):
                self.send_response(403)
                self.end_headers()
                return

            mime_type, _ = mimetypes.guess_type(file_to_serve)
            self.send_response(200)
            self.send_header("Content-Type", mime_type or "application/octet-stream")
            self.end_headers()
            with open(file_to_serve, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    # Start git update worker
    t = threading.Thread(target=git_update_worker, daemon=True)
    t.start()
    
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"✅ Markdown preview server running at http://localhost:{PORT}")
    print(f"   Serving UI from: {UI_DIR}")
    print(f"   Serving syllabus from: {SYLLABUS_DIR}")
    print("   Press Ctrl+C to stop.")
    server.serve_forever()
