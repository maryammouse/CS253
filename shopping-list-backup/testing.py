def escape_html(s):
    to_replace = ['>', '<', '"', '&']
    replacement = {'>' : '&gt;', '<' : '&lt;', '"' : '&quot;', '&': '&amp;'}
    for stuff in to_replace:
        if stuff in s:
            s = s.replace(stuff, replacement[stuff])
            return s


print escape_html('Plenty of <, >, ", and & in here! Replace them ALL!')


stupid = '<, >, "'

print stupid.replace('<', '&lt;')

to_replace = ['>', '<', '"', '&']
replacement = {'>' : '&gt;', '<' : '&lt;', '"' : '&quot;', '&': '&amp;'}

for stuff in stupid:
    if stuff in to_replace:
        stupid.replace(stuff, replacement[stuff])

print stupid
