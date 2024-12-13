import os
import re
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Define the mapping for country codes
country_code_mapping = {
    'GB': 'EN',
    'IE': 'EN',
    'NI': 'EN',
    'GR': 'EL',
    'DK': 'DA',
    'RS': 'SR',
    'SI': 'SL',
    'CZ': 'CS',
    'SE': 'SV',
    'AT': 'DE',
    'CH': 'CH_DE_FR_IT',
    'CY': 'CY_EN_EL',
    'BE': 'BE_FR_NL',
    'OS': 'OS-DE_EN_FR_NL_PL_CS_SK_ES_DA_IT_HU',
    'US': 'US_AE_AS'
}

# Function to rename files and move them to a new directory
def rename_files(directory, log_widget, start_button):
    # Create a new directory with the current timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    new_directory = os.path.join(directory, f"renamed_files_{timestamp}")
    
    files_renamed = False
    total_files = 0
    renamed_files_count = 0
    failed_files_count = 0
    
    for filename in os.listdir(directory):
        # Skip directories
        if os.path.isdir(os.path.join(directory, filename)):
            continue
        
        total_files += 1
        
        try:
            # Attempt to extract the leading numbers
            leading_numbers_match = re.match(r'^(\d+)', filename)
            leading_numbers = leading_numbers_match.group(1) if leading_numbers_match else 'unknown'
            
            # Extract all country codes (two uppercase letters)
            country_codes = re.findall(r'[A-Z]{2}', filename)
            
            # Apply the mapping to the country codes and remove duplicates
            mapped_country_codes = []
            seen = set()
            for code in country_codes:
                mapped_codes = country_code_mapping.get(code, code).split('_')
                for mapped_code in mapped_codes:
                    if mapped_code not in seen:
                        mapped_country_codes.append(mapped_code)
                        seen.add(mapped_code)
            
            # Check for StyleA, StyleB, StyleC, etc., disregarding case
            style_match = re.search(r'Style[A-Z]', filename, re.IGNORECASE)
            style = style_match.group(0) if style_match else ''
            
            # Create the new filename without extension
            new_filename = f"{leading_numbers}_{'_'.join(mapped_country_codes)}"
            
            # Add the style if it exists
            if style:
                new_filename += f"_{style}"
            
            # Add the .pdf extension
            new_filename += ".pdf"
            
            # Check if the new filename already exists and add a number if necessary
            base_new_filename = new_filename[:-4]  # Remove the .pdf extension for counting
            count = 1
            while os.path.exists(os.path.join(new_directory, new_filename)):
                new_filename = f"{base_new_filename}_{count}.pdf"
                count += 1
            
            # Create the new directory if not already created
            if not files_renamed:
                os.makedirs(new_directory)
                files_renamed = True
            
            # Get the full paths
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(new_directory, new_filename)
            
            # Rename (move) the file to the new directory
            os.rename(old_file, new_file)
            log_widget.insert(tk.END, f"Renamed '{filename}' to '{new_filename}'\n")
            renamed_files_count += 1
        
        except Exception as e:
            log_widget.insert(tk.END, f"Failed to rename '{filename}': {str(e)}\n")
            failed_files_count += 1
    
    if not files_renamed:
        log_widget.insert(tk.END, "No files found to rename.\n")
        messagebox.showinfo("Result", "No files found to rename.")
    else:
        log_widget.insert(tk.END, f"\nTotal files found: {total_files}\n")
        log_widget.insert(tk.END, f"Successfully renamed: {renamed_files_count}\n")
        log_widget.insert(tk.END, f"Failed to rename: {failed_files_count}\n")
        log_widget.insert(tk.END, f"New directory: {new_directory}\n")
        log_widget.insert(tk.END, "Process completed.\n")
        messagebox.showinfo("Result", "Renaming process completed.")
        
        # Change the start button to exit button with red background
        start_button.config(text="Exit", bg="red", command=root.quit)

# Function to browse directory
def browse_directory(entry_widget):
    directory_path = filedialog.askdirectory()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, directory_path)

# Function to start renaming process
def start_renaming(entry_widget, log_widget, start_button):
    directory_path = entry_widget.get()
    if not os.path.isdir(directory_path):
        messagebox.showerror("Error", "Invalid directory path.")
        return
    
    log_widget.delete(1.0, tk.END)
    rename_files(directory_path, log_widget, start_button)

# Create GUI window
root = tk.Tk()
root.title("File Renamer")

# Directory path input
tk.Label(root, text="Directory Path:").grid(row=0, column=0, padx=10, pady=10)
directory_entry = tk.Entry(root, width=50)
directory_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: browse_directory(directory_entry)).grid(row=0, column=2, padx=10, pady=10)

# Log output
log_text = scrolledtext.ScrolledText(root, width=80, height=20)
log_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Start button
start_button = tk.Button(root, text="Start Renaming", command=lambda: start_renaming(directory_entry, log_text, start_button))
start_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Run the GUI event loop
root.mainloop()