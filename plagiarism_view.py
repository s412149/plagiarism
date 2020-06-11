# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 20:32:59 2020

@author: agato
"""
import statistics
from collections import Counter
import re
from difflib import SequenceMatcher
import tkinter as tk
from tkinter import filedialog


def get_file1():
    file_path1.set(filedialog.askopenfilename())
    
def get_file2():
    file_path2.set(filedialog.askopenfilename())

def open_file():
    filename1 = file_path1.get()
    file1 = open(filename1,'r' ,encoding ='utf8')
    text1 = file1.read()
    file1.close()
    filename2 = file_path2.get()
    file2 = open(filename2,'r' ,encoding ='utf8')
    text2 = file2.read()
    file2.close()
    text1st.set(text1)
    text2nd.set(text2)

def save_results():
    f = filedialog.asksaveasfile(mode='w', defaultextension = 'txt')
    if f is None:
        return
    f.write('1st file: \nStyle: ' + style1.get() + 
            '\nVariety: ' + accent1.get() + 
            '\nMost common words: '+ top5a.get() + 
            '\nWords per sentence: '+ str(word_per1.get()) + '\n' + '\n' +
            '2nd file: \nStyle: ' + style2.get() + 
            '\nVariety: ' + accent2.get() + 
            '\nMost common words: '+ top5b.get() + 
            '\nWords per sentence: '+ str(word_per2.get()) + '\n'
            '\n' + prob_text.get() + 
            '\n' + plagiat_text.get())
    f.close()
    
    
def contractions():
    text1 = text1st.get().lower()
    text2 = text2nd.get().lower()
    text = [text1, text2]
    style = []
    i=0
    for i in range(0,2):
        pattern = r'\w+\'[^s]+\b'
        match = re.findall(pattern, text[i])
        count = 0
        for m in match:
            count += 1
        if count > 0:
            st = 'informal'
            style.append(st)
        else:
            st = 'formal'
            style.append(st)
    style1.set(style[0])
    style2.set(style[1])

def variety():
    text1 = text1st.get().lower()
    text1 = text1.strip()
    text2 = text2nd.get().lower()
    text2 = text2.strip()
    text = [text1, text2]
    accent = []
    i=0
    for i in range(0,2):
        pattern_brit = r'\w+ys(e|es|ed|ing|er|ers)+\b|\w+our(s|ist|ists|ism|al|ed|abl|hood|ing|er|y|ies)*\b|\w+is(e|es|ed|ing|ingly|ation|er|ers)+\b|\w+mme(s)*\b'
        match_brit = re.findall(pattern_brit,text[i])
        count_brit = 0
        for match in match_brit:
            count_brit += 1
        pattern_ame = r'\w+yz(e|es|ed|ing|er|ers)+\b|\w+or(s|ist|ists|ism|al|ed|abl|hood|ing|er|y|ies)*\b|\w+iz(e|es|ed|ing|ingly|ation|er|ers)+\b|\w+m(s)*\b'
        match_ame = re.findall(pattern_ame, text[i])
        count_ame = 0
        for match in match_ame:
            count_ame += 1
        if count_brit > count_ame:
            acc = 'British'
            accent.append(acc)
        elif count_brit < count_ame:
            acc = 'American'
            accent.append(acc)
        else:
            acc = 'Are you sure your file is written in English?'
            accent.append(acc)
    accent1.set(accent[0])
    accent2.set(accent[1])

def top5():
    text1 = text1st.get().lower()
    text2 = text2nd.get().lower()
    text = [text1, text2]
    top5 = []
    common_words = []
    i=0
    for i in range(0,2):
        counting = dict()
        words = text[i].split()
        for word in words:
            if word in counting:
                counting[word] += 1
            else:
                counting[word] = 1
        sorted_counting = dict(Counter(counting).most_common(5))
        for word in sorted_counting:
            common_words.append(word)
        string_counting = str(sorted_counting)
        breaks = "{}'"
        cleaned_top = ''
        for character in string_counting:
            if character in breaks:
                cleaned_top += ' '
            else :
                cleaned_top += character
        top5.append(cleaned_top)
    top5a.set(top5[0])
    top5b.set(top5[1])
    common1.set(common_words[:5])
    common2.set(common_words[5:])
    
def word_per_sentence():
    text1 = text1st.get().lower()
    text2 = text2nd.get().lower()
    text = [text1, text2]
    i=0
    average =[]
    for i in range(0,2):
        splitters = ".?!;:"
        sentences = []
        sent = ''
        for character in text[i]:
            sent += character
            if character in splitters:
                sentences.append(sent)
                sent = ''      
        word_number = []
        for sentence in sentences:
            count = len(sentence.split())
            word_number.append(count)
        word_ave = statistics.mean(word_number)
        average.append(round(word_ave))
    word_per1.set(average[0])
    word_per2.set(average[1]) 
    
def same_author():
    probability = 0
    if style1.get() == style2.get():
        probability += 1
    if accent1.get() == accent2.get():
        probability +=1
    w_num = 0
    com1 = common1.get()
    com2 = common2.get()
    for i in range(0,5):
        if com1[i] == com2[0] or com1[i] == com2[1] or com1[i] == com2[3] or com1[i] == com2[4]: 
            w_num += 1
    probability = probability + (w_num/5)
    w_per_s1 = word_per1.get()
    w_per_s2 = word_per2.get()
    sen = int(w_per_s1/w_per_s2)
    if w_per_s1 > w_per_s2:
        probability += (sen-1)
    else:
        probability += sen
    prob_same.set((probability*100)/4)
    prob_text.set(str(prob_same.get()) + '% probability that both papers were written by the same author.') 
    
def plagiarism():
    text1 = text1st.get()
    text2 = text2nd.get()
    similarity_ratio = SequenceMatcher(None,text1,text2).ratio()
    similarity_ratio = round(similarity_ratio, 2)
    plagiat.set(similarity_ratio*100)
    plagiat_text.set(str(plagiat.get()) + '% chance of plagiarism in the second paper.')
    
root = tk.Tk()

root.title('Plagiarism checker')
root.configure(background = 'lightblue')
root.iconbitmap('transparent.ico')

menubar = tk.Menu(root)

filemenu = tk.Menu(menubar)
filemenu.add_command(label='Open 1st file', command=get_file1)
filemenu.add_command(label='Open 2nd file', command=get_file2)
filemenu.add_command(label='Save as', command=save_results)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.destroy)
menubar.add_cascade(label='File', menu=filemenu)

root.config(menu=menubar)

for col in range(0,4):
    root.grid_columnconfigure(col, minsize=20)

for row in range(0,15):
    root.grid_rowconfigure(row, minsize=20)

instruction_label = tk.Label(root, text="INSTRUCTION\n1. Choose file 1 and file 2 to compare.\n2 .Click button 'Load the files'\n3. You can save the results as .txt using 'Save' button.").grid(sticky = "W",row=0, column=2, rowspan = 2, padx = 5)

label_intro = tk.Label (root, text = 'Features of the contents:', background = 'lightblue', font = 'calibri 14 bold').grid(row = 3, column = 1, columnspan = 2)

label_style = tk.Label (root, text = 'Style:',background = 'lightblue',font = 'calibri 9 underline').grid(sticky = "W", row = 5, column = 0)
label_variety = tk.Label (root, text = 'Variety:',background = 'lightblue', font = 'calibri 9 underline').grid(sticky = "W", row = 6, column = 0)
label_top5 = tk.Label (root, text = 'Top 5 words:',background = 'lightblue', font = 'calibri 9 underline').grid(sticky = "W", row = 7, column = 0)
label_words = tk.Label (root, text = 'Mean number of words:',background = 'lightblue', font = 'calibri 9 underline').grid(sticky = "W", row = 8, column = 0)

label_plagiarism_checker = tk.Label (root, text = 'Plagiarism checker:',background = 'lightblue',font = 'calibri 14 bold').grid (row = 10, column = 1, columnspan = 2)

label_author = tk.Label (root, text = 'Probability of the same author:',background = 'lightblue', font = 'calibri 9 underline').grid(sticky = "W", row = 13, column = 0)
label_plagiarism = tk.Label (root, text = 'Probability of plagiarism:',background = 'lightblue', font = 'calibri 9 underline').grid(sticky = "W", row = 12, column = 0)


file_path1 = tk.StringVar(root)
file_path1.set('1st File location...')

file_path2 = tk.StringVar(root)
file_path2.set('2nd File location...')


file_label1 = tk.Label(root, textvariable=file_path1,background = 'lightblue').grid(row=0, column=0)

file_label2 = tk.Label(root, textvariable=file_path2,background = 'lightblue').grid(row=1, column=0)


file_button1 = tk.Button(root, text='Choose 1st file ', command = get_file1).grid(row=0, column=1)

file_button2 = tk.Button(root, text='Choose 2nd file', command = get_file2).grid(row=1, column=1)


text1st = tk.StringVar(root)

text2nd = tk.StringVar(root)


style1 = tk.StringVar(root)
style1.set('Formal/Informal')

style1_label = tk.Label(root, textvariable = style1,background = 'lightblue').grid(row=5, column=1)

style2 = tk.StringVar(root)
style2.set('Formal/Informal')

style2_label = tk.Label(root, textvariable = style2,background = 'lightblue').grid(row=5, column=2)


accent1 = tk.StringVar(root)
accent1.set('British/American')

accent1_label = tk.Label(root, textvariable=accent1,background = 'lightblue').grid(row=6, column=1)

accent2 = tk.StringVar(root)
accent2.set('British/American')

accent2_label = tk.Label(root, textvariable=accent2,background = 'lightblue').grid(row=6, column=2)



top5a = tk.StringVar(root)
top5a.set('Most common words')

top5a_label = tk.Label(root, textvariable=top5a,background = 'lightblue').grid(row=7, column=1)

top5b = tk.StringVar(root)
top5b.set('Most common words')

top5b_label = tk.Label(root, textvariable=top5b,background = 'lightblue').grid(row=7, column=2)

common1 = tk.StringVar(root)
common2 = tk.StringVar(root)

    
word_per1 = tk.IntVar(root)
word_per1.set(0)

word_per_sentence1_label = tk.Label(root, textvariable=word_per1,background = 'lightblue').grid(row=8, column=1)

word_per2 = tk.IntVar(root)
word_per2.set(0)

word_per_sentence2_label = tk.Label(root, textvariable=word_per2,background = 'lightblue').grid(row=8, column=2)


prob_same = tk.IntVar(root)
prob_text = tk.StringVar(root)
prob_text.set('%')
prob_same_label = tk.Label(root, textvariable=prob_text, padx = 10,background = 'lightblue').grid(sticky = "W", row=13, column=1)
 

plagiat = tk.IntVar(root)
plagiat_text = tk.StringVar(root)
plagiat_text.set('%')
plagiarism_label = tk.Label(root, textvariable=plagiat_text, padx = 10,background = 'lightblue').grid(sticky = "W", row=12, column=1)


button = tk.Button(text='Load',font = 'calibri 11 bold', command=lambda:[open_file(),contractions(), variety(), top5(), word_per_sentence(), plagiarism(), same_author()]).grid(sticky = "E", row=14, column=2, padx = 5, pady = 10)
    
button_quit = tk.Button(text='Quit', command = root.destroy, font = 'calibri 11 bold').grid(row = 14, column = 4, padx = 5, pady = 10)

button_save = tk.Button(text='Save', command = save_results, font = 'calibri 11 bold').grid(sticky = "E", row = 14, column = 3, padx = 5, pady = 10)



    





















root.mainloop()