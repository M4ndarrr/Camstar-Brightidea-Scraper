# Camstar - Brightidea Scraper

## Camstar - Brightidea Scraper  

A Python tool that extracts data from the Siemens Product Feedback system (Camstar Brightidea) and converts it into an Excel table for easy analysis.

[Explore the Documentation »](https://github.com/M4ndarrr/Camstar-Brightidea-Scraper)  

[Report a Bug](https://github.com/M4ndarrr/Camstar-Brightidea-Scraper/issues) · [Request a Feature](https://github.com/M4ndarrr/Camstar-Brightidea-Scraper/issues)

---

## Table of Contents  

- [About the Project](#about-the-project)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
- [Usage](#usage)  
- [License](#license)  
- [Contact](#contact)  

---

## About the Project  

Camstar Brightidea is Siemens' platform for managing product feedback and feature requests. However, extracting and analyzing this data manually can be time-consuming.  

This Python script automates the process by parsing the website’s HTML and generating a structured Excel table, making it easier to track and analyze feedback.  

### Key Features  

✅ Web scraping of Camstar Brightidea pages  
✅ Parses HTML and extracts key feedback data  
✅ Saves structured information in an Excel file  
✅ Simple and efficient automation  

[Back to top](#camstar---brightidea-scraper)

---

## Getting Started  

### Prerequisites  

Ensure you have the following installed:  

- **Python 3.7+**: [Download here](https://www.python.org/downloads/)  
- **Required Libraries**: Install dependencies using pip:  

  ```sh
  pip install requests beautifulsoup4 pandas openpyxl
  ```

### Installation  

1. **Clone the repository**  

   ```sh
   git clone https://github.com/M4ndarrr/Camstar-Brightidea-Scraper.git
   cd Camstar-Brightidea-Scraper
   ```

2. **Install dependencies**  

   ```sh
   pip install -r requirements.txt
   ```

3. **Run the scraper**  

   ```sh
   python main.py
   ```

[Back to top](#camstar---brightidea-scraper)

---

## Usage  

1. **Run the script**  
   - The script will automatically parse the feedback data from the `CamstarIdeaScrap.htm` and save it to an Excel file.  

2. **Output**  
   - The extracted data will be stored in `output` in the project directory.  

[Back to top](#camstar---brightidea-scraper)

---

## License  

Distributed under the MIT License. See `LICENSE.txt` for details.  

[Back to top](#camstar---brightidea-scraper)

---

## Contact  

Jan Tichy  
[![LinkedIn][linkedin-shield]][linkedin-url]  
Email: jan.tichy@jnt-digital.net  

[Back to top](#camstar---brightidea-scraper)

---

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555  
[linkedin-url]: https://www.linkedin.com/in/jantichy-jntdigital/  
