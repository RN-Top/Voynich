import numpy as np
import pandas as pd
from collections import Counter
import io

# -------------------------------------------------------------------------
# 1. CORPUS DATA INGESTION (YOUR ACTUAL RUN DATA)
# -------------------------------------------------------------------------
DATA_CSV = """
,folio,token,carrier,predicted,expected,match
1,f70v2,dar,EMPTY,outlet,medium,false
2,f70v2,otey,ote,reflux,reflux,true
3,f70v2,ykeey,ykee,reflux,reflux,true
4,f70v2,tchy,tch,reflux,reflux,true
6,f70v2,oteotey,oteote,reflux,reflux,true
7,f70v2,shey,she,reflux,reflux,true
10,f70v2,dateey,atee,reflux,reflux,true
11,f70v2,sal,s,outlet,medium,false
12,f70v2,ody,od,reflux,reflux,true
13,f70v2,choteey,chotee,reflux,reflux,true
14,f70v2,choeteedy,choeteed,reflux,reflux,true
16,f70v2,yteos,yteos,outlet,,false
17,f70v2,alain,al,medium,medium,true
18,f70v2,sheodaly,sheodal,reflux,reflux,true
20,f70v2,aiin,EMPTY,medium,medium,true
21,f70v2,cholkal,cholk,outlet,medium,false
22,f70v2,chokear,choke,outlet,medium,false
23,f70v2,oteody,oteod,reflux,reflux,true
24,f70v2,cholaiin,chol,medium,medium,true
25,f70v2,oteeoal,oteeo,outlet,medium,false
26,f70v2,al,EMPTY,outlet,medium,false
27,f70v2,sheeos,sheeos,outlet,,false
28,f70v2,okey,oke,reflux,reflux,true
30,f70v2,dy,EMPTY,reflux,reflux,true
34,f70v2,olar,ol,outlet,medium,false
35,f70v2,otoaiin,oto,medium,medium,true
36,f70v2,oteeody,oteeod,reflux,reflux,true
38,f70v2,todaiin,tod,medium,medium,true
39,f70v2,chokain,chok,medium,medium,true
40,f70v2,otalal,otal,outlet,medium,false
41,f70v2,oteeam,otee,positional,positional,true
43,f70v2,ykary,ykar,reflux,reflux,true
44,f70v2,otar,ot,outlet,medium,false
45,f70v2,oty,ot,reflux,reflux,true
46,f70v2,oky,ok,reflux,reflux,true
47,f70v2,ody,od,reflux,reflux,true
48,f70v2,oty,ot,reflux,reflux,true
49,f70v2,ar,EMPTY,outlet,medium,false
51,f70v2,otody,otod,reflux,reflux,true
53,f70v2,otaldar,otald,outlet,medium,false
54,f70v2,okody,okod,reflux,reflux,true
55,f70v2,opysam,opys,positional,positional,true
56,f70v2,chy,ch,reflux,reflux,true
57,f70v2,otaly,otal,reflux,reflux,true
58,f70v2,otal,ot,outlet,medium,false
59,f70v2,arar,ar,outlet,medium,false
60,f70v2,otaldy,otald,reflux,reflux,true
61,f70v2,okeoly,okeol,reflux,reflux,true
62,f70v2,okydy,okyd,reflux,reflux,true
64,f70v2,daiiamdy,aiiamd,reflux,reflux,true
"""

# -------------------------------------------------------------------------
# 2. FROZEN STRUCTURAL RULES & BASELINE SEMANTIC ROLES
# -------------------------------------------------------------------------
PREFIX_RULES = {
    'qo': 'C', 'qok': 'C', 'ok': 'C', 'ot': 'C',
    'ch': 'P', 'sh': 'P', 'da': 'P',
    's': 'L', 't': 'L',
    'd': 'R', 'y': 'R'
}

