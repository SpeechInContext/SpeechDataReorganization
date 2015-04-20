import os
import shutil
import subprocess
import csv

from acousticsim.praat.textgrid import TextGrid

praatpath = r'C:\Users\michael\Documents\Praat\praatcon.exe'

old_ati = r'C:\Users\michael\Documents\Data\ATI'

fixed = r'C:\Users\michael\Documents\Data\ATI_new'

genders = ['Male','Female']

model_dir = os.path.join(old_ati,'Models')

shadow_dir = os.path.join(old_ati,'Shadowers')

def reset():
    if os.path.exists(fixed):
        shutil.rmtree(fixed)

    os.mkdir(fixed)
    os.makedirs(os.path.join(fixed,'Models','Male'))
    os.makedirs(os.path.join(fixed,'Models','Female'))

    os.makedirs(os.path.join(fixed,'Shadowers','Male'))
    os.makedirs(os.path.join(fixed,'Shadowers','Female'))

    shutil.copy2(os.path.join(old_ati, 'axb.txt'),os.path.join(fixed, 'axb.txt'))

def organize_models():
    for g in genders:
        for s in os.listdir(os.path.join(model_dir,g)):
            new_speak_dir = os.path.join(fixed,'Models',g,s)
            os.makedirs(new_speak_dir)
            speak_dir = os.path.join(model_dir,g,s)
            for f in os.listdir(speak_dir):
                name,ext = os.path.splitext(f)
                l = name.split('_')
                word = l[3]
                newname = '{}_{}{}'.format(s,word,ext)
                if ext == '.wav':
                    shutil.copy2(os.path.join(speak_dir,f),os.path.join(new_speak_dir,newname))
                elif ext == '.TextGrid':
                    subprocess.call([praatpath, 'standardize_textgrid.praat',
                                            os.path.join(speak_dir,f),
                                            os.path.join(new_speak_dir,newname)])


def organize_shadowers():
    for g in genders:
        for s in os.listdir(os.path.join(shadow_dir,g)):
            new_speak_dir = os.path.join(fixed,'Shadowers',g,s)
            os.makedirs(new_speak_dir)
            speak_dir = os.path.join(shadow_dir,g,s)
            for p in os.listdir(speak_dir):
                if p == 'Baseline':
                    for f in os.listdir(os.path.join(speak_dir,p)):

                        name,ext = os.path.splitext(f)
                        l = name.split('-')
                        word = l[-1]
                        newname = '{}_{}_{}{}'.format(s,word,'baseline',ext)
                        if ext == '.wav':
                                shutil.copy2(os.path.join(speak_dir,p,f),
                                os.path.join(new_speak_dir,newname))
                        elif ext == '.TextGrid':
                                subprocess.call([praatpath, 'trim_textgrid.praat',
                                            os.path.join(speak_dir,p,f),
                                            os.path.join(new_speak_dir,newname)])
                else:
                    for ms in os.listdir(os.path.join(speak_dir,p)):
                        if ms.endswith('.wav') or ms.endswith('.TextGrid'):
                            continue
                        for f in os.listdir(os.path.join(speak_dir,p,ms)):
                            name,ext = os.path.splitext(f)
                            l = name.split('-')
                            word = l[-1]
                            newname = '{}_{}_shadowing{}{}'.format(s,word,ms, ext)
                            if ext == '.wav':
                                shutil.copy2(os.path.join(speak_dir,p,ms,f),os.path.join(new_speak_dir,newname))
                            elif ext == '.TextGrid':
                                subprocess.call([praatpath, 'trim_textgrid.praat',
                                            os.path.join(speak_dir,p,ms,f),
                                            os.path.join(new_speak_dir,newname)])


def wav_files():
    data_dir = fixed
    model_dir = os.path.join(data_dir, 'Models')
    shadower_dir = os.path.join(data_dir, 'Shadowers')
    female_models = os.listdir(os.path.join(model_dir,'Female'))
    male_models = os.listdir(os.path.join(model_dir,'Male'))
    female_shadowers = os.listdir(os.path.join(shadower_dir,'Female'))
    male_shadowers = os.listdir(os.path.join(shadower_dir,'Male'))

    path_mapping = list()
    with open(os.path.join(data_dir,'axb.txt'),'r') as f:
        reader = csv.DictReader(f, delimiter = '\t')
        for line in reader:
            shadower = line['Shadower'][-3:]
            model = line['Model'][-3:]
            word = line['Word']
            if model in female_models:
                model_path = os.path.join(model_dir, 'Female',model, '{}_{}.wav'.format(model,word))
            else:
                model_path = os.path.join(model_dir, 'Male',model, '{}_{}.wav'.format(model,word))
            if shadower in female_shadowers:
                baseline_path = os.path.join(shadower_dir, 'Female',shadower, '{}_{}_baseline.wav'.format(shadower,word))
                shadowed_path = os.path.join(shadower_dir, 'Female',shadower, '{}_{}_shadowing{}.wav'.format(shadower,word, model))
            else:
                baseline_path = os.path.join(shadower_dir, 'Male',shadower, '{}_{}_baseline.wav'.format(shadower,word))
                shadowed_path = os.path.join(shadower_dir, 'Male',shadower, '{}_{}_shadowing{}.wav'.format(shadower,word, model))
            path_mapping.extend([baseline_path, model_path, shadowed_path])
    return list(set(path_mapping))

class TextGridError(Exception):
    pass

def get_vowel_points(textgrid_path, tier_name = 'Vowel', vowel_label = 'V'):
    tg = TextGrid()
    tg.read(textgrid_path)
    vowel_tier = tg.getFirst(tier_name)
    for i in vowel_tier:
        if i.mark == vowel_label:
            begin = i.minTime
            end = i.maxTime
            break
    else:
        raise(TextGridError('No vowel label was found in \'{}\'.'.format(textgrid_path)))
    return begin, end

def validate_models():
    files = wav_files()
    for f in files:
        if not os.path.exists(f):
            print('File not found: ',f)

        textgrid_path = os.path.splitext(f)[0] + '.TextGrid'
        try:
            get_vowel_points(textgrid_path)
        except TextGridError:
            print('Problem with textgrid: ',textgrid_path)



if __name__ == '__main__':
    reset()
    organize_models()
    organize_shadowers()
    validate_models()
