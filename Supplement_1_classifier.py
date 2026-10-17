# -*- coding: utf-8 -*-
"""Reference implementation of the rule set specified in Supplement 1.

Applied to each preoperative index report; returns (label, certainty_tier).

Scope of the cues matters and is implemented explicitly. Rule E1 cancels a
candidate positive only when a negation cue GOVERNS the diagnostic term, so a
cue is read in the text immediately preceding the term, not anywhere in the
clause: "中肠旋转不良术后：未见明显梗阻征象" stays positive, because the
negation governs the obstruction, not the rotation. Rule E2 takes precedence
over E1, because a request to exclude the diagnosis raises it.

The positive-evidence dictionary implements exactly the definition frozen in
the Methods: the diagnosis named, a whirlpool or an explicit statement of
mesenteric vessel inversion for ultrasound, a corkscrew or spring appearance
or a malpositioned duodenojejunal junction for the upper gastrointestinal
series, and a mesenteric whirl or an abnormal duodenal position for CT.
Jejunal position and mesenteric-vessel course are audited as documented
content, not counted as positivity criteria.
"""
import re

ORGAN_EXCLUSIONS = r'(?:胃|睾丸|卵巢|附件|精索|大网膜|阑尾)(?:扭转|翻转)'
# rule B: 、 is a clause separator here, and is also used as a list marker ("1、")
CLAUSE_SPLIT     = r'[。；;、\n]+'
# a cue binds to the diagnostic term only within this many characters
WIN_BEFORE       = 12

POSITIVE_COMMON  = r'肠旋转不良|中肠旋转不良|旋转不良|中肠扭转|肠扭转|肠系膜扭转|小肠扭转'
POSITIVE_US      = (r'漩涡征|旋涡征|涡流|螺旋状|漩涡状|旋涡状'
                    r'|(?:动静脉|静脉.{0,6}动脉|动脉.{0,6}静脉).{0,12}(?:换位|反位|倒置|异常关系|关系异常)'
                    r'|静脉.{0,8}(?:位于|在).{0,6}动脉.{0,4}左')
POSITIVE_UGI     = (r'弹簧征|螺旋征|螺旋状|盘曲|绞索'
                    r'|十二指肠空肠曲.{0,10}(?:异常|偏|低|中线|右)')
POSITIVE_CT      = r'漩涡征|旋涡样|旋涡状|漩涡状|十二指肠.{0,8}(?:位置异常|异常位置)'
POSITIVE = {'US': POSITIVE_COMMON+'|'+POSITIVE_US,
            'UGI': POSITIVE_COMMON+'|'+POSITIVE_UGI,
            'CT': POSITIVE_COMMON+'|'+POSITIVE_CT}

# rule E1. 无 is a cue except in 有无 ("whether or not"), which raises the
# question rather than answering it. 排除 and 除外 are NOT negation cues here:
# in this corpus they appear only in requests to exclude the diagnosis, which
# rule E2 treats as raising it.
NEGATION   = r'未见|未闻|未发现|未探及|未探查|未显示|未提示|无明显|不考虑|正常|阴性|(?<!有)无'
# rule E2, read before the term or, up to the next punctuation, after it
HEDGED_EXC = r'建议.{0,12}(?:除外|排除|进一步)|待(?:排|除外)|不(?:除外|排除)|不能排除|请.{0,8}(?:除外|排除)|必要时.{0,10}(?:除外|排除)|排除|除外'

TIER_POSSIBLE = r'可疑|可能|\?|？|不除外|不排除|待排|待除外|建议.{0,10}(?:除外|排除|进一步)|似|排除|除外'
TIER_PROBABLE = r'多考虑|首先考虑|考虑|倾向|符合.{0,6}表现'

def classify(conclusion: str, modality: str):
    text = re.sub(ORGAN_EXCLUSIONS, '', str(conclusion or ''))
    hits = []
    for clause in re.split(CLAUSE_SPLIT, text):
        if not clause.strip():
            continue
        for m in re.finditer(POSITIVE[modality], clause):
            before = clause[max(0, m.start() - WIN_BEFORE):m.start()]
            after  = re.split(r'[，,：:！!？?]', clause[m.end():])[0]
            # rule F: E2 is read before E1, because a request to exclude the
            # diagnosis raises it and must not be cancelled as a negation
            if re.search(HEDGED_EXC, before) or re.search(HEDGED_EXC, after):
                hits.append(clause); break
            if re.search(NEGATION, before):
                continue
            hits.append(clause); break
    if not hits:
        return 0, None
    joined = ' '.join(hits)
    if re.search(TIER_POSSIBLE, joined): tier = 'possible'
    elif re.search(TIER_PROBABLE, joined): tier = 'probable'
    else: tier = 'definite'
    return 1, tier


