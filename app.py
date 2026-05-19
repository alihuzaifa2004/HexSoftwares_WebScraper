import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Web Scraper Pro X",
    page_icon="🌐",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background: #0f172a;
}

.title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    color: white;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
    font-size: 18px;
}

.card {
    background: #111827;
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
    border: 1px solid #1f2937;
}

.metric-box {
    background: linear-gradient(135deg, #1e293b, #111827);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    color: white;
    border: 1px solid #334155;
}

.success-box {
    background-color: #14532d;
    color: white;
    padding: 15px;
    border-radius: 12px;
    margin-top: 20px;
}

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 50px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown(
    '<div class="title">🌐 Web Scraper Pro X</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Advanced Web Scraper using Python, Requests & BeautifulSoup</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# URL VALIDATION
# ---------------------------------------------------
def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# ---------------------------------------------------
# SCRAPER FUNCTION
# ---------------------------------------------------
def scrape_website(url, option):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    extracted_data = []

    # -----------------------------------------------
    # HEADINGS
    # -----------------------------------------------
    if option == "Headings":

        headings = soup.find_all(
            ["h1", "h2", "h3", "h4", "h5", "h6"]
        )

        for heading in headings:

            text = heading.get_text(strip=True)

            if text:
                extracted_data.append({
                    "Heading": text
                })

    # -----------------------------------------------
    # PARAGRAPHS
    # -----------------------------------------------
    elif option == "Paragraphs":

        paragraphs = soup.find_all("p")

        for para in paragraphs:

            text = para.get_text(strip=True)

            if text and len(text) > 30:

                extracted_data.append({
                    "Paragraph": text
                })

    # -----------------------------------------------
    # LINKS
    # -----------------------------------------------
    elif option == "Links":

        links = soup.find_all("a")

        for link in links:

            href = link.get("href")

            if href:

                full_link = urljoin(url, href)

                extracted_data.append({
                    "Link": full_link
                })

    # -----------------------------------------------
    # IMAGES
    # -----------------------------------------------
    elif option == "Images":

        images = soup.find_all("img")

        for img in images:

            src = img.get("src")

            if src:

                full_src = urljoin(url, src)

                extracted_data.append({
                    "Image URL": full_src
                })

    # REMOVE DUPLICATES
    unique_data = [
        dict(t)
        for t in {
            tuple(d.items())
            for d in extracted_data
        }
    ]

    return unique_data

# ---------------------------------------------------
# MAIN CONTAINER
# ---------------------------------------------------


url = st.text_input(
    "🔗 Enter Website URL",
    placeholder="https://example.com"
)

scrape_option = st.selectbox(
    "📌 Select Data Type",
    [
        "Headings",
        "Paragraphs",
        "Links",
        "Images",
        "Email",
        "Contact"
    ]
)

start_button = st.button("🚀 Start Scraping")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# SCRAPING LOGIC
# ---------------------------------------------------
if start_button:

    if not url:

        st.warning("⚠️ Please enter a website URL")

    elif not is_valid_url(url):

        st.error("❌ Invalid URL format")

    else:

        try:

            with st.spinner("Scraping website... Please wait..."):

                data = scrape_website(
                    url,
                    scrape_option
                )

            if data:

                df = pd.DataFrame(data)

                # ---------------------------------------------------
                # METRICS
                # ---------------------------------------------------
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div class="metric-box">
                        <h2>{len(df)}</h2>
                        <p>Total Records</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-box">
                        <h2>{scrape_option}</h2>
                        <p>Extraction Type</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    domain = urlparse(url).netloc

                    st.markdown(f"""
                    <div class="metric-box">
                        <h2>{domain}</h2>
                        <p>Website Domain</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ---------------------------------------------------
                # TABS
                # ---------------------------------------------------
                tab1, tab2 = st.tabs([
                    "📄 Preview Data",
                    "📊 Data Info"
                ])

                with tab1:
                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                with tab2:

                    st.write("Shape:", df.shape)

                    st.write("Columns:", list(df.columns))

                # ---------------------------------------------------
                # SAVE FILES
                # ---------------------------------------------------
                os.makedirs(
                    "scraped_data",
                    exist_ok=True
                )

                csv_filename = (
                    f"scraped_data/"
                    f"{scrape_option.lower()}_data.csv"
                )

                json_filename = (
                    f"scraped_data/"
                    f"{scrape_option.lower()}_data.json"
                )

                df.to_csv(
                    csv_filename,
                    index=False
                )

                with open(json_filename, "w") as f:
                    json.dump(
                        data,
                        f,
                        indent=4
                    )

                st.markdown(
                    f"""
                    <div class="success-box">
                    ✅ Data saved successfully
                    <br><br>
                    CSV: {csv_filename}
                    <br>
                    JSON: {json_filename}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ---------------------------------------------------
                # DOWNLOAD BUTTONS
                # ---------------------------------------------------
                col1, col2 = st.columns(2)

                with col1:

                    csv = df.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=(
                            f"{scrape_option.lower()}_data.csv"
                        ),
                        mime="text/csv"
                    )

                with col2:

                    json_data = json.dumps(
                        data,
                        indent=4
                    )

                    st.download_button(
                        label="📥 Download JSON",
                        data=json_data,
                        file_name=(
                            f"{scrape_option.lower()}_data.json"
                        ),
                        mime="application/json"
                    )

            else:

                st.warning(
                    "⚠️ No data found on this webpage"
                )

        except requests.exceptions.Timeout:

            st.error(
                "⌛ Request timed out"
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "🌐 Connection failed"
            )

        except requests.exceptions.HTTPError as e:

            st.error(
                f"🚫 HTTP Error: {e}"
            )

        except Exception as e:

            st.error(
                f"❌ Error: {e}"
            )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("""
<div class="footer">
Made By Ali Huzaifa using Streamlit, Requests & BeautifulSoup
</div>
""", unsafe_allow_html=True)