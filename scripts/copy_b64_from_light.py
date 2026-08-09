with open('priaansh-banner-light.svg', 'r', encoding='utf-8') as f:
    light = f.read()

start_tag = 'href="data:image/png;base64,'
idx_light = light.find(start_tag)
if idx_light != -1:
    end_light = light.find('"', idx_light + len(start_tag))
    b64_str = light[idx_light + len(start_tag):end_light]
    print(f'Extracted base64 string length: {len(b64_str)}')
    
    with open('priaansh-banner.svg', 'r', encoding='utf-8') as f:
        dark = f.read()
    
    idx_dark = dark.find(start_tag)
    if idx_dark != -1:
        end_dark = dark.find('"', idx_dark + len(start_tag))
        new_dark = dark[:idx_dark + len(start_tag)] + b64_str + dark[end_dark:]
        with open('priaansh-banner.svg', 'w', encoding='utf-8') as f:
            f.write(new_dark)
        print('Successfully copied base64 string from light banner into priaansh-banner.svg!')
    else:
        print('start_tag not found in dark banner')
else:
    print('start_tag not found in light banner')