# ---------------------------------------------------------------------------
# Original-language material referred to in Supplement 1. The study reports are written in Chinese,
# so these strings are Chinese by necessity; Supplement 1 gives their English translation.
# ---------------------------------------------------------------------------
# Search of the institutional research database for operative records (Supplement 1, Section C): field name -> string,
# matched case-insensitively. Field names: operative diagnosis, procedure name.
OPERATIVE_SEARCH = {'术中诊断': '肠旋转不良', '手术名称': 'Ladd'}

# Report-content audit patterns (Table S1 of Supplement 1): (element, modality, pattern as used, verbatim).
# Where a row holds a note in English after the pattern, the note describes a further condition applied in the audit.
CONTENT_PATTERNS = [
    ('Third portion of duodenum (D3)', 'Ultrasound', '十二指肠水平部|十二指肠水平段|十二指肠横部|十二指肠第三段|(?<![弓])横部|水平部'),
    ('Duodenojejunal junction', 'Ultrasound', '十二指肠空肠曲|屈氏|Treitz|十二指肠悬韧带|十二指肠[-—与和]?空肠交界'),
    ('Duodenum mentioned in any form', 'Ultrasound', '十二指肠'),
    ('Superior mesenteric artery–vein relationship', 'Ultrasound / CT', '肠系膜上动、?静脉|肠系膜上动静脉|肠系膜上动脉|肠系膜上静脉|肠系膜血管|系膜血管|SMA|SMV; excluding matches whose only context is 左肾静脉 / 胡桃夹 / 肾静脉受压 with no whirlpool term'),
    ('Explicit vessel inversion', 'Ultrasound', '(?:静脉|动脉)[^。；\\n]{0,10}(?:换位|反位|倒置|关系异常|异常关系)|静脉位于[^。；\\n]{0,8}左|动脉位于[^。；\\n]{0,8}右'),
    ('Whirlpool / swirl / spiral appearance', 'All', '漩涡|旋涡|涡流|螺旋; counted only where no negation (未见|未探及|未显示|未发现|无明显|不明显|未闻) occurs in the 12 characters preceding the match within the same clause'),
    ('Enteric fluid administered', 'Ultrasound', '饮水|口服[^。；\\n]{0,6}(?:水|液|造影剂)|注水|注入|胃内注|温开水|经胃管'),
    ('Dynamic (real-time) assessment', 'Ultrasound', '动态|实时观察|连续观察'),
    ('Graded compression', 'Ultrasound', '加压|探头压|压迫探查'),
    ('Color Doppler used', 'Ultrasound', 'CDFI|彩色多普勒|多普勒'),
    ('Bowel gas explicitly limiting the study', 'Ultrasound', 'clause containing both (肠气|积气|气体干扰|气体遮挡|气体遮盖|气体较多|气强反射|充满气体) and (干扰|遮挡|遮盖|显示不清|显示欠清|探及?不满意|不满意)'),
    ('Cecal position', 'Ultrasound / UGI', '回盲'),
    ('Bedside examination', 'Ultrasound', '床旁 (in the examination name)'),
    ('Examination type: great-vessel study', 'Ultrasound', '腹部大血管 (in the examination name)'),
    ('Examination type: gastrointestinal ultrasound', 'Ultrasound', '胃肠道 (in the examination name)'),
    ('Contrast enhancement', 'CT', '增强 (in the examination name)'),
    ('Three-dimensional reconstruction', 'CT', '三维重建 (in the examination name)'),
    ('Duodenojejunal junction', 'UGI', '空肠曲|屈氏|Treitz|悬韧带|十二指肠[-—与和]?空肠交界'),
    ('Corkscrew / spring appearance', 'UGI', '弹簧|螺旋|绞索|盘曲'),
    ('Jejunal position', 'UGI', '空肠.{0,10}(位于|居|偏)'),
    ('Whole-gastrointestinal study', 'UGI', '全消化道 (in the examination name)'),
    ('Barium contrast', 'UGI', '钡 (in the examination name)'),
]
