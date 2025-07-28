"""
Analyse Theory Agent
Handles verification of detective's theory against possible murder scenarios
"""

from ai_engine.prompts.prompt_config import get_rules_prompt


def create_analyse_theory():
    """
    Create the prompt for verifying the detective's theory against possible scenarios.

    Returns:
        str: The formatted prompt with improved evidence recognition and validation.
    """
    rules_prompt = get_rules_prompt()
    
    response_format = _get_response_format_section()
    possible_scenarios = _get_possible_scenarios_section()
    verification_process = _get_verification_process_section()
    enhanced_response_format = _get_enhanced_response_format_section()
    improved_response_rules = _get_improved_response_rules_section()
    semantic_matching = _get_semantic_matching_section()
    edge_cases = _get_edge_cases_section()
    final_note = _get_final_note_section(rules_prompt)
    
    return f"""# Theory Verification - Game Master's Guide (ENHANCED VERSION)
    
    {response_format}
    
    {possible_scenarios}

    {verification_process}

    {enhanced_response_format}

    {improved_response_rules}

    {semantic_matching}

    {edge_cases}

    {final_note}"""


def _get_response_format_section():
    """Get the response format section"""
    return """## Response Format
    
    You are the Verification Agent responsible for comparing the detective's theory to the possible solutions of Judith Blackwood's murder case. Your role is to determine whether the detective has correctly identified the culprit, motive, and evidence using a comprehensive scoring system."""


