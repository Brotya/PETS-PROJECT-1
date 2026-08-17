import hmac
import hashlib
import time
import secrets
import struct
from dataclasses import dataclass
from typing import Set

# ==========================================
# INNOVATION 1: The "Drop-Fast" Decorator
# This simulates the Phase 5.3 "Drop Fast" Philosophy.
# It checks for Replay Attacks BEFORE running heavy Crypto.
# ==========================================
def drop_fast_filter(func):
    def wrapper(self, packet_bytes):
        # Phase 4.2: Extract basic info without decrypting/hashing yet
        # We assume the first 16 bytes are [Timestamp(8b), Nonce(8b)]
        timestamp, nonce = struct.unpack("!QQ", packet_bytes[:16])
        
        # Check Timestamp (Drop if older than 30 seconds)
        if time.time() - timestamp > 30:
            print(f"⚠️  [DROP FAST] Packet Expired. Timing: {timestamp}")
            return False
            
        # Check Nonce Cache
        if nonce in self.nonce_cache:
            print(f"⚠️  [DROP FAST] Replay Detected! Nonce: {nonce}")
            return False
            
        return func(self, packet_bytes)
    return wrapper

# ==========================================
# INNOVATION 2: The Secure Enclave Simulation
# Uses a Context Manager to simulate "Powering On" the Secure Hardware.
# ==========================================
class MobileEnclave:
    def __init__(self):
        # Topic 4.3: Secure Key generated inside the Enclave
        self._secret_key = secrets.token_bytes(32) 
        self.nonce_cache: Set[int] = set()

    def __enter__(self):
        print("🔒 [ENCLAVE] Hardware Powered On. Key Loaded into Isolated RAM.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("🔓 [ENCLAVE] Hardware Powered Off. Secure Memory Purged.")

    @drop_fast_filter
    def verify_nni_packet(self, packet_bytes: bytes) -> bool:
        # Phase 3.2: Split Data from HMAC Tag
        # Packet = Timestamp(8) + Nonce(8) + Payload(var) + HMAC(32)
        data_to_verify = packet_bytes[:-32]
        received_hmac = packet_bytes[-32:]

        # Phase 2.3: Re-calculate HMAC-SHA256
        h = hmac.new(self._secret_key, data_to_verify, hashlib.sha256)
        calculated_hmac = h.digest()

        # Topic 3.3: Constant-Time Comparison
        # Python's compare_digest prevents Timing Attacks!
        if hmac.compare_digest(calculated_hmac, received_hmac):
            # Store Nonce only after successful verification
            _, nonce = struct.unpack("!QQ", packet_bytes[:16])
            self.nonce_cache.add(nonce)
            return True
        return False

# ==========================================
# PHASE 5: Implementation & Attack Simulation
# ==========================================
def simulate_nni_routing():
    # 1. SETUP: Create the Enclave
    with MobileEnclave() as enclave:
        
        # 2. SENDER: Construct a valid Binary Packet
        payload = b"AI_DATA_PROMPT_001"
        timestamp = int(time.time())
        nonce = secrets.randbits(64)
        
        # Binary packing: ! = Network Byte Order, Q = 8-byte Unsigned Long
        header = struct.pack("!QQ", timestamp, nonce)
        data = header + payload
        
        # Topic 2.3: Sign the packet
        tag = hmac.new(enclave._secret_key, data, hashlib.sha256).digest()
        valid_packet = data + tag

        print("\n--- SIMULATION 1: Valid Packet ---")
        is_ok = enclave.verify_nni_packet(valid_packet)
        print(f"Result: {'✅ AUTHENTIC' if is_ok else '❌ REJECTED'}")

        # --- SIMULATION 2: Data Tampering (Topic 1.1 Avalanche) ---
        print("\n--- SIMULATION 2: Man-in-the-Middle Tampering ---")
        # Attacker changes one byte in the payload
        tampered_packet = valid_packet[:20] + b"X" + valid_packet[21:]
        is_ok = enclave.verify_nni_packet(tampered_packet)
        print(f"Result: {'✅ AUTHENTIC' if is_ok else '❌ REJECTED'}")

        # --- SIMULATION 3: Replay Attack (Topic 4.1) ---
        print("\n--- SIMULATION 3: Replay Attack ---")
        # Attacker sends the EXACT same valid packet again
        is_ok = enclave.verify_nni_packet(valid_packet)
        print(f"Result: {'✅ AUTHENTIC' if is_ok else '❌ REJECTED'}")

        # --- SIMULATION 4: Old Packet ---
        print("\n--- SIMULATION 4: Expired Packet ---")
        old_header = struct.pack("!QQ", timestamp - 500, secrets.randbits(64))
        old_data = old_header + payload
        old_tag = hmac.new(enclave._secret_key, old_data, hashlib.sha256).digest()
        is_ok = enclave.verify_nni_packet(old_data + old_tag)
        print(f"Result: {'✅ AUTHENTIC' if is_ok else '❌ REJECTED'}")

if __name__ == "__main__":
    simulate_nni_routing()