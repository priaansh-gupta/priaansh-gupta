import re

drone_defs = '''
    <linearGradient id="droneLight" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#00f0ff" stop-opacity="0.0"/>
    </linearGradient>
'''

drone_group = '''
<!-- 🛸 FLYING CYBER PATROL DRONE -->
<g>
  <animateTransform attributeName="transform" type="translate" values="980,105; 910,80; 1050,130; 980,105" dur="11s" repeatCount="indefinite"/>
  <polygon points="0,12 -130,230 130,230" fill="url(#droneLight)" opacity="0.3">
    <animate attributeName="opacity" values="0.2;0.5;0.2" dur="2.5s" repeatCount="indefinite"/>
  </polygon>
  <line x1="-36" y1="-10" x2="36" y2="10" stroke="#00f0ff" stroke-width="2.5" opacity="0.9"/>
  <line x1="-36" y1="10" x2="36" y2="-10" stroke="#00f0ff" stroke-width="2.5" opacity="0.9"/>
  <ellipse cx="-36" cy="-10" rx="13" ry="3" fill="none" stroke="#22d65e" stroke-width="1.5" opacity="0.85"/>
  <ellipse cx="36" cy="-10" rx="13" ry="3" fill="none" stroke="#22d65e" stroke-width="1.5" opacity="0.85"/>
  <ellipse cx="-36" cy="10" rx="13" ry="3" fill="none" stroke="#22d65e" stroke-width="1.5" opacity="0.85"/>
  <ellipse cx="36" cy="10" rx="13" ry="3" fill="none" stroke="#22d65e" stroke-width="1.5" opacity="0.85"/>
  <rect x="-15" y="-9" width="30" height="18" rx="5" fill="#0d1220" stroke="#00f0ff" stroke-width="1.8"/>
  <circle cx="0" cy="0" r="4" fill="#00f0ff">
    <animate attributeName="fill" values="#00f0ff;#22d65e;#00f0ff" dur="2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="-7" cy="-3" r="1.5" fill="#22d65e"/>
  <circle cx="7" cy="-3" r="1.5" fill="#f59e0b"/>
</g>
'''

def add_drone(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'id="droneLight"' not in content:
        content = content.replace('</defs>', drone_defs + '\n</defs>')
    
    if 'FLYING CYBER PATROL DRONE' not in content:
        target_str = '<!-- RIGHT: ILLUSTRATION -->'
        if target_str in content:
            content = content.replace(target_str, drone_group + '\n' + target_str)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Successfully added Patrol Drone to {filepath}')

add_drone('priaansh-banner.svg')
add_drone('priaansh-banner-light.svg')
