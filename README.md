# Invoice Analyzer

## Overview

This Python project is designed to analyze invoices by extracting information from PDF files, emails, and text files. It processes the data to calculate the total amount in euros.

## Features

- **PDF to Text Conversion**: Utilizes `Pdf2Txt.py` to convert PDF files to text format for easy analysis.
- **Email Parsing**: Extracts relevant invoice data from emails using `ExtractMails.py`.
- **Text Analysis**: Analyzes text files containing invoice information with `AnalyzeTxtFINAL.py`.
- **Total Calculation**: Calculates the total amount in euros based on the extracted data.

## Getting Started

1. **Clone the Repository**: Clone this repository to your local machine using:
   ```
   git clone <repository_url>
   ```

2. **Install Dependencies**: Ensure you have Python installed on your system. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

3. **Usage**: 
   - Place your PDF files in the `Descargas` directory.
   - Run the relevant Python scripts to process the invoices and generate the total amount in euros.

## How does it work

This is the Input:

![image](https://github.com/rickypcyt/ScriptPythonMercadona/assets/105986682/2e1550cb-b951-4cef-b7ab-76a758920e9f)

The script 'Pdf2Txt.py' converts the pdf to text so Python can analyze it and manipulate it.

Output:

![image](https://github.com/rickypcyt/ScriptPythonMercadona/assets/105986682/b4193772-5a0e-4c57-a9b3-ae41ad36774d)


## File Structure

- **DescargasMail**: Directory where PDFs files are located.
- **OutputTxtsV2**: Output directory for converted text files.
- **AnalyzeTxtFINAL.py**: Python script to analyze text files and calculate totals.
- **ExtractMails.py**: Python script to extract invoice information from emails.
- **Pdf2Txt.py**: Python script to convert PDF files to text format.

## Notes

- Some items needed manual modification so the total woks well.
- Review `OutputTxtsV2` for insights into the analyzed data and file descriptions.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to adjust the content and add more details as needed!
