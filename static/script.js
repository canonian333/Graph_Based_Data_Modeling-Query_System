// Node colors mapping
const TYPE_COLORS = {
    'SalesOrder': '#58a6ff',
    'Customer': '#d29922',
    'BillingDocument': '#3fb950',
    'DeliveryDocument': '#f85149',
    'Product': '#bc8cff',
    'DEFAULT': '#8b949e'
};

const cy = cytoscape({
    container: document.getElementById('graph'),
    elements: [],
    style: [
        {
            selector: 'node',
            style: {
                label: 'data(label)',
                'background-color': '#8b949e',
                'color': '#fff',
                'text-valign': 'center',
                'text-halign': 'center',
                'font-size': '11px',
                'width': (ele) => Math.min(100, 40 + ele.degree() * 2),
                'height': (ele) => Math.min(100, 40 + ele.degree() * 2),
                'border-width': 2,
                'border-color': '#30363d',
                'font-weight': 'bold',
                'text-outline-width': 1,
                'text-outline-color': '#000'
            }
        },
        {
            selector: 'node[type="SalesOrder"]',
            style: { 'background-color': '#58a6ff' }
        },
        {
            selector: 'node[type="BillingDocument"]',
            style: { 'background-color': '#3fb950' }
        },
        {
            selector: 'node[type="Customer"]',
            style: { 'background-color': '#d29922' }
        },
        {
            selector: 'node[type="Product"]',
            style: { 'background-color': '#bc8cff' }
        },
        {
            selector: 'node[type="DeliveryDocument"]',
            style: { 'background-color': '#f85149' }
        },
        {
            selector: 'node:selected',
            style: {
                'width': (ele) => Math.min(120, 60 + ele.degree() * 2),
                'height': (ele) => Math.min(120, 60 + ele.degree() * 2),
                'border-width': 4,
                'border-color': '#fff',
                'shadow-blur': 15,
                'shadow-color': '#58a6ff',
                'shadow-opacity': 0.8,
                'z-index': 1000
            }
        },
        {
            selector: 'node.highlighted',
            style: {
                'border-color': '#f8e3a1',
                'border-width': 3
            }
        },
        {
            selector: '.dimmed',
            style: {
                'opacity': 0.1,
                'events': 'no'
            }
        },
        {
            selector: 'edge',
            style: {
                label: '',
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'line-color': '#30363d',
                'target-arrow-color': '#30363d',
                'font-size': '9px',
                'color': '#c9d1d9',
                'width': 1.5,
                'text-background-opacity': 0.8,
                'text-background-color': '#0d1117',
                'text-background-padding': '2px',
                'text-rotation': 'autorotate'
            }
        },
        {
            selector: 'edge:selected, edge.hover',
            style: {
                label: 'data(label)',
                'line-color': '#58a6ff',
                'target-arrow-color': '#58a6ff',
                'width': 2.5
            }
        },
        {
            selector: 'node.highlighted',
            style: {
                'border-color': '#fffa65',
                'border-width': 4,
                'background-color': '#fffa65',
                'color': '#000',
                'text-outline-width': 0,
                'font-size': '12px',
                'width': (ele) => Math.min(140, 50 + ele.degree() * 5),
                'height': (ele) => Math.min(140, 50 + ele.degree() * 5)
            }
        }
    ],
    layout: { 
    name: 'fcose', 
    animate: true,
    randomize: false,
    quality: 'high',
    nodeSpacing: 70,
    nodeOverlap: 20,
    fit: true,
    padding: 50
    }
});

// Initial Graph Load
async function loadInitialGraph() {
    try {
        const res = await fetch('/init');
        const data = await res.json();
        
        if (data.nodes && data.edges) {
            cy.add([...data.nodes, ...data.edges]);
            cy.layout({ 
                name: 'fcose', 
                animate: true,
                nodeSpacing: 80,
                componentSpacing: 100
            }).run();
        }
    } catch (error) {
        console.error("Error loading initial graph:", error);
    }
}

