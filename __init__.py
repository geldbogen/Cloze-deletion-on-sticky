from aqt.addcards import AddCards
from aqt import gui_hooks
import re
import os

# def remove_colons(s:str):
#     reversed_s = s[::-1]
#     rgx=r"\}\}.*?::!(\dc|\d\dc)"
#     reversed_s = re.sub(rgx, "}}", reversed_s)
#     normal_s = reversed_s[::-1]
#     return normal_s

# print(remove_colons("{{c13::This::remove!}} {{c1::ist}} {{c12::a}} "))


def find_clozed_expressions(s:str,n:int):
    """removes the cloze {{cn:: ___ }} from string"""
    compare_string="c" + str(n) +"::"
    i=0
    counter=0
    destroy_set=set()
    
    colons_counted = 0
    destroying_mode = False
    colon_search = False

    two_digits = (n>=10)
    
    while True:
        try:
            buffer_string=str(s[i])+str(s[i+1])
            if buffer_string=="{{":
                if two_digits:
                    check_string=s[i+2]+s[i+3]+s[i+4]+s[i+5]+s[i+6]
                    #check_string=cxy::
                else:
                    check_string=s[i+2]+s[i+3]+s[i+4]+s[i+5]
                    #check_string=cx::
                try:
                    if check_string==compare_string:
                        if counter==0:
                            #add to counter 
                            #add indices of characters which get destroyed
                            colon_search = True
                            destroy_set.add(i)
                            destroy_set.add(i+1)
                            destroy_set.add(i+2)
                            destroy_set.add(i+3)
                            destroy_set.add(i+4)
                            destroy_set.add(i+5)
                            if two_digits:
                                destroy_set.add(i+6)
                            counter+=1
                    elif counter!=0:
                        counter+=1
                except IndexError:
                    pass
            if buffer_string=="}}":
                colon_search = False
                destroying_mode = False
                colons_counted = 0
                old_counter=counter
                counter=max(counter-1,0)
                if counter==0 and old_counter!=counter:
                    destroy_set.add(i)
                    destroy_set.add(i+1)
                    destroying_mode = False
            if buffer_string == "::" and colon_search:
                colons_counted +=1
                if colons_counted == 2 :
                    destroy_set.add(i)
                    destroying_mode = True
        except IndexError:
            break
        if destroying_mode:
            destroy_set.add(i)
        i+=1

    return_list=[str(char) for i,char in enumerate(s) if i not in destroy_set]
    return_string="".join(return_list)
    return return_string





def modified_load_new_note(self, sticky_fields_from = None) -> None:
    note = self._new_note()
    if old_note := sticky_fields_from:
        flds = note.note_type()["flds"]
        # copy fields from old note
        if old_note:
            for n in range(min(len(note.fields), len(old_note.fields))):
                if flds[n]["sticky"]:
                    if True:
                        old_note_copy = old_note.fields[n]
                        for i in range(100):
                            old_note_copy = find_clozed_expressions(old_note_copy,i)
                        note.fields[n] = old_note_copy
                    else:
                        note.fields[n] = old_note.fields[n]
        # and tags
        note.tags = old_note.tags
    self.setAndFocusNote(note)


AddCards._load_new_note = modified_load_new_note
