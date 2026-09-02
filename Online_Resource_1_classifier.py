# -*- coding: utf-8 -*-
"""Reference implementation of the rule set specified in Online Resource 1.
Applied to each preoperative index report; returns (label, certainty_tier)."""
import re

ORGAN_EXCLUSIONS = r'(?:胃|睾丸|卵巢|附件|精索|大网膜|阑尾)(?:扭转|翻转)'
CLAUSE_SPLIT     = r'[。；;\n]+'

POSITIVE_COMMON  = r'肠旋转不良|中肠旋转不良|旋转不良|中肠扭转|肠扭转|肠系膜扭转|小肠扭转'
POSITIVE_US      = r'漩涡征|旋涡征|涡流|螺旋状|漩涡状|旋涡状|(?:动静脉|静脉.{0,6}动脉|动脉.{0,6}静脉).{0,12}(?:换位|反位|倒置|异常关系|关系异常)'
POSITIVE_UGI     = r'弹簧征|螺旋征|绞索|十二指肠空肠曲.{0,10}(?:异常|偏|低|中线|右)'
POSITIVE_CT      = r'漩涡征|旋涡样|旋涡状|漩涡状|十二指肠.{0,8}(?:位置异常|异常位置)'
POSITIVE = {'US': POSITIVE_COMMON+'|'+POSITIVE_US,
            'UGI': POSITIVE_COMMON+'|'+POSITIVE_UGI,
            'CT': POSITIVE_COMMON+'|'+POSITIVE_CT}

NEGATION   = r'未见|未闻|未发现|未探及|未探查|未显示|未提示|无明显|排除了|除外了|不考虑|正常|阴性'
HEDGED_EXC = r'建议.{0,12}(?:除外|排除|进一步)|待(?:排|除外)|不(?:除外|排除)|请结合临床.{0,6}(?:除外|排除)'

TIER_POSSIBLE = r'可疑|可能|\?|？|不除外|不排除|待排|待除外|建议.{0,10}(?:除外|排除|进一步)|似'
TIER_PROBABLE = r'多考虑|首先考虑|考虑|倾向|符合.{0,6}表现'

def classify(conclusion: str, modality: str):
    text = re.sub(ORGAN_EXCLUSIONS, '', str(conclusion or ''))
    hits = []
    for clause in re.split(CLAUSE_SPLIT, text):
        if not clause.strip():
            continue
        if not re.search(POSITIVE[modality], clause):
            continue
        # rule E2: a hedged request to exclude the diagnosis RAISES it, so it
        # is evaluated before, and overrides, clause-level negation
        if re.search(HEDGED_EXC, clause):
            hits.append(clause); continue
        if re.search(NEGATION, clause):
            continue
        hits.append(clause)
    if not hits:
        return 0, None
    joined = ' '.join(hits)
    if re.search(TIER_POSSIBLE, joined): tier = 'possible'
    elif re.search(TIER_PROBABLE, joined): tier = 'probable'
    else: tier = 'definite'
    return 1, tier
