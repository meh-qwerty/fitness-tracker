
# 3-Month Body Progress Tracker (Streamlit App)

This is a beautiful, mobile-friendly Streamlit app for women to track their body measurements and progress over a 12-week period.

## Features
- Daily tracking: weight, chest, stomach, glutes
- Monthly goal setting
- Animated progress charts with Plotly
- Weekly summary with motivational messages
- Google Sheets integration for persistent storage

## Setup Instructions

1. **Clone or Download this Project**

2. **Install Dependencies**

```bash
pip install streamlit pandas plotly gspread oauth2client streamlit-option-menu
```

3. **Add Google Sheets Credentials**

Place your `credentials.json` file (from Google Cloud) in the root directory.

Make sure your Google Sheet has:
- A worksheet named `Data` with columns: `Date`, `Weight`, `Chest`, `Stomach`, `Glutes`
- A worksheet named `Goals` will be auto-created

4. **Run the App**

```bash
streamlit run app.py
```

5. **Enjoy!**
Access the app on your mobile or desktop browser and track your transformation journey!

---

**Styling:** Feminine theme with pink & purple tones  
**Deployment:** You can deploy this app on [Streamlit Cloud](https://streamlit.io/cloud)

