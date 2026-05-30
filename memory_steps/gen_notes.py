# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

import html
import re
import time
from dataclasses import dataclass

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
PUNCT = re.compile(r"([，。！？；：、,.!?;:\n])")
WORD_RE = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’-][A-Za-zÀ-ÖØ-öø-ÿ]+)*|"
    r"[0-9]+|[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]|\s+|[^\w\s]",
    re.UNICODE,
)

@dataclass
class LineItem:
    collection_id: str
    collection_title: str
    line_index: int
    label: str
    answer: str
    memorization_mode: str
    anchor_profile: str
    layout_profile: str
    step_1: str; step_2: str; step_3: str; step_4: str; step_5: str; step_6: str
    step_7: str; step_8: str; step_9: str; step_10: str; step_11: str; step_12: str
    step_1_label: str; step_2_label: str; step_3_label: str; step_4_label: str; step_5_label: str; step_6_label: str
    step_7_label: str; step_8_label: str; step_9_label: str; step_10_label: str; step_11_label: str; step_12_label: str

def tokens(text):
    return WORD_RE.findall(text)

def is_word(token):
    return bool(re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’-][A-Za-zÀ-ÖØ-öø-ÿ]+)*$", token))

def is_cjk_token(token):
    return len(token) == 1 and bool(CJK.match(token))

def is_mem_char(char):
    return bool(CJK.match(char)) or (char.isalpha() and not char.isspace())

def word_blank(token):
    width = max(2, min(18, sum(1 for char in token if char.isalnum())))
    return f'<span class="ms-blank" style="--ch:{width}"></span>'

def char_mask(token, mask='＿'):
    return ''.join(mask if is_mem_char(char) else char for char in token)

def mask_token(token, mask='＿'):
    return word_blank(token) if is_word(token) else char_mask(token, mask)

def keep_every_n(text, n=2, offset=0, mask='＿'):
    out=[]; idx=0
    for char in text:
        if is_mem_char(char):
            out.append(char if idx % n == offset else mask); idx += 1
        else:
            out.append(char)
    return ''.join(out)

def punctuation_skeleton(text, mask='＿'):
    return ''.join(mask if is_mem_char(char) else char for char in text)

def chunks(text):
    out=[]; cur=''
    for part in PUNCT.split(text):
        if not part: continue
        cur += part
        if PUNCT.fullmatch(part):
            out.append(cur); cur=''
    if cur: out.append(cur)
    return out

def first_last_per_phrase(text, mask='＿'):
    result=[]
    for chunk in chunks(text):
        chars=list(chunk); ids=[i for i,char in enumerate(chars) if is_mem_char(char)]
        for idx in ids[1:-1]: chars[idx]=mask
        result.append(''.join(chars))
    return ''.join(result)

def anchor_prompt(text, keywords=None, mask='＿'):
    keywords=[kw for kw in (keywords or []) if kw]
    keep=[False]*len(text); lowered=text.lower()
    for keyword in sorted(keywords, key=len, reverse=True):
        start=0; key=keyword.lower()
        while True:
            pos=lowered.find(key,start)
            if pos < 0: break
            for idx in range(pos, min(pos+len(keyword), len(text))): keep[idx]=True
            start=pos+len(keyword)
    return ''.join(char if keep[idx] or not is_mem_char(char) else mask for idx,char in enumerate(text))

def word_initials(text, mask='＿', every=None, offset=0):
    out=[]; word_idx=0
    for token in tokens(text):
        if is_word(token) or is_cjk_token(token):
            out.append(token[0] if every is None or word_idx % every == offset else mask_token(token, mask)); word_idx += 1
        else:
            out.append(token)
    return ''.join(out)

def word_outline(text, mask='＿'):
    out=[]
    for token in tokens(text):
        if is_word(token):
            chars=list(token); letters=[idx for idx,char in enumerate(chars) if char.isalpha()]
            for idx in letters[1:-1]: chars[idx]=mask
            out.append(''.join(chars))
        else:
            out.append(token)
    return ''.join(out)

def hide_vowels(text, mask='＿'):
    return ''.join(mask if char in 'aeiouAEIOU' else char for char in text)

def cloze_every_n_words(text, n, offset, mask='＿'):
    out=[]; word_idx=0
    for token in tokens(text):
        if is_word(token) or is_cjk_token(token):
            out.append(mask_token(token, mask) if word_idx % n == offset else token); word_idx += 1
        else:
            out.append(token)
    return ''.join(out)

def clause_starts(text, mask='＿'):
    out=[]; at_start=True
    for token in tokens(text):
        if is_word(token) or is_cjk_token(token):
            out.append(token if at_start else mask_token(token, mask)); at_start=False
        else:
            out.append(token)
            if token in ['.','!','?',';',':','。','！','？','；','：','\n']:
                at_start=True
    return ''.join(out)

def label_first(text, label):
    for token in tokens(text):
        if is_word(token) or is_cjk_token(token):
            return f'{label} · {token}'
    return label

def first_char_punctuation(text, mask='＿'):
    out=[]; seen=False
    for char in text:
        if is_mem_char(char):
            out.append(char if not seen else mask); seen=True
        else:
            out.append(char)
    return ''.join(out)

def detect_layout(text, requested='Auto-detect'):
    if requested != 'Auto-detect':
        return {'CJK character layout':'layout-cjk','Latin word layout':'layout-latin','Mixed layout':'layout-mixed'}.get(requested,'layout-mixed')
    cjk_count=len(CJK.findall(text)); latin_count=sum(1 for char in text if char.isalpha() and not CJK.match(char))
    return 'layout-mixed' if cjk_count and latin_count else ('layout-cjk' if cjk_count >= latin_count else 'layout-latin')

