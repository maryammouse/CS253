def escape_html(s):
    to_replace = ['&', '>', '<', '"']
    replacement = {'>' : '&gt;', '<' : '&lt;', '"' : '&quot;', '&': '&amp;'}
    for stuff in to_replace:
        if stuff in s:
            s = s.replace(stuff, replacement[stuff])
    return s



print escape_html('Coriander <is> a "very" beautiful <girl! & I love her <lots!>')

#print escape_html('I < love > you')

print escape_html('<')



test = 'Rosalene & Azhoran & Aurielle'

expendables = {'Aurielle': 'Maialynn', 'Azhoran': 'Rosalene'}
test = test.replace('Aurielle', expendables['Aurielle'])

print test

silly = 'There is definitely an & in this OK!?'
replacement = {'>' : '&gt;', '<' : '&lt;', '"' : '&quot;', '&': 'other'}
if '&' in silly:
    silly = silly.replace('&', replacement['&'])

print silly


