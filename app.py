from flask import Flask, render_template, request, jsonify
from db import run_query, close_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/init')
def init_graph():
    query = """
    MATCH (n)-[r]->(m)
    RETURN elementId(n) AS n_id, n, elementId(r) AS r_id, type(r) AS r_type, elementId(m) AS m_id, m
    LIMIT 50
    """
    try:
        results = run_query(query)

        nodes = []
        edges = []
        node_ids = set()

        for r in results:
            n_id = r["n_id"]
            m_id = r["m_id"]
            n_label = r["n"].get("name") or r["n"].get("id") or n_id
            m_label = r["m"].get("name") or r["m"].get("id") or m_id
            
            if n_id not in node_ids:
                nodes.append({"data": {"id": n_id, "label": n_label, "properties": r["n"]}})
                node_ids.add(n_id)
                
            if m_id not in node_ids:
                nodes.append({"data": {"id": m_id, "label": m_label, "properties": r["m"]}})
                node_ids.add(m_id)
                
            edges.append({"data": {
                "id": r["r_id"],
                "source": n_id,
                "target": m_id,
                "label": r["r_type"]
            }})

        return jsonify({"nodes": nodes, "edges": edges})
    except Exception as e:
        print(f"Error in /init: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/search')
def search():
    q = request.args.get('q', '')
    query = """
    MATCH (n)
    WHERE toLower(n.name) CONTAINS toLower($q) OR toLower(n.id) CONTAINS toLower($q)
    RETURN elementId(n) AS id, coalesce(n.name, n.id, "Node") AS label, n AS properties
    """
    try:
        results = run_query(query, {'q': q})
        return jsonify(results)
    except Exception as e:
        print(f"Error in /search: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/neighbors/<node_id>')
def neighbors(node_id):
    query = """
    MATCH (n)-[r]-(m)
    WHERE elementId(n) = $id
    RETURN elementId(n) AS n_id, n, elementId(r) AS r_id, type(r) AS r_type, elementId(m) AS m_id, m
    """
    try:
        results = run_query(query, {'id': node_id})

        nodes = []
        edges = []

        for r in results:
            n_label = r["n"].get("name") or r["n"].get("id") or r["n_id"]
            m_label = r["m"].get("name") or r["m"].get("id") or r["m_id"]
            
            nodes.append({"data": {"id": r["n_id"], "label": n_label, "properties": r["n"]}})
            nodes.append({"data": {"id": r["m_id"], "label": m_label, "properties": r["m"]}})
            edges.append({"data": {
                "id": r["r_id"],
                "source": r["n_id"],
                "target": r["m_id"],
                "label": r["r_type"]
            }})

        return jsonify({"nodes": nodes, "edges": edges})
    except Exception as e:
        print(f"Error in /neighbors/{node_id}: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    close_db()