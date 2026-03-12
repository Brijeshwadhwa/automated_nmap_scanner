"""
main.py - GUI Application for Automated Nmap Scanner
This module contains the main GUI window and user interface logic.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
from scanner import NmapScanner

class NmapScannerGUI:
    """Main GUI application class for Nmap Scanner"""
    
    def __init__(self, root):
        """
        Initialize the main application window
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Automated Nmap Scanner")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Initialize scanner
        self.scanner = NmapScanner()
        self.scan_results = ""
        
        # Configure grid weights for responsive layout
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        
        # Title Label
        title_label = tk.Label(
            self.root, 
            text="Automated Nmap Scanner", 
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        # Target IP Input
        tk.Label(self.root, text="Target IP Address:", font=("Arial", 10)).grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.ip_entry = tk.Entry(self.root, width=30, font=("Arial", 10))
        self.ip_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.ip_entry.insert(0, "127.0.0.1")  # Default value for testing
        
        # Port Range Input
        tk.Label(self.root, text="Port Range (e.g., 1-1000):", font=("Arial", 10)).grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.port_entry = tk.Entry(self.root, width=30, font=("Arial", 10))
        self.port_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.port_entry.insert(0, "1-1000")  # Default value for testing
        
        # Button Frame
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Start Scan Button
        self.scan_button = tk.Button(
            button_frame,
            text="Start Scan",
            command=self.start_scan,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        self.scan_button.pack(side=tk.LEFT, padx=5)
        
        # Save Results Button
        self.save_button = tk.Button(
            button_frame,
            text="Save Results",
            command=self.save_results,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5,
            state=tk.DISABLED  # Initially disabled until scan completes
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Clear Output Button
        self.clear_button = tk.Button(
            button_frame,
            text="Clear Output",
            command=self.clear_output,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 10, "italic"),
            fg="blue"
        )
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Scrollable Text Area for Results
        self.result_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=("Courier", 10)
        )
        self.result_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        # Configure tags for colored output
        self.result_text.tag_config("open", foreground="green")
        self.result_text.tag_config("closed", foreground="red")
        self.result_text.tag_config("header", foreground="blue", font=("Courier", 10, "bold"))
        
    def validate_inputs(self):
        """
        Validate user inputs before scanning
        
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        ip_address = self.ip_entry.get().strip()
        port_range = self.port_entry.get().strip()
        
        # Check for empty fields
        if not ip_address:
            messagebox.showwarning("Input Error", "Please enter a target IP address")
            return False
        
        if not port_range:
            messagebox.showwarning("Input Error", "Please enter a port range")
            return False
        
        # Simple IP validation (basic check)
        ip_parts = ip_address.split('.')
        if len(ip_parts) != 4:
            messagebox.showerror("Invalid IP", "Please enter a valid IPv4 address")
            return False
        
        for part in ip_parts:
            if not part.isdigit() or int(part) < 0 or int(part) > 255:
                messagebox.showerror("Invalid IP", "Please enter a valid IPv4 address")
                return False
        
        # Validate port range format
        try:
            if '-' in port_range:
                start, end = map(int, port_range.split('-'))
                if start < 1 or end > 65535 or start > end:
                    raise ValueError
            else:
                port = int(port_range)
                if port < 1 or port > 65535:
                    raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Port Range",
                "Please enter a valid port range (e.g., 1-1000 or 80)"
            )
            return False
        
        return True
    
    def start_scan(self):
        """Start the Nmap scan in a separate thread"""
        if not self.validate_inputs():
            return
        
        # Disable scan button during scan
        self.scan_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.clear_output()
        
        # Update status
        self.status_label.config(text="Scanning...", fg="orange")
        
        # Get input values
        ip_address = self.ip_entry.get().strip()
        port_range = self.port_entry.get().strip()
        
        # Start scan in a separate thread
        scan_thread = threading.Thread(
            target=self.perform_scan,
            args=(ip_address, port_range),
            daemon=True
        )
        scan_thread.start()
    
    def perform_scan(self, ip_address, port_range):
        """
        Perform the actual scan (runs in a separate thread)
        
        Args:
            ip_address: Target IP address
            port_range: Port range to scan
        """
        try:
            # Perform scan
            results = self.scanner.scan_target(ip_address, port_range)
            
            # Update GUI in main thread
            self.root.after(0, self.display_results, results)
            
        except Exception as e:
            # Handle any scanning errors
            error_message = f"Scan Error: {str(e)}"
            self.root.after(0, self.display_error, error_message)
    
    def display_results(self, results):
        """
        Display scan results in the text area
        
        Args:
            results: Dictionary containing scan results
        """
        self.result_text.delete(1.0, tk.END)
        
        if "error" in results:
            self.result_text.insert(tk.END, f"Error: {results['error']}\n")
            self.status_label.config(text="Scan Failed", fg="red")
            self.scan_button.config(state=tk.NORMAL)
            return
        
        # Format and display results
        target_info = f"Target: {results['target']}\n"
        target_info += f"Scan Time: {results['scan_time']}\n"
        target_info += "-" * 50 + "\n\n"
        
        self.result_text.insert(tk.END, target_info, "header")
        
        # Store results for saving
        self.scan_results = target_info
        
        if not results['ports']:
            self.result_text.insert(tk.END, "No open ports found.\n")
            self.scan_results += "No open ports found.\n"
        else:
            for port_info in results['ports']:
                port_text = f"Port {port_info['port']:<6} - {port_info['state']:<6} - {port_info['service']}\n"
                
                # Apply color tags based on port state
                if port_info['state'].lower() == 'open':
                    self.result_text.insert(tk.END, port_text, "open")
                else:
                    self.result_text.insert(tk.END, port_text, "closed")
                
                self.scan_results += port_text
        
        # Update status
        self.status_label.config(text="Scan Completed", fg="green")
        self.scan_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
    
    def display_error(self, error_message):
        """
        Display error message in the text area
        
        Args:
            error_message: Error message to display
        """
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, error_message)
        self.status_label.config(text="Scan Failed", fg="red")
        self.scan_button.config(state=tk.NORMAL)
    
    def save_results(self):
        """Save scan results to a text file"""
        if not self.scan_results:
            messagebox.showwarning("No Results", "No scan results to save")
            return
        
        # Get target IP for filename suggestion
        ip_address = self.ip_entry.get().strip()
        default_filename = f"scan_results_{ip_address}.txt"
        
        # Open file dialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(self.scan_results)
                messagebox.showinfo("Success", f"Results saved to {filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file: {str(e)}")
    
    def clear_output(self):
        """Clear the output text area"""
        self.result_text.delete(1.0, tk.END)
        self.scan_results = ""
        self.status_label.config(text="Ready", fg="blue")
        self.save_button.config(state=tk.DISABLED)


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = NmapScannerGUI(root)
    
    # Check if Nmap is installed
    if not app.scanner.check_nmap_installed():
        messagebox.showerror(
            "Nmap Not Found",
            "Nmap is not installed or not in system PATH.\n"
            "Please install Nmap from: https://nmap.org/download.html\n"
            "Make sure to add it to your system PATH."
        )
        root.destroy()
        return
    
    root.mainloop()


if __name__ == "__main__":
    main()