import os, json
cwd = os.getcwd()
while True:
    k = 0
    p = []
    s = []
    i = input()
    f = os.listdir(i)
    if i.split('\\')[-1]+'.json' in os.listdir(cwd):
        with open(i.split('\\')[-1] + '.json') as file:
            k = json.load(file)
    with open(i.split('\\')[-1]+'.json', 'w') as file:
        json.dump(f, file)
    if not k == 0:
        for d in k:
            if d not in f:
                p.append(d)
            if d in f:
                s.append(d)
        print('Deleted files from last request: '+str(p))
        print('Files created again: '+str(s))
    if k == 0:
        print('Folder never registered before, therefore it was created now')
    print('File data: '+str(f))
    print('Json file named after last folder: {} of the request: {} is present'.format(str(i.split('\\')[-1]+'.json'), i))
    print('As can be seen in the script folder files list:'+str(os.listdir(cwd)))