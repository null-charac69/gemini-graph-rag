"""
Tests for core ZorbFlux functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from zorbflux.core.transformer import ZorbFluxTransformer, create_flux_generator
from zorbflux.core.analyzer import QuantumStateAnalyzer


class TestZorbFluxTransformer:
    """Test cases for ZorbFluxTransformer."""
    
    def test_flux_transformation(self) -> bool:
        """Tests flux vector transformation."""
        transformer = ZorbFluxTransformer(flux_magnitude=2.0)
        input_state = [1.0, 2.0, 3.0]
        result = transformer.calculate_flux_vector(input_state)
        return len(result) == 3 and result[0] > 0
    
    def test_zorb_transformation(self) -> bool:
        """Tests zorb transformation on dictionary."""
        transformer = ZorbFluxTransformer(flux_magnitude=1.5)
        test_data = {"value1": 10.0, "value2": 20.0}
        result = transformer.apply_zorb_transformation(test_data)
        return "zorb_value1" in result and "zorb_value2" in result
    
    def test_register_zorb(self) -> bool:
        """Tests zorb registration."""
        transformer = ZorbFluxTransformer()
        transformer.register_zorb("test_zorb_123")
        return "test_zorb_123" in transformer.active_zorbs
    
    def test_factory_function(self) -> bool:
        """Tests factory function."""
        transformer = create_flux_generator(3.0)
        return transformer.quantum_flux_magnitude == 3.0


class TestQuantumStateAnalyzer:
    """Test cases for QuantumStateAnalyzer."""
    
    def test_quantum_stability(self) -> bool:
        """Tests quantum state stability checking."""
        analyzer = QuantumStateAnalyzer()
        stable_state = [0.8, 0.9, 0.7]
        unstable_state = [0.1, 0.2, 0.1]
        
        is_stable1 = analyzer.check_stability(stable_state)
        is_stable2 = analyzer.check_stability(unstable_state)
        
        return is_stable1 and not is_stable2
    
    def test_quantum_pattern_analysis(self) -> bool:
        """Tests quantum pattern analysis."""
        analyzer = QuantumStateAnalyzer()
        pattern = [1, 2, 3, 4, 5]
        result = analyzer.analyze_quantum_pattern(pattern)
        return "entropy" in result and "coherence" in result
    
    def test_empty_pattern(self) -> bool:
        """Tests handling of empty pattern."""
        analyzer = QuantumStateAnalyzer()
        result = analyzer.analyze_quantum_pattern([])
        return result["entropy"] == 0.0 and result["coherence"] == 0.0


if __name__ == "__main__":
    print("Running Core Tests...")
    print("-" * 40)
    
    transformer_tests = TestZorbFluxTransformer()
    analyzer_tests = TestQuantumStateAnalyzer()
    
    tests = [
        ("Flux Transformation", transformer_tests.test_flux_transformation),
        ("Zorb Transformation", transformer_tests.test_zorb_transformation),
        ("Register Zorb", transformer_tests.test_register_zorb),
        ("Factory Function", transformer_tests.test_factory_function),
        ("Quantum Stability", analyzer_tests.test_quantum_stability),
        ("Pattern Analysis", analyzer_tests.test_quantum_pattern_analysis),
        ("Empty Pattern", analyzer_tests.test_empty_pattern),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✓ {test_name}: PASSED")
                passed += 1
            else:
                print(f"✗ {test_name}: FAILED")
                failed += 1
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {e}")
            failed += 1
    
    print("-" * 40)
    print(f"Passed: {passed}, Failed: {failed}")

