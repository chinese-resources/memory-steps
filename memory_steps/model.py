# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

"""Universal Memory Steps note type with an in-card Ladder Player."""

MODEL_NAME = "Memory Steps: Universal Ladder"
LEGACY_MODEL_NAME = "Memory Steps: Line-by-Line Memorizer"
TEMPLATE_NAME = "Universal Ladder Player"

FIELDS = [
    "collection_id", "collection_title", "line_index", "label", "answer",
    "memorization_mode", "anchor_profile", "layout_profile", "audio",
    "step_1", "step_2", "step_3", "step_4", "step_5", "step_6",
    "step_7", "step_8", "step_9", "step_10", "step_11", "step_12",
    "step_1_label", "step_2_label", "step_3_label", "step_4_label",
    "step_5_label", "step_6_label", "step_7_label", "step_8_label",
    "step_9_label", "step_10_label", "step_11_label", "step_12_label",
    "front_context", "back_context", "learned", "id",
]

CSS = r"""
.card{font-family:"Noto Serif CJK SC",Georgia,serif;font-size:23px;line-height:1.75;text-align:left;color:#1f2933;background:#fffdf8;padding:24px}.wrap{max-width:860px;margin:0 auto}.title{font-size:17px;color:#7b6b56}.reference{display:inline-block;font-size:22px;font-weight:700;color:#7a4e1d;background:#fff1cc;border-radius:999px;padding:4px 12px;margin:4px 0 12px}.meta{font-size:14px;color:#8a7b69;margin:4px 0 12px}.instructions,.grading,.context{font-size:17px;color:#5f6b7a;background:#fff8e8;border:1px solid #f3e2bd;border-radius:14px;padding:12px 14px;margin:12px 0}.player{background:#fffaf0;border:1px solid #eadcc4;border-radius:22px;padding:16px;box-shadow:0 2px 10px rgba(93,64,25,.06);margin:14px 0}.player-top{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;margin-bottom:10px}.badge{display:inline-block;font-size:13px;font-weight:700;color:#7a4e1d;background:#ffe8ad;border-radius:999px;padding:4px 10px}.step-title{font-size:16px;font-weight:700;color:#5b4020}.prompt-label{font-size:14px;color:#8a7b69;letter-spacing:.08em;text-transform:uppercase;margin:4px 0 6px}.versebox{white-space:pre-wrap;color:#111827;background:white;border:1px solid #f2e6d0;border-radius:18px;padding:20px;margin:8px 0 12px}.player .versebox{border-width:2px;border-color:#e7c478;min-height:3.4em}.versebox.layout-cjk{font-family:"Noto Sans Mono CJK SC","Microsoft YaHei Mono","SimSun",monospace;font-size:32px;line-height:1.9;word-break:break-all;overflow-wrap:anywhere;letter-spacing:0;font-variant-east-asian:full-width}.versebox.layout-latin{font-family:Georgia,"Times New Roman",serif;font-size:28px;line-height:1.65;word-break:normal;overflow-wrap:normal;letter-spacing:normal}.versebox.layout-mixed{font-family:"Noto Serif CJK SC",Georgia,serif;font-size:30px;line-height:1.75;word-break:normal;overflow-wrap:anywhere;letter-spacing:normal}.ms-blank{display:inline-block;width:calc(var(--ch,4)*.55em);height:.72em;border-bottom:.075em solid currentColor;vertical-align:baseline;margin:0 .08em}.controls{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}@media (min-width:720px){.controls{grid-template-columns:repeat(5,minmax(0,1fr))}}.ms-btn{border:1px solid #d7b56d;background:#fff4d6;color:#5b4020;border-radius:13px;padding:10px 12px;font-size:16px;font-weight:700;cursor:pointer}.ms-btn:active{transform:translateY(1px)}.ms-btn.primary{background:#f4bd4f;border-color:#d69b2b;color:#3d2a12}.ms-btn.secondary{background:#fff}.keyboard-help{font-size:13px;color:#8a7b69;margin-top:9px}.sources{display:none}.fallback-title{margin-top:18px}details.hint{background:#fff;border:1px solid #eadcc4;border-radius:14px;margin:9px 0;overflow:hidden}details.hint>summary{cursor:pointer;list-style-position:inside;padding:11px 14px;color:#7a4e1d;font-size:17px;font-weight:700;background:#fff7e6}details.hint[open]>summary{border-bottom:1px solid #eadcc4}.hint-body{padding:12px 14px 4px}.ms-js .fallback{display:none}hr{border:none;border-top:1px solid #eadcc4;margin:22px 0}.nightMode.card{background:#1f1b16;color:#f7efe2}.nightMode .versebox,.nightMode .player,.nightMode details.hint{background:#2a241d;color:#fff7ed;border-color:#5f4a2f}.nightMode details.hint>summary,.nightMode .instructions,.nightMode .grading,.nightMode .context{background:#352b1f;color:#f7dca6;border-color:#5f4a2f}.nightMode .ms-btn{background:#4b3822;color:#f7dca6;border-color:#7b5b35}.nightMode .ms-btn.primary{background:#d69b2b;color:#231607}
"""

def _template_by_name(model, name):
    for template in model.get("tmpls", []):
        if template.get("name") == name:
            return template
    return None

def _upsert_template(col, model, name, qfmt, afmt):
    template = _template_by_name(model, name)
    if template is None:
        template = col.models.new_template(name)
        template["qfmt"] = qfmt; template["afmt"] = afmt
        col.models.addTemplate(model, template)
    else:
        template["qfmt"] = qfmt; template["afmt"] = afmt
    return template

def _remove_extra_templates(model):
    model["tmpls"] = [t for t in model.get("tmpls", []) if t.get("name") == TEMPLATE_NAME]
    for ordinal, template in enumerate(model.get("tmpls", [])):
        template["ord"] = ordinal

