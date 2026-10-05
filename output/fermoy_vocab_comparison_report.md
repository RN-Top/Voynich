======================================================================
Fermoy Vocabulary Comparison Test
======================================================================

Loaded 25 Voynich closing words
Example: ['qodaiin', 'olcheey', 'ychedy', 'chey', 'sheody']

Loaded 42 Fermoy medical terms
Example: ['hepate', 'liver', 'organs_of_generation', 'membrorum_generacivorum', 'dropsy']

======================================================================
LEVENSHTEIN DISTANCE TEST (distance ≤ 3)
======================================================================

26 matches found:
voynich_word fermoy_term  distance
        chey         hot         3
        chey        cold         3
        chey       cures         3
       cheeo       cures         3
        olor       colic         3
        olor         pox         3
        olor         hot         3
        olor        cold         3
        chol       colic         3
        chol         pox         3
        chol         hot         2
        chol        cold         2
       chody         hot         3
       chody        cold         3
         qoy         pox         2
         qoy         hot         2
         qoy        cold         3
        chos         pox         3
        chos         hot         2
        chos        cold         3
        chos       cures         3
           y         pox         3
           y         hot         3
           o         pox         2
           o         hot         2
           o        cold         3

Matches by Voynich word:
  chey: 3 match(es)
    → hot (distance=3)
    → cold (distance=3)
    → cures (distance=3)
  cheeo: 1 match(es)
    → cures (distance=3)
  olor: 4 match(es)
    → colic (distance=3)
    → pox (distance=3)
    → hot (distance=3)
    → cold (distance=3)
  chol: 4 match(es)
    → colic (distance=3)
    → pox (distance=3)
    → hot (distance=2)
    → cold (distance=2)
  chody: 2 match(es)
    → hot (distance=3)
    → cold (distance=3)
  qoy: 3 match(es)
    → pox (distance=2)
    → hot (distance=2)
    → cold (distance=3)
  chos: 4 match(es)
    → pox (distance=3)
    → hot (distance=2)
    → cold (distance=3)
    → cures (distance=3)
  y: 2 match(es)
    → pox (distance=3)
    → hot (distance=3)
  o: 3 match(es)
    → pox (distance=2)
    → hot (distance=2)
    → cold (distance=3)

Binomial test (null = 5% random match rate):
  Observed: 26 matches
  p-value: 1.0000
  Result: NOT SIGNIFICANT

======================================================================
SUBSTRING OVERLAP TEST
======================================================================

27 substring matches found:
voynich_word             fermoy_term        match_type
           y                  dropsy voynich_in_fermoy
           y                 urinary voynich_in_fermoy
           y                 leprosy voynich_in_fermoy
           y                symptoms voynich_in_fermoy
           y        dietary_guidance voynich_in_fermoy
           y               lifestyle voynich_in_fermoy
           o    organs_of_generation voynich_in_fermoy
           o membrorum_generacivorum voynich_in_fermoy
           o                  dropsy voynich_in_fermoy
           o                   colic voynich_in_fermoy
           o                   worms voynich_in_fermoy
           o          utereal_tumour voynich_in_fermoy
           o       arthritica_passio voynich_in_fermoy
           o                     pox voynich_in_fermoy
           o                 leprosy voynich_in_fermoy
           o    plant_identification voynich_in_fermoy
           o              properties voynich_in_fermoy
           o                     hot voynich_in_fermoy
           o                    cold voynich_in_fermoy
           o                symptoms voynich_in_fermoy
           o                 seasons voynich_in_fermoy
           o            probatum_est voynich_in_fermoy
           o            complexiones voynich_in_fermoy
           o                 humores voynich_in_fermoy
           o            bloodletting voynich_in_fermoy
           o               purgation voynich_in_fermoy
           o              flebotomia voynich_in_fermoy

======================================================================
SUMMARY
======================================================================
Pre-registration: analyses/fermoy_vocab_comparison_prereg.md
Voynich closing words: 25
Fermoy medical terms: 42
Levenshtein matches (≤3): 26
Substring matches: 27

Prediction: ≥8 Levenshtein matches AND ≥5 phonetic matches
Actual: 26 Levenshtein + 27 substring

Result: SUPPORTED ✓
