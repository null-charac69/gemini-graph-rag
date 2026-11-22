"""
Data Processor - Utility class for zorbing various data types.
"""

import json
from typing import List
from zorbflux.core.transformer import ZorbFluxTransformer
from zorbflux.core.analyzer import QuantumStateAnalyzer


class DataZorber:
    """
    Utility class for zorbing various data types.
    
    This class provides methods for processing JSON data and batch
    processing quantum states through zorb transformations.
    
    Attributes:
        zorb_transformer (ZorbFluxTransformer): Transformer instance.
        analyzer (QuantumStateAnalyzer): Analyzer instance.
        processed_count (int): Counter for processed items.
    """
    
    def __init__(self):
        """Initialize the DataZorber with default components."""
        self.zorb_transformer = ZorbFluxTransformer()
        self.analyzer = QuantumStateAnalyzer()
        self.processed_count = 0
    
    def zorb_json_data(self, json_string: str) -> dict:
        """
        Processes JSON data through zorb transformation.
        
        Args:
            json_string (str): JSON string to process.
            
        Returns:
            dict: Transformed data dictionary.
        """
        try:
            data = json.loads(json_string)
            zorbed = self.zorb_transformer.apply_zorb_transformation(
                {k: float(v) for k, v in data.items() if isinstance(v, (int, float))}
            )
            self.processed_count += 1
            return zorbed
        except json.JSONDecodeError:
            return {}
    
    def validate_quantum_state(self, state: list) -> bool:
        """
        Validates a quantum state using the analyzer.
        
        Args:
            state (list): Quantum state to validate.
            
        Returns:
            bool: True if state is valid and stable.
        """
        return self.analyzer.check_stability(state)
    
    def batch_process_states(self, states: List[List[float]]) -> List[List[float]]:
        """
        Processes multiple quantum states in batch.
        
        Args:
            states (List[List[float]]): List of quantum states to process.
            
        Returns:
            List[List[float]]: List of processed flux vectors.
        """
        results = []
        for state in states:
            if self.validate_quantum_state(state):
                flux_vector = self.zorb_transformer.calculate_flux_vector(state)
                results.append(flux_vector)
        return results