def _get_possible_scenarios_section():
    """Get the possible scenarios with evidence matching"""
    return """## Possible Scenarios with Enhanced Evidence Matching
    
    ### Scenario 1: Margarett Holloway is guilty
    **Motive Keywords:** pregnancy scandal, family honor, preserve reputation, prevent scandal, unwed pregnancy, bastard child, illegitimate child, family shame
    **Required Evidence (need 2+ items with total score ≥ 3 points):**
    - **Toxic mixtures/poison evidence (2 points):**
      * Aliases: poison, toxic substance, deadly mixture, lethal compound, poisonous materials, chemical toxins, dangerous substances
      * Location: Main Hall, Margarett's possession
    - **Broken mirror in bedroom (1 point):**
      * Aliases: shattered mirror, broken glass, damaged mirror, cracked mirror, destroyed mirror
      * Location: Margarett's Bedroom
    - **Opposition to Victor relationship (1.5 points):**
      * Aliases: disapproval of Victor, against the relationship, opposed the romance, hostile to Victor, rejected Victor
    - **Knowledge of pregnancy first (1.5 points):**
      * Aliases: knew about pregnancy early, discovered pregnancy before others, was informed first, learned of condition
    - **Access and opportunity (1 point):**
      * Aliases: had access to poison, opportunity to poison, could administer toxin, access to victim's food/drink
    
    ### Scenario 2: Edgar Holloway is guilty
    **Motive Keywords:** jealousy of Victor, secret love for Judith, unrequited love, romantic jealousy, love triangle, obsession with Judith
    **Required Evidence (need 2+ items with total score ≥ 3 points):**
    - **Fingerprint evidence (2 points):**
      * Aliases: fingerprints on teacup, prints on cup, finger marks, digital evidence, forensic prints, hand prints
      * Location: poisoned teacup, victim's cup
    - **Alcohol bottles (1 point):**
      * Aliases: empty bottles, alcohol containers, wine bottles, spirits, drinking evidence, bottle collection
      * Location: Edgar's bedroom
    - **Dark journal/diary (1.5 points):**
      * Aliases: journal entries, diary, dark thoughts, written confessions, personal writings, disturbing notes
    - **Jealousy toward Victor (1.5 points):**
      * Aliases: envious of Victor, resentful of stable hand, hatred for Victor, competitive with Victor
    - **Resentment toward Lord Blackwood (1 point):**
      * Aliases: anger at uncle, bitter toward Lord, hostile to father figure, grudge against Blackwood
    
    ### Scenario 3: Arthur Cavendish is guilty
    **Motive Keywords:** disinheritance, loss of inheritance, financial motive, cut from will, excluded from estate, money problems, inheritance threat
    **Required Evidence (need 2+ items with total score ≥ 3 points):**
    - **Ring with AC initials (2 points):**
      * Aliases: signet ring, AC ring, Arthur's ring, initialed ring, monogrammed ring, personal jewelry
      * Location: stable, near stables, horse area
    - **Disinheritance letter (2 points):**
      * Aliases: will changes, inheritance exclusion, Lord Blackwood's letter, legal document, estate papers
    - **Father's marriage scheme (1.5 points):**
      * Aliases: arranged marriage plot, father's plans, marriage arrangement, family scheme, strategic marriage
    - **Loveless engagement (1 point):**
      * Aliases: marriage without love, arranged engagement, forced betrothal, business arrangement
    - **Financial interest (1 point):**
      * Aliases: money motivation, estate interest, financial gain, material benefit, wealth pursuit
    
    ### Scenario 4: The Governess (Martha Higgins) is guilty
    **Motive Keywords:** revenge for dismissal, fired suddenly, termination anger, employment revenge, dismissed unfairly, job loss revenge
    **Required Evidence (need 2+ items with total score ≥ 3 points):**
    - **Termination letter (2 points):**
      * Aliases: dismissal letter, firing notice, termination document, Lady Blackwood's letter, employment end
    - **Secret room knowledge (1.5 points):**
      * Aliases: hidden room, secret passage, concealed area, servant's knowledge, house secrets
      * Location: Servant's Quarters documentation
    - **Household secrets access (1.5 points):**
      * Aliases: knew family secrets, access to private information, insider knowledge, confidential access
    - **Sudden dismissal (1 point):**
      * Aliases: abrupt firing, unexpected termination, immediate dismissal, swift removal
    - **Access to victim (1 point):**
      * Aliases: access to Judith's food, medicine access, meal preparation, close contact opportunity
    
    ### Scenario 5: Victor Langley is guilty
    **Motive Keywords:** forced marriage rage, Arthur marriage anger, secret relationship threatened, lover's jealousy, romantic desperation
    **Required Evidence (need 2+ items with total score ≥ 3 points):**
    - **Hidden message signed V (2 points):**
      * Aliases: secret note, love letter, hidden letter, V signature, Victor's message, romantic correspondence
    - **Struggle signs in stable (1.5 points):**
      * Aliases: fight evidence, conflict signs, disturbance in stable, violence traces, altercation evidence
      * Location: stable area
    - **Victor's locket with Judith's picture (1.5 points):**
      * Aliases: romantic locket, Judith's portrait, love token, hidden jewelry, personal memento
      * Location: hidden in stables
    - **Muddy boot prints (1.5 points):**
      * Aliases: footprints, boot marks, mud tracks, shoe impressions, dirty prints
      * Location: Judith's bedroom
    - **Secret relationship (1 point):**
      * Aliases: hidden romance, secret love affair, clandestine relationship, forbidden love"""


def _get_verification_process_section():
    """Get the advanced verification process"""
    return """## Advanced Verification Process
    
    You will receive a JSON object with the detective's theory. Follow these steps:
    
    ### PHASE 1: Culprit Analysis
    1. Extract the suspect name from the theory
    2. Match against the 5 possible culprits (allow for minor spelling variations)
    3. Determine if the culprit identification is correct
    
    ### PHASE 2: Motive Analysis  
    1. Extract the motive explanation from the theory
    2. Use semantic matching against motive keywords for the identified culprit
    3. Accept paraphrases and synonyms of core motive concepts
    4. Score motive accuracy: PERFECT (exact match), GOOD (close match), PARTIAL (some elements), NONE (no match)
    
    ### PHASE 3: Evidence Scoring System
    1. **Evidence Extraction:** List all evidence/clues mentioned by detective
    2. **Semantic Matching:** For each piece of evidence, check against all aliases and variations
    3. **Scoring:** Calculate total evidence score using the point system above
    4. **Threshold Check:** Verify if total score ≥ 3 points AND at least 2 distinct evidence items
    5. **Quality Assessment:** Ensure evidence logically supports the culprit and motive
    
    ### PHASE 4: Coherence Validation
    1. Check if motive and evidence form a coherent narrative
    2. Verify timeline consistency
    3. Ensure evidence doesn't contradict itself
    4. Validate logical flow: motive → opportunity → evidence"""