def normalize_pasted_text(text):
    text=text.replace('\r\n','\n').replace('\r','\n').replace('\u3000',' ')
    text=re.sub(r'[ \t]+',' ',text).strip()
    closers = r'["”’\'»」』）\)\]\}]*'
    end_punc = r'[。！？；;.!?]'
    text=re.sub(f'({end_punc}{closers})\\s*(?=\\d{{1,3}}\\s+[\\u3400-\\u4dbf\\u4e00-\\u9fffA-Za-z])', r'\1\n', text)
    text=re.sub(f'({end_punc}{closers})\\s*(?=\\d{{1,3}}\\s*[:：]\\s*\\d{{1,3}}\\s+)', r'\1\n', text)
    return '\n'.join(line.strip() for line in text.split('\n') if line.strip())

def parse_label_content(line, fallback_index):
    text=line.strip()
    patterns=[
        r'^(?P<label>\d{1,3}\s*[:：]\s*\d{1,3})\s*(?P<content>.+)$',
        r'^(?P<label>\d{1,3})[\.、\)]?\s+(?P<content>.+)$',
        r'^(?P<label>[A-Za-z]+\s*\d{1,3})[:：]?\s+(?P<content>.+)$',
    ]
    for pattern in patterns:
        match=re.match(pattern,text)
        if match:
            return match.group('label').strip(), match.group('content').strip()
    return str(fallback_index), text

def build_steps(content, label, mode, keywords=None, mask='＿'):
    mode=mode or 'CJK Character Steps'
    if mode == 'Word Initial Steps':
        values=[content, word_initials(content,mask), word_initials(content,mask,2,0), word_initials(content,mask,2,1), word_initials(content,mask,3,0), clause_starts(content,mask), anchor_prompt(content,keywords,mask), punctuation_skeleton(content,mask), f'{label} · {word_initials(content,mask)}', label_first(content,label), f'{label} · {punctuation_skeleton(content,mask)}', label]
        labels=['Read / full line','Word initials','Alternating word initials A','Alternating word initials B','Sparse word initials','Clause starts only','Anchor words','Punctuation skeleton','Label + word initials','Label + first word','Label + punctuation','Label only']
    elif mode == 'Word Outline Steps':
        values=[content, word_outline(content,mask), word_initials(content,mask), hide_vowels(content,mask), cloze_every_n_words(content,4,3,mask), cloze_every_n_words(content,3,2,mask), cloze_every_n_words(content,2,1,mask), anchor_prompt(content,keywords,mask), clause_starts(content,mask), punctuation_skeleton(content,mask), label_first(content,label), label]
        labels=['Read / full line','Word outlines','Word initials','Vowels hidden','Every fourth word hidden','Every third word hidden','Every other word hidden','Anchor words','Clause starts only','Punctuation skeleton','Label + first word','Label only']
    elif mode == 'Cloze Word Steps':
        values=[content, cloze_every_n_words(content,6,5,mask), cloze_every_n_words(content,5,4,mask), cloze_every_n_words(content,4,3,mask), cloze_every_n_words(content,3,2,mask), cloze_every_n_words(content,2,1,mask), cloze_every_n_words(content,2,0,mask), anchor_prompt(content,keywords,mask), clause_starts(content,mask), punctuation_skeleton(content,mask), label_first(content,label), label]
        labels=['Read / full line','Cloze every sixth word','Cloze every fifth word','Cloze every fourth word','Cloze every third word','Cloze every other word A','Cloze every other word B','Anchor words','Clause starts only','Punctuation skeleton','Label + first word','Label only']
    else:
        values=[content, keep_every_n(content,2,0,mask), keep_every_n(content,2,1,mask), keep_every_n(content,3,0,mask), keep_every_n(content,4,0,mask), keep_every_n(content,5,0,mask), first_last_per_phrase(content,mask), anchor_prompt(content,keywords,mask), punctuation_skeleton(content,mask), first_char_punctuation(content,mask), label_first(content,label), label]
        labels=['Read / full line','Alternating characters A','Alternating characters B','Every third character','Every fourth character','Every fifth character','First/last per phrase','Anchor words','Punctuation skeleton','First character + punctuation','Label + first character','Label only']
    return values, labels

def process_lines(text, title, collection_id=None, mask='＿', keywords=None, auto_split=True, memorization_mode='CJK Character Steps', anchor_profile='General / Mixed Text', layout_request='Auto-detect'):
    if auto_split:
        text=normalize_pasted_text(text)
    collection_id = collection_id or 'ms-%d' % int(time.time()*1000)
    out=[]
    for idx,line in enumerate([line.strip() for line in text.splitlines() if line.strip()],1):
        label, content = parse_label_content(line, idx)
        values, labels = build_steps(content, label, memorization_mode, keywords, mask)
        out.append(LineItem(collection_id,title,idx,label,content,memorization_mode,anchor_profile,detect_layout(content,layout_request),*values,*labels))
    return out

def context_for(data, idx, window=1):
    previous=[item for item in data if idx-window <= item.line_index < idx]
    next_items=[item for item in data if idx < item.line_index <= idx+window]
    return '<br>'.join(f'{html.escape(item.label)} {html.escape(item.answer)}' for item in previous) or '【Start】', '<br>'.join(f'{html.escape(item.label)} {html.escape(item.answer)}' for item in next_items)
