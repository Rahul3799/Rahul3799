from weasyprint import HTML
import os
import multiprocessing

def convert_html_to_pdf(input_html, output_pdf, base_url, timeout=30):
    """ Converts a single HTML file to PDF with a timeout. """
    try:
        HTML(filename=input_html, base_url=base_url).write_pdf(output_pdf)
        print(f"Converted: {input_html} -> {output_pdf}")
    except Exception as e:
        print(f"Error converting {input_html}: {e}")

def convert_html_folder_to_pdf(input_folder, output_folder, timeout=30):
    """ Converts all HTML files in a folder to PDF with a timeout per file. """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    html_files = [f for f in os.listdir(input_folder) if f.endswith(".html")]
    
    if not html_files:
        print(f"No HTML files found in '{input_folder}'.")
        return

    for html_file in html_files:
        input_html = os.path.join(input_folder, html_file)
        output_pdf = os.path.join(output_folder, os.path.splitext(html_file)[0] + ".pdf")

        process = multiprocessing.Process(target=convert_html_to_pdf, args=(input_html, output_pdf, input_folder))
        process.start()
        process.join(timeout)  # Allow only `timeout` seconds

        if process.is_alive():
            print(f"Timeout! Skipping {input_html} after {timeout} seconds.")
            process.terminate()
            process.join()

if __name__ == "__main__":
    input_folder = "sakshi_files"  # Folder containing HTML files
    output_folder = "pdf_output new"  # Output folder for PDFs
    convert_html_folder_to_pdf(input_folder, output_folder, timeout=30)  # Set timeout in seconds
