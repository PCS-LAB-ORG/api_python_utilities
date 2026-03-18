import pickle
import hmac
import hashlib

# Use a strong, environment-secured key in production
SECRET_KEY = b'your-secret-shared-key'

def sign_and_pickle(data, filename, SECRET_KEY=SECRET_KEY):
    # Serialize data
    serialized = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    # Create a signature based on the serialized bytes
    signature = hmac.new(SECRET_KEY, serialized, hashlib.sha256).digest()
    
    with open(filename, 'wb') as f:
        f.write(signature + serialized)

def verify_and_unpickle(filename, SECRET_KEY=SECRET_KEY):
    with open(filename, 'rb') as f:
        file_content = f.read()
    
    # Extract signature (first 32 bytes for SHA256) and data
    signature = file_content[:32]
    serialized_data = file_content[32:]
    
    # Recalculate signature to verify
    expected_signature = hmac.new(SECRET_KEY, serialized_data, hashlib.sha256).digest()
    
    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("Security Alert: Data tampering detected!")
    
    return pickle.loads(serialized_data)
