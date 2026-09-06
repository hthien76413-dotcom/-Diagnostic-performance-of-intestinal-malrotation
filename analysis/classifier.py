# -*- coding: utf-8 -*-
"""Reference implementation of the rule set specified in Online Resource 1.

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
