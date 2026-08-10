def generate_projects_matrix_svg():
    width = 1280
    height = 720
    
    # 15 exact projects categorized into 5 domain clusters (XML escaped &amp;)
    clusters = [
        {
            "title": "🤖 Autonomous Robotics &amp; Hardware",
            "color": "#00f0ff", # cyan
            "x": 40, "y": 70, "w": 380, "h": 280,
            "projects": [
                {"name": "FarmBot", "desc": "Webots agri omni-directional robot with 6-DOF arm", "tech": ["ROS2", "Webots"]},
                {"name": "Drone-Powered Race Cars", "desc": "Repurposed drone propulsion for high-speed RC cars", "tech": ["Hardware", "Motors"]},
                {"name": "Autonomous Edge Devices", "desc": "Voice obstacle car &amp; SLAM Micromouse", "tech": ["SLAM", "Edge AI"]}
            ]
        },
        {
            "title": "👁️ Computer Vision &amp; Edge AI",
            "color": "#22d65e", # green
            "x": 450, "y": 70, "w": 380, "h": 280,
            "projects": [
                {"name": "CASTA", "desc": "Counter-Drone C-UAS real-time drone &amp; trajectory tracking", "tech": ["YOLO", "TensorRT"]},
                {"name": "Fabguard-AI", "desc": "Real-time SEM wafer fabrication defect detection", "tech": ["CV", "PyTorch"]},
                {"name": "SafeScan", "desc": "Mobile health app identifying harmful ingredients &amp; allergens", "tech": ["Flutter", "CV"]}
            ]
        },
        {
            "title": "⚡ Hardware, Circuits &amp; IoT",
            "color": "#f59e0b", # amber
            "x": 860, "y": 70, "w": 380, "h": 280,
            "projects": [
                {"name": "CGS (Circuit Graphic Symphony)", "desc": "Text → schematics &amp; SPICE netlists framework", "tech": ["JavaScript", "SPICE"]},
                {"name": "Smart Medical Scale", "desc": "IoT healthcare load cell &amp; HX711 patient data device", "tech": ["IoT", "HX711"]}
            ]
        },
        {
            "title": "🧠 Multimodal AI, LLMs &amp; Assistants",
            "color": "#3b82f6", # blue
            "x": 40, "y": 370, "w": 790, "h": 320,
            "projects": [
                {"name": "PetPal", "desc": "Dog health voice/video AI vet consultations", "tech": ["Flutter", "Gemini", "Firebase"]},
                {"name": "Hapticus", "desc": "Digital text &amp; PDF to tactile Braille pipeline", "tech": ["Python", "NLP"]},
                {"name": "PostMortemAI", "desc": "AI technical audit report generator from multiple POVs", "tech": ["LLM", "Audit"]},
                {"name": "Tenderlytics", "desc": "AI bid qualification automating legal tender parsing", "tech": ["NLP", "LegalTech"]},
                {"name": "LendBuddy", "desc": "Multilingual n8n loan advisor on WhatsApp", "tech": ["n8n", "WhatsApp"]}
            ]
        },
        {
            "title": "⚙️ Platforms, Tools &amp; Web3",
            "color": "#a855f7", # purple
            "x": 860, "y": 370, "w": 380, "h": 320,
            "projects": [
                {"name": "Klytik", "desc": "Freelance gig lead generator Rust Chrome extension", "tech": ["Rust", "Chrome Ext"]},
                {"name": "Fundify", "desc": "DeFi crowdfunding platform with DAO governance", "tech": ["DeFi", "DAO"]}
            ]
        }
    ]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">')
    svg.append('<style type="text/css">')
    svg.append('<![CDATA[')
    svg.append('  .bg { fill: #0a0e17; rx: 16px; stroke: #1a4a7a; stroke-width: 1.5; }')
    svg.append('  .hdr { font-family: SFMono-Regular,Consolas,monospace; font-size: 15px; font-weight: bold; fill: #e6edf3; }')
    svg.append('  .subhdr { font-family: SFMono-Regular,Consolas,monospace; font-size: 11px; fill: #8b949e; }')
    svg.append('  .cat-title { font-family: SFMono-Regular,Consolas,monospace; font-size: 12px; font-weight: bold; }')
    svg.append('  .p-title { font-family: SFMono-Regular,Consolas,monospace; font-size: 11px; font-weight: bold; fill: #ffffff; }')
    svg.append('  .p-desc { font-family: SFMono-Regular,Consolas,monospace; font-size: 9.5px; fill: #8b949e; }')
    svg.append('  .pill-bg { fill: #1c2536; rx: 4px; }')
    svg.append('  .pill-txt { font-family: SFMono-Regular,Consolas,monospace; font-size: 8.5px; fill: #00f0ff; font-weight: bold; }')
    svg.append(']]>')
    svg.append('</style>')

    # Background
    svg.append(f'  <rect class="bg" width="{width}" height="{height}" x="0" y="0"/>')

    # Header
    svg.append('  <text x="40" y="36" class="hdr">🚀 15 PROJECTS DEEPTECH ECOSYSTEM MATRIX</text>')
    svg.append('  <text x="1240" y="36" class="subhdr" text-anchor="end">PRIAANSH GUPTA • SILICON TO SOFTWARE ⚡</text>')
    svg.append('  <line x1="40" y1="48" x2="1240" y2="48" stroke="#1a4a7a" stroke-width="1.2"/>')

    # Render Clusters
    for c in clusters:
        cx, cy, cw, ch = c['x'], c['y'], c['w'], c['h']
        ccolor = c['color']

        # Cluster box
        svg.append(f'  <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="10" fill="#0d1220" stroke="{ccolor}" stroke-width="1.2" opacity="0.95"/>')
        svg.append(f'  <text x="{cx + 14}" y="{cy + 24}" class="cat-title" fill="{ccolor}">{c["title"]}</text>')
        svg.append(f'  <line x1="{cx + 14}" y1="{cy + 34}" x2="{cx + cw - 14}" y2="{cy + 34}" stroke="{ccolor}" stroke-opacity="0.3" stroke-width="1"/>')

        # Projects inside cluster
        curr_y = cy + 50
        for p in c["projects"]:
            svg.append(f'    <g transform="translate({cx + 14}, {curr_y})">')
            svg.append(f'      <circle cx="4" cy="-4" r="3" fill="{ccolor}"/>')
            svg.append(f'      <text x="14" y="0" class="p-title">{p["name"]}</text>')
            svg.append(f'      <text x="14" y="14" class="p-desc">{p["desc"]}</text>')
            
            # Tech pills
            tx = 14
            for t in p["tech"]:
                tw = len(t) * 6 + 10
                svg.append(f'      <rect x="{tx}" y="20" width="{tw}" height="14" class="pill-bg"/>')
                svg.append(f'      <text x="{tx + tw/2}" y="30" class="pill-txt" text-anchor="middle">{t}</text>')
                tx += tw + 6

            svg.append(f'    </g>')
            curr_y += 52

    svg.append('</svg>')

    with open('priaansh-projects-matrix.svg', 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))
    print("Generated valid XML priaansh-projects-matrix.svg successfully!")

if __name__ == "__main__":
    generate_projects_matrix_svg()
