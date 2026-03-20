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
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote

SYLLABUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "syllabus")
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


HTML = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Interview Syllabus</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
  :root {
    --bg:       #0d1117;
    --sidebar:  #161b22;
    --border:   #30363d;
    --accent:   #58a6ff;
    --text:     #e6edf3;
    --muted:    #8b949e;
    --hover:    #1f2937;
    --active:   #1c2d3f;
    --code-bg:  #161b22;
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
    display: flex;
    height: 100vh;
    overflow: hidden;
  }

  /* Activity Bar */
  #activity-bar {
    width: 56px;
    background: #090c10;
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 16px;
    gap: 12px;
    flex-shrink: 0;
    z-index: 10;
  }
  .activity-item {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    cursor: pointer;
    font-size: 20px;
    color: var(--muted);
    transition: all 0.15s;
    position: relative;
    opacity: 0.6;
  }
  .activity-item:hover { opacity: 1; background: var(--hover); }
  .activity-item.active { opacity: 1; background: var(--hover); }
  .activity-item.active::before {
    content: '';
    position: absolute;
    left: -10px;
    top: 6px;
    bottom: 6px;
    width: 3px;
    background: var(--accent);
    border-radius: 0 3px 3px 0;
  }

  /* ── Sidebar ── */
  #sidebar {
    width: 250px;
    min-width: 200px;
    max-width: 360px;
    background: var(--sidebar);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    flex-shrink: 0;
  }
  #sidebar-header {
    padding: 18px 16px 12px;
  }
  #sidebar-header h1 {
    font-size: 11px;
    text-transform: uppercase;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 0.05em;
  }

  #search-wrap {
    padding: 0 12px 10px;
    border-bottom: 1px solid var(--border);
  }
  #search {
    width: 100%;
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 4px;
    padding: 6px 8px;
    font-size: 12px;
    outline: none;
    transition: border-color 0.2s;
  }
  #search:focus { border-color: var(--accent); }

  #file-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }
  
  /* Tree Nodes */
  .folder-item {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 10px;
    cursor: pointer;
    font-size: 13px;
    color: var(--text);
    font-weight: 500;
    user-select: none;
  }
  .folder-item:hover { background: var(--hover); }
  .folder-icon {
    font-size: 12px;
  }
  .folder-icon::after { content: '📂'; }
  .folder-item.collapsed .folder-icon::after { content: '📁'; }

  .file-item {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 10px;
    cursor: pointer;
    font-size: 13px;
    color: var(--muted);
    user-select: none;
  }
  .file-item:hover { background: var(--hover); color: var(--text); }
  .file-item.active { background: var(--active); color: var(--accent); }

  /* ── Sidebar Toggle ── */
  #sidebar.collapsed { display: none !important; }
  #sidebar-toggle {
    font-size: 20px;
    cursor: pointer;
    color: var(--muted);
    user-select: none;
    line-height: 1;
  }
  #sidebar-toggle:hover { color: var(--text); }

  @media (max-width: 768px) {
    #sidebar {
      position: absolute;
      left: 56px;
      top: 53px;
      bottom: 0;
      z-index: 50;
      box-shadow: 4px 4px 12px rgba(0,0,0,0.5);
    }
    #content-wrap { padding: 20px 16px !important; }
  }

  /* ── Main ── */
  #main {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: var(--bg);
  }
  #topbar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 24px;
    border-bottom: 1px solid var(--border);
    background: var(--sidebar);
    min-height: 52px;
  }
  #topbar-title {
    font-size: 13px;
    font-weight: 500;
    color: var(--text);
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  #loading-badge { display: none; font-size: 11px; color: var(--muted); }

  #content-wrap {
    flex: 1;
    overflow-y: auto;
    padding: 36px 48px;
    scrollbar-width: thin;
  }
  #content { max-width: 800px; margin: 0 auto; }

  /* Markdown styles */
  #content h1 { font-size: 26px; font-weight: 700; border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 20px; color: var(--text); }
  #content h2 { font-size: 19px; font-weight: 600; margin: 32px 0 12px; color: var(--text); }
  #content h3 { font-size: 15px; font-weight: 600; margin: 24px 0 8px; color: #cdd9e5; }
  #content p  { line-height: 1.75; margin-bottom: 14px; font-size: 14px; color: #cdd9e5; }
  #content a  { color: var(--accent); text-decoration: none; }
  #content a:hover { text-decoration: underline; }
  #content ul, #content ol { padding-left: 22px; margin-bottom: 14px; }
  #content li { line-height: 1.75; font-size: 14px; color: #cdd9e5; margin-bottom: 4px; }
  #content strong { color: var(--text); font-weight: 600; }
  #content em { color: #d2a634; }
  #content blockquote { border-left: 3px solid var(--accent); padding: 8px 16px; margin: 16px 0; background: #1c2d3f55; border-radius: 0 6px 6px 0; color: #8b949e; font-size: 13.5px; }
  #content code { font-family: 'JetBrains Mono', monospace; background: var(--code-bg); border: 1px solid var(--border); border-radius: 4px; padding: 1px 5px; font-size: 12.5px; color: #f85149; }
  #content pre { background: var(--code-bg); border: 1px solid var(--border); border-radius: 8px; padding: 18px 20px; overflow-x: auto; margin: 16px 0; }
  #content pre code { background: none; border: none; padding: 0; color: #e6edf3; }
  #content table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; }
  #content th { background: #1c2d3f; color: var(--accent); font-weight: 600; padding: 9px 14px; text-align: left; border: 1px solid var(--border); }
  #content td { padding: 8px 14px; border: 1px solid var(--border); color: #cdd9e5; vertical-align: top; }
  #content tr:nth-child(even) td { background: #ffffff06; }
  #content hr { border: none; border-top: 1px solid var(--border); margin: 28px 0; }

  #placeholder { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--muted); gap: 12px; }
  #placeholder .icon { font-size: 48px; }
