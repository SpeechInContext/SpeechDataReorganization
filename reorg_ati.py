import os
import shutil
import subprocess

praatpath = r'C:\Users\michael\Documents\Praat\praatcon.exe'

old_ati = r'C:\Users\michael\Documents\Data\ATI'

fixed = r'C:\Users\michael\Documents\Data\ATI_new'

if os.path.exists(fixed):
    shutil.rmtree(fixed)

os.mkdir(fixed)

os.makedirs(os.path.join(fixed,'Models','Male'))
os.makedirs(os.path.join(fixed,'Models','Female'))

os.makedirs(os.path.join(fixed,'Shadowers','Male'))
os.makedirs(os.path.join(fixed,'Shadowers','Female'))

genders = ['Male','Female']

model_dir = os.path.join(old_ati,'Models')

shadow_dir = os.path.join(old_ati,'Shadowers')

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

#def validate_models():
#   pass

if __name__ == '__main__':
    organize_models()
    organize_shadowers()
    #validate_models()
