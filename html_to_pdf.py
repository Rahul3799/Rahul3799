import os
import zipfile
from weasyprint import HTML

def extract_zip(zip_path, extract_folder):
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    
    return [os.path.join(extract_folder, file) for file in os.listdir(extract_folder) if file.endswith(".html")]

def convert_html_to_pdf(input_files, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for input_html in input_files:
        output_pdf = os.path.join(output_folder, os.path.splitext(os.path.basename(input_html))[0] + ".pdf")
        try:
            HTML(input_html).write_pdf(output_pdf)
            print(f"Conversion successful! PDF saved as: {output_pdf}")
        except Exception as e:
            print(f"Error converting {input_html}: {e}")

if __name__ == "__main__":
    zip_file = "sakshi_files 3.zip"  # Path to your ZIP file
    extract_folder = "extracted_html"  # Folder to extract files
    output_folder = "pdf_output"  # Output folder for PDFs
    
    input_files = extract_zip(zip_file, extract_folder)
    convert_html_to_pdf(input_files, output_folder)