SUFFIX_RULES = {
    'am': 'R', 'm': 'R',
    'aiin': 'L', 'ain': 'L', 'iin': 'L', 'in': 'L',
    'al': 'P', 'ol': 'P', 'ar': 'P', 'or': 'P',
    'edy': 'C', 'dy': 'C', 'y': 'C'
}

# The 4 operational concepts assigned to the structural roles:
ORIGINAL_SEMANTIC_MAP = {
    'C': 'reflux',
    'L': 'medium',
    'P': 'process',
    'R': 'outlet'
}

def classify_token(token: str) -> str:
    """Morphotactic classifier locked to your affix rules."""
    token = str(token).strip().lower()
    if not token or token == 'empty':
        return 'UNKNOWN'

    for sfx, role in sorted(SUFFIX_RULES.items(), key=lambda x: len(x[0]), reverse=True):
        if token.endswith(sfx):
            return role

    for pfx, role in sorted(PREFIX_RULES.items(), key=lambda x: len(x[0]), reverse=True):
        if token.startswith(pfx):
            return role

    return 'UNKNOWN'


# -------------------------------------------------------------------------
# 3. CONTEXTUAL METRICS & SCORING
# -------------------------------------------------------------------------
def score_semantic_transitions(tokens: list, role_to_meaning: dict) -> float:
    """
    Evaluates directed transition flow:
    reflux -> medium -> process -> outlet -> reflux
    """
    valid_transitions = {
        ('reflux', 'medium'),
        ('medium', 'process'),
        ('process', 'outlet'),
        ('outlet', 'reflux')
    }

    assigned = [role_to_meaning[classify_token(t)] for t in tokens if classify_token(t) in role_to_meaning]
    if len(assigned) < 2:
        return 0.0

    transitions = list(zip(assigned[:-1], assigned[1:]))
    matches = sum(1 for pair in transitions if pair in valid_transitions)
    return matches / len(transitions)


# -------------------------------------------------------------------------
# 4. PERMUTATION TOURNAMENT RUNNER
# -------------------------------------------------------------------------
def run_tournament(df: pd.DataFrame, num_permutations: int = 10000, seed: int = 42):
    np.random.seed(seed)
    tokens = df['token'].dropna().tolist()

    roles = list(ORIGINAL_SEMANTIC_MAP.keys())
    labels = list(ORIGINAL_SEMANTIC_MAP.values())

    # 1. Hypothesized model score
    actual_score = score_semantic_transitions(tokens, ORIGINAL_SEMANTIC_MAP)

    # 2. Monte Carlo permutation under random role-meaning permutations
    null_scores = np.empty(num_permutations)
    for i in range(num_permutations):
        shuffled_labels = np.random.permutation(labels)
        permuted_map = dict(zip(roles, shuffled_labels))
        null_scores[i] = score_semantic_transitions(tokens, permuted_map)

    mean_null = np.mean(null_scores)
    std_null = np.std(null_scores)
    p_value = np.mean(null_scores >= actual_score)
    z_score = (actual_score - mean_null) / std_null if std_null > 0 else 0.0

    print("=" * 65)
    print("           SEMANTIC PERMUTATION TOURNAMENT (f70v2)           ")
    print("=" * 65)
    print(f"Tokens Analyzed:             {len(tokens)}")
    print(f"Hypothesized Alignment Score:{actual_score:.4f}")
    print(f"Null Model Mean (Chance):    {mean_null:.4f} (std: {std_null:.4f})")
    print(f"Z-Score:                     {z_score:+.3f}")
    print(f"Permutations:                {num_permutations:,}")
    print(f"Empirical p-value:           {p_value:.5f}")
    print("-" * 65)
    
    if p_value < 0.05:
        print("RESULT: SIGNIFICANT. The hypothesized labels outperform random assignments.")
    else:
        print("RESULT: NOT SIGNIFICANT. The assignments do not beat random permutation.")
    print("=" * 65)


if __name__ == '__main__':
    # Loads directly from your provided f70v2 evaluation data
    df = pd.read_csv(io.StringIO(DATA_CSV.strip()))
    run_tournament(df, num_permutations=10000)
