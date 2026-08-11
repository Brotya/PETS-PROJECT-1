import numpy as np
from diffprivlib.mechanisms import Laplace
import random
import hashlib

# --- FEATURE 1: PRIVACY BUDGET MONITOR ---
# Tracks how much 'Privacy Budget' (Epsilon) is used to prevent data leaks.
class PrivacyGuard:
    def __init__(self, total_budget=5.0):
        self.budget = total_budget

    def consume_budget(self, amount):
        if self.budget >= amount:
            self.budget -= amount
            return True
        return False

# --- FEATURE 2: PRIVATE SET INTERSECTION (PSI) ---
# Finds common patients using Hashed IDs (Digital Fingerprints).
def private_set_intersection(list_a, list_b):
    # Hash everything so raw names/IDs are never compared directly
    hash_a = {hashlib.sha256(str(x).encode()).hexdigest() for x in list_a}
    hash_b = {hashlib.sha256(str(x).encode()).hexdigest() for x in list_b}
    common_hashes = hash_a.intersection(hash_b)
    return len(common_hashes) # Returns count of common elements only

# --- FEATURE 3: ZERO-KNOWLEDGE PROOF (SIMULATED) ---
# Prove a condition (Age > 18) without revealing the age.
class ZKPAgeVerifier:
    @staticmethod
    def prove_membership(age, threshold=18):
        # In a real ZKP, this would involve complex polynomials.
        # Here we simulate the result: returning a proof that is 'True' 
        # without returning the variable 'age'.
        is_valid = age >= threshold
        commitment = hashlib.sha256(str(is_valid).encode()).hexdigest()
        return commitment, is_valid

# --- REUSING PREVIOUS TFHE & DP LOGIC ---
class LocalHospitalDB:
    def __init__(self, data):
        self.data = np.array(data)

    def query_avg_age(self, epsilon, guard):
        if not guard.consume_budget(epsilon):
            return "ERROR: Privacy budget exhausted!"
        dp_mechanism = Laplace(epsilon=epsilon, sensitivity=20)
        return dp_mechanism.randomise(np.mean(self.data))

class TorusFHE:
    def encode_bit(self, bit):
        mu = 0.0 if bit == 0 else 0.5
        noise = random.uniform(-0.05, 0.05)
        return (mu + noise) % 1.0

    def decrypt_bit(self, torus_val):
        dist_to_half = abs(torus_val - 0.5)
        return 1 if dist_to_half < 0.25 else 0

# --- MAIN ENGINE EXECUTION ---
if __name__ == "__main__":
    print("\n" + "=".center(40, "="))
    print(" PriviSense v2.0 Engine ".center(40, "="))
    print("=".center(40, "="))

    # Setup Budget
    guard = PrivacyGuard(total_budget=2.0)
    hospital_a = LocalHospitalDB([25, 30, 45, 50, 80])

    # 1. DP with Budget Monitor
    print(f"\n[Budget] Initial Privacy Budget: {guard.budget}")
    print(f"[DP] Query 1 (Epsilon 1.0): {hospital_a.query_avg_age(1.0, guard):.2f}")
    print(f"[DP] Query 2 (Epsilon 1.0): {hospital_a.query_avg_age(1.0, guard):.2f}")
    print(f"[DP] Query 3 (Epsilon 1.0): {hospital_a.query_avg_age(1.0, guard)}")

    # 2. Private Set Intersection (PSI)
    hosp_1_patients = [101, 102, 103, 104]
    hosp_2_patients = [103, 104, 105, 106]
    matches = private_set_intersection(hosp_1_patients, hosp_2_patients)
    print(f"\n[PSI] Patients found in both databases: {matches} (without sharing IDs)")

    # 3. Zero-Knowledge Proof (ZKP)
    my_age = 25
    proof, result = ZKPAgeVerifier.prove_membership(my_age, threshold=18)
    print(f"\n[ZKP] Proving Age > 18... \n[ZKP] Proof Hash: {proof} \n[ZKP] Verdict: {'User is Adult' if result else 'User is Minor'}")

    # 4. TFHE (Encrypted Logic)
    fhe = TorusFHE()
    c1 = fhe.encode_bit(1)
    c2 = fhe.encode_bit(1)
    # Adding two encrypted 1s on a Torus wraps around (1+1=0 in XOR logic)
    res = (c1 + c2) % 1.0
    print(f"\n[TFHE] Computing 1 XOR 1 on Encrypted Torus...")
    print(f"[TFHE] Decrypted Result: {fhe.decrypt_bit(res)}")

    print("\n" + "=".center(40, "="))