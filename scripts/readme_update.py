anti_dupe_text = ''
admin_text = ''
extension_text = ''
readme = ''

with open('anti-dupe.md', 'r') as f:
    anti_dupe_text = f.read()

with open('admin.md', 'r') as f:
    admin_text = f.read()

with open('extension.md', 'r') as f:
    extension_text = f.read()

# read the stub
with open('stubs/README.stub', 'r') as f:
    stub = f.read()
    readme = stub.replace('{ANTI}', anti_dupe_text);
    readme = readme.replace('{ADMIN}', admin_text);
    readme = readme.replace('{EXT}', extension_text);

with open('README.md','w') as f:
    f.write(readme)