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
    offset_y = 30
    width = 750
    height = 165
    dur = 18.0 # seconds loop

    bg_empty = "#0d1220"
    # Cyber-Neon Robotic Palette matching Banner, Lanyard & Stats cards
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

    # Serpentine track path for the Cyber Rover visiting active checkpoint cells
    active_coords = [(c, r) for (c, r), info in grid_cells.items() if info['level'] > 0]
    active_coords.sort(key=lambda item: (item[0], item[1] if item[0] % 2 == 0 else -item[1]))

    path_coords = []
    if active_coords:
        for c, r in active_coords:
            px = offset_x + c * (cell_size + gap) + cell_size / 2
            py = offset_y + r * (cell_size + gap) + cell_size / 2
            path_coords.append((c, r, px, py))
    else:
        for c in range(cols):
            r = 3 if c % 2 == 0 else 4
            px = offset_x + c * (cell_size + gap) + cell_size / 2
            py = offset_y + r * (cell_size + gap) + cell_size / 2
            path_coords.append((c, r, px, py))

    path_d = "M " + " L ".join([f"{px:.1f},{py:.1f}" for _, _, px, py in path_coords])
    num_steps = max(len(path_coords), 1)

    cell_anim_data = {}
    for idx, (c, r, px, py) in enumerate(path_coords):
        t_eat = (idx / num_steps) * dur
        delay = random.uniform(3.0, 10.0)
        t_poop = (t_eat + delay) % dur
        cell_anim_data[(c, r)] = {
            't_eat': t_eat,
            't_poop': t_poop,
            'color': grid_cells[(c, r)]['color']
        }

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">')
    svg.append('<style>')
    svg.append('  .bg { fill: #0a0e17; rx: 12px; stroke: #1a4a7a; stroke-width: 1.5; }')
    svg.append('  .lbl { font-family: SFMono-Regular,Consolas,monospace; font-size: 9px; fill: #8b949e; font-weight: bold; }')
    svg.append('</style>')

    # Background
    svg.append(f'  <rect class="bg" width="{width}" height="{height}" x="0" y="0"/>')
    svg.append(f'  <text x="40" y="18" class="lbl" fill="#00f0ff">🏎️ AUTONOMOUS CYBER ROVER — COMMIT CHECKPOINT TRACK 🏁</text>')
    
    # Month labels
    svg.append('  <g class="lbl">')
    for c, m_name in month_labels:
        x_pos = offset_x + c * (cell_size + gap)
        svg.append(f'    <text x="{x_pos}" y="18">{m_name}</text>')
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
            cell_info = grid_cells.get((c, r), {'color': bg_empty})
            init_color = cell_info['color']
            border_attr = ' stroke="#1a4a7a" stroke-width="0.5"' if cell_info['level'] == 0 else ''

            if (c, r) in cell_anim_data:
                anim = cell_anim_data[(c, r)]
                t_eat = anim['t_eat']
                t_poop = anim['t_poop']
                p_color = anim['color']

                k_eat = t_eat / dur
                k_poop = t_poop / dur

                if k_eat < k_poop:
                    key_times = f"0; {k_eat:.3f}; {k_poop:.3f}; 1"
                    values = f"{init_color}; {bg_empty}; {p_color}; {p_color}"
                else:
                    key_times = f"0; {k_poop:.3f}; {k_eat:.3f}; 1"
                    values = f"{p_color}; {p_color}; {bg_empty}; {bg_empty}"

                svg.append(f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{init_color}"{border_attr}>')
                svg.append(f'    <animate attributeName="fill" values="{values}" keyTimes="{key_times}" dur="{dur}s" repeatCount="indefinite"/>')
                svg.append(f'  </rect>')
            else:
                svg.append(f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{init_color}"{border_attr}/>')

    # Cyber Rover Motion (Car Chassis, Headlights, Tail Trail)
    svg.append(f'  <g>')
    # Front Headlight Glow Beam
    svg.append(f'    <polygon points="0,-4 14,-10 14,10 0,4" fill="#00f0ff" opacity="0.4">')
    svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" repeatCount="indefinite"/>')
    svg.append(f'    </polygon>')
    # Cyber Rover Main Chassis (Rect 12x7, rx=2)
    svg.append(f'    <rect x="-6" y="-3.5" width="12" height="7" rx="2" fill="#00f0ff" stroke="#0a0e17" stroke-width="1" filter="drop-shadow(0 0 5px #00f0ff)">')
    svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" repeatCount="indefinite"/>')
    svg.append(f'    </rect>')
    # Rover Wheels / Details
    svg.append(f'    <circle r="1.2" fill="#22d65e">')
    svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" repeatCount="indefinite"/>')
    svg.append(f'    </circle>')

    # Exhaust / Checkpoint Neon Trail (trailing behind car chassis)
    trail_offsets = [0.18, 0.36, 0.54, 0.72]
    trail_radii = [4.5, 3.8, 3.0, 2.2]
    trail_colors = ["#3b82f6", "#22d65e", "#f59e0b", "#a855f7"]

    for i, offset in enumerate(trail_offsets):
        begin_val = f"-{dur - offset:.2f}s"
        r_val = trail_radii[i]
        c_val = trail_colors[i]
        svg.append(f'    <circle r="{r_val}" fill="{c_val}" opacity="0.85">')
        svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" begin="{begin_val}" repeatCount="indefinite"/>')
        svg.append(f'    </circle>')

    svg.append(f'  </g>')

    # Legend
    svg.append('  <g class="lbl" transform="translate(520, 150)">')
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
    print("Generated priaansh-car-track.svg successfully!")

if __name__ == "__main__":
    generate_car_track_svg()
