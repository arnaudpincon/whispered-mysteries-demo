"""
Theory Prompts
Separated into agents for theory collection and verification
"""

from .collect_theory_agent import create_collect_theory
from .analyse_theory_agent import create_analyse_theory

__all__ = [
    'create_collect_theory',
    'create_analyse_theory',
]