</style>
</head>
<body>

<div id="activity-bar">
  <div class="activity-item" data-section="system_design" title="System Design">🏗️</div>
  <div class="activity-item" data-section="algorithms" title="Algorithms">⚙️</div>
  <div class="activity-item" data-section="behavioral" title="Behavioral">💬</div>
  <div class="activity-item" data-section="ai_architecture" title="AI Architecture">🤖</div>
  <div style="margin-top: auto; padding-bottom: 16px;">
    <div id="git-status-dot" title="Git Status" style="width: 10px; height: 10px; border-radius: 50%; background: #238636; margin: 0 auto;"></div>
  </div>
</div>

<nav id="sidebar">
  <div id="sidebar-header">
    <h1 id="sidebar-title">System Design</h1>
  </div>
  <div id="search-wrap">
    <input id="search" type="text" placeholder="Search files..." autocomplete="off" />
  </div>
  <div id="file-list"></div>
</nav>

<div id="main">
  <div id="topbar">
    <div id="sidebar-toggle" title="Toggle Sidebar">☰</div>
    <span id="topbar-title">Select a file to preview</span>
    <span id="git-status-text" style="font-size: 11px; color: var(--muted); margin-right: 12px;">Git: idle</span>
    <span id="last-update-text" style="font-size: 11px; color: var(--muted); margin-right: 12px;"></span>
    <span id="loading-badge">Loading…</span>
  </div>
  <div id="content-wrap">
    <div id="placeholder">
      <div class="icon">📖</div>
      <p>Select a file from the sidebar to start reading.</p>
    </div>
    <div id="content" style="display:none"></div>
  </div>
</div>

<script>
let files = [];
let activeItem = null;
let currentSection = 'system_design';
const sectionTitles = {
  algorithms: 'Algorithms',
  system_design: 'System Design',
  behavioral: 'Behavioral',
  ai_architecture: 'AI Architecture'
};

document.getElementById('sidebar-toggle').addEventListener('click', () => {
  document.getElementById('sidebar').classList.toggle('collapsed');
});

if (window.innerWidth <= 768) {
  document.getElementById('sidebar').classList.add('collapsed');
}

