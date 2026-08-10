def generate_compact_projects_matrix_svg():
    width = 1280
    height = 410
    
    # 15 exact projects in 5 compact clusters
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">')
    svg.append('<style type="text/css">')
    svg.append('<![CDATA[')
    svg.append('  .bg { fill: #0a0e17; rx: 14px; stroke: #1a4a7a; stroke-width: 1.5; }')
    svg.append('  .hdr { font-family: SFMono-Regular,Consolas,monospace; font-size: 13px; font-weight: bold; fill: #e6edf3; }')
    svg.append('  .subhdr { font-family: SFMono-Regular,Consolas,monospace; font-size: 10px; fill: #8b949e; }')
    svg.append('  .cat-title { font-family: SFMono-Regular,Consolas,monospace; font-size: 11px; font-weight: bold; }')
    svg.append('  .p-name { font-family: SFMono-Regular,Consolas,monospace; font-size: 10px; font-weight: bold; fill: #ffffff; }')
    svg.append('  .p-desc { font-family: SFMono-Regular,Consolas,monospace; font-size: 8.5px; fill: #8b949e; }')
    svg.append('  .pill-bg { fill: #1c2536; rx: 3px; }')
    svg.append('  .pill-txt { font-family: SFMono-Regular,Consolas,monospace; font-size: 8px; fill: #00f0ff; font-weight: bold; }')
    svg.append(']]>')
    svg.append('</style>')

    # Background
    svg.append(f'  <rect class="bg" width="{width}" height="{height}" x="0" y="0"/>')

    # Header
    svg.append('  <text x="30" y="28" class="hdr">🚀 15 PROJECTS DEEPTECH ECOSYSTEM MATRIX</text>')
    svg.append('  <text x="1250" y="28" class="subhdr" text-anchor="end">PRIAANSH GUPTA • SILICON TO SOFTWARE ⚡</text>')
    svg.append('  <line x1="30" y1="36" x2="1250" y2="36" stroke="#1a4a7a" stroke-width="1"/>')

    # Helper to draw a project item
    def draw_project(x, y, name, desc, tech, dot_color):
        res = []
        res.append(f'    <g transform="translate({x}, {y})">')
        res.append(f'      <circle cx="3" cy="-3" r="2.5" fill="{dot_color}"/>')
        res.append(f'      <text x="10" y="0" class="p-name">{name}</text>')
        res.append(f'      <text x="10" y="11" class="p-desc">{desc}</text>')
        tx = 10
        for t in tech:
            tw = len(t) * 5.5 + 8
            res.append(f'      <rect x="{tx}" y="15" width="{tw}" height="12" class="pill-bg"/>')
            res.append(f'      <text x="{tx + tw/2}" y="23.5" class="pill-txt" text-anchor="middle">{t}</text>')
            tx += tw + 4
        res.append(f'    </g>')
        return "\n".join(res)

    # 1. Robotics & Hardware (Col 1, Top)
    svg.append('  <rect x="30" y="48" width="390" height="165" rx="8" fill="#0d1220" stroke="#00f0ff" stroke-width="1.2"/>')
    svg.append('  <text x="42" y="66" class="cat-title" fill="#00f0ff">🤖 Autonomous Robotics &amp; Hardware</text>')
    svg.append('  <line x1="42" y1="72" x2="408" y2="72" stroke="#00f0ff" stroke-opacity="0.3"/>')
    svg.append(draw_project(42, 88, "FarmBot", "Webots agri omni-directional robot with 6-DOF arm", ["ROS2", "Webots"], "#00f0ff"))
    svg.append(draw_project(42, 128, "Drone-Powered Race Cars", "Repurposed drone propulsion for RC race cars", ["Hardware", "Motors"], "#00f0ff"))
    svg.append(draw_project(42, 168, "Autonomous Edge Devices", "Voice obstacle car &amp; SLAM Micromouse", ["SLAM", "Edge AI"], "#00f0ff"))

    # 2. Vision & Edge AI (Col 2, Top)
    svg.append('  <rect x="445" y="48" width="390" height="165" rx="8" fill="#0d1220" stroke="#22d65e" stroke-width="1.2"/>')
    svg.append('  <text x="457" y="66" class="cat-title" fill="#22d65e">👁️ Computer Vision &amp; Edge AI</text>')
    svg.append('  <line x1="457" y1="72" x2="823" y2="72" stroke="#22d65e" stroke-opacity="0.3"/>')
    svg.append(draw_project(457, 88, "CASTA", "Counter-Drone C-UAS drone &amp; trajectory tracking", ["YOLO", "TensorRT"], "#22d65e"))
    svg.append(draw_project(457, 128, "Fabguard-AI", "Real-time SEM wafer defect detection", ["CV", "PyTorch"], "#22d65e"))
    svg.append(draw_project(457, 168, "SafeScan", "Mobile app identifying harmful ingredients &amp; allergens", ["Flutter", "CV"], "#22d65e"))

    # 3. Hardware & IoT (Col 3, Top)
    svg.append('  <rect x="860" y="48" width="390" height="165" rx="8" fill="#0d1220" stroke="#f59e0b" stroke-width="1.2"/>')
    svg.append('  <text x="872" y="66" class="cat-title" fill="#f59e0b">⚡ Hardware, Circuits &amp; IoT</text>')
    svg.append('  <line x1="872" y1="72" x2="1238" y2="72" stroke="#f59e0b" stroke-opacity="0.3"/>')
    svg.append(draw_project(872, 88, "CGS (Circuit Graphic Symphony)", "Text → schematics &amp; SPICE netlists framework", ["JavaScript", "SPICE"], "#f59e0b"))
    svg.append(draw_project(872, 134, "Smart Medical Scale", "IoT healthcare load cell &amp; HX711 patient device", ["IoT", "HX711"], "#f59e0b"))

    # 4. Multimodal AI & Assistants (Col 1 & 2, Bottom - Wide Card)
    svg.append('  <rect x="30" y="225" width="805" height="165" rx="8" fill="#0d1220" stroke="#3b82f6" stroke-width="1.2"/>')
    svg.append('  <text x="42" y="243" class="cat-title" fill="#3b82f6">🧠 Multimodal AI, LLMs &amp; Assistants</text>')
    svg.append('  <line x1="42" y1="249" x2="823" y2="249" stroke="#3b82f6" stroke-opacity="0.3"/>')
    # Left Sub-column
    svg.append(draw_project(42, 265, "PetPal", "Dog health voice/video AI vet consultations", ["Flutter", "Gemini", "Firebase"], "#3b82f6"))
    svg.append(draw_project(42, 305, "Hapticus", "Digital text &amp; PDF to tactile Braille pipeline", ["Python", "NLP"], "#3b82f6"))
    svg.append(draw_project(42, 345, "PostMortemAI", "AI audit report generator from multiple POVs", ["LLM", "Audit"], "#3b82f6"))
    # Right Sub-column
    svg.append(draw_project(445, 265, "Tenderlytics", "AI bid qualification automating legal tender parsing", ["NLP", "LegalTech"], "#3b82f6"))
    svg.append(draw_project(445, 305, "LendBuddy", "Multilingual n8n loan advisor on WhatsApp", ["n8n", "WhatsApp"], "#3b82f6"))

    # 5. Platforms & Web3 (Col 3, Bottom)
    svg.append('  <rect x="860" y="225" width="390" height="165" rx="8" fill="#0d1220" stroke="#a855f7" stroke-width="1.2"/>')
    svg.append('  <text x="872" y="243" class="cat-title" fill="#a855f7">⚙️ Platforms, Tools &amp; Web3</text>')
    svg.append('  <line x1="872" y1="249" x2="1238" y2="249" stroke="#a855f7" stroke-opacity="0.3"/>')
    svg.append(draw_project(872, 265, "Klytik", "Freelance gig lead generator Rust Chrome extension", ["Rust", "Chrome Ext"], "#a855f7"))
    svg.append(draw_project(872, 305, "Fundify", "DeFi crowdfunding platform with DAO governance", ["DeFi", "DAO"], "#a855f7"))

    svg.append('</svg>')

    with open('priaansh-projects-matrix.svg', 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))
    print("Generated compact priaansh-projects-matrix.svg (height 410px) successfully!")

if __name__ == "__main__":
    generate_compact_projects_matrix_svg()
