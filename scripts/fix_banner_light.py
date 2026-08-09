with open('priaansh-banner-light.svg', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('image x="722" y="152" width="558" height="522"', 'image x="690" y="140" width="600" height="600"')

with open('priaansh-banner-light.svg', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully updated priaansh-banner-light.svg image coordinates')
