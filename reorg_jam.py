import os
import shutil

old_jam = r'C:\Users\michael\Documents\Data\Jam_old'

new_jam = r'C:\Users\michael\Documents\Data\JAM_new'

fixed_jam = r'C:\Users\michael\Documents\Data\JAM'

if os.path.exists(fixed_jam):
    shutil.rmtree(fixed_jam)

os.mkdir(fixed_jam)

for root, subdirs, files in os.walk(new_jam):
    for f in files:
        if not f.lower().endswith('.wav'):
            continue
        name = os.path.splitext(f)[0]
        if 'wrong' in name:
            continue
        print(name)
        speaker, word, prod = name.split('_')
        if speaker.startswith('7'):
            IS = True
        else:
            IS = False


        if prod == 'BaselineList':
            prod = 'baseline'
        elif prod == 'ExposureList1':
            prod = 'shadowedone'
        elif prod == 'ExposureList2':
            prod = 'shadowedtwo'
        elif prod == 'ExposureList3':
            prod = 'shadowedthree'
        elif prod == 'PostExpList':
            prod = 'posttask'
        else:
            raise(Exception(name))

        speakerdir = os.path.join(fixed_jam, speaker)
        if not os.path.exists(speakerdir):
            os.mkdir(speakerdir)
        newname = '_'.join([speaker,word,prod]) + '.wav'
        shutil.copy2(os.path.join(root,f),os.path.join(speakerdir,newname))

for root, subdirs, files in os.walk(old_jam):
    for f in files:
        if not f.lower().endswith('.wav'):
            continue
        name = os.path.splitext(f)[0]
        if 'wrong' in name:
            continue
        if name == 'modeltalker':
            continue
        print(name)
        speaker, name = name.split('_')
        if speaker.startswith('7') and speaker.endswith('IS'):
            IS = True
            speaker = speaker[:-2]
        elif speaker.startswith('7'):
            continue
        else:
            IS = False


        if IS:
            prod = name[-3:]
            word = name[:-3]
            if prod == '1is':
                prod = 'baseline'
            elif prod == '2is':
                prod = 'shadowedone'
            elif prod == '3is':
                prod = 'posttask'
        else:
            if speaker == 'modeltalker':
                prod = ''
                word = name
            else:
                prod = name[-1]
                word = name[:-1]
                if prod == '1':
                    prod = 'baseline'
                else:
                    prod = 'posttask'

        speakerdir = os.path.join(fixed_jam, speaker)
        if not os.path.exists(speakerdir):
            os.mkdir(speakerdir)
        if speaker == 'modeltalker':
            newname = '_'.join([speaker,word]) + '.wav'
        else:
            newname = '_'.join([speaker,word,prod]) + '.wav'
        shutil.copy2(os.path.join(root,f),os.path.join(speakerdir,newname))
