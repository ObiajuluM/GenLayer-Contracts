# Decentralized Identifiers

A Decentralized Identifier (DID) is a new type of identifier defined by the World Wide Web Consortium (W3C) that enables verifiable, digital identities. DIDs are fully under the control of the DID owner, independent from any centralized registry, identity provider, or certificate authority.

The key principles of a DID are:

*   **Decentralization**: No central issuing agency controls the DID, enabling the owner to update, resolve, or deactivate it. This also makes your identity highly-available, since DIDs are usually stored on a blockchain and always available for verification.
*   **Verifiable Credentials**: Anyone can create a DID and falsify the information on it. To prove the authenticity of a DID, a user must provide a verifiable credential (VC) that is cryptographically secure and tamper-evident. In the DID ecosystem, there are three parties: user, issuer, and verifier. The user controls the DID, but needs a trusted issuer to verify the information offline. The issuer provides a verfiable credential, which the user gives to verifiers that need to confirm the user's identity. To learn more about the DID ecosystem, see: [Ecosystem Overview](https://www.w3.org/TR/vc-data-model/#ecosystem-overview).
*   **Interoperability**: DIDs are open to any solution that recognizes the W3C DID standard. This means a DID can be used to authenticate and establish trust in various digital transactions and interactions.

> **Note**
> The implementation of DIDs on the GenLayer conforms to the requirements in the [DID v1.0 specification](https://www.w3.org/TR/did-1.0/).

## How It Works

1.  An GenLayer account holder generates a DID that is controlled by the account.
2.  The DID is associated with a DID document as defined by W3C specifications.
3.  A user provides their DID and VC to a verifier for a digital task.
4.  The verifier resolves the DID to its document and uses the VC to verify its authenticity.

## DID Documents

DID documents contain the necessary information to cryptographically verify the identity of the subject described by a DID document. The subject can be a person, organization, or thing. For example, a DID document could contain cryptographic public keys that the DID subject can use to authenticate itself and prove its association with the DID.

> **Note**
> DID documents usually serialize to a JSON or JSON-LD representation.

On GenLayer, there are several ways to associate a DID to a DID document:

1.  Store a reference to the document in the URI field of the DID object, which points to a document stored on another decentralized storage network, such as IPFS or STORJ.
2.  Store a minimal DID document in the DIDDocument field of the DID object.
3.  Use a minimal implicit DID document generated from the DID and other available public information.

> **Note**
> Simpler use cases may only need signatures and simple authorization tokens. In cases where there isn't explicitly a DID document on the ledger, an implicit document is used instead. For example, the implicit DID Document of `did:genlayer:1:0330E7FC9D56BB25D6893BA3F317AE5BCF33B3291BD63DB32654A313222F7FD020` enables only a single key `0330E7FC9D56BB25D6893BA3F317AE5BCF33B3291BD63DB32654A313222F7FD020` to authorize changes on the DID document or sign credentials in the name of the DID.

### Sample GenLayer DID Document

```json
{
    "@context": "https://w3id.org/did/v1",
    "id": "did:genlayer:1:923A46b80e10E21750885e8f0674834Ba9570C45",
    "publicKey": [
        {
            "id": "did:genlayer:1:923A46b80e10E21750885e8f0674834Ba9570C45#keys-1",
            "type": ["CryptographicKey", "EcdsaKoblitzPublicKey"],
            "curve": "secp256k1",
            "expires": 15674657,
            "publicKeyHex": "04f42987b7faee8b95e2c3a3345224f00e00dfc67ba882..."
        }
    ]
}
```

To learn more about the core properties of a DID document, see: [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-1.0/#core-properties).

## Privacy and Security Concerns

*   Whoever controls the private keys of a GenLayer account, controls the DID and reference to the DID document it resolves to. Take care to ensure your private keys aren't compromised.
*   You can include any content in a DID document, but should limit it to verification methods and service points. Since DIDs on GenLayer are publicly available, you shouldn't include any personal information.
*   IPFS allows anyone to store content on the nodes in a distributed network. A common misconception is that anyone can edit that content; however, the content-addressability of IPFS means any edited content will have a different address from the original. While any entity can copy a DID document anchored with an GenLayer account's DIDDocument or URI fields, they can't change the document itself unless they control the private key that created the corresponding DID object.

## Use Cases

DIDs enable many use cases, such as:

1.  Meeting Know Your Client (KYC) and Anti-money Laundering (AML) standards.
2.  User identity management across the GenLayer.
3.  Differentiated access to DeFi apps.
4.  Signing digital documents.
5.  Making secure online transactions.
6.  Logging into websites.

---

# Smart Contract Implementation

This repository contains a GenLayer smart contract for managing Decentralized Identifiers (DIDs).

## Overview

The `DID` contract allows users to register, update, retrieve, and delete DID information on the GenLayer network. It stores the DID document, associated data, and a URI.

## Features

-   **Registration**: Initialize a new DID with a document, data, and URI.
-   **Update**: The owner can update the DID information.
-   **Retrieval**: Anyone can read the stored DID information.
-   **Deletion**: The owner can clear the DID information.

## Contract Interface

### `__init__(self, did_document: str, did_data: str, did_uri: str)`

Initializes the contract and sets the deployer as the owner.

-   `did_document`: The content of the DID document.
-   `did_data`: Additional metadata or data associated with the DID.
-   `did_uri`: A URI pointing to the DID resource.

### `set_did(self, did_document: str, did_data: str, did_uri: str)`

Updates the stored DID information. This method is restricted to the contract owner.

-   `did_document`: The new DID document content.
-   `did_data`: The new additional data.
-   `did_uri`: The new URI.

### `get_did(self) -> tuple[str, str, str]`

Retrieves the current DID information.

-   **Returns**: A tuple containing `(did_document, did_data, did_uri)`.

### `delete_did(self)`

Clears the stored DID information. This method is restricted to the contract owner.

## Usage

To use this contract, deploy it to the GenLayer network. The account that deploys the contract becomes the owner and is the only one authorized to modify the DID data.
