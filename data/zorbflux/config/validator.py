"""
Configuration Validator - Validates configuration settings.
"""

from typing import Tuple, List
from zorbflux.config.settings import ZorbConfig


class ConfigValidator:
    """
    Validates configuration settings.
    
    This class provides static methods for validating individual
    settings and instance methods for validating entire configurations.
    """
    
    @staticmethod
    def validate_flux_magnitude(magnitude: float) -> bool:
        """
        Validates that flux magnitude is within acceptable range.
        
        Args:
            magnitude (float): Flux magnitude value to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        return 0.1 <= magnitude <= 10.0
    
    @staticmethod
    def validate_quantum_threshold(threshold: float) -> bool:
        """
        Validates that quantum threshold is within acceptable range.
        
        Args:
            threshold (float): Quantum threshold value to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        return 0.0 <= threshold <= 1.0
    
    def validate_config(self, config: ZorbConfig) -> Tuple[bool, List[str]]:
        """
        Validates an entire configuration object.
        
        Args:
            config (ZorbConfig): Configuration object to validate.
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = []
        
        flux = config.get_setting("flux_magnitude")
        if not self.validate_flux_magnitude(flux):
            errors.append(f"Invalid flux_magnitude: {flux}")
        
        threshold = config.get_setting("quantum_threshold")
        if not self.validate_quantum_threshold(threshold):
            errors.append(f"Invalid quantum_threshold: {threshold}")
        
        return len(errors) == 0, errors