// // Metadata Display
function showMetadata(nodeData) {
    const panel = document.getElementById('metadata-panel');
    const content = document.getElementById('metadata-content');
    
    panel.classList.add('visible');
    
    let html = `<h3 style="margin-bottom: 5px;">${nodeData.label || 'Unnamed Node'}</h3>`;
    html += `<p style="font-size: 0.7rem; color: var(--text-muted); margin-bottom: 20px; font-family: 'JetBrains Mono';">ID: ${nodeData.id}</p>`;
    
    const properties = nodeData.properties || {};
    
    // Sort properties to keep it consistent
    const sortedKeys = Object.keys(properties).sort((a, b) => {
        if (a === 'name' || a === 'id') return -1;
        return a.localeCompare(b);
    });

    for (const key of sortedKeys) {
        if (key === 'name' || key === 'id') continue; 
        const value = properties[key];
        html += `
            <div class="metadata-item">
                <span class="metadata-label">${key}</span>
                <span class="metadata-value">${typeof value === 'object' ? JSON.stringify(value) : value}</span>
            </div>
        `;
    }
    
    if (Object.keys(properties).length === 0) {
        html += '<p class="placeholder-text">No additional metadata available.</p>';
    }
    
    content.innerHTML = html;
}

function closePanel() {
    document.getElementById('metadata-panel').classList.remove('visible');
    cy.nodes().removeClass('highlighted');
}

// Tooltip Handling
const tooltip = document.getElementById('tooltip');

function showTooltip(evt, content) {
    tooltip.innerHTML = content;
    tooltip.style.display = 'block';
    updateTooltipPos(evt);
}

function updateTooltipPos(evt) {
    const margin = 15;
    let x = evt.renderedPosition.x + margin;
    let y = evt.renderedPosition.y + margin;
    
    // Boundary check
    const tooltipWidth = tooltip.offsetWidth;
    const tooltipHeight = tooltip.offsetHeight;
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    
    if (x + tooltipWidth > windowWidth) x = evt.renderedPosition.x - tooltipWidth - margin;
    if (y + tooltipHeight > windowHeight) y = evt.renderedPosition.y - tooltipHeight - margin;
    
    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
}

function hideTooltip() {
    tooltip.style.display = 'none';
}

cy.on('mouseover', 'node', (evt) => {
    const data = evt.target.data();
    let content = `<div style="font-weight:700; color:var(--accent-color); margin-bottom:4px;">${data.type || 'Node'}</div>`;
    content += `<div style="font-size:0.9rem; font-weight:600;">${data.label || data.id}</div>`;
    
    if (data.properties) {
        const props = data.properties;
        const keys = Object.keys(props).filter(k => k !== 'id' && k !== 'label' && typeof props[k] !== 'object').slice(0, 3);
        if (keys.length > 0) {
            content += `<div style="margin-top:8px; border-top:1px solid #30363d; padding-top:5px;">`;
            keys.forEach(k => {
                content += `<div><span class="tooltip-key">${k}:</span> ${props[k]}</div>`;
            });
            content += `</div>`;
        }
    }
    showTooltip(evt, content);
});

cy.on('mouseover', 'edge', (evt) => {
    const data = evt.target.data();
    showTooltip(evt, `<div class="tooltip-key">Relationship</div><div style="font-weight:600;">${data.label}</div>`);
});

cy.on('mousemove', 'node, edge', (evt) => updateTooltipPos(evt));
cy.on('mouseout', 'node, edge', () => hideTooltip());

// Edge Hover Handling (Style changes)
cy.on('mouseover', 'edge', (evt) => evt.target.addClass('hover'));
cy.on('mouseout', 'edge', (evt) => evt.target.removeClass('hover'));

// --- Extensions Initialization ---

// Navigator (Minimap)
cy.navigator({});

// Context Menus
cy.contextMenus({
    menuItems: [
        {
            id: 'expand',
            content: 'Expand Neighbors',
            selector: 'node',
            onClickFunction: (evt) => {
                expandNode(evt.target.id(), currentDepth);
            }
        },
        {
            id: 'collapse',
            content: 'Collapse Neighbors',
            selector: 'node',
            onClickFunction: (evt) => {
                const node = evt.target;
                const neighbors = node.neighborhood().not(':selected');
                neighbors.remove();
            }
        },
        {
            id: 'select',
            content: 'Select',
            selector: 'node',
            onClickFunction: (evt) => {
                evt.target.select();
                node.trigger('tap');
            }
        }
    ]
});

// --- Interaction State ---
let currentFocusNode = null;
let currentDepth = 1;

