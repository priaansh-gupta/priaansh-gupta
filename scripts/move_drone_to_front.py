import re

drone_pattern = r'(<!-- 🛸 FLYING CYBER PATROL DRONE -->\s*<g>.*?</g>)'

def move_drone_front(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(drone_pattern, content, flags=re.DOTALL)
    if match:
        drone_code = match.group(1)
        # Remove drone from original position
        content_no_drone = re.sub(drone_pattern, '', content, flags=re.DOTALL)
        # Insert drone right before </svg>
        new_content = content_no_drone.replace('</svg>', '\n' + drone_code + '\n</svg>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Successfully moved Drone in front of Avatar in {filepath}')
    else:
        print(f'Drone group not found in {filepath}')

move_drone_front('priaansh-banner.svg')
move_drone_front('priaansh-banner-light.svg')