def _step_sources():
    parts = ['<div class="sources" id="ms-sources">']
    for idx in range(1, 13):
        parts.append(f'<div class="ms-step-source" data-label="{{{{step_{idx}_label}}}}">{{{{step_{idx}}}}}</div>')
    parts.append('</div>')
    return ''.join(parts)

def _fallback_hints():
    blocks = ['<div class="fallback"><div class="prompt-label fallback-title">Fallback progressive hints</div>']
    for idx in range(11, 0, -1):
        blocks.append('<details class="hint">' + f'<summary>Hint: {{{{step_{idx}_label}}}}</summary>' + '<div class="hint-body">' + f'<div class="versebox {{{{layout_profile}}}}">{{{{step_{idx}}}}}</div>' + '</div></details>')
    blocks.append('</div>')
    return ''.join(blocks)

def _player_script():
    return r"""
<script>
(function(){
  document.documentElement.classList.add('ms-js');
  var sourceRoot=document.getElementById('ms-sources'); if(!sourceRoot){return;}
  var nodes=Array.prototype.slice.call(sourceRoot.querySelectorAll('.ms-step-source'));
  var steps=nodes.map(function(n){return {label:n.getAttribute('data-label')||'',html:n.innerHTML||''};});
  var mode='recall', current=11;
  var modeEl=document.getElementById('ms-mode'), countEl=document.getElementById('ms-count'), labelEl=document.getElementById('ms-label'), promptEl=document.getElementById('ms-prompt'), hintBtn=document.getElementById('ms-hint'), harderBtn=document.getElementById('ms-harder');
  function clamp(n){return Math.max(0,Math.min(11,n));}
  function render(){current=clamp(current);var step=steps[current]||{label:'',html:''};modeEl.textContent=mode==='recall'?'Recall mode':'Training mode';countEl.textContent='Step '+(current+1)+' / 12';labelEl.textContent=step.label;promptEl.innerHTML=step.html;hintBtn.textContent=mode==='recall'?'Need hint ←':'Easier ←';harderBtn.textContent=mode==='recall'?'Harder →':'Next harder →';}
  function recall(){mode='recall';current=11;render();} function train(){mode='train';current=0;render();} function easier(){current-=1;render();} function harder(){current+=1;render();} function full(){current=0;render();}
  document.getElementById('ms-recall').addEventListener('click',recall); document.getElementById('ms-train').addEventListener('click',train); hintBtn.addEventListener('click',easier); harderBtn.addEventListener('click',harder); document.getElementById('ms-full').addEventListener('click',full);
  document.addEventListener('keydown',function(ev){if(ev.target&&/input|textarea/i.test(ev.target.tagName)){return;}var k=(ev.key||'').toLowerCase();if(k==='h'||k==='arrowleft'){easier();} if(k==='l'||k==='arrowright'){harder();} if(k==='r'){recall();} if(k==='t'){train();} if(k==='f'){full();}});
  render();
})();
</script>
"""

def front_template():
    return ('<div class="wrap"><div class="title">{{collection_title}}</div><div class="reference">{{label}}</div><div class="meta">{{memorization_mode}} · {{anchor_profile}}</div>'
        '<div class="instructions"><b>Use the ladder player.</b> Recall mode starts hard. Training mode starts easy and walks upward.</div>'
        '<div class="player" id="ms-player"><div class="player-top"><span class="badge" id="ms-mode">Recall mode</span><span class="badge" id="ms-count">Step 12 / 12</span></div>'
        '<div class="step-title" id="ms-label">{{step_12_label}}</div><div class="versebox {{layout_profile}}" id="ms-prompt">{{step_12}}</div>'
        '<div class="controls"><button type="button" class="ms-btn primary" id="ms-recall">Recall</button><button type="button" class="ms-btn primary" id="ms-train">Train</button><button type="button" class="ms-btn" id="ms-hint">Need hint ←</button><button type="button" class="ms-btn" id="ms-harder">Harder →</button><button type="button" class="ms-btn secondary" id="ms-full">Full line</button></div>'
        '<div class="keyboard-help">Desktop keys: H/← easier hint · L/→ harder · R recall · T train · F full line.</div></div>'
        + _step_sources() + _fallback_hints() + _player_script() + '{{#front_context}}<div class="context"><b>Previous:</b><br>{{front_context}}</div>{{/front_context}}</div>')

def back_template():
    return ('{{FrontSide}}<hr><div class="wrap"><div class="prompt-label">Answer / complete text</div><div class="versebox {{layout_profile}}">{{answer}}</div>{{#audio}}<div class="audio">{{audio}}</div>{{/audio}}'
        '<div class="grading"><b>Suggested grading</b><br><b>Easy</b>: recalled from the primary cue with confidence.<br><b>Good</b>: recalled with a small hint or minor hesitation.<br><b>Hard</b>: needed several hints but eventually recalled it.<br><b>Again</b>: needed the full answer or could not recite accurately.</div>'
        '{{#back_context}}<div class="context"><b>Next:</b><br>{{back_context}}</div>{{/back_context}}</div>')

def ensure_model(col):
    model = col.models.by_name(MODEL_NAME); existed = model is not None
    if model:
        existing = {field["name"] for field in model["flds"]}
        for field_name in FIELDS:
            if field_name not in existing:
                col.models.addField(model, col.models.new_field(field_name))
    else:
        model = col.models.new(MODEL_NAME)
        for field_name in FIELDS:
            col.models.addField(model, col.models.new_field(field_name))
    model["css"] = CSS; _remove_extra_templates(model); _upsert_template(col, model, TEMPLATE_NAME, front_template(), back_template())
    if existed: col.models.save(model)
    else: col.models.add(model)
    return model
