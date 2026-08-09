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

def generate_snake_svg():
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

    bg_empty = "#161b22"
    # Cyber theme contribution levels 0..4
    color_levels = {
        0: "#161b22",
        1: "#0e4429",
        2: "#006d32",
        3: "#26a641",
        4: "#39d353"
    }

    # Map raw_days to grid (52 weeks x 7 days)
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
            # Track month label positions
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

    # Build snake path visiting active contribution cells (level > 0)
    active_coords = [(c, r) for (c, r), info in grid_cells.items() if info['level'] > 0]
    
    # Sort active coords into a serpentine snake path
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

    # Assign eat & poop timings for each active cell on path
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

    # Build SVG
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">')
    svg.append('<style>')
    svg.append('  .bg { fill: #0a0e17; rx: 12px; stroke: #1a4a7a; stroke-width: 1.5; }')
    svg.append('  .lbl { font-family: SFMono-Regular,Consolas,monospace; font-size: 9px; fill: #656d76; }')
    svg.append('</style>')

    # Background rect
    svg.append(f'  <rect class="bg" width="{width}" height="{height}" x="0" y="0"/>')
    
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

    # Render Grid Cells
    for c in range(cols):
        for r in range(rows):
            x = offset_x + c * (cell_size + gap)
            y = offset_y + r * (cell_size + gap)
            cell_info = grid_cells.get((c, r), {'color': bg_empty})
            init_color = cell_info['color']

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

                svg.append(f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{init_color}">')
                svg.append(f'    <animate attributeName="fill" values="{values}" keyTimes="{key_times}" dur="{dur}s" repeatCount="indefinite"/>')
                svg.append(f'  </rect>')
            else:
                svg.append(f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{init_color}"/>')

    # Snake Motion (CORRECTED DIRECTION: Head leads, body segments TRAIL behind!)
    # Head at begin=0s
    svg.append(f'  <g>')
    # Snake Head (glowing cyan circle, r=5.5)
    svg.append(f'    <circle r="5.5" fill="#00f0ff" filter="drop-shadow(0 0 5px #00f0ff)">')
    svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" repeatCount="indefinite"/>')
    svg.append(f'    </circle>')
    # Snake Eye (tiny dark dot on head)
    svg.append(f'    <circle r="1.5" fill="#0a0e17">')
    svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" repeatCount="indefinite"/>')
    svg.append(f'    </circle>')

    # Body segments trailing behind head
    # To trail 0.15s, 0.30s, 0.45s, 0.60s behind head during a 18.0s loop:
    # begin = -(dur - delay)
    body_offsets = [0.18, 0.36, 0.54, 0.72]
    body_radii = [4.8, 4.2, 3.6, 3.0]
    body_colors = ["#38bdf8", "#22d65e", "#4ade80", "#f59e0b"]

    for i, offset in enumerate(body_offsets):
        begin_val = f"-{dur - offset:.2f}s"
        r_val = body_radii[i]
        c_val = body_colors[i]
        svg.append(f'    <circle r="{r_val}" fill="{c_val}" opacity="0.9">')
        svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" begin="{begin_val}" repeatCount="indefinite"/>')
        svg.append(f'    </circle>')

    svg.append(f'  </g>')

    # Legend at bottom right
    svg.append('  <g class="lbl" transform="translate(520, 150)">')
    svg.append('    <text x="0" y="0">Less</text>')
    svg.append('    <rect x="28" y="-8" width="9" height="9" rx="2" fill="#161b22"/>')
    svg.append('    <rect x="40" y="-8" width="9" height="9" rx="2" fill="#0e4429"/>')
    svg.append('    <rect x="52" y="-8" width="9" height="9" rx="2" fill="#006d32"/>')
    svg.append('    <rect x="64" y="-8" width="9" height="9" rx="2" fill="#26a641"/>')
    svg.append('    <rect x="76" y="-8" width="9" height="9" rx="2" fill="#39d353"/>')
    svg.append('    <text x="90" y="0">More 💩</text>')
    svg.append('  </g>')

    svg.append('</svg>')

    with open('priaansh-snake.svg', 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))
    print("Generated Platane-styled priaansh-snake.svg with forward snake motion & poop loop!")

if __name__ == "__main__":
    generate_snake_svg()
