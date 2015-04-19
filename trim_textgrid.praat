

form Variables
    sentence filename
    sentence outname
endform

Read from file... 'filename$'

num_intervals = Get number of intervals... 1

for i from 1 to num_intervals
    label$ = Get label of interval... 1 'i'
    if label$ == "word"
        start = Get start point... 1 'i'
        end = Get end point... 1 'i'
        Extract part... 'start' 'end' no
        Save as text file... 'outname$'
        goto done
    endif
endfor
label done
