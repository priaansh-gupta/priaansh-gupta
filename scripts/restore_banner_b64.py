with open('avatar_full_b64.txt', 'r', encoding='utf-8') as f:
    b64 = f.read().strip()

print(f'Base64 length: {len(b64)}')

with open('priaansh-banner.svg', 'r', encoding='utf-8') as f:
    banner = f.read()

start_tag = 'href="data:image/png;base64,'
idx = banner.find(start_tag)
if idx != -1:
    end_idx = banner.find('"', idx + len(start_tag))
    new_banner = banner[:idx + len(start_tag)] + b64 + banner[end_idx:]
    with open('priaansh-banner.svg', 'w', encoding='utf-8') as f:
        f.write(new_banner)
    print('Successfully restored full base64 avatar in priaansh-banner.svg!')
else:
    print('start_tag not found!')
