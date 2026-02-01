# Contract Intelligence System

AI-powered procurement contract extraction system achieving 92.2% validated accuracy. Automatically extracts vendor information, dates, amounts, and terms from PDF contracts using OpenAI GPT-4o-mini.


## Features

- **Automated PDF Extraction**: Uses GPT-4o-mini to extract 8 key contract fields from any PDF
- **Real-time Validation**: Automated validation rules catch errors before database insertion
- **Duplicate Prevention**: Intelligent duplicate detection prevents re-processing same contracts
- **Web Interface**: User-friendly Streamlit dashboard for upload, browsing, and analytics
- **Data Export**: Export contracts to CSV, Excel, or JSON formats
- **Analytics Dashboard**: Visual insights with charts showing contract distribution and trends
- **Accuracy**: 92.2% validated accuracy across diverse contract types and edge cases

## Screenshots

### Upload & Extraction
<img width="1468" height="836" alt="Screenshot 2026-01-30 at 4 32 04 PM" src="https://github.com/user-attachments/assets/d142ccf9-9161-4bd9-8dde-88af9bfc1455" />

<img width="1468" height="842" alt="Screenshot 2026-01-30 at 4 32 32 PM" src="https://github.com/user-attachments/assets/be31abef-901e-4f97-bafd-da5bbda256ec" />

### Duplicate Prevention
<img width="1468" height="842" alt="Screenshot 2026-01-30 at 4 32 41 PM" src="https://github.com/user-attachments/assets/b00a965e-084a-4fd3-85f3-fa536ea32ad5" />


### Contract History
<img width="1468" height="836" alt="Screenshot 2026-01-30 at 4 31 44 PM" src="https://github.com/user-attachments/assets/858e9498-da69-4979-8c30-b4357e35d984" /> 

### Filter Functionality
<img width="1468" height="836" alt="Screenshot 2026-01-30 at 4 31 44 PM" src="https://github.com/user-attachments/assets/2868dbb6-ccf1-428b-9126-735c7dc0be19" />


### Export Functionality
<img width="1468" height="836" alt="Screenshot 2026-01-30 at 4 31 54 PM" src="https://github.com/user-attachments/assets/874d5594-53a5-4faf-b9ed-baebe9e48781" />

### Analytics Dashboard
<img width="1468" height="836" alt="Screenshot 2026-01-30 at 4 31 20 PM" src="https://github.com/user-attachments/assets/899d89a4-688d-411c-bf65-8df4b4f3719f" />


## Tech Stack

**AI & Extraction:**
- OpenAI GPT-4o-mini (AI extraction)
- PyPDF2 (PDF text extraction)

**Backend:**
- Python 3.11+
- SQLite (database)
- Custom validation framework

**Frontend:**
- Streamlit (web interface)
- Plotly (interactive charts)
- Pandas (data manipulation)

## Installation

### Prerequisites

- Python 3.11 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Step 1: Clone Repository
```bash
git clone https://github.com/Harini-1021/Contract_Intelligence_System.git
cd Contract_Intelligence_System
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your-api-key-here
```

### Step 5: Initialize Database

The database will be created automatically on first run.

## Usage

### Start the Web Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Upload a Contract

1. Navigate to **Upload Contract** page
2. Drag and drop or browse for a PDF contract
3. Click **Extract Contract Data**
4. Review extracted information
5. Click **Save to Database**

**Note:** The system automatically detects duplicate files and prevents re-processing.

### Browse Contracts

1. Navigate to **Contract History** page
2. Use filters to search by vendor or contract type
3. Sort by date, vendor, or amount
4. Export data in CSV, Excel, or JSON format

### View Analytics

1. Navigate to **Dashboard** page
2. View key metrics (total contracts, unique vendors, recent uploads)
3. Explore interactive charts showing contract distribution


## Extracted Fields

The system extracts the following information from each contract:

| Field | Description | Format |
|-------|-------------|--------|
| Vendor Name | Company or individual providing services | Text |
| Contract Number | Unique contract identifier | Text |
| Effective Date | Contract start date | YYYY-MM-DD |
| Expiration Date | Contract end date | YYYY-MM-DD |
| Total Amount | Contract total value | Currency string |
| Payment Terms | Payment schedule and conditions | Text |
| Contract Type | Type of agreement | Text |
| Key Deliverables | Main services or products | Text |

## Accuracy & Validation

### Documented Accuracy: 92.2%

Validated on 8 contracts including 5 intentionally challenging edge cases:
- **Informal contracts** with vague language ("around $20k", "one year")
- **European date formats** (DD.MM.YYYY converted to ISO standard)
- **Multiple dollar amounts** in single contract (correctly identified total)
- **Contract amendments** referencing other documents
- **Ambiguous dates** (draft vs negotiation vs effective dates)

**Results:**
- 59/64 fields extracted correctly (92.2% overall accuracy)
- 5/8 contracts achieved 100% accuracy
- Edge cases averaged 87.5% accuracy

### Automated Validation Rules

The system includes real-time validation:

1. **Required Field Checks**: Ensures critical fields like vendor_name are present
2. **Date Format Validation**: Verifies dates are in YYYY-MM-DD format
3. **Amount Validation**: Checks that amounts contain numeric values
4. **Date Logic Validation**: Ensures expiration date is after effective date
5. **Business Rules**: Flags suspicious amounts or invalid patterns

Validation runs automatically before database insertion and provides user-friendly error/warning messages in the UI.

## Project Structure
```
Contract_Intelligence_System/
├── src/
│   ├── simple_extractor.py      # AI extraction logic
│   ├── database.py               # Database operations
│   ├── contract_validator.py    # Validation rules
│   └── schema.py                 # Data schemas
├── data/
│   ├── contracts.db              # SQLite database
│   └── contracts/                # Sample PDFs
├── app.py                        # Streamlit web application
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## Known Limitations

- **Informal Language**: Accuracy drops to ~75% on contracts with vague terms like "around $20k"
- **Scanned PDFs**: Works best on text-based PDFs; scanned/image PDFs may have lower accuracy
- **Contract Amendments**: May miss amendment suffixes in contract numbers (e.g., -AMD2)
- **Processing Time**: Takes 10-30 seconds per contract (AI API call)
- **Token Limits**: Very long contracts (50+ pages) may need chunking

## Future Enhancements

- [ ] Email notifications for completed extractions
- [ ] User authentication and multi-tenant support
- [ ] REST API endpoint for programmatic access
- [ ] Support for additional document types (invoices, purchase orders)

## Development

### Run Validation Tests
```bash
python test_validator.py
```

### Calculate Accuracy Report
```bash
python validate_accuracy.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## Contact

**Harini Dandu**  
[GitHub](https://github.com/Harini-1021) | [LinkedIn](https://www.linkedin.com/in/harini-dandu)

---

**Note**: This project was built as a portfolio demonstration of AI integration, full-stack development, data validation, and production-ready software practices.
