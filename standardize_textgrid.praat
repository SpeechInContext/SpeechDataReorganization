

form Variables
    sentence filename
    sentence outname
endform

Read from file... 'filename$'

num_intervals = Get number of intervals... 1

vowel_start = Get start point... 1 2
vowel_end = Get end point... 1 2

num_tiers = Get number of tiers

for i from 2 to num_tiers
    Remove tier... 'i'
endfor

Set tier name... 1 Vowel



Set interval text... 1 1 U
Set interval text... 1 2 V
if num_intervals == 3
    Set interval text... 1 3 U
endif

Insert interval tier... 1 Word
Set interval text... 1 1 word
Save as text file... 'outname$'
