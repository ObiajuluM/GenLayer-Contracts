# { "Depends": "py-genlayer:latest" }
from email.headerregistry import Address
from genlayer import *


# TODO add DID_SET & DID_DELETE events


class DID(gl.Contract):
    """
    A smart contract for managing Decentralized Identifiers (DIDs).

    This contract allows an owner to store, update, retrieve, and delete
    DID-related information such as the DID document, data, and URI.

    Attributes:
        owner (Address): The address of the contract owner.
        network_entry_type (str): The type of network entry, set to "DID".
        did_document (str): The DID document content.
        did_data (str): Additional data associated with the DID.
        did_uri (str): The URI pointing to the DID resource.
    """

    owner: Address
    network_entry_type: str
    did_document: str
    did_data: str
    did_uri: str

    def __init__(self, did_document: str, did_data: str, did_uri: str):
        """
        Initializes the DID contract.

        Args:
            did_document (str): The initial DID document.
            did_data (str): Initial additional data for the DID.
            did_uri (str): The initial URI for the DID.
        """
        self.owner = gl.message.sender_address
        self.network_entry_type = "DID"
        self.did_document = did_document
        self.did_data = did_data
        self.did_uri = did_uri
        # TODO add DID_SET event emission here

    @gl.public.write
    def set_did(self, did_document: str, did_data: str, did_uri: str):
        """
        Updates the DID information.

        Only the owner of the contract can call this method.

        Args:
            did_document (str): The new DID document.
            did_data (str): The new additional data.
            did_uri (str): The new URI.

        Raises:
            AssertionError: If the caller is not the owner.
        """
        assert (
            gl.message.sender_address == self.owner
        ), "Only the owner can call this method"
        self.did_document = did_document
        self.did_data = did_data
        self.did_uri = did_uri
        # TODO add DID_SET event emission here

    @gl.public.view
    def get_did(self) -> TreeMap[str, str]:
        """
        Retrieves the current DID information.

        Returns:
            Treemap[str, str]: A tuple containing (did_document, did_data, did_uri).
        """
        return {"did_document": self.did_document, "did_data": self.did_data, "did_uri": self.did_uri}

    @gl.public.write
    def delete_did(self):
        """
        Deletes the DID information by clearing the stored fields.

        Only the owner of the contract can call this method.

        Raises:
            AssertionError: If the caller is not the owner.
        """
        assert (
            gl.message.sender_address == self.owner
        ), "Only the owner can call this method"
        self.did_document = ""
        self.did_data = ""
        self.did_uri = ""
        # TODO: see if we want to selfdestruct the contract here
        # TODO add DID_DELETE event emission here
