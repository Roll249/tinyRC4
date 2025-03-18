class RC4:
    def __init__(self, key):
        """Initialize the RC4 cipher with a key."""
        self.key = key
        self.keystream = []
        self.key_generation_steps = []
        
        # Initialize S-box (substitution box)
        self.s_box = [i for i in range(256)]
        self.initialize_s_box()
    
    def initialize_s_box(self):
        """Key Scheduling Algorithm (KSA) to initialize the S-box."""
        key_bytes = str.encode(self.key)
        j = 0
        steps = []
        
        # Store the initial state
        steps.append({
            "step": "Initial S-box",
            "s_box": self.s_box.copy()
        })
        
        # KSA algorithm
        for i in range(256):
            j = (j + self.s_box[i] + key_bytes[i % len(key_bytes)]) % 256
            # Swap values
            self.s_box[i], self.s_box[j] = self.s_box[j], self.s_box[i]
            
            # Store the step
            steps.append({
                "step": f"KSA iteration {i}",
                "i": i,
                "j": j,
                "s_box": self.s_box.copy()
            })
        
        self.key_generation_steps.append({"ksa_steps": steps})
    
    def gen_keystream(self, data):
        """Generate the keystream for the input data."""
        self.keystream = []
        steps = []
        
        i = 0
        j = 0
        
        for idx in range(len(data)):
            i = (i + 1) % 256
            j = (j + self.s_box[i]) % 256
            
            # Swap values
            self.s_box[i], self.s_box[j] = self.s_box[j], self.s_box[i]
            
            # Generate keystream byte
            t = (self.s_box[i] + self.s_box[j]) % 256
            k = self.s_box[t]
            self.keystream.append(k)
            
            # Store the step
            steps.append({
                "step": f"PRGA iteration {idx}",
                "i": i,
                "j": j,
                "t": t,
                "keystream_byte": k,
                "s_box": self.s_box.copy()
            })
        
        self.key_generation_steps.append({"prga_steps": steps})
        return self.keystream
    
    def crypt(self, data):
        """Encrypt or decrypt data using the generated keystream."""
        data_bytes = str.encode(data)
        result_bytes = bytearray()
        
        # XOR each byte with the corresponding keystream byte
        for i in range(len(data_bytes)):
            result_bytes.append(data_bytes[i] ^ self.keystream[i])
        
        # Return as a string (may contain non-printable characters)
        return result_bytes.decode('latin-1')
    
    def get_key_generation_steps(self):
        """Return the recorded steps of key generation."""
        return self.key_generation_steps