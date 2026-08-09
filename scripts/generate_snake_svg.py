import random

def generate_snake_svg():
    random.seed(42) # deterministic for reproducibility
    cols = 50
    rows = 7
    cell_size = 10
    gap = 3
    offset_x = 55
    offset_y = 35
    width = 750
    height = 165
    dur = 16.0 # seconds loop

    # Define colors
    bg_empty = "#161b22"
    colors = ["#00f0ff", "#22d65e", "#3b82f6", "#f59e0b", "#a855f7"]

    # Generate a snake path traversing columns
    # We will pick a winding path through the grid
    path_coords = []
    # Serpentine path visiting some grid cells
    step_cols = list(range(0, cols, 1))
    current_row = 3
    direction = 1

    for c in step_cols:
        x = offset_x + c * (cell_size + gap) + cell_size / 2
        y = offset_y + current_row * (cell_size + gap) + cell_size / 2
        path_coords.append((c, current_row, x, y))
        
        # occasionally change row
        if random.random() < 0.6:
            current_row += direction
            if current_row >= rows:
                current_row = rows - 1
                direction = -1
            elif current_row < 0:
                current_row = 0
                direction = 1
            x = offset_x + c * (cell_size + gap) + cell_size / 2
            y = offset_y + current_row * (cell_size + gap) + cell_size / 2
            path_coords.append((c, current_row, x, y))

    path_d = "M " + " L ".join([f"{px:.1f},{py:.1f}" for _, _, px, py in path_coords])

    # Total points along path
    num_steps = len(path_coords)

    # Map each cell in grid to initial color
    # Some cells are active contribution dots
    active_cells = {}
    for c in range(cols):
        for r in range(rows):
            if random.random() < 0.45:
                active_cells[(c, r)] = random.choice(colors)

    # Determine when cells are eaten (when snake visits them)
    # and when they get "pooped" back randomly!
    cell_anim_data = {}
    for idx, (c, r, px, py) in enumerate(path_coords):
        t_eat = (idx / num_steps) * dur
        if (c, r) not in cell_anim_data:
            # Assign random poop time later in the loop
            delay = random.uniform(2.5, 9.0)
            t_poop = (t_eat + delay) % dur
            cell_anim_data[(c, r)] = {
                't_eat': t_eat,
                't_poop': t_poop,
                'color': active_cells.get((c, r), random.choice(colors))
            }

    # Build SVG content
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">')
    svg.append('<style>')
    svg.append('  .bg { fill: #0a0e17; rx: 14px; stroke: #1a4a7a; stroke-width: 1.5; }')
    svg.append('  .title { font-family: SFMono-Regular,Consolas,monospace; font-size: 11px; fill: #8b949e; font-weight: bold; }')
    svg.append('  .snake-head { fill: #00f0ff; filter: drop-shadow(0 0 4px #00f0ff); }')
    svg.append('  .snake-body { fill: #22d65e; opacity: 0.8; }')
    svg.append('  .poop-sparkle { animation: pop 0.4s ease-out; }')
    svg.append('</style>')

    # Background rect
    svg.append(f'  <rect class="bg" width="{width}" height="{height}" x="0" y="0"/>')
    svg.append(f'  <text x="20" y="22" class="title">🐍 CONTRIBUTION SNAKE — EAT &amp; RANDOM POOP LOOP 💩</text>')
    
    # Days labels (Mon, Wed, Fri)
    svg.append('  <g font-family="monospace" font-size="9" fill="#656d76">')
    svg.append(f'    <text x="20" y="{offset_y + 1 * 13 + 8}">Mon</text>')
    svg.append(f'    <text x="20" y="{offset_y + 3 * 13 + 8}">Wed</text>')
    svg.append(f'    <text x="20" y="{offset_y + 5 * 13 + 8}">Fri</text>')
    svg.append('  </g>')

    # Render Grid Cells with Eat & Poop Animate Keyframes
    for c in range(cols):
        for r in range(rows):
            x = offset_x + c * (cell_size + gap)
            y = offset_y + r * (cell_size + gap)
            init_color = active_cells.get((c, r), bg_empty)

            if (c, r) in cell_anim_data:
                anim = cell_anim_data[(c, r)]
                t_eat = anim['t_eat']
                t_poop = anim['t_poop']
                p_color = anim['color']

                # Create SMIL keytimes/values for eat and poop cycle
                # Normalize times to 0..1
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

    # Snake Motion (Head + Trailing Body)
    # Head
    svg.append(f'  <g>')
    svg.append(f'    <circle r="6" fill="#00f0ff" filter="drop-shadow(0 0 6px #00f0ff)">')
    svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" repeatCount="indefinite"/>')
    svg.append(f'    </circle>')
    # Eyes on snake head
    svg.append(f'    <circle r="1.5" fill="#0a0e17">')
    svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" repeatCount="indefinite"/>')
    svg.append(f'    </circle>')

    # 4 Trailing body segments with delayed motion
    delays = [0.15, 0.30, 0.45, 0.60]
    body_colors = ["#22d65e", "#22d65e", "#3b82f6", "#f59e0b"]
    for i, d_time in enumerate(delays):
        b_col = body_colors[i]
        svg.append(f'    <circle r="{5 - i * 0.6:.1f}" fill="{b_col}" opacity="0.85">')
        svg.append(f'      <animateMotion path="{path_d}" dur="{dur}s" begin="-{d_time}s" repeatCount="indefinite"/>')
        svg.append(f'    </circle>')

    svg.append(f'  </g>')

    # Legend at bottom
    svg.append('  <g font-family="monospace" font-size="9" fill="#8b949e" transform="translate(530, 152)">')
    svg.append('    <text x="0" y="0">Less</text>')
    svg.append('    <rect x="28" y="-8" width="9" height="9" rx="2" fill="#161b22"/>')
    svg.append('    <rect x="40" y="-8" width="9" height="9" rx="2" fill="#3b82f6"/>')
    svg.append('    <rect x="52" y="-8" width="9" height="9" rx="2" fill="#22d65e"/>')
    svg.append('    <rect x="64" y="-8" width="9" height="9" rx="2" fill="#00f0ff"/>')
    svg.append('    <rect x="76" y="-8" width="9" height="9" rx="2" fill="#f59e0b"/>')
    svg.append('    <text x="90" y="0">More 💩</text>')
    svg.append('  </g>')

    svg.append('</svg>')

    with open('priaansh-snake.svg', 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))
    print("Generated priaansh-snake.svg successfully!")

if __name__ == "__main__":
    generate_snake_svg()
