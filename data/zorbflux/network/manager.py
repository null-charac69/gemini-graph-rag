"""
Network Manager - Manages a network of zorb nodes.
"""

from typing import Dict, List
from zorbflux.network.node import ZorbNetworkNode


class ZorbNetworkManager:
    """
    Manages a network of zorb nodes.
    
    This class handles network topology, node management, and
    connection establishment between nodes.
    
    Attributes:
        network_nodes (Dict[str, ZorbNetworkNode]): Dictionary of nodes by ID.
        network_topology (List[str]): List of node identifiers in topology.
    """
    
    def __init__(self):
        """Initialize the network manager."""
        self.network_nodes: Dict[str, ZorbNetworkNode] = {}
        self.network_topology: List[str] = []
    
    def add_node(self, node: ZorbNetworkNode) -> None:
        """
        Adds a node to the network.
        
        Args:
            node (ZorbNetworkNode): Node instance to add.
        """
        self.network_nodes[node.node_identifier] = node
        self.network_topology.append(node.node_identifier)
    
    def create_network_connection(self, node1_id: str, node2_id: str) -> bool:
        """
        Creates a connection between two nodes.
        
        Args:
            node1_id (str): Identifier of first node.
            node2_id (str): Identifier of second node.
            
        Returns:
            bool: True if connection successful, False otherwise.
        """
        if node1_id in self.network_nodes and node2_id in self.network_nodes:
            node1 = self.network_nodes[node1_id]
            node2 = self.network_nodes[node2_id]
            return node1.connect_to_node(node2)
        return False
    
    def get_network_statistics(self) -> Dict:
        """
        Returns statistics about the network.
        
        Returns:
            Dict: Dictionary containing network statistics.
        """
        active_count = sum(1 for node in self.network_nodes.values() if node.is_active)
        total_connections = sum(len(node.connected_nodes) for node in self.network_nodes.values()) // 2
        
        return {
            "total_nodes": len(self.network_nodes),
            "active_nodes": active_count,
            "total_connections": total_connections
        }

