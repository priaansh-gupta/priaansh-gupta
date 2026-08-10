import urllib.request
import json
import random
import os
from datetime import datetime

def fetch_real_contributions(username="priaansh-gupta"):
    url = f"https://github-contributions-api.jogruber.de/v4/{username}?y=last"
    headers = {'User-Agent': 'Mozilla/5.0'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('contributions', [])
    except Exception as e:
        print(f"Warning: Could not fetch live contributions ({e}), fallback to fallback grid.")
        return []

def generate_car_track_svg():
    random.seed(42)
    raw_days = fetch_real_contributions("priaansh-gupta")

    cols = 52
    rows = 7
    cell_size = 10
    gap = 3
    offset_x = 40
    offset_y = 40  # Header title at y=16, month labels at y=31
    width = 750
    height = 175
    dur = 25.0     # Smooth 25s full circuit driving loop

    bg_empty = "#0d1220"
    color_levels = {
        0: "#0d1220",
        1: "#1a4a7a", # dark blue
        2: "#3b82f6", # electric blue
        3: "#00f0ff", # glowing cyan
        4: "#22d65e"  # neon green
    }

    grid_cells = {}
    month_labels = []
    
    if len(raw_days) >= 364:
        recent_days = raw_days[-364:]
        last_month = None
        for idx, day in enumerate(recent_days):
            c = idx // 7
            r = idx % 7
            level = day.get('level', 0)
            count = day.get('count', 0)
            date_str = day.get('date', '')
            grid_cells[(c, r)] = {
                'level': level,
                'count': count,
                'color': color_levels.get(level, bg_empty),
                'date': date_str
            }
            if r == 0 and date_str:
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    m_name = dt.strftime("%b")
                    if m_name != last_month:
                        month_labels.append((c, m_name))
                        last_month = m_name
                except:
                    pass
    else:
        for c in range(cols):
            for r in range(rows):
                lvl = random.choice([0, 0, 1, 2, 3, 4])
                grid_cells[(c, r)] = {'level': lvl, 'count': lvl * 2, 'color': color_levels[lvl], 'date': ''}

    # Continuous smooth autonomous rover driving road across grid terrain
    road_coords = []
    for c in range(cols):
        r_range = range(rows) if c % 2 == 0 else range(rows - 1, -1, -1)
        for r in r_range:
            px = offset_x + c * (cell_size + gap) + cell_size / 2
            py = offset_y + r * (cell_size + gap) + cell_size / 2
            road_coords.append((c, r, px, py))

    path_d = "M " + " L ".join([f"{px:.1f},{py:.1f}" for _, _, px, py in road_coords])
    total_road_steps = len(road_coords)

    # Checkpoint activation timestamps as rover passes each cell
    cell_anim_data = {}
    for idx, (c, r, px, py) in enumerate(road_coords):
        t_pass = (idx / total_road_steps) * dur
        cell_anim_data[(c, r)] = {
            't_pass': t_pass,
            'color': grid_cells.get((c, r), {}).get('color', bg_empty),
            'level': grid_cells.get((c, r), {}).get('level', 0)
        }

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">')
    svg.append('<defs>')
    svg.append('  <linearGradient id="roverHeadlight" x1="0" y1="0" x2="1" y2="0">')
    svg.append('    <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.8"/>')
    svg.append('    <stop offset="100%" stop-color="#00f0ff" stop-opacity="0.0"/>')
    svg.append('  </linearGradient>')
    svg.append('</defs>')
    svg.append('<style>')
    svg.append('  .bg { fill: #0a0e17; rx: 12px; stroke: #1a4a7a; stroke-width: 1.5; }')
    svg.append('  .title { font-family: SFMono-Regular,Consolas,monospace; font-size: 11px; fill: #00f0ff; font-weight: bold; }')
    svg.append('  .lbl { font-family: SFMono-Regular,Consolas,monospace; font-size: 9px; fill: #8b949e; font-weight: bold; }')
    svg.append('</style>')

    # Background
    svg.append(f'  <rect class="bg" width="{width}" height="{height}" x="0" y="0"/>')
    
    # Header Title (Clean y=16 without overlap)
    svg.append(f'  <text x="40" y="16" class="title">🏎️ AUTONOMOUS CYBER ROVER — COMMIT CHECKPOINT TRACK 🏁</text>')
    
    # Month labels (Clean y=31 below header title!)
    svg.append('  <g class="lbl">')
    for c, m_name in month_labels:
        x_pos = offset_x + c * (cell_size + gap)
        svg.append(f'    <text x="{x_pos}" y="31">{m_name}</text>')
    svg.append('  </g>')

    # Day labels
    svg.append('  <g class="lbl">')
    svg.append(f'    <text x="12" y="{offset_y + 1 * 13 + 8}">Mon</text>')
    svg.append(f'    <text x="12" y="{offset_y + 3 * 13 + 8}">Wed</text>')
    svg.append(f'    <text x="12" y="{offset_y + 5 * 13 + 8}">Fri</text>')
    svg.append('  </g>')

    # Render Grid Cells (Checkpoints)
    for c in range(cols):
        for r in range(rows):
            x = offset_x + c * (cell_size + gap)
            y = offset_y + r * (cell_size + gap)
            cell_info = grid_cells.get((c, r), {'color': bg_empty, 'level': 0})
            final_color = cell_info['color']
            level = cell_info['level']
            border_attr = ' stroke="#1a4a7a" stroke-width="0.5"' if level == 0 else ''

            if (c, r) in cell_anim_data and level > 0:
                t_pass = cell_anim_data[(c, r)]['t_pass']
                k_pass = t_pass / dur
                key_times = f"0; {k_pass:.3f}; 1"
                values = f"{bg_empty}; {final_color}; {final_color}"

                svg.append(f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{bg_empty}"{border_attr}>')
                svg.append(f'    <animate attributeName="fill" values="{values}" keyTimes="{key_times}" dur="{dur}s" repeatCount="indefinite"/>')
                svg.append(f'  </rect>')
            else:
                svg.append(f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{final_color}"{border_attr}/>')

    # Realistic Cyber Rover Vehicle Model (<g> facing forward, rotate="auto")
    svg.append(f'  <g>')
    # Front Headlight Searchlight Cone Beam
    svg.append(f'    <g>')
    svg.append(f'      <polygon points="10,0 30,-10 30,10" fill="url(#roverHeadlight)" opacity="0.75"/>')
    svg.append(f'      <animateMotion path="{path_d}" rotate="auto" dur="{dur}s" repeatCount="indefinite"/>')
    svg.append(f'    </g>')

    # Cyber Rover Body Assembly
    svg.append(f'    <g>')
    # 4 All-Terrain Treaded Wheels
    svg.append(f'      <rect x="-9" y="-8.5" width="6" height="3" rx="1" fill="#1a4a7a" stroke="#00f0ff" stroke-width="0.8"/>')
    svg.append(f'      <rect x="3" y="-8.5" width="6" height="3" rx="1" fill="#1a4a7a" stroke="#00f0ff" stroke-width="0.8"/>')
    svg.append(f'      <rect x="-9" y="5.5" width="6" height="3" rx="1" fill="#1a4a7a" stroke="#00f0ff" stroke-width="0.8"/>')
    svg.append(f'      <rect x="3" y="5.5" width="6" height="3" rx="1" fill="#1a4a7a" stroke="#00f0ff" stroke-width="0.8"/>')
    # Main Body Frame
    svg.append(f'      <rect x="-10" y="-6" width="20" height="12" rx="3" fill="#0d1220" stroke="#00f0ff" stroke-width="1.5"/>')
    # Front Cyber Bumper
    svg.append(f'      <rect x="9" y="-4" width="3" height="8" rx="1" fill="#22d65e"/>')
    # Central Glowing LiDAR / Sensor Dome
    svg.append(f'      <circle cx="-1" cy="0" r="3" fill="#00f0ff"/>')
    svg.append(f'      <circle cx="-1" cy="0" r="1.2" fill="#ffffff"/>')
    # Status Antenna LEDs
    svg.append(f'      <circle cx="-6" cy="-3" r="1" fill="#f59e0b"/>')
    svg.append(f'      <circle cx="-6" cy="3" r="1" fill="#22d65e"/>')
    # Trailing Rear Energy Flame
    svg.append(f'      <polygon points="-10,-3 -18,-5 -13,0 -18,5 -10,3" fill="#f59e0b" opacity="0.85"/>')

    svg.append(f'      <animateMotion path="{path_d}" rotate="auto" dur="{dur}s" repeatCount="indefinite"/>')
    svg.append(f'    </g>')
    svg.append(f'  </g>')

    # Legend
    svg.append('  <g class="lbl" transform="translate(520, 158)">')
    svg.append('    <text x="0" y="0">Less</text>')
    svg.append('    <rect x="28" y="-8" width="9" height="9" rx="2" fill="#0d1220" stroke="#1a4a7a" stroke-width="0.5"/>')
    svg.append('    <rect x="40" y="-8" width="9" height="9" rx="2" fill="#1a4a7a"/>')
    svg.append('    <rect x="52" y="-8" width="9" height="9" rx="2" fill="#3b82f6"/>')
    svg.append('    <rect x="64" y="-8" width="9" height="9" rx="2" fill="#00f0ff"/>')
    svg.append('    <rect x="76" y="-8" width="9" height="9" rx="2" fill="#22d65e"/>')
    svg.append('    <text x="90" y="0">More 🏁</text>')
    svg.append('  </g>')

    svg.append('</svg>')

    with open('priaansh-car-track.svg', 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))
    print("Generated smooth vehicle Cyber Rover priaansh-car-track.svg successfully!")

if __name__ == "__main__":
    generate_car_track_svg()
