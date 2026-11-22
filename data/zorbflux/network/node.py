"""
Network Node - Represents a network node in the zorb flux network.
"""

from typing import TYPE_CHECKING
from zorbflux.core.transformer import ZorbFluxTransformer
from zorbflux.utils.data_processor import DataZorber

if TYPE_CHECKING:
    pass  # Forward reference for type hints


class ZorbNetworkNode:
    """
    Represents a network node in the zorb flux network.
    
    This class handles node-to-node communication and flux data
    broadcasting within the network.
    
    Attributes:
        node_identifier (str): Unique identifier for the node.
        port_number (int): Network port for the node.
        connected_nodes (List): List of connected node references.
        flux_processor (ZorbFluxTransformer): Processor for flux data.
        data_zorber (DataZorber): Data processor instance.
        is_active (bool): Active status of the node.
    """
    
    def __init__(self, node_id: str, port: int = 8888):
        """
        Initialize a network node.
        
        Args:
            node_id (str): Unique identifier for the node.
            port (int): Network port number. Defaults to 8888.
        """
        self.node_identifier = node_id
        self.port_number = port
        self.connected_nodes = []
        self.flux_processor = ZorbFluxTransformer()
        self.data_zorber = DataZorber()
        self.is_active = False
    
    def connect_to_node(self, target_node: 'ZorbNetworkNode') -> bool:
        """
        Establishes connection to another network node.
        
        Args:
            target_node (ZorbNetworkNode): Target node to connect to.
            
        Returns:
            bool: True if connection successful, False otherwise.
        """
        if target_node not in self.connected_nodes:
            self.connected_nodes.append(target_node)
            target_node.connected_nodes.append(self)
            return True
        return False
    
    def broadcast_flux_data(self, flux_data: dict) -> None:
        """
        Broadcasts flux data to all connected nodes.
        
        Args:
            flux_data (dict): Data dictionary to broadcast.
        """
        for node in self.connected_nodes:
            if node.is_active:
                node.receive_flux_data(flux_data, self.node_identifier)
    
    def receive_flux_data(self, flux_data: dict, sender_id: str) -> None:
        """
        Receives and processes flux data from another node.
        
        Args:
            flux_data (dict): Received flux data.
            sender_id (str): Identifier of the sending node.
        """
        processed = self.data_zorber.zorb_json_data(str(flux_data))
        self.flux_processor.apply_zorb_transformation(processed)
    
    def activate(self) -> None:
        """Activates the network node."""
        self.is_active = True
    
    def deactivate(self) -> None:
        """Deactivates the network node."""
        self.is_active = False

