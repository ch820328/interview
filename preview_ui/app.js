let files = [];
let activeItem = null;
let currentSection = 'algorithms';
let mastery = JSON.parse(localStorage.getItem('interview_mastery') || '{}');
let hideMastered = localStorage.getItem('hide_mastered') === 'true';

const categoryIcons = {
  algorithms: '🧩',
  system_design: '🏗️',
  behavioral: '💬',
  ai_architecture: '🧠',
  questions: '📚',
  roadmaps: '🎯',
  concurrency: '🔒',
  golang: '🐹',
  python: '🐍',
  networking: '🌐',
  system: '⚙️',
  tech_core: '💎'
};

function saveMastery() {
  localStorage.setItem('interview_mastery', JSON.stringify(mastery));
}

function saveSettings() {
  localStorage.setItem('hide_master_enabled', hideMastered);
}
const sectionTitles = {
  algorithms: 'Algorithms',
  system_design: 'System Design',
  behavioral: 'Behavioral',
  ai_architecture: 'AI Architecture',
  tech_core: 'Technical Core',
  questions: 'Question Vault',
  roadmaps: 'Target Prep'
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
  
  // Calculate progress
  const masteredCount = sectionFiles.filter(f => mastery[f.path]).length;
  const percent = sectionFiles.length > 0 ? Math.round((masteredCount / sectionFiles.length) * 100) : 0;
  document.getElementById('progress-percent').textContent = `${percent}%`;
  document.getElementById('progress-fill').style.width = `${percent}%`;

  // Multi-keyword filtering
  const keywords = filter.toLowerCase().split(' ').filter(k => k.length > 0);
  const filteredFiles = sectionFiles.filter(f => {
    // Hide mastered if enabled
    if (hideMastered && mastery[f.path]) return false;
    
    if (keywords.length === 0) return true;
    const label = f.label.toLowerCase();
    return keywords.every(k => label.includes(k));
  });

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
        const isMastered = mastery[f.path];
        item.className = 'file-item' + (activeItem === f.path ? ' active' : '') + (isMastered ? ' mastered' : '');
        item.style.paddingLeft = (depth * 14 + 10) + 'px';
        const fname = k.replace('.md', '');
        
        // Pick icon based on category or file content hints
        let icon = isMastered ? '✅' : '📄';
        if (!isMastered) {
          const category = f.label.split('/')[1]?.toLowerCase();
          icon = categoryIcons[category] || categoryIcons[currentSection] || '📄';
        }

        item.innerHTML = `
          <span class="icon">${icon}</span>
          <span class="name">${fname}</span>
        `;
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

    // Trigger Mermaid rendering
    if (window.mermaid) {
      mermaid.run({
        nodes: document.querySelectorAll('.mermaid')
      });
    }
    
    // Update Mastery Toggle
    const toggle = document.getElementById('mastered-toggle');
    const checkbox = document.getElementById('mastered-checkbox');
    toggle.style.display = 'flex';
    checkbox.checked = !!mastery[path];
    
    // Clean up old listener
    checkbox.onchange = () => {
      if (checkbox.checked) {
        mastery[path] = true;
      } else {
        delete mastery[path];
      }
      saveMastery();
      buildSidebar(document.getElementById('search').value);
    };

  } catch(e) {
    document.getElementById('content').innerHTML = `<p style="color:#f85149">Error loading file: ${e}</p>`;
  }
  document.getElementById('loading-badge').style.display = 'none';
}

document.getElementById('search').addEventListener('input', e => buildSidebar(e.target.value));

// Configure marked with KaTeX support
marked.use(markedKatex({
  throwOnError: false,
  displayMode: false
}));

// Mermaid Configuration
if (window.mermaid) {
  mermaid.initialize({
    startOnLoad: false,
    theme: 'dark'
  });
}

// Custom Marked Renderer for Mermaid
const renderer = new marked.Renderer();
const originalCodeRenderer = renderer.code.bind(renderer);
renderer.code = function(token) {
  if (token.lang === 'mermaid') {
    return `<div class="mermaid">${token.text}</div>`;
  }
  return originalCodeRenderer(token);
};
marked.setOptions({ renderer });

// Hide Mastered Toggle Logic
const hideMasteredBtn = document.getElementById('hide-mastered-btn');
function updateHideMasteredUI() {
  hideMasteredBtn.style.opacity = hideMastered ? '1' : '0.4';
  hideMasteredBtn.style.borderColor = hideMastered ? '#238636' : 'var(--border)';
  hideMasteredBtn.title = hideMastered ? 'Showing: Only Incomplete' : 'Showing: All';
}

hideMasteredBtn.addEventListener('click', () => {
    hideMastered = !hideMastered;
    localStorage.setItem('hide_mastered', hideMastered);
    updateHideMasteredUI();
    buildSidebar(document.getElementById('search').value);
});
updateHideMasteredUI();

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