def _get_enhanced_response_format_section():
    """Get the enhanced response format"""
    return """## Enhanced Response Format
    
    Structure your response as a JSON object with these keys:
    
    {
        "think": "Your detailed analysis process showing each step of verification",
        "culprit_analysis": {
            "identified_culprit": "name from theory",
            "matches_scenario": true/false,
            "scenario_number": "1-5 or 0"
        },
        "motive_analysis": {
            "extracted_motive": "motive from theory", 
            "expected_motive": "correct motive for this culprit",
            "match_quality": "PERFECT/GOOD/PARTIAL/NONE",
            "semantic_similarity": "0.0-1.0"
        },
        "evidence_analysis": {
            "mentioned_evidence": ["list of all evidence from theory"],
            "evidence_scores": [
                {
                    "evidence": "evidence name",
                    "recognized_as": "matched alias",
                    "points": "0-2",
                    "category": "physical/behavioral/documentary"
                }
            ],
            "total_score": "0.0",
            "evidence_count": 0,
            "threshold_met": "true/false"
        },
        "coherence_check": {
            "narrative_coherent": "true/false",
            "timeline_consistent": "true/false",
            "logical_flow": "true/false"
        },
        "culprit_match": "true/false",
        "motive_match": "true/false", 
        "evidence_match": "true/false",
        "valid": "true/false",
        "confidence_score": "0.0-1.0",
        "matching_scenario": "scenario name or false",
        "scenario": "1-5 or 0",
        "answer": "response to detective following the original rules"
    }"""


def _get_improved_response_rules_section():
    """Get the improved response rules"""
    return """## Improved Response Rules
    
    The "answer" field should follow these enhanced rules:
    
    **IF valid is true (theory matches a scenario):**
    - Acknowledge the specific strengths of their deduction
    - Mention which evidence was particularly compelling
    - Celebrate their detective work with specific praise
    
    **ELSE IF confidence_score > 0.7 (very close but not quite):**
    - "You're extremely close, detective! Your reasoning shows real insight."
    - Provide specific guidance on what's strong vs. what needs refinement
    - "Your evidence about [specific strong point] is particularly compelling."
    
    **ELSE IF confidence_score > 0.4 (partially correct):**
    - Follow original "You're onto something" approach
    - Be specific about which element (culprit/motive/evidence) needs work
    - Provide targeted hints without revealing the solution
    
    **ELSE (low confidence):**
    - Follow original approach for completely incorrect theories
    - Suggest systematic re-examination of evidence"""


def _get_semantic_matching_section():
    """Get the semantic matching guidelines"""
    return """## Semantic Matching Guidelines
    
    - Accept synonyms, paraphrases, and reasonable interpretations
    - Consider context when matching evidence descriptions
    - Allow for player creativity in describing the same evidence
    - Focus on the substance of the evidence rather than exact wording
    - Weight physical evidence higher than circumstantial evidence
    - Consider cumulative effect of multiple weak pieces of evidence"""


def _get_edge_cases_section():
    """Get the edge cases handling"""
    return """## Edge Cases to Handle
    
    - Multiple possible culprits mentioned → take the primary/emphasized one
    - Evidence that could apply to multiple scenarios → award points to strongest match
    - Vague or ambiguous evidence descriptions → use best reasonable interpretation  
    - Mixed correct and incorrect evidence → calculate net score
    - Creative but accurate interpretations → reward with full points
    - Historical/timeline errors → reduce coherence score but don't invalidate evidence"""


def _get_final_note_section(rules_prompt):
    """Get the final note section"""
    return f"""IMPORTANT: Focus on the detective's understanding and reasoning rather than exact keyword matching. The goal is to recognize when they've genuinely solved the case, even if their explanation doesn't use the exact words from the scenarios.
    
    {rules_prompt}"""