function buildSidebar(filter = '') {
  document.getElementById('sidebar-title').textContent = sectionTitles[currentSection] || 'Files';
  const list = document.getElementById('file-list');
  list.innerHTML = '';

  const sectionFiles = files.filter(f => f.label.startsWith(currentSection + '/'));
  const filteredFiles = sectionFiles.filter(f => !filter || f.label.toLowerCase().includes(filter.toLowerCase()));

  if (filteredFiles.length === 0) {
    list.innerHTML = '<div style="padding: 10px 16px; color: var(--muted); font-size: 12px;">No files found</div>';
    return;
  }

  const tree = {};
  filteredFiles.forEach(f => {
    const relPath = f.label.slice(currentSection.length + 1);
    const parts = relPath.split('/');
    let curr = tree;
    for (let i = 0; i < parts.length - 1; i++) {
      if (!curr[parts[i]]) curr[parts[i]] = { _isDir: true, children: {} };
      curr = curr[parts[i]].children;
    }
    curr[parts[parts.length - 1]] = { _isDir: false, file: f };
  });

  function drawNode(node, domParent, depth) {
    const keys = Object.keys(node).sort((a,b) => {
       const isDirA = node[a]._isDir ? 1 : 0;
       const isDirB = node[b]._isDir ? 1 : 0;
       if (isDirA !== isDirB) return isDirB - isDirA;
       return a.localeCompare(b);
    });

    keys.forEach(k => {
      const child = node[k];
      
      if (child._isDir) {
        const div = document.createElement('div');
        const folderHead = document.createElement('div');
        folderHead.className = 'folder-item';
        folderHead.style.paddingLeft = (depth * 14 + 10) + 'px';
        folderHead.innerHTML = `<span class="icon folder-icon"></span><span class="name">${k}</span>`;
        
        const folderContent = document.createElement('div');
        folderContent.className = 'folder-content';
        folderContent.style.display = 'block'; // Default to expanded
        
        folderHead.addEventListener('click', () => {
          const isCollapsed = folderContent.style.display === 'none';
          folderContent.style.display = isCollapsed ? 'block' : 'none';
          folderHead.classList.toggle('collapsed', !isCollapsed);
        });

        div.appendChild(folderHead);
        div.appendChild(folderContent);
        domParent.appendChild(div);
        
        drawNode(child.children, folderContent, depth + 1);
      } else {
        const f = child.file;
        const item = document.createElement('div');
        item.className = 'file-item' + (activeItem === f.path ? ' active' : '');
        item.style.paddingLeft = (depth * 14 + 10) + 'px';
        const fname = k.replace('.md', '');
        item.innerHTML = `<span class="icon">📄</span><span class="name">${fname}</span>`;
        item.title = f.label;
        item.addEventListener('click', () => {
          document.querySelectorAll('.file-item').forEach(i => i.classList.remove('active'));
          item.classList.add('active');
          loadFile(f.path, f.label, item);
        });
        domParent.appendChild(item);
      }
    });
  }
  
  drawNode(tree, list, 0);
}

function updateActivityBar() {
  document.querySelectorAll('.activity-item').forEach(el => {
    el.classList.toggle('active', el.dataset.section === currentSection);
  });
}

document.querySelectorAll('.activity-item').forEach(el => {
  el.addEventListener('click', () => {
    currentSection = el.dataset.section;
    document.getElementById('search').value = '';
    
    // Auto-expand sidebar if it was collapsed
    document.getElementById('sidebar').classList.remove('collapsed');
    
    updateActivityBar();
    buildSidebar();
  });
});

async function loadFile(path, label, item) {
  activeItem = path;
  document.getElementById('loading-badge').style.display = 'inline';
  document.getElementById('topbar-title').textContent = label;
  document.getElementById('placeholder').style.display = 'none';
  document.getElementById('content').style.display = 'block';
  document.getElementById('content').innerHTML = '<p style="color:var(--muted);font-size:13px">Loading…</p>';

  if (window.innerWidth <= 768) {
    document.getElementById('sidebar').classList.add('collapsed');
  }

  try {
    const res = await fetch('/file?path=' + encodeURIComponent(path));
    const text = await res.text();
    document.getElementById('content').innerHTML = marked.parse(text);
    document.getElementById('content-wrap').scrollTop = 0;
  } catch(e) {
    document.getElementById('content').innerHTML = `<p style="color:#f85149">Error loading file: ${e}</p>`;
  }
  document.getElementById('loading-badge').style.display = 'none';
}

document.getElementById('search').addEventListener('input', e => buildSidebar(e.target.value));

(async () => {
  const res = await fetch('/files');
  files = await res.json();
  updateActivityBar();
  buildSidebar();
})();

// Git Status Polling
async function checkGitStatus() {
  try {
    const res = await fetch('/status');
    const data = await res.json();
    const dot = document.getElementById('git-status-dot');
    const text = document.getElementById('git-status-text');
    
    text.textContent = `Git: ${data.message}`;
    if (data.last_check) {
        const d = new Date(data.last_check * 1000);
        const timeStr = d.toLocaleTimeString('zh-TW', { hour12: false });
        document.getElementById('last-update-text').textContent = `Check: ${timeStr}`;
    }
    
    if (data.status === 'idle') dot.style.background = '#238636';
    else if (data.status === 'checking' || data.status === 'pulling') dot.style.background = '#d29922';
    else if (data.status === 'updated') {
        dot.style.background = '#58a6ff';
        // Auto refresh sidebar if updated
        const resFiles = await fetch('/files');
        files = await resFiles.json();
        buildSidebar();
    } else if (data.status === 'error') dot.style.background = '#f85149';
    
  } catch (e) {}
}
setInterval(checkGitStatus, 15000); // Check every 15s
checkGitStatus();

</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress access logs

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))

        elif path == "/files":
            files = get_all_files()
            body = json.dumps(files).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)

        elif path == "/status":
            body = json.dumps(git_status).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)

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
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    # Start git update worker
    t = threading.Thread(target=git_update_worker, daemon=True)
    t.start()
    
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"✅ Markdown preview server running at http://localhost:{PORT}")
    print(f"   Serving files from: {SYLLABUS_DIR}")
    print("   Press Ctrl+C to stop.")
    server.serve_forever()
