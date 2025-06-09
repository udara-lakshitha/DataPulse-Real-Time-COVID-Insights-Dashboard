# 📊 Data Pulse – COVID-19 Country Dashboard

![image](https://github.com/user-attachments/assets/d5f11dd9-ad2b-431b-948d-3f684b593ec3)


**Data Pulse** is a simple, dynamic COVID-19 dashboard built with **Flask**, using data from [Our World in Data](https://ourworldindata.org/covid-data). Users can interactively view cases, vaccinations, and more by country and timeframe.

> ✅ The app **automatically updates data every 6 hours**, so it always reflects the latest numbers.

---

## 🧩 Features

- 🌍 View COVID-19 data by country
- 📆 Choose time ranges: `3M`, `6M`, `1Y`, `2Y`, `5Y`
- 📈 Interactive chart (Total cases, New cases, Vaccinations)
- 📊 Real-time stats with last available date
- 🔁 Auto-updates data in background every 6 hours
- 💡 Simple frontend with JavaScript + Flask

---

## 📂 Project Structure

```plaintext
data-pulse/
│
├── app.py                 # Main Flask app
├── routes.py              # Blueprint with logic
├── requirements.txt       # Python dependencies
│
├── templates/
│   └── index.html         # Web dashboard UI
│
├── static/
│   ├── js/
│   │   └── main.js        # Async JS for dropdown actions
│   └── plots/             # Generated chart images
│
├── data/
│   └── owid-covid-data.csv
```
## 🙋‍♂️ Author

Developed by Udara Lakshitha 🇱🇰
