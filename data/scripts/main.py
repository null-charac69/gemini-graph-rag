"""
ZorbFlux Main Application - Entry point for the ZorbFlux system.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from zorbflux import (
    ZorbFluxTransformer,
    QuantumStateAnalyzer,
    DataZorber,
    ZorbNetworkNode,
    ZorbNetworkManager,
    ZorbConfig,
    ConfigValidator,
    create_flux_generator,
    generate_timestamp_zorb
)


def initialize_zorb_system():
    """
    Initializes the complete ZorbFlux system.
    
    Returns:
        tuple: (transformer, analyzer, data_zorber) or (None, None, None) on error
    """
    config = ZorbConfig()
    config.load_from_environment()
    
    validator = ConfigValidator()
    is_valid, errors = validator.validate_config(config)
    
    if not is_valid:
        print(f"Configuration errors: {errors}")
        return None, None, None
    
    flux_magnitude = config.get_setting("flux_magnitude")
    transformer = create_flux_generator(flux_magnitude)
    analyzer = QuantumStateAnalyzer()
    data_zorber = DataZorber()
    
    return transformer, analyzer, data_zorber


def run_zorb_processing_example():
    """Runs an example of zorb processing workflow."""
    transformer, analyzer, zorber = initialize_zorb_system()
    
    if not transformer:
        print("Failed to initialize system")
        return
    
    # Example quantum state
    quantum_state = [0.5, 0.7, 0.9, 0.3]
    
    # Calculate flux vector
    flux_vector = transformer.calculate_flux_vector(quantum_state)
    print(f"Flux Vector: {flux_vector}")
    
    # Check stability
    is_stable = analyzer.check_stability(quantum_state)
    print(f"State Stable: {is_stable}")
    
    # Process data
    test_data = {"value1": 10.5, "value2": 20.3, "value3": 15.7}
    zorbed_data = transformer.apply_zorb_transformation(test_data)
    print(f"Zorbed Data: {zorbed_data}")
    
    # Generate zorb ID
    zorb_id = generate_timestamp_zorb()
    print(f"Generated Zorb ID: {zorb_id}")


def setup_network_example():
    """Sets up and demonstrates network functionality."""
    manager = ZorbNetworkManager()
    
    node1 = ZorbNetworkNode("node_alpha", 8888)
    node2 = ZorbNetworkNode("node_beta", 8889)
    node3 = ZorbNetworkNode("node_gamma", 8890)
    
    manager.add_node(node1)
    manager.add_node(node2)
    manager.add_node(node3)
    
    manager.create_network_connection("node_alpha", "node_beta")
    manager.create_network_connection("node_beta", "node_gamma")
    
    node1.activate()
    node2.activate()
    
    stats = manager.get_network_statistics()
    print(f"Network Statistics: {stats}")
    
    # Broadcast test data
    test_flux = {"test": 42.0, "data": 3.14}
    node1.broadcast_flux_data(test_flux)


if __name__ == "__main__":
    print("=== ZorbFlux System Initialization ===")
    run_zorb_processing_example()
    
    print("\n=== Network Setup Example ===")
    setup_network_example()
    
    print("\n=== ZorbFlux System Ready ===")

