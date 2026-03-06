#!/usr/bin/env python3
"""
Markdown Preview Server for Interview Syllabus
Run: python3 preview_server.py
Then open: http://localhost:8765
"""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote

SYLLABUS_DIR = "/home/interview/syllabus"
PORT = 8765


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
    --accent2:  #3fb950;
    --text:     #e6edf3;
    --muted:    #8b949e;
    --hover:    #1f2937;
    --active:   #1c2d3f;
    --code-bg:  #161b22;
    --tag-coding:  #388bfd22;
    --tag-system:  #3fb95022;
    --tag-behav:   #d2a63422;
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

  /* ── Sidebar ── */
  #sidebar {
    width: 280px;
    min-width: 220px;
    max-width: 360px;
    background: var(--sidebar);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  #sidebar-header {
    padding: 20px 16px 12px;
    border-bottom: 1px solid var(--border);
  }
  #sidebar-header h1 {
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
    letter-spacing: 0.03em;
  }
  #sidebar-header p {
    font-size: 11px;
    color: var(--muted);
    margin-top: 3px;
  }

  #search-wrap {
    padding: 10px 12px;
    border-bottom: 1px solid var(--border);
  }
  #search {
    width: 100%;
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
    font-family: 'Inter', sans-serif;
    outline: none;
    transition: border-color 0.2s;
  }
  #search:focus { border-color: var(--accent); }

  #file-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px 6px;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }
  .section-label {
    font-size: 10px;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 10px 10px 4px;
  }
  .file-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 7px 10px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12.5px;
    color: var(--muted);
    transition: background 0.15s, color 0.15s;
    line-height: 1.4;
  }
  .file-item:hover { background: var(--hover); color: var(--text); }
  .file-item.active { background: var(--active); color: var(--accent); }
  .file-item .icon { font-size: 14px; flex-shrink: 0; }
  .file-item .name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .tag {
    font-size: 9px;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 99px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    flex-shrink: 0;
  }
  .tag-coding  { background: var(--tag-coding);  color: #58a6ff; border: 1px solid #388bfd55; }
  .tag-system  { background: var(--tag-system);  color: #3fb950; border: 1px solid #3fb95055; }
  .tag-behav   { background: var(--tag-behav);   color: #d2a634; border: 1px solid #d2a63455; }
  .tag-ai      { background: #8957e522;           color: #bc8cff; border: 1px solid #8957e555; }

  /* ── Main ── */
  #main {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
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
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  #loading-badge {
    font-size: 11px;
    color: var(--muted);
    display: none;
  }

  #content-wrap {
    flex: 1;
    overflow-y: auto;
    padding: 36px 48px;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }
  #content { max-width: 800px; margin: 0 auto; }

  /* ── Markdown styles ── */
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
  #content blockquote {
    border-left: 3px solid var(--accent);
    padding: 8px 16px;
    margin: 16px 0;
    background: #1c2d3f55;
    border-radius: 0 6px 6px 0;
    color: #8b949e;
    font-size: 13.5px;
  }
  #content code {
    font-family: 'JetBrains Mono', monospace;
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 5px;
    font-size: 12.5px;
    color: #f85149;
  }
  #content pre {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px 20px;
    overflow-x: auto;
    margin: 16px 0;
    scrollbar-width: thin;
  }
  #content pre code {
    background: none;
    border: none;
    padding: 0;
    font-size: 12.5px;
    color: #e6edf3;
  }
  #content table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 13px;
  }
  #content th {
    background: #1c2d3f;
    color: var(--accent);
    font-weight: 600;
    padding: 9px 14px;
    text-align: left;
    border: 1px solid var(--border);
  }
  #content td {
    padding: 8px 14px;
    border: 1px solid var(--border);
    color: #cdd9e5;
    vertical-align: top;
  }
  #content tr:nth-child(even) td { background: #ffffff06; }
  #content hr { border: none; border-top: 1px solid var(--border); margin: 28px 0; }

  /* placeholder */
  #placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--muted);
    gap: 12px;
  }
  #placeholder .icon { font-size: 48px; }
  #placeholder p { font-size: 14px; }
</style>
</head>
<body>

<nav id="sidebar">
  <div id="sidebar-header">
    <h1>📚 Interview Syllabus</h1>
    <p>Google L4/L5 Mock Review Notes</p>
  </div>
  <div id="search-wrap">
    <input id="search" type="text" placeholder="Search files..." />
  </div>
  <div id="file-list"></div>
</nav>

<div id="main">
  <div id="topbar">
    <span id="topbar-title">Select a file to preview</span>
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

function tagFor(label) {
  if (label.startsWith('algorithms/')) return '<span class="tag tag-coding">Coding</span>';
  if (label.startsWith('system_design/')) return '<span class="tag tag-system">System</span>';
  if (label.startsWith('behavioral/')) return '<span class="tag tag-behav">Behav</span>';
  if (label.startsWith('ai_architecture/')) return '<span class="tag tag-ai">AI</span>';
  return '';
}

function iconFor(label) {
  if (label.startsWith('algorithms/')) return '⚙️';
  if (label.startsWith('system_design/')) return '🏗️';
  if (label.startsWith('behavioral/')) return '💬';
  if (label.startsWith('ai_architecture/')) return '🤖';
  return '📄';
}

function buildSidebar(filter = '') {
  const list = document.getElementById('file-list');
  list.innerHTML = '';

  const sections = {};
  files.forEach(f => {
    if (filter && !f.label.toLowerCase().includes(filter.toLowerCase())) return;
    const dir = f.label.includes('/') ? f.label.split('/')[0] : 'root';
    if (!sections[dir]) sections[dir] = [];
    sections[dir].push(f);
  });

  const sectionNames = { algorithms: '⚙️ Algorithms', system_design: '🏗️ System Design', behavioral: '💬 Behavioral', ai_architecture: '🤖 AI Architecture' };

  Object.keys(sections).forEach(dir => {
    const label = document.createElement('div');
    label.className = 'section-label';
    label.textContent = sectionNames[dir] || dir;
    list.appendChild(label);

    sections[dir].forEach(f => {
      const item = document.createElement('div');
      item.className = 'file-item' + (activeItem === f.path ? ' active' : '');
      const fname = f.label.split('/').pop().replace('.md', '');
      item.innerHTML = `<span class="icon">${iconFor(f.label)}</span><span class="name">${fname}</span>${tagFor(f.label)}`;
      item.title = f.label;
      item.addEventListener('click', () => loadFile(f.path, f.label, item));
      list.appendChild(item);
    });
  });
}

async function loadFile(path, label, item) {
  // Clear active
  document.querySelectorAll('.file-item').forEach(i => i.classList.remove('active'));
  item.classList.add('active');
  activeItem = path;

  document.getElementById('loading-badge').style.display = 'inline';
  document.getElementById('topbar-title').textContent = label;
  document.getElementById('placeholder').style.display = 'none';
  document.getElementById('content').style.display = 'block';
  document.getElementById('content').innerHTML = '<p style="color:var(--muted);font-size:13px">Loading…</p>';

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

// Init
(async () => {
  const res = await fetch('/files');
  files = await res.json();
  buildSidebar();
})();
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
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"✅ Markdown preview server running at http://localhost:{PORT}")
    print(f"   Serving files from: {SYLLABUS_DIR}")
    print("   Press Ctrl+C to stop.")
    server.serve_forever()
