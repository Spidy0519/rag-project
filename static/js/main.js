const chatBox = document.getElementById('chat-box');
const queryInput = document.getElementById('query-input');
const sendBtn = document.getElementById('send-btn');

function showSection(section) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(`${section}-section`).classList.add('active');
    document.querySelectorAll('.btn-nav').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    if (section === 'chat') queryInput.focus();
}

function escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = text;
    return d.innerHTML;
}

function formatAnswer(text) {
    let html = escapeHtml(text);
    // code blocks ```...```
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
        return `<pre><code>${code.trim()}</code></pre>`;
    });
    // inline `code`
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    // **bold**
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // *italic*
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    // newlines to paragraphs
    html = html.split(/\n{2,}/).map(p => p.trim() ? `<p>${p.replace(/\n/g, '<br>')}</p>` : '').join('');
    return html;
}

function getSourceLabel(s) {
    if (!s.source || s.source === 'unknown') return null;
    try {
        const u = new URL(s.source);
        if (u.hostname.includes('python.org')) return u.pathname.split('/').pop().replace(/\.html$/, '').replace(/_/g, ' ');
        if (u.hostname.includes('dev.java')) return u.pathname.split('/').filter(Boolean).pop() || 'Java Docs';
        if (u.hostname.includes('learn-c.org')) return 'C Tutorial';
        return u.hostname.replace('www.', '');
    } catch {
        // not a URL — filename
        const name = s.source;
        return name.length > 30 ? name.substring(0, 27) + '...' : name;
    }
}

function addMessage(text, type, sources = null) {
    const msg = document.createElement('div');
    msg.className = `message ${type}-message`;

    const avatar = type === 'bot' ? 'AI' : 'You';
    let contentHtml = type === 'bot' ? formatAnswer(text) : escapeHtml(text);

    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        const unique = [];
        const seen = new Set();
        for (const s of sources) {
            if (s.source && s.source !== 'unknown' && !seen.has(s.source)) {
                seen.add(s.source);
                unique.push(s);
            }
        }
        if (unique.length > 0) {
            sourcesHtml = `<div class="sources-bar">`;
            for (const s of unique) {
                const label = getSourceLabel(s);
                if (label) {
                    sourcesHtml += `<a class="source-chip" href="${escapeHtml(s.source)}" target="_blank" title="${escapeHtml(s.source)}">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/></svg>
                        ${escapeHtml(label)}
                    </a>`;
                }
            }
            sourcesHtml += `</div>`;
        }
    }

    msg.innerHTML = `
        <div class="msg-row">
            <div class="msg-avatar">${avatar}</div>
            <div class="msg-body">
                <div class="message-content">${contentHtml}</div>
                ${sourcesHtml}
            </div>
        </div>`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addTyping() {
    const msg = document.createElement('div');
    msg.className = 'message bot-message';
    msg.id = 'typing';
    msg.innerHTML = `
        <div class="msg-row">
            <div class="msg-avatar">AI</div>
            <div class="msg-body">
                <div class="message-content">
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
        </div>`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
    const el = document.getElementById('typing');
    if (el) el.remove();
}

let sending = false;
async function sendMessage() {
    const query = queryInput.value.trim();
    if (!query || sending) return;
    sending = true;
    addMessage(query, 'user');
    queryInput.value = '';
    queryInput.style.height = 'auto';
    sendBtn.disabled = true;
    addTyping();
    try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 30000);
        const res = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query }),
            signal: controller.signal,
        });
        clearTimeout(timeout);
        const data = await res.json();
        removeTyping();
        if (data.error) {
            addMessage(data.error, 'bot');
        } else {
            addMessage(data.answer, 'bot', data.sources);
        }
    } catch (err) {
        removeTyping();
        const msg = err.name === 'AbortError'
            ? 'Request timed out. The server may be busy.'
            : `Network error: ${err.message}`;
        addMessage(msg, 'bot');
    }
    sending = false;
    sendBtn.disabled = false;
    queryInput.focus();
}

queryInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

function showStatus(areaId, msg, type) {
    const area = document.getElementById(areaId);
    const div = document.createElement('div');
    div.className = `status-msg status-${type}`;
    const icons = { success: '&#10003;', error: '&#10007;', loading: '&#8987;' };
    div.innerHTML = `<span>${icons[type] || ''}</span> ${msg}`;
    area.prepend(div);
    if (type !== 'loading') setTimeout(() => div.remove(), 8000);
}

async function handleFiles(files) {
    for (const file of files) {
        showStatus('upload-status', `Uploading ${file.name}...`, 'loading');
        const formData = new FormData();
        formData.append('file', file);
        try {
            const res = await fetch('/upload', { method: 'POST', body: formData });
            const data = await res.json();
            if (data.error) {
                showStatus('upload-status', `${file.name}: ${data.error}`, 'error');
            } else {
                showStatus('upload-status', `${data.message} (${data.chunks} chunks)`, 'success');
            }
        } catch (err) {
            showStatus('upload-status', `${file.name}: Upload failed`, 'error');
        }
    }
    document.getElementById('file-input').value = '';
}

function handleDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
}

document.getElementById('drop-zone').addEventListener('click', (e) => {
    if (e.target.tagName !== 'BUTTON') document.getElementById('file-input').click();
});

async function scrapeAll() {
    showStatus('scrape-status', 'Scraping default sources... This may take a while.', 'loading');
    try {
        const res = await fetch('/scrape', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
        const data = await res.json();
        showStatus('scrape-status', `Scraping complete. ${Object.keys(data.results || {}).length} sources processed.`, 'success');
    } catch (err) {
        showStatus('scrape-status', 'Scraping failed.', 'error');
    }
}

async function scrapeUrl() {
    const url = document.getElementById('scrape-url').value.trim();
    const name = document.getElementById('scrape-name').value.trim() || 'custom';
    if (!url) return;
    showStatus('scrape-status', `Scraping ${url}...`, 'loading');
    try {
        const res = await fetch('/scrape', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, name }),
        });
        const data = await res.json();
        if (data.status === 'ok') {
            showStatus('scrape-status', `Scraped: ${data.chunks} chunks from ${url}`, 'success');
        } else {
            showStatus('scrape-status', `Failed to scrape ${url}`, 'error');
        }
    } catch (err) {
        showStatus('scrape-status', 'Request failed.', 'error');
    }
    document.getElementById('scrape-url').value = '';
    document.getElementById('scrape-name').value = '';
}
