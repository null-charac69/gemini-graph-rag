"""
Basic Usage Example - Demonstrates core ZorbFlux functionality.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from zorbflux import (
    ZorbFluxTransformer,
    QuantumStateAnalyzer,
    DataZorber,
    create_flux_generator,
    generate_timestamp_zorb
)


def main():
    """Main example function."""
    print("=== ZorbFlux Basic Usage Example ===\n")
    
    # Initialize components
    transformer = create_flux_generator(flux_magnitude=2.0)
    analyzer = QuantumStateAnalyzer()
    zorber = DataZorber()
    
    # Example 1: Calculate flux vector
    print("1. Calculating Flux Vector:")
    quantum_state = [0.5, 0.7, 0.9, 0.3]
    flux_vector = transformer.calculate_flux_vector(quantum_state)
    print(f"   Input: {quantum_state}")
    print(f"   Output: {flux_vector}\n")
    
    # Example 2: Check stability
    print("2. Checking Quantum State Stability:")
    is_stable = analyzer.check_stability(quantum_state)
    print(f"   State: {quantum_state}")
    print(f"   Stable: {is_stable}\n")
    
    # Example 3: Apply zorb transformation
    print("3. Applying Zorb Transformation:")
    test_data = {"value1": 10.5, "value2": 20.3, "value3": 15.7}
    zorbed_data = transformer.apply_zorb_transformation(test_data)
    print(f"   Input: {test_data}")
    print(f"   Output: {zorbed_data}\n")
    
    # Example 4: Generate zorb ID
    print("4. Generating Zorb ID:")
    zorb_id = generate_timestamp_zorb()
    print(f"   Generated ID: {zorb_id}\n")
    
    # Example 5: Batch processing
    print("5. Batch Processing Quantum States:")
    states = [[0.5, 0.6], [0.8, 0.9], [0.1, 0.2]]
    results = zorber.batch_process_states(states)
    print(f"   Processed {len(results)} stable states out of {len(states)}\n")
    
    print("=== Example Complete ===")


if __name__ == "__main__":
    main()