// Click → Expand & Show Metadata
cy.on('tap', 'node', async (evt) => {
    const node = evt.target;
    const nodeId = node.id();
    currentFocusNode = nodeId;

    // Reset previous highlights
    cy.elements().removeClass('dimmed');
    
    // Dim everything else
    cy.elements().addClass('dimmed');
    
    // Highlight neighborhood
    node.removeClass('dimmed');
    node.neighborhood().removeClass('dimmed');

    // Show metadata
    showMetadata(node.data());

    // Fetch neighbors (progressive expansion)
    expandNode(nodeId, currentDepth);
});

// Clear selection on background tap
cy.on('tap', (evt) => {
    if (evt.target === cy) {
        cy.elements().removeClass('dimmed');
        currentFocusNode = null;
    }
});

async function expandNode(nodeId, depth = 1) {
    try {
        const res = await fetch(`/neighbors/${nodeId}?depth=${depth}`);
        const data = await res.json();

        // Add neighbors and edges
        const elementsToAdd = [];
        
        if (data.nodes) {
            data.nodes.forEach(n => {
                if (cy.getElementById(n.data.id).empty()) {
                    elementsToAdd.push(n);
                }
            });
        }
        
        if (data.edges) {
            data.edges.forEach(e => {
                if (cy.getElementById(e.data.id).empty()) {
                    elementsToAdd.push(e);
                }
            });
        }

        if (elementsToAdd.length > 0) {
            cy.add(elementsToAdd);
            cy.layout({ 
                name: 'fcose', 
                animate: true, 
                fit: false, 
                randomize: false,
                nodeSpacing: 70
            }).run();
        }

        // Refresh dimming to include new neighbors if a node is selected
        if (currentFocusNode) {
            const focusEle = cy.getElementById(currentFocusNode);
            cy.elements().addClass('dimmed');
            focusEle.removeClass('dimmed');
            focusEle.neighborhood().removeClass('dimmed');
        }
    } catch (error) {
        console.error("Error expanding node:", error);
    }
}

// --- UI Controls Logic ---

// Degree Toggle
document.querySelectorAll('#degree-toggle .btn-item').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('#degree-toggle .btn-item').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentDepth = parseInt(btn.dataset.depth);
        
        if (currentFocusNode) {
            expandNode(currentFocusNode, currentDepth);
        }
    });
});

// Focus mode toggle
let focusMode = false;
document.getElementById('focus-btn').addEventListener('click', () => {
    focusMode = !focusMode;
    const btn = document.getElementById('focus-btn');
    
    if (focusMode) {
        btn.classList.add('active');
        if (currentFocusNode) {
            const neighborhood = cy.getElementById(currentFocusNode).closedNeighborhood();
            cy.elements().not(neighborhood).style('display', 'none');
        }
    } else {
        btn.classList.remove('active');
        cy.elements().show();
    }
});

// Node Type Filtering
document.querySelectorAll('.filter-tag').forEach(tag => {
    tag.addEventListener('click', () => {
        tag.classList.toggle('active');
        const type = tag.dataset.type;
        const isActive = tag.classList.contains('active');
        
        if (isActive) {
            cy.nodes().filter(n => n.data('labels') && n.data('labels').includes(type)).show();
        } else {
            cy.nodes().filter(n => n.data('labels') && n.data('labels').includes(type)).hide();
        }
    });
});

// --- Search Functionality ---
async function searchNodes() {
    const query = document.getElementById('node-search').value.trim();
    if (!query) return;

    // Search in current graph items first
    let foundNode = cy.nodes().filter(n => 
        n.data('id').toLowerCase().includes(query.toLowerCase()) || 
        (n.data('properties') && Object.values(n.data('properties')).some(v => String(v).toLowerCase().includes(query.toLowerCase())))
    ).first();

    if (!foundNode.empty()) {
        highlightFoundNode(foundNode);
    } else {
        // Fetch from server
        try {
            const res = await fetch(`/search?q=${query}`);
            const data = await res.json();
            if (data.nodes && data.nodes.length > 0) {
                const newNode = data.nodes[0];
                cy.add(newNode);
                foundNode = cy.getElementById(newNode.data.id);
                highlightFoundNode(foundNode);
            }
        } catch (error) {
            console.error("Search error:", error);
        }
    }
}

function highlightFoundNode(node) {
    node.show(); // Ensure visible if filtered
    node.select();
    cy.animate({
        center: { eles: node },
        zoom: 1.2,
        duration: 800,
        easing: 'ease-in-out'
    });
    
    // Trigger tap behavior (show metadata and dim others)
    node.trigger('tap');
}

