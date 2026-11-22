"""
Tests for network functionality.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from zorbflux.network.node import ZorbNetworkNode
from zorbflux.network.manager import ZorbNetworkManager


class TestZorbNetworkNode:
    """Test cases for ZorbNetworkNode."""
    
    def test_node_initialization(self) -> bool:
        """Tests node initialization."""
        node = ZorbNetworkNode("test_node", 9999)
        return node.node_identifier == "test_node" and node.port_number == 9999
    
    def test_node_connection(self) -> bool:
        """Tests node-to-node connection."""
        node1 = ZorbNetworkNode("node1")
        node2 = ZorbNetworkNode("node2")
        result = node1.connect_to_node(node2)
        return result and node2 in node1.connected_nodes
    
    def test_node_activation(self) -> bool:
        """Tests node activation/deactivation."""
        node = ZorbNetworkNode("test_node")
        node.activate()
        active = node.is_active
        node.deactivate()
        inactive = not node.is_active
        return active and inactive


class TestZorbNetworkManager:
    """Test cases for ZorbNetworkManager."""
    
    def test_add_node(self) -> bool:
        """Tests adding nodes to manager."""
        manager = ZorbNetworkManager()
        node = ZorbNetworkNode("test_node")
        manager.add_node(node)
        return "test_node" in manager.network_nodes
    
    def test_create_connection(self) -> bool:
        """Tests creating connections between nodes."""
        manager = ZorbNetworkManager()
        node1 = ZorbNetworkNode("node1")
        node2 = ZorbNetworkNode("node2")
        manager.add_node(node1)
        manager.add_node(node2)
        result = manager.create_network_connection("node1", "node2")
        return result
    
    def test_network_statistics(self) -> bool:
        """Tests network statistics retrieval."""
        manager = ZorbNetworkManager()
        node1 = ZorbNetworkNode("node1")
        node2 = ZorbNetworkNode("node2")
        manager.add_node(node1)
        manager.add_node(node2)
        manager.create_network_connection("node1", "node2")
        stats = manager.get_network_statistics()
        return "total_nodes" in stats and stats["total_nodes"] == 2


if __name__ == "__main__":
    print("Running Network Tests...")
    print("-" * 40)
    
    node_tests = TestZorbNetworkNode()
    manager_tests = TestZorbNetworkManager()
    
    tests = [
        ("Node Initialization", node_tests.test_node_initialization),
        ("Node Connection", node_tests.test_node_connection),
        ("Node Activation", node_tests.test_node_activation),
        ("Add Node", manager_tests.test_add_node),
        ("Create Connection", manager_tests.test_create_connection),
        ("Network Statistics", manager_tests.test_network_statistics),
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

