import sys
js=open('src/tool.js',encoding='utf8').read()
assert 'ǂ' not in js and '</script' not in js.lower()
w=open('src/widget.html',encoding='utf8').read()
out=w.replace('/*@@JS@@*/',js.replace('&','ǂ'))
open('dist/widget.html','w',encoding='utf8').write(out)
print(len(out))