// Support Enter key in search
document.getElementById('node-search').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchNodes();
});

// --- Chat Functionality ---

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const question = input.value.trim();
    if (!question) return;

    // Add user message to UI
    appendMessage('user', question);
    input.value = '';

    // Add loading indicator
    const loadingId = 'loading-' + Date.now();
    appendMessage('ai', '<span class="loading-dots">Thinking</span>', loadingId);

    try {
        const res = await fetch('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        const data = await res.json();

        // Remove loading indicator
        const loadingEle = document.getElementById(loadingId);
        if (loadingEle) loadingEle.remove();

        if (data.error) {
            appendMessage('ai', `<span style="color: #f85149;">Error: ${data.error}</span>`);
            return;
        }

        // Add AI response with split screen
        const aiMsgHtml = `
            <div class="ai-answer">${data.answer}</div>
            <div class="split-screen">
                <div class="split-left">
                    <div class="split-header">
                        <span class="split-label">System Query (Cypher)</span>
                        <span class="copy-btn" onclick="copyToClipboard(this, \`${data.cypher.replace(/`/g, '\\`').replace(/\n/g, '\\n')}\`)">Copy</span>
                    </div>
                    <div class="cypher-code">${data.cypher || 'No query generated'}</div>
                </div>
                <div class="split-right">
                    <div class="split-header">
                        <span class="split-label">Graph Results</span>
                    </div>
                    <div class="cypher-code" style="color: var(--text-muted); font-size: 0.75rem;">${JSON.stringify(data.results, null, 2)}</div>
                </div>
            </div>
        `;
        appendMessage('ai', aiMsgHtml);

        // Highlight nodes from results
        if (data.results) {
            const potentialIds = extractPotentialIds(data.results);
            if (potentialIds.length > 0) {
                highlightNodesByIds(potentialIds);
            }
        }

    } catch (error) {
        console.error("Chat Error:", error);
        const loadingEle = document.getElementById(loadingId);
        if (loadingEle) loadingEle.remove();
        appendMessage('ai', `<span style="color: #f85149;">Failed to connect to server.</span>`);
    }
}

function extractPotentialIds(results) {
    const ids = new Set();
    const traverse = (obj) => {
        if (typeof obj === 'string') {
            const looksLikeId = /^(SO_|CUST_|PR_|DEL_|BILL_|ITEM_)/i.test(obj) || 
                               (obj.length > 3 && obj.length < 20 && /^[A-Z0-9_-]+$/i.test(obj));
            if (looksLikeId && !obj.includes(' ')) {
                ids.add(obj);
            }
        } else if (typeof obj === 'object' && obj !== null) {
            Object.values(obj).forEach(val => traverse(val));
        }
    };
    results.forEach(res => traverse(res));
    return Array.from(ids);
}

async function highlightNodesByIds(ids) {
    try {
        const res = await fetch('/api/nodes_by_ids', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ids })
        });
        const nodesData = await res.json();

        if (!nodesData || nodesData.length === 0) return;

        // Reset highlights
        cy.nodes().removeClass('highlighted');

        const elementsToHighlight = [];

        nodesData.forEach(n => {
            let ele = cy.getElementById(n.id);
            if (ele.empty()) {
                ele = cy.add({ data: { id: n.id, label: n.label, properties: n.properties, labels: n.labels } });
            }
            ele.addClass('highlighted');
            elementsToHighlight.push(ele);
        });

        if (elementsToHighlight.length > 0) {
            const collection = cy.collection(elementsToHighlight);
            cy.animate({
                fit: { eles: collection, padding: 100 },
                duration: 800,
                easing: 'ease-in-out'
            });
            
            if (nodesData.length === 1) {
                showMetadata(nodesData[0]);
            }
        }
    } catch (error) {
        console.error("Error highlighting nodes:", error);
    }
}

function appendMessage(sender, content, id = null) {
    const history = document.getElementById('chat-history');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}-message`;
    if (id) msgDiv.id = id;
    msgDiv.innerHTML = content;
    history.appendChild(msgDiv);
    history.scrollTop = history.scrollHeight;
}

function copyToClipboard(btn, text) {
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
        const originalText = btn.innerText;
        btn.innerText = 'Copied!';
        btn.style.color = 'var(--success-color)';
        setTimeout(() => {
            btn.innerText = originalText;
            btn.style.color = '';
        }, 2000);
    });
}

// Run initial load
loadInitialGraph();