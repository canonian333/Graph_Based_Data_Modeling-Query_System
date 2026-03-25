const cy = cytoscape({
    container: document.getElementById('graph'),
    elements: [],
    style: [
        {
            selector: 'node',
            style: {
                label: 'data(label)',
                'background-color': '#58a6ff',
                'color': '#c9d1d9',
                'text-valign': 'center',
                'text-halign': 'center',
                'font-size': '10px',
                'width': (ele) => Math.min(100, 30 + ele.degree() * 5),
                'height': (ele) => Math.min(100, 30 + ele.degree() * 5),
                'border-width': 2,
                'border-color': '#30363d'
            }
        },
        {
            selector: 'edge',
            style: {
                label: 'data(label)',
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'line-color': '#30363d',
                'target-arrow-color': '#30363d',
                'font-size': '8px',
                'color': '#8b949e',
                'width': 1
            }
        },
        {
            selector: 'node.highlighted',
            style: {
                'border-color': '#fffa65',
                'border-width': 4,
                'background-color': '#fffa65',
                'color': '#000',
                'width': (ele) => Math.min(120, 40 + ele.degree() * 5),
                'height': (ele) => Math.min(120, 40 + ele.degree() * 5)
            }
        }
    ],
    layout: { name: 'cose', animate: true }
});

// Initial Graph Load
async function loadInitialGraph() {
    try {
        const res = await fetch('/init');
        const data = await res.json();
        
        if (data.nodes && data.edges) {
            cy.add([...data.nodes, ...data.edges]);
            cy.layout({ name: 'cose' }).run();
        }
    } catch (error) {
        console.error("Error loading initial graph:", error);
    }
}

// Search
async function searchNode() {
    const q = document.getElementById('search').value;
    if (!q) return;

    try {
        const res = await fetch(`/search?q=${q}`);
        const data = await res.json();

        // Clear previous highlights
        cy.nodes().removeClass('highlighted');

        data.forEach(n => {
            let ele = cy.getElementById(n.id);
            if (ele.empty()) {
                ele = cy.add({ data: { id: String(n.id), label: n.label, properties: n.properties } });
            }
            ele.addClass('highlighted');
        });

        if (data.length > 0) {
            cy.layout({ name: 'cose' }).run();
            
            // If only one result, show metadata and focus
            if (data.length === 1) {
                showMetadata(data[0]);
                cy.animate({
                    center: { eles: cy.getElementById(data[0].id) },
                    zoom: 1.5,
                    duration: 500
                });
            }
        }
    } catch (error) {
        console.error("Error searching node:", error);
    }
}

// Metadata Display
function showMetadata(nodeData) {
    const panel = document.getElementById('metadata-panel');
    const content = document.getElementById('metadata-content');
    
    panel.classList.add('visible');
    
    let html = `<h3>${nodeData.label || 'Unnamed Node'}</h3>`;
    html += `<p style="font-size: 0.8rem; color: #8b949e; margin-bottom: 15px;">ID: ${nodeData.id}</p>`;
    
    const properties = nodeData.properties || {};
    
    for (const [key, value] of Object.entries(properties)) {
        if (key === 'name' || key === 'id') continue; // Already shown
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

// Click → Expand & Show Metadata
cy.on('tap', 'node', async (evt) => {
    const node = evt.target;
    const nodeId = node.id();

    // Reset previous highlights
    cy.nodes().removeClass('highlighted');
    // Highlight current node
    node.addClass('highlighted');

    // Show metadata immediately
    showMetadata(node.data());

    try {
        const res = await fetch(`/neighbors/${nodeId}`);
        const data = await res.json();

        // Add neighbors and edges
        const elementsToAdd = [];
        
        // Handle nodes: only add if they don't exist
        if (data.nodes) {
            data.nodes.forEach(n => {
                if (cy.getElementById(n.data.id).empty()) {
                    elementsToAdd.push(n);
                }
            });
        }
        
        // Handle edges: only add if they don't exist
        if (data.edges) {
            data.edges.forEach(e => {
                if (cy.getElementById(e.data.id).empty()) {
                    elementsToAdd.push(e);
                }
            });
        }

        if (elementsToAdd.length > 0) {
            cy.add(elementsToAdd);
            cy.layout({ name: 'cose', animate: true, fit: false }).run();
        }
    } catch (error) {
        console.error("Error expanding node:", error);
    }
});

// Run initial load
loadInitialGraph();