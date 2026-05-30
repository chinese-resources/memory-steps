# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

MODEL_NAME='Memory Steps: Line-by-Line Memorizer'
FIELDS=['collection_id', 'collection_title', 'line_index', 'label', 'answer', 'memorization_mode', 'anchor_profile', 'layout_profile', 'audio', 'step_1', 'step_2', 'step_3', 'step_4', 'step_5', 'step_6', 'step_7', 'step_8', 'step_9', 'step_10', 'step_11', 'step_12', 'step_1_label', 'step_2_label', 'step_3_label', 'step_4_label', 'step_5_label', 'step_6_label', 'step_7_label', 'step_8_label', 'step_9_label', 'step_10_label', 'step_11_label', 'step_12_label', 'front_context', 'back_context', 'learned', 'id']
CSS='\n.card{font-family:"Noto Serif CJK SC",Georgia,serif;font-size:24px;line-height:1.8;text-align:left;color:#1f2933;background:#fffdf8;padding:26px}.wrap{max-width:820px;margin:0 auto}.title{font-size:17px;color:#7b6b56}.reference{display:inline-block;font-size:22px;font-weight:700;color:#7a4e1d;background:#fff1cc;border-radius:999px;padding:4px 12px;margin-bottom:12px}.meta{font-size:14px;color:#8a7b69;margin:4px 0 8px}.prompt-label{font-size:15px;color:#8a7b69;letter-spacing:.08em;text-transform:uppercase}.versebox{white-space:pre-wrap;color:#111827;background:white;border:1px solid #f2e6d0;border-radius:18px;padding:22px;margin-top:8px}.versebox.layout-cjk{font-family:"Noto Sans Mono CJK SC","Microsoft YaHei Mono","SimSun",monospace;font-size:32px;line-height:1.9;word-break:break-all;overflow-wrap:anywhere;letter-spacing:0;font-variant-east-asian:full-width}.versebox.layout-latin{font-family:Georgia,"Times New Roman",serif;font-size:28px;line-height:1.65;word-break:normal;overflow-wrap:normal;letter-spacing:normal}.versebox.layout-mixed{font-family:"Noto Serif CJK SC",Georgia,serif;font-size:30px;line-height:1.75;word-break:normal;overflow-wrap:anywhere;letter-spacing:normal}.ms-blank{display:inline-block;width:calc(var(--ch,4)*.55em);height:.72em;border-bottom:.075em solid currentColor;vertical-align:baseline;margin:0 .08em}.context{font-size:18px;color:#6b7280;margin-top:16px}.nightMode.card{background:#1f1b16;color:#f7efe2}.nightMode .versebox{background:#2a241d;color:#fff7ed}\n'
STEP_NAMES=[f'{i:02d} Step {i}' for i in range(1,13)]

def _template_by_name(model,name):
    for template in model.get('tmpls',[]):
        if template.get('name') == name:
            return template
    return None

def _upsert_template(col, model, name, qfmt, afmt):
    template=_template_by_name(model,name)
    if template is None:
        template=col.models.new_template(name)
        template['qfmt']=qfmt; template['afmt']=afmt
        col.models.addTemplate(model,template)
    else:
        template['qfmt']=qfmt; template['afmt']=afmt
    return template

def ensure_model(col):
    model=col.models.by_name(MODEL_NAME); existed=model is not None
    if model:
        existing={field['name'] for field in model['flds']}
        for field_name in FIELDS:
            if field_name not in existing:
                col.models.addField(model,col.models.new_field(field_name))
    else:
        model=col.models.new(MODEL_NAME)
        for field_name in FIELDS:
            col.models.addField(model,col.models.new_field(field_name))
    model['css']=CSS
    back='<div class="wrap"><div class="title">{{collection_title}}</div><div class="reference">{{label}}</div><div class="meta">{{memorization_mode}} · {{anchor_profile}}</div><div class="prompt-label">Answer / Complete text</div><div class="versebox {{layout_profile}}">{{answer}}</div>{{#back_context}}<div class="context"><b>Next:</b><br>{{back_context}}</div>{{/back_context}}</div>'
    for idx,name in enumerate(STEP_NAMES,1):
        qfmt='<div class="wrap"><div class="title">{{collection_title}}</div><div class="reference">{{label}}</div><div class="meta">{{memorization_mode}} · {{anchor_profile}}</div><div class="prompt-label">{{step_'+str(idx)+'_label}}</div><div class="versebox {{layout_profile}}">{{step_'+str(idx)+'}}</div>{{#front_context}}<div class="context"><b>Previous:</b><br>{{front_context}}</div>{{/front_context}}</div>'
        _upsert_template(col,model,name,qfmt,back)
    if existed:
        col.models.save(model)
    else:
        col.models.add(model)
    return model
