import pandas as pd
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import os
from typing import Dict, List, Optional
import re
import openpyxl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'scraping_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)


class IdeaScraper:
    def __init__(self, html_file_path: str):
        self.html_file_path = html_file_path
        self.soup = None

    def load_html(self) -> None:
        """Load and parse HTML file"""
        try:
            with open(self.html_file_path, "r", encoding="utf-8") as file:
                self.soup = BeautifulSoup(file, "html.parser")
                logging.info(f"Successfully loaded HTML file: {self.html_file_path}")
        except Exception as e:
            logging.error(f"Error loading HTML file: {str(e)}")
            raise

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        # Remove extra whitespace and normalize newlines
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;?!-]', '', text)
        return text

    def extract_tags(self, idea_container) -> List[str]:
        """Extract tags from idea container"""
        tags = []
        tag_elements = idea_container.find_all("span", class_="tag")
        for tag in tag_elements:
            tag_text = tag.get_text(strip=True)
            if tag_text:
                tags.append(tag_text)
        return tags

    def extract_vote_counts(self, idea_container) -> Dict[str, int]:
        """Extract voting information"""
        vote_info = {
            "promote_count": 0,
            "comment_count": 0,
            "chips_total": 0
        }

        try:
            # Extract promote count
            promote_count = idea_container.find("span", class_="promote-count")
            if promote_count:
                vote_info["promote_count"] = int(promote_count.get_text(strip=True) or 0)

            # Extract comment count
            comment_count = idea_container.find("div", class_="il-lv-comment-count-wrapper")
            if comment_count:
                count_text = comment_count.find("span").get_text(strip=True)
                vote_info["comment_count"] = int(count_text or 0)

            # Extract chips total
            chips_total = idea_container.find("div", class_="il-lv-chips-total")
            if chips_total:
                total_text = chips_total.find("span").get_text(strip=True)
                vote_info["chips_total"] = int(total_text or 0)
        except ValueError as e:
            logging.warning(f"Error parsing vote counts: {str(e)}")

        return vote_info

    def extract_idea_details(self, idea_container) -> Dict:
        """Extract all details from an idea container"""
        try:
            # Basic information
            title_tag = idea_container.find("div", class_="il-lv-title")
            title = self.clean_text(
                title_tag.find("span", class_="il-lv-span-title").get_text()) if title_tag else "No Title"

            # Extract link
            link = title_tag.find("a")["href"] if title_tag and title_tag.find("a") else ""

            # Extract idea code
            idea_code_tag = idea_container.find("span", class_="il-lv-span-code")
            idea_code = self.clean_text(idea_code_tag.get_text()) if idea_code_tag else ""

            # Category and status
            category = self.clean_text(
                idea_container.find("span", class_="idea_category").get_text()) if idea_container.find("span",
                                                                                                       class_="idea_category") else ""
            status = self.clean_text(
                idea_container.find("span", class_="idea_status").get_text()) if idea_container.find("span",
                                                                                                     class_="idea_status") else ""

            # Author and date
            author_tag = idea_container.find("a", class_="screen_name")
            author = self.clean_text(author_tag.get_text()) if author_tag else ""
            author_id = author_tag["member_id"] if author_tag and "member_id" in author_tag.attrs else ""

            # Find the date (need to handle multiple il-lv-data spans)
            date_spans = idea_container.find_all("span", class_="il-lv-data")
            date_submitted = ""
            for span in date_spans:
                if re.match(r'\d{2}/\d{2}/\d{4}', span.get_text(strip=True)):
                    date_submitted = span.get_text(strip=True)
                    break

            # Description
            description_div = idea_container.find("div", class_="il-lv-description")
            description = self.clean_text(description_div.get_text()) if description_div else ""

            # Get tags and vote information
            tags = self.extract_tags(idea_container)
            vote_info = self.extract_vote_counts(idea_container)

            return {
                "Title": title,
                "Idea Code": idea_code,
                "Link": link,
                "Category": category,
                "Status": status,
                "Submitted By": author,
                "Author ID": author_id,
                "Date Submitted": date_submitted,
                "Description": description,
                "Tags": ", ".join(tags),
                "Promote Count": vote_info["promote_count"],
                "Comment Count": vote_info["comment_count"],
                "Chips Total": vote_info["chips_total"]
            }

        except Exception as e:
            logging.error(f"Error extracting idea details: {str(e)}")
            return {}

    def scrape(self) -> pd.DataFrame:
        """Main method to scrape all ideas and return a DataFrame"""
        if not self.soup:
            self.load_html()

        ideas = self.soup.find_all("div", class_="il-lv-idea-container")
        logging.info(f"Found {len(ideas)} ideas to process")

        idea_list = []
        for idx, idea in enumerate(ideas, 1):
            try:
                idea_details = self.extract_idea_details(idea)
                if idea_details:
                    idea_list.append(idea_details)
                logging.info(f"Processed idea {idx}/{len(ideas)}")
            except Exception as e:
                logging.error(f"Error processing idea {idx}: {str(e)}")

        return pd.DataFrame(idea_list)


def main():
    # Input and output file paths
    html_file_path = "CamstarIdeaScrap.htm"
    output_dir = "output"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Initialize and run scraper
        scraper = IdeaScraper(html_file_path)
        df = scraper.scrape()

        # Save to Excel with timestamp
        output_file = os.path.join(output_dir, f"ideas_export_{timestamp}.xlsx")
        df.to_excel(output_file, index=False)
        logging.info(f"Successfully exported {len(df)} ideas to {output_file}")

        # Generate summary statistics
        summary = {
            "Total Ideas": len(df),
            "Categories": df["Category"].nunique(),
            "Statuses": df["Status"].nunique(),
            "Total Comments": df["Comment Count"].sum(),
            "Total Promotes": df["Promote Count"].sum(),
            "Date Range": f"{df['Date Submitted'].min()} to {df['Date Submitted'].max()}"
        }

        # Save summary to text file
        summary_file = os.path.join(output_dir, f"summary_{timestamp}.txt")
        with open(summary_file, "w") as f:
            for key, value in summary.items():
                f.write(f"{key}: {value}\n")

        logging.info("Script completed successfully")

    except Exception as e:
        logging.error(f"Script failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()