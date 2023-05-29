import os, sys
import json
import time
from retry import retry
import streamlit as st


from scrapers.execute_scraper import Scapers

DATA_FOLDER_PATH = "scrapers/scrapers/data"


@retry(exceptions=ValueError, tries=5, delay=6)
def open_json_with_retry(filepath):
    with open(os.path.join(filepath), "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


#################################
# App
st.title("💼 Job Scraping Demo")

st.write("⚠️ **Note**: The project is not for commercial use.")
st.write("*Updated*: Indeed spider is not working due to new Cloudfare protection.")


website_option = st.selectbox(
    "Select a website to scrape",
    ["Indeed", "Jobstreet", "Glassdoor (Coming Soon)"],
)

option_left, option_right = st.columns(2)

if website_option == "Indeed":
    output_file_path = os.path.join(DATA_FOLDER_PATH, "indeed_jobs.json")

    search_query = option_left.text_input(
        "Which job title you want to search for?", placeholder="e.g. Data Scientist"
    )

    location = option_left.selectbox(
        "Which location you want to search for?",
        ["Ho Chi Minh", "Da Nang", "Hanoi"],
        index=0,
    )

    max_pages = option_left.selectbox(
        "How many pages of the search result you want to scrape? (The result also depends on the available jobs)",
        [1, 2, 5, 10],
        index=0,
    )
elif website_option == "Jobstreet":
    output_file_path = os.path.join(DATA_FOLDER_PATH, "jobstreet_jobs.json")

    search_query = option_left.text_input(
        "Which job title you want to search for?", placeholder="e.g. Data Scientist"
    )

    location = option_left.selectbox(
        "Which location you want to search for?",
        ["Ho Chi Minh", "Da Nang", "Hanoi"],
        index=0,
    )

    max_pages = option_left.selectbox(
        "How many pages of the search result you want to scrape? (The result also depends on the available jobs)",
        [1, 2, 5, 10],
        index=0,
    )


scrape_btn = st.button("Start Scraping")

# Display sample data

if website_option == "Indeed":
    output_data = os.path.join(DATA_FOLDER_PATH, "indeed_jobs.json")
    if os.path.isfile(output_data):
        os.remove(output_data)
elif website_option == "Jobstreet":
    output_data = os.path.join(DATA_FOLDER_PATH, "jobstreet_jobs.json")
    if os.path.isfile(output_data):
        os.remove(output_data)


#################################
# Start Scraping

if scrape_btn:

    with st.spinner(f"Scraping {website_option}..."):

        if website_option == "Indeed":
            scraper = Scapers()
            scraper.run_indeed_spider(
                search_query=search_query, location=location, max_pages=max_pages
            )
        elif website_option == "Jobstreet":
            scraper = Scapers()
            scraper.run_jobstreetvn_spider(
                search_query=search_query, location=location, max_pages=max_pages
            )
        elif website_option == "Glassdoor (Coming Soon)":
            st.write("Scraping Glassdoor")
        else:
            st.write("Please select a website")

        while (
            not os.path.isfile(output_file_path)
            or os.path.getsize(output_file_path) == 0
        ):
            pass

    st.success("Scraping Complete!")

    # Preview results
    with st.spinner(f"Preparing file for preview and dowload ..."):

        data = open_json_with_retry(output_data)
        st.subheader("Preview")
        st.write(f"{len(data)} jobs found for the first {max_pages} pages")
        st.write("Sample data:")
        st.json(data[:5], expanded=False)
        json_string = json.dumps(data, ensure_ascii=False)

        st.download_button(
            label="Download JSON",
            # job data + date + scraper
            file_name="job_data.json",
            mime="application/json",
            data=json_string,
        )
