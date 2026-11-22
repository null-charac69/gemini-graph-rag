"""
Network Demo - Demonstrates network functionality.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from zorbflux import ZorbNetworkNode, ZorbNetworkManager


def main():
    """Main network demo function."""
    print("=== ZorbFlux Network Demo ===\n")
    
    # Create network manager
    manager = ZorbNetworkManager()
    
    # Create nodes
    print("1. Creating Network Nodes:")
    node1 = ZorbNetworkNode("node_alpha", 8888)
    node2 = ZorbNetworkNode("node_beta", 8889)
    node3 = ZorbNetworkNode("node_gamma", 8890)
    
    print(f"   Created: {node1.node_identifier}, {node2.node_identifier}, {node3.node_identifier}\n")
    
    # Add nodes to network
    print("2. Adding Nodes to Network:")
    manager.add_node(node1)
    manager.add_node(node2)
    manager.add_node(node3)
    print(f"   Total nodes: {len(manager.network_nodes)}\n")
    
    # Create connections
    print("3. Creating Network Connections:")
    manager.create_network_connection("node_alpha", "node_beta")
    manager.create_network_connection("node_beta", "node_gamma")
    print("   Connections established\n")
    
    # Activate nodes
    print("4. Activating Nodes:")
    node1.activate()
    node2.activate()
    print(f"   Node 1 active: {node1.is_active}")
    print(f"   Node 2 active: {node2.is_active}")
    print(f"   Node 3 active: {node3.is_active}\n")
    
    # Get statistics
    print("5. Network Statistics:")
    stats = manager.get_network_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    # Broadcast test data
    print("6. Broadcasting Flux Data:")
    test_flux = {"test": 42.0, "data": 3.14}
    node1.broadcast_flux_data(test_flux)
    print("   Data broadcasted from node_alpha\n")
    
    print("=== Demo Complete ===")


if __name__ == "__main__":
    main()

