```markdown
# LASRERA Practitioners Scraper

A Python web scraper for extracting practitioner information from the Lagos State Real Estate Regulatory Authority (LASRERA) website. This tool automates the collection of registered real estate practitioners' contact details and saves them to an Excel file.

## 🎯 Features

- **Automated Data Extraction**: Scrapes practitioner names, phone numbers, emails, office addresses, and registration status
- **Pagination Support**: Automatically navigates through all pages of results (94+ pages)
- **CloudFlare Email Decoding**: Bypasses CloudFlare email protection to extract real email addresses
- **Multiple Email Detection Methods**: Uses three different approaches to find email addresses
- **Excel Export**: Saves all data to a properly formatted Excel file
- **Robust Error Handling**: Continues scraping even if individual records fail
- **Progress Tracking**: Real-time progress updates during scraping
- **Stealth Mode**: Configured to avoid detection as an automated browser

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Chrome browser installed
- ChromeDriver (automatically managed by Selenium)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/lasrera-scraper.git
cd lasrera-scraper
```

2. Install required packages:
```bash
pip install selenium openpyxl
```

3. Run the scraper:
```bash
python scraper.py
```

## 📋 Dependencies

```
selenium>=4.0.0
openpyxl>=3.0.0
```

## 🔧 Configuration

### Browser Settings
The scraper runs in headless mode by default. To watch the scraping process:
```python
# Comment out this line in the code:
# options.add_argument("--headless")
```

### Output Customization
The Excel file is saved as `lasrera_practitioners.xlsx` in the same directory. To change the filename:
```python
excel_filename = "your_custom_filename.xlsx"
```

## 📊 Output Format

The scraper generates an Excel file with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| Name | Company/Practitioner name | ROCKMOULD LIMITED |
| Mobile | Phone number | 08157341538 |
| Email | Email address | info@rockmould.com |
| Office | Office address | 24 TAIYE OLOWU STREET, OFF ADMIRALTY WAY |
| Status | Registration status | ACTIVE |

## 🛠️ How It Works

### 1. Website Analysis
- Connects to the LASRERA practitioner search page
- Handles dynamic content loading with JavaScript
- Identifies pagination structure (94+ pages of data)

### 2. Data Extraction Process
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Load Page     │───▶│  Extract Data    │───▶│  Save to Excel  │
│                 │    │  from Agents     │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       ▲
         ▼                       ▼                       │
┌─────────────────┐    ┌──────────────────┐              │
│  Next Page?     │    │  Decode Emails   │──────────────┘
│                 │    │  (CloudFlare)    │
└─────────────────┘    └──────────────────┘
```

### 3. Email Extraction Methods
The scraper uses three methods to extract emails:

1. **CloudFlare Decoding**: Decodes protected emails using `data-cfemail` attribute
2. **Regex Pattern Matching**: Finds plain text email addresses
3. **Mailto Link Extraction**: Extracts emails from `mailto:` links

### 4. Pagination Handling
- Automatically detects pagination controls
- Navigates through all available pages
- Stops when reaching the last page or encountering errors

## 🔍 Debugging Features

The scraper includes comprehensive debugging output:

```
📄 Processing page 1...
Found 12 agents on page 1
🔍 Debug - Agent 1: Encoded email = a5c4cbcbc4cdc4d7d7ccd6e5c3cccbclcdcaded6c@8bc6cac8
🔍 Debug - Agent 1: Decoded email = info@rockmould.com
✅ Agent 1: ROCKMOULD LIMITED | 08157341538 | info@rockmould.com
```

## ⚠️ Important Notes

### Legal Compliance
- This scraper is designed for educational and research purposes
- Always respect the website's terms of service and robots.txt
- Consider rate limiting and being respectful to the server
- The scraped data should be used responsibly

### Rate Limiting
The scraper includes built-in delays:
- 3-5 seconds between page loads
- 4 seconds after pagination clicks
- Additional delays for CloudFlare protection

### Error Handling
- Continues scraping even if individual records fail
- Provides detailed error messages for debugging
- Gracefully handles network timeouts and element not found errors

## 🚨 Troubleshooting

### Common Issues

1. **ChromeDriver not found**
   ```bash
   # Update Selenium to auto-manage ChromeDriver
   pip install --upgrade selenium
   ```

2. **CloudFlare blocking requests**
   - The scraper includes stealth settings
   - Increase delays between requests if needed
   - Consider using proxy rotation for large-scale scraping

3. **Elements not found**
   - Website structure may have changed
   - Check the CSS selectors in the code
   - Run in non-headless mode to debug visually

4. **Empty email addresses**
   - Check the debugging output for encoded email values
   - Verify CloudFlare protection is still using the same method
   - Website may have updated their email protection

## 📈 Performance

- **Speed**: ~3-5 seconds per page
- **Capacity**: Handles 94+ pages with 10-15 practitioners each
- **Memory**: Low memory footprint with streaming Excel writing
- **Reliability**: Robust error handling for continuous operation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black lasrera_scraper.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Lagos State Real Estate Regulatory Authority (LASRERA) for providing public access to practitioner data
- Selenium WebDriver community for excellent documentation
- CloudFlare email decoding solution contributors

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/lasrera-scraper/issues) page
2. Create a new issue with detailed description
3. Include error messages and system information

## 🔄 Version History

- **v1.0.0** - Initial release with basic scraping functionality
- **v1.1.0** - Added CloudFlare email decoding
- **v1.2.0** - Enhanced error handling and debugging features
- **v1.3.0** - Added multiple email extraction methods and stealth mode

---

**Disclaimer**: This tool is for educational and research purposes only. Always respect website terms of service and use responsibly.
```

This README provides comprehensive documentation including:

1. **Clear project description** and features
2. **Step-by-step installation** instructions
3. **Usage examples** and configuration options
4. **Technical details** about how it works
5. **Troubleshooting guide** for common issues
6. **Contributing guidelines** for open source collaboration
7. **Legal disclaimers** and responsible use guidelines
8. **Performance metrics** and technical specifications

The documentation is structured to be helpful for both users and contributors, with proper formatting and emoji icons for better readability.
