"""
Factory for creating theory processing components
"""

from typing import Tuple

from .final_scene import FinalSceneHandler
from .theory_verifier import TheoryVerifier
from .ending_writer import EndingWriter


class TheoryComponentFactory:
    """Factory for creating theory processing components"""
    
    @staticmethod
    def create_standard_setup(
        api_service, 
        cache, 
        dev_mode: bool = False
    ) -> Tuple[
        FinalSceneHandler,
        TheoryVerifier,
        EndingWriter
    ]:
        """
        Create a standard theory processing setup
        
        Args:
            api_service: API service instance
            cache: Cache manager instance
            dev_mode: Enable development mode features
            
        Returns:
            Tuple of all theory processing components
        """
        
        # Create all components
        final_scene_handler = FinalSceneHandler(api_service, cache, dev_mode)
        theory_verifier = TheoryVerifier(api_service, cache, dev_mode)
        ending_writer = EndingWriter(api_service, cache, dev_mode)
        
        return final_scene_handler, theory_verifier, ending_writer