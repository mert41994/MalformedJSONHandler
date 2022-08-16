# False State is solved but should be checked.
# trailing comma has been solved.

s = open(r"C:\Users\Emre Mert\Desktop\Yeni klasör (2)\corrupted-file.json").read()
out = open(r"C:\Users\Emre Mert\Desktop\Yeni klasör (2)\output.json", 'w')

in_key = False
reverse = False


def is_num(c):
    return c.isdigit() or c in ['.', '-']


def read_until(s, i, token):
    value = ''
    prev = None
    while i + len(token) < len(s):
        if s[i:i + len(token)] == token and prev != '\\':
            break
        value += s[i]
        prev = s[i]
        i += 1
    return value


i = 0  # skip initial "
line = 1
while i < len(s) - 2:  # skip trailing " and \n
    c = s[i]
    i += 1

    if i == 1:
        in_key = True
        out.write('[\n')  # Adding Starting Bracket.
    if i == len(s) + 1:
        in_key = True
        out.write(']')  # Adding Ending Bracket.
    if c == '{':
        in_key = True
        out.write('{')  # Reformatting
    elif c == '}':
        out.write('}\n')  # Reformatting
        line += 1
    elif c == '[':
        out.write('[')  # Reformatting
    elif c == ']':
        out.write(']')  # Reformatting
    elif c == ':':
        in_key = False
        out.write(':')  # Reformatting
    elif c == ',':
        in_key = True
        out.write(',')  # Reformatting
    elif c == ',' and s[i] == ' ':
        in_key = True
        out.write('')  # Reformatting

    elif is_num(c):
        v = c
        while i < len(s) and is_num(s[i]):
            v += s[i]
            i += 1
        i += 1
        out.write(v)
        if v != '0':
            out.write('0')
        out.write(', ')  # adds , on last item on the list, bug.

    elif c == 'n' and s[i] == 'a' and s[i + 1] == 'n':
        i += 2
        out.write('null')
        pass
    elif c == 'f' and s[i] == 'a' and s[i + 1] == 'l' and s[i + 2] == 's' and s[i + 3] == 'e':
        i += 4
        out.write("false")  # bool states not working properly. This is why this condition added.
        pass
    elif c == 't' and s[i] == 'r' and s[i + 1] == 'u' and s[i + 2] == 'e':
        i += 3
        out.write("true")  # bool states not working properly. This is why this condition added.
        pass
    elif c.isspace():
        pass
    elif c == '\\' and s[i] == '"':
        if not in_key:
            reverse = True
    elif c == '"':
        v = ''
        if not reverse:
            v = read_until(s, i, '"')
            i += len(v) + 1
        else:
            v = read_until(s, i, '\\"')
            i += len(v) + 2
            reverse = False
        if v.endswith('", '):
            v = v[:-3]
            i -= 3  # go back to comma
        if v.endswith('\\"}, {'):
            v = v[:-6]
            i -= 5  # go back to }

        if not in_key:
            v = v.replace('\\', '').replace('"', '\\"')
        out.write('"')
        out.write(v)
        out.write('"')
    else:
        print([i])
        print(c)
        # break

out.close()
