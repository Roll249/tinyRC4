import tkinter as tk
from tkinter import messagebox, scrolledtext
from tinyrc4 import RC4

class TinyRC4App:
    def __init__(self, master):
        self.master = master
        master.title("TinyRC4 Encryption/Decryption")
        master.geometry("700x600")  # Wider and taller window

        # Create frames for better organization
        input_frame = tk.Frame(master)
        input_frame.pack(pady=10)

        # Input fields
        self.label1 = tk.Label(input_frame, text="Plaintext:")
        self.label1.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.plaintext_entry = tk.Entry(input_frame, width=50)
        self.plaintext_entry.grid(row=0, column=1, padx=5, pady=5)

        self.label2 = tk.Label(input_frame, text="Encryption Key:")
        self.label2.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.encryption_key_entry = tk.Entry(input_frame, width=50)
        self.encryption_key_entry.grid(row=1, column=1, padx=5, pady=5)

        self.label3 = tk.Label(input_frame, text="Decryption Key:")
        self.label3.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.decryption_key_entry = tk.Entry(input_frame, width=50)
        self.decryption_key_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        self.encrypt_button = tk.Button(button_frame, text="Encrypt", command=self.encrypt)
        self.encrypt_button.pack(side=tk.LEFT, padx=10)

        self.decrypt_button = tk.Button(button_frame, text="Decrypt", command=self.decrypt)
        self.decrypt_button.pack(side=tk.LEFT, padx=10)

        # Result display
        self.result_label = tk.Label(master, text="Result:")
        self.result_label.pack(anchor="w", padx=10)
        
        self.result_text = tk.Entry(master, width=70)
        self.result_text.pack(fill=tk.X, padx=10, pady=5)
        
        # Key generation steps display
        steps_label = tk.Label(master, text="Key Generation Steps:")
        steps_label.pack(anchor="w", padx=10)
        
        self.steps_text = scrolledtext.ScrolledText(master, width=80, height=20)
        self.steps_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def encrypt(self):
        plaintext = self.plaintext_entry.get()
        key = self.encryption_key_entry.get()
        
        if not plaintext or not key:
            messagebox.showerror("Error", "Plaintext and encryption key are required")
            return
        
        rc4 = RC4(key)
        rc4.gen_keystream(plaintext)
        ciphertext = rc4.crypt(plaintext)
        
        self.result_text.delete(0, tk.END)
        self.result_text.insert(0, ciphertext)
        
        # Display key generation steps
        self.display_key_generation_steps(rc4.get_key_generation_steps(), plaintext, ciphertext)

    def decrypt(self):
        ciphertext = self.plaintext_entry.get()
        key = self.decryption_key_entry.get()
        
        if not ciphertext or not key:
            messagebox.showerror("Error", "Ciphertext and decryption key are required")
            return
        
        rc4 = RC4(key)
        rc4.gen_keystream(ciphertext)
        decrypted_text = rc4.crypt(ciphertext)
        
        self.result_text.delete(0, tk.END)
        self.result_text.insert(0, decrypted_text)
        
        # Display key generation steps
        self.display_key_generation_steps(rc4.get_key_generation_steps(), ciphertext, decrypted_text)

    def display_key_generation_steps(self, steps, input_text, output_text):
        self.steps_text.delete(1.0, tk.END)
        
        # Display input and output
        self.steps_text.insert(tk.END, f"Input: {input_text}\n")
        self.steps_text.insert(tk.END, f"Output: {output_text}\n\n")
        
        # Display KSA steps
        if steps and len(steps) > 0 and 'ksa_steps' in steps[0]:
            self.steps_text.insert(tk.END, "=== KEY SCHEDULING ALGORITHM (KSA) ===\n")
            for step in steps[0]['ksa_steps']:
                if step['step'] == "Initial S-box":
                    self.steps_text.insert(tk.END, f"{step['step']}:\n")
                else:
                    self.steps_text.insert(tk.END, f"{step['step']}: i={step['i']}, j={step['j']}\n")
        
        # Display PRGA steps
        if steps and len(steps) > 1 and 'prga_steps' in steps[1]:
            self.steps_text.insert(tk.END, "\n=== PSEUDO-RANDOM GENERATION ALGORITHM (PRGA) ===\n")
            for step in steps[1]['prga_steps']:
                self.steps_text.insert(tk.END, f"{step['step']}: i={step['i']}, j={step['j']}, t={step['t']}, keystream byte={step['keystream_byte']}\n")
                
            # Display final keystream as a list of bytes
            keystream = [step['keystream_byte'] for step in steps[1]['prga_steps']]
            self.steps_text.insert(tk.END, f"\nFinal keystream: {keystream}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = TinyRC4App(root)
    root.mainloop()