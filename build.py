import os
import shutil

dist_dir = 'dist'
if os.path.exists(dist_dir):
    shutil.rmtree(dist_dir)
os.makedirs(dist_dir)

templates_dir = 'templates'
for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        shutil.copy(os.path.join(templates_dir, filename), dist_dir)

with open(os.path.join(dist_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI智能教室调研</title>
  <meta http-equiv="refresh" content="0;url=/survey.html">
</head>
<body>
  <p>正在重定向...</p>
</body>
</html>
''')

print('Build completed successfully!')
