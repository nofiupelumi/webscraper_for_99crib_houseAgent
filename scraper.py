from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import openpyxl
import re
import tempfile

# Improved Cloudflare email decoder with debugging
def decode_cf_email(encoded_string):
    try:
        if not encoded_string or len(encoded_string) < 2:
            return ""
        
        r = int(encoded_string[:2], 16)
        email = ''.join([chr(int(encoded_string[i:i+2], 16) ^ r) for i in range(2, len(encoded_string), 2)])
        return email
    except Exception as e:
        print(f"Error decoding email: {encoded_string}, Error: {e}")
        return ""

# Setup Chrome options
options = Options()
options.add_argument("--headless")  # Remove this line to see browser in action
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Unique user data dir
user_data_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={user_data_dir}")

# Setup Excel workbook
wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["Name", "Mobile", "Email", "Office", "Status"])

# Setup Selenium driver
driver = webdriver.Chrome(options=options)

# Add stealth settings
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    url = "https://lasrera.lagosstate.gov.ng/practitionerSearch.jsp"
    driver.get(url)
    time.sleep(5)
    
    # Click "Show all Practitioners" button if it exists
    try:
        show_all_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Show all Practitioners')]")
        show_all_btn.click()
        time.sleep(5)
        print("✅ Clicked 'Show all Practitioners' button")
    except:
        print("ℹ️ 'Show all Practitioners' button not found or not needed")
    
    page_count = 0
    total_agents = 0
    
    # Pagination loop
    while True:
        page_count += 1
        print(f"\n📄 Processing page {page_count}...")
        
        # Wait for agents to load
        time.sleep(3)
        
        # Find all agent containers
        agents = driver.find_elements(By.CSS_SELECTOR, "div.feat_property.home7.agent")
        
        if not agents:
            print("❌ No agents found on this page")
            break
            
        print(f"Found {len(agents)} agents on page {page_count}")
        
        for i, agent in enumerate(agents):
            try:
                # Extract name
                try:
                    name_elem = agent.find_element(By.TAG_NAME, "h4")
                    name = name_elem.text.strip()
                except:
                    name = "N/A"
                
                # Extract mobile number
                try:
                    mobile_elem = agent.find_element(By.XPATH, ".//a[contains(text(), 'Mobile:')]")
                    mobile = mobile_elem.text.replace("Mobile: ", "").strip()
                except:
                    mobile = "N/A"
                
                # Extract office address
                try:
                    office_elem = agent.find_element(By.XPATH, ".//a[contains(text(), 'Office:')]")
                    office = office_elem.text.replace("Office:", "").strip()
                except:
                    office = "N/A"
                
                # Extract status
                try:
                    status_elem = agent.find_element(By.XPATH, ".//a[contains(text(), 'Status:')]")
                    status = status_elem.text.replace("Status: ", "").strip()
                except:
                    status = "N/A"
                
                # Extract email with improved debugging
                email = "N/A"
                try:
                    # Method 1: Look for CloudFlare protected email
                    email_elems = agent.find_elements(By.CSS_SELECTOR, "span.__cf_email__")
                    
                    if email_elems:
                        for email_elem in email_elems:
                            encoded_email = email_elem.get_attribute("data-cfemail")
                            print(f"🔍 Debug - Agent {i+1}: Encoded email = {encoded_email}")
                            
                            if encoded_email:
                                decoded_email = decode_cf_email(encoded_email)
                                if decoded_email and decoded_email != "annaharris@findhouse.com":
                                    email = decoded_email
                                    break
                                print(f"🔍 Debug - Agent {i+1}: Decoded email = {decoded_email}")
                    
                    # Method 2: Look for plain text emails
                    if email == "N/A":
                        email_text = agent.text
                        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                        email_matches = re.findall(email_pattern, email_text)
                        if email_matches:
                            email = email_matches[0]
                            print(f"🔍 Debug - Agent {i+1}: Found plain text email = {email}")
                    
                    # Method 3: Look in href attributes
                    if email == "N/A":
                        email_links = agent.find_elements(By.XPATH, ".//a[contains(@href, 'mailto:')]")
                        if email_links:
                            href = email_links[0].get_attribute("href")
                            email = href.replace("mailto:", "")
                            print(f"🔍 Debug - Agent {i+1}: Found mailto email = {email}")
                
                except Exception as e:
                    print(f"❌ Error extracting email for agent {i+1}: {e}")
                    email = "N/A"
                
                # Add to Excel
                sheet.append([name, mobile, email, office, status])
                total_agents += 1
                
                print(f"✅ Agent {i+1}: {name} | {mobile} | {email}")
                
            except Exception as e:
                print(f"❌ Error processing agent {i+1}: {e}")
                continue
        
        # Try to go to next page
        try:
            # Look for next button
            next_btns = driver.find_elements(By.CSS_SELECTOR, "li.paginationjs-next")
            
            if not next_btns:
                print("🏁 No next button found - end of pagination")
                break
                
            next_btn = next_btns[0]
            
            # Check if next button is disabled
            if "disabled" in next_btn.get_attribute("class"):
                print("🏁 Next button is disabled - reached last page")
                break
            
            # Click next button
            driver.execute_script("arguments[0].click();", next_btn)
            print(f"➡️ Moving to page {page_count + 1}")
            time.sleep(4)  # Wait for page to load
            
        except Exception as e:
            print(f"❌ Error navigating to next page: {e}")
            break
    
    print(f"\n🎉 Scraping completed!")
    print(f"📊 Total pages processed: {page_count}")
    print(f"👥 Total agents collected: {total_agents}")

except Exception as e:
    print(f"❌ Critical error: {e}")

finally:
    driver.quit()
    
    # Save Excel file
    excel_filename = "lasrera_practitioners.xlsx"
    wb.save(excel_filename)
    print(f"💾 Data saved to '{excel_filename}'")
    
    # Print summary
    print(f"\n📋 Summary:")
    print(f"Total records: {sheet.max_row - 1}")
    print(f"Columns: Name, Mobile, Email, Office, Status")
