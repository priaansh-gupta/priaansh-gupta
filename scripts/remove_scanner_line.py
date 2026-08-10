import re

def remove_scanner_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to remove the Scanner Line group
    pattern = r'<!-- Scanner Line -->\s*<g clip-path="url\(#charBox\)">.*?</g>'
    new_content = re.sub(pattern, '<!-- Scanner Line Removed -->', content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Successfully removed scanner line from {filepath}')
    else:
        print(f'Scanner line pattern not found in {filepath}')

remove_scanner_from_file('priaansh-banner.svg')
remove_scanner_from_file('priaansh-banner-light.svg')
