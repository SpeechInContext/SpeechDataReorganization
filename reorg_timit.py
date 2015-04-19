import os
import shutil

orig = r'C:\Users\michael\Documents\Data\TIMIT Corpus\TIMIT'
newwav = r'C:\Users\michael\Documents\Data\other_timit'

final_out = r'C:\Users\michael\Documents\Data\TIMIT_fixed'

orig_train = os.path.join(orig,'TRAIN')
orig_test = os.path.join(orig,'TEST')

TIMIT_DRS = ['DR1','DR2','DR3','DR4','DR5','DR6','DR7','DR8']

shutil.rmtree(final_out)

os.mkdir(final_out)

shutil.copytree(os.path.join(orig,'DOC'),os.path.join(final_out,'DOC'))

os.mkdir(os.path.join(final_out,'TEST'))
os.mkdir(os.path.join(final_out,'TRAIN'))

#for dr in TIMIT_DRS:
#   os.mkdir(os.path.join(final_out,'TEST',dr))
#   os.mkdir(os.path.join(final_out,'TRAIN',dr))

for root, subdirs, files in os.walk(orig_train):
    print(root)
    for f in files:
        speaker = os.path.basename(root)
        dr = os.path.basename(os.path.dirname(root))
        final_dr_path = os.path.join(final_out,'TRAIN',dr)
        if not os.path.exists(final_dr_path):
            os.mkdir(final_dr_path)
        final_speaker_path = os.path.join(final_dr_path,speaker)
        if not os.path.exists(final_speaker_path):
            os.mkdir(final_speaker_path)
        if f.lower().endswith('.wav'):
            wavname = '.'.join([dr,speaker,f.split('.')[0]])+'.WAV'
            shutil.copy2(os.path.join(newwav,wavname),os.path.join(final_speaker_path,f))
        else:
            shutil.copy2(os.path.join(root,f),os.path.join(final_speaker_path,f))

for root, subdirs, files in os.walk(orig_test):
    print(root)
    for f in files:
        speaker = os.path.basename(root)
        dr = os.path.basename(os.path.dirname(root))
        final_dr_path = os.path.join(final_out,'TEST',dr)
        if not os.path.exists(final_dr_path):
            os.mkdir(final_dr_path)
        final_speaker_path = os.path.join(final_dr_path,speaker)
        if not os.path.exists(final_speaker_path):
            os.mkdir(final_speaker_path)
        if f.lower().endswith('.wav'):
            wavname = '.'.join([dr,speaker,f.split('.')[0]])+'.WAV'
            shutil.copy2(os.path.join(newwav,wavname),os.path.join(final_speaker_path,f))
        else:
            shutil.copy2(os.path.join(root,f),os.path.join(final_speaker_path,f))
