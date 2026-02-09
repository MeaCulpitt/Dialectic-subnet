
```python
"""
Merkle Tree Implementation for Reasoning Trees

Provides cryptographic commitment to reasoning structure,
enabling efficient O(log n) verification of contested branches.
"""

import hashlib
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class MerkleNode:
    """A node in the Merkle tree."""
    hash: str
    data_id: Optional[str] = None  # Corresponding reasoning node ID
    left: Optional['MerkleNode'] = None
    right: Optional['MerkleNode'] = None


def hash_data(data: str) -> str:
    """Hash data using SHA-256."""
    return hashlib.sha256(data.encode()).hexdigest()


def hash_node(node_data: Dict) -> str:
    """
    Hash a reasoning node for Merkle commitment.
    
    Includes: id, claim, node_type, evidence, children
    """
    # Canonical JSON for consistent hashing
    canonical = json.dumps(node_data, sort_keys=True, separators=(',', ':'))
    return hash_data(canonical)


def combine_hashes(left: str, right: str) -> str:
    """Combine two hashes into a parent hash."""
    combined = left + right
    return hash_data(combined)


class ReasoningMerkleTree:
    """
    Merkle tree for reasoning structure verification.
    
    Allows:
    - Efficient proof that a node exists in the tree
    - Verification that a node hasn't been modified
    - O(log n) challenge verification
    """
    
    def __init__(self):
        self.root: Optional[MerkleNode] = None
        self.nodes: Dict[str, str] = {}  # node_id -> hash
        self.proofs: Dict[str, List[Tuple[str, str]]] = {}  # node_id -> proof path
    
    def build_from_reasoning_tree(self, reasoning_nodes: List[Dict]) -> str:
        """
        Build Merkle tree from reasoning nodes.
        
        Args:
            reasoning_nodes: List of reasoning node dictionaries
            
        Returns:
            Merkle root hash
        """
        if not reasoning_nodes:
            return hash_data("")
        
        # Hash each reasoning node
        leaves = []
        for node in reasoning_nodes:
            node_hash = hash_node(node)
            self.nodes[node['id']] = node_hash
            leaves.append(MerkleNode(hash=node_hash, data_id=node['id']))
        
        # Build tree bottom-up
        self.root = self._build_tree(leaves)
        
        # Generate proofs for each node
        for node_id in self.nodes:
            self.proofs[node_id] = self._generate_proof(node_id)
        
        return self.root.hash
    
    def _build_tree(self, nodes: List[MerkleNode]) -> MerkleNode:
        """Recursively build tree from leaf nodes."""
        if len(nodes) == 1:
            return nodes[0]
        
        # Pad to even number
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])
        
        # Build parent level
        parents = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1]
            parent_hash = combine_hashes(left.hash, right.hash)
            parents.append(MerkleNode(hash=parent_hash, left=left, right=right))
        
        return self._build_tree(parents)
    
    def _generate_proof(self, node_id: str) -> List[Tuple[str, str]]:
        """
        Generate Merkle proof for a specific node.
        
        Returns list of (hash, direction) tuples.
        """
        if node_id not in self.nodes:
            return []
        
        target_hash = self.nodes[node_id]
        proof = []
        
        def find_and_prove(node: Optional[MerkleNode], target: str) -> bool:
            if node is None:
                return False
            if node.hash == target and node.data_id == node_id:
                return True
            
            # Check left subtree
            if node.left and find_and_prove(node.left, target):
                if node.right:
                    proof.append((node.right.hash, "right"))
                return True
            
            # Check right subtree
            if node.right and find_and_prove(node.right, target):
                if node.left:
                    proof.append((node.left.hash, "left"))
                return True
            
            return False
        
        find_and_prove(self.root, target_hash)
        return proof
    
    def get_proof(self, node_id: str) -> Optional[List[Tuple[str, str]]]:
        """Get Merkle proof for a node."""
        return self.proofs.get(node_id)
    
    def verify_proof(
        self, 
        node_data: Dict, 
        proof: List[Tuple[str, str]], 
        root_hash: str
    ) -> bool:
        """
        Verify a Merkle proof.
        
        Args:
            node_data: The reasoning node to verify
            proof: List of (sibling_hash, direction) tuples
            root_hash: Expected root hash
            
        Returns:
            True if proof is valid
        """
        current_hash = hash_node(node_data)
        
        for sibling_hash, direction in proof:
            if direction == "left":
                current_hash = combine_hashes(sibling_hash, current_hash)
            else:
                current_hash = combine_hashes(current_hash, sibling_hash)
        
        return current_hash == root_hash
    
    def get_root(self) -> Optional[str]:
        """Get the Merkle root hash."""
        return self.root.hash if self.root else None


def create_merkle_commitment(reasoning_tree: Dict) -> Tuple[str, Dict[str, List]]:
    """
    Create Merkle commitment for a reasoning tree.
    
    Args:
        reasoning_tree: Dict with 'root' and 'nodes' keys
        
    Returns:
        Tuple of (merkle_root, node_proofs)
    """
    tree = ReasoningMerkleTree()
    
    # Collect all nodes
    all_nodes = [reasoning_tree['root']] + reasoning_tree.get('nodes', [])
    
    # Convert to dicts if needed
    nodes_as_dicts = []
    for node in all_nodes:
        if hasattr(node, 'dict'):
            nodes_as_dicts.append(node.dict())
        else:
            nodes_as_dicts.append(node)
    
    merkle_root = tree.build_from_reasoning_tree(nodes_as_dicts)
    
    return merkle_root, tree.proofs
```

---
