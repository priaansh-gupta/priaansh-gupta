import urllib.request
import json
import random
import os

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
    random.seed(42) # repeatable randomized poop delays per cell
    raw_days = fetch_real_contributions("priaansh-gupta")

    cols = 52
    rows = 7
    cell_size = 10
    gap = 3
    offset_x = 55
    offset_y = 35
    width = 750
    height = 165
    dur = 16.0 # seconds loop

    bg_empty = "#161b22"
    # Cyber palette matching contribution levels 0..4
    color_levels = {
        0: "#161b22",
        1: "#0e4429",
        2: "#006d32",
        3: "#26a641",
        4: "#39d353"
    }

    # Map raw_days to grid (52 weeks x 7 days)
    # Take the last 52*7 = 364 days
    grid_cells = {}
    if len(raw_days) >= 364:
        recent_days = raw_days[-364:]
        for idx, day in enumerate(recent_days):
            c = idx // 7
            r = idx % 7
            level = day.get('level', 0)
            count = day.get('count', 0)
            grid_cells[(c, r)] = {
                'level': level,
                'count': count,
                'color': color_levels.get(level, bg_empty)
            }
    else:
        # Fallback grid
        for c in range(cols):
            for r in range(rows):
                lvl = random.choice([0, 0, 1, 2, 3, 4])
                grid_cells[(c, r)] = {'level': lvl, 'count': lvl * 2, 'color': color_levels[lvl]}

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
        # Default serpentine path across center
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
        delay = random.uniform(2.5, 9.0)
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
    svg.append('  .bg { fill: #0a0e17; rx: 14px; stroke: #1a4a7a; stroke-width: 1.5; }')
    svg.append('  .title { font-family: SFMono-Regular,Consolas,monospace; font-size: 11px; fill: #8b949e; font-weight: bold; }')
    svg.append('</style>')

    # Background rect
    svg.append(f'  <rect class="bg" width="{width}" height="{height}" x="0" y="0"/>')
    svg.append(f'  <text x="20" y="22" class="title">🐍 REAL-TIME CONTRIBUTION SNAKE — EAT &amp; RANDOM POOP LOOP 💩</text>')
    
    # Days labels
    svg.append('  <g font-family="monospace" font-size="9" fill="#656d76">')
    svg.append(f'    <text x="20" y="{offset_y + 1 * 13 + 8}">Mon</text>')
    svg.append(f'    <text x="20" y="{offset_y + 3 * 13 + 8}">Wed</text>')
    svg.append(f'    <text x="20" y="{offset_y + 5 * 13 + 8}">Fri</text>')
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

    # Snake Motion (Head + Body)
    svg.append(f'  <g>')
    svg.append(f'    <circle r="6" fill="#00f0ff" filter="drop-shadow(0 0 6px #00f0ff)">')
    svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" repeatCount="indefinite"/>')
    svg.append(f'    </circle>')
    svg.append(f'    <circle r="1.5" fill="#0a0e17">')
    svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" repeatCount="indefinite"/>')
    svg.append(f'    </circle>')

    delays = [0.15, 0.30, 0.45, 0.60]
    body_colors = ["#22d65e", "#22d65e", "#3b82f6", "#f59e0b"]
    for i, d_time in enumerate(delays):
        b_col = body_colors[i]
        svg.append(f'    <circle r="{5 - i * 0.6:.1f}" fill="{b_col}" opacity="0.85">')
        svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" begin="-{d_time}s" repeatCount="indefinite"/>')
        svg.append(f'    </circle>')

    svg.append(f'  </g>')

    # Legend at bottom
    svg.append('  <g font-family="monospace" font-size="9" fill="#8b949e" transform="translate(520, 152)">')
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
    print("Generated real-time priaansh-snake.svg successfully!")

if __name__ == "__main__":
    generate_snake_svg()
