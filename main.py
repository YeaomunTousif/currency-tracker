import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import plotly.io as pio
from statsmodels.tsa.arima.model import ARIMA

flags = {
    "USD": "🇺🇸",  # United States Dollar
    "EUR": "🇪🇺",  # Euro (European Union flag)
    "GBP": "🇬🇧",  # British Pound Sterling
    "JPY": "🇯🇵",  # Japanese Yen
    "AUD": "🇦🇺",  # Australian Dollar
    "CAD": "🇨🇦",  # Canadian Dollar
    "CHF": "🇨🇭",  # Swiss Franc
    "CNY": "🇨🇳",  # Chinese Yuan Renminbi
    "INR": "🇮🇳",  # Indian Rupee
    "BRL": "🇧🇷",  # Brazilian Real
    "ZAR": "🇿🇦",  # South African Rand
    "KRW": "🇰🇷",  # South Korean Won
    "SGD": "🇸🇬",  # Singapore Dollar
    "MXN": "🇲🇽",  # Mexican Peso
    "RUB": "🇷🇺",  # Russian Ruble
    "TRY": "🇹🇷",  # Turkish Lira
    "NZD": "🇳🇿",  # New Zealand Dollar
    "HKD": "🇭🇰",  # Hong Kong Dollar
    "NOK": "🇳🇴",  # Norwegian Krone
    "SEK": "🇸🇪",  # Swedish Krona
    "DKK": "🇩🇰",  # Danish Krone
    "PLN": "🇵🇱",  # Polish Zloty
    "THB": "🇹🇭",  # Thai Baht
    "IDR": "🇮🇩",  # Indonesian Rupiah
    "HUF": "🇭🇺",  # Hungarian Forint
    "CZK": "🇨🇿",  # Czech Koruna
    "ILS": "🇮🇱",  # Israeli New Shekel
    "SAR": "🇸🇦",  # Saudi Riyal
    "AED": "🇦🇪",  # UAE Dirham
    "MYR": "🇲🇾",  # Malaysian Ringgit
    "PHP": "🇵🇭",  # Philippine Peso
    "CLP": "🇨🇱",  # Chilean Peso
    "PKR": "🇵🇰",  # Pakistani Rupee
    "EGP": "🇪🇬",  # Egyptian Pound
    "COP": "🇨🇴",  # Colombian Peso
    "VND": "🇻🇳",  # Vietnamese Dong
    "BDT": "🇧🇩",  # Bangladeshi Taka
    "LKR": "🇱🇰",  # Sri Lankan Rupee
    "NGN": "🇳🇬",  # Nigerian Naira
    "UAH": "🇺🇦",  # Ukrainian Hryvnia
    "KWD": "🇰🇼",  # Kuwaiti Dinar
    "QAR": "🇶🇦",  # Qatari Riyal
    "OMR": "🇴🇲",  # Omani Rial
    "JOD": "🇯🇴",  # Jordanian Dinar
    "TWD": "🇹🇼",  # New Taiwan Dollar
    "CZK": "🇨🇿",  # Czech Koruna
    "HRK": "🇭🇷",  # Croatian Kuna
    "BGN": "🇧🇬",  # Bulgarian Lev
    "RON": "🇷🇴",  # Romanian Leu
    "ISK": "🇮🇸",  # Icelandic Krona
}

# --- Setup ---
st.set_page_config(
    page_title="💱 Currency Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Theme Toggle ---
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

mode_btn = st.sidebar.button(
    "Toggle Light/Dark Mode", on_click=toggle_theme
)

dark_mode = st.session_state.dark_mode

base_color = "#0ff" if dark_mode else "#0077cc"
bg_color = "#111" if dark_mode else "#f8f9fa"     # 💡 softer white
font_color = "#eee" if dark_mode else "#212529"   # 🧠 stronger readable text for light
grid_color = "#333" if dark_mode else "#ccc"      # ✨ lighter grid

st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {font_color};
            max-width: 1300px;
            margin: auto;
            opacity: 70;
            transform: translateY(20px);
            animation: fadeInSoft 1.5s ease-out forwards;
        }}

        h1, h2, h3, h4, h5 {{
            color: {base_color};
            animation: fadeInSoft 1.2s ease-out forwards;
        }}

        .block-container {{
            padding-top: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }}

        .stButton>button {{
            background-color: {base_color} !important;
            color: {bg_color} !important;
            border-radius: 8px;
            font-weight: 600;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .stButton>button:hover {{
            transform: scale(1.03);
            box-shadow: 0 0 10px {base_color};
        }}

        .forex-news {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.25rem;
            margin-top: 1rem;
        }}

        .news-card {{
            background-color: {'#1b1e24' if dark_mode else '#ffffff'};  /* crisp white */
            border-left: 4px solid {base_color};
            border-radius: 10px;
            padding: 1rem 1.25rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 150px;
        }}

        .news-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 0 15px {base_color};
        }}

        .news-card a {{
            font-size: 1.05rem;
            font-weight: 600;
            color: {base_color};
            text-decoration: none;
            line-height: 1.4;
            transition: color 0.3s ease;
        }}

        .news-card a:hover {{
            text-decoration: underline;
            color: {base_color};
        }}

        .news-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
            color: {'#bbb' if dark_mode else '#666'};
            margin-top: 0.75rem;
        }}

        .news-desc {{
            font-size: 0.9rem;
            color: {font_color};
            opacity: 0.85;
            margin-top: 0.5rem;
            line-height: 1.5;
        }}

        @keyframes fadeInSoft {{
            from {{opacity: 0; transform: translateY(20px);}}
            to {{opacity: 1; transform: translateY(0);}}
        }}
    </style>
""", unsafe_allow_html=True)

st.title("💱 Pro Currency Tracker and Forecaster using ARIMA model")

# --- Get currency list ---
@st.cache_data
def get_currencies():
    url = "https://api.frankfurter.app/currencies"
    res = requests.get(url)
    return dict(sorted(res.json().items()))

currencies = get_currencies()

# --- Sidebar: Manual Base Currency & Amount ---
st.sidebar.markdown("### Enter base currency and amount")
col1, col2 = st.sidebar.columns(2)

with col1:
    from_currency = st.text_input("Currency (e.g., USD):", value="USD").upper()

with col2:
    base_amount = st.number_input("Amount (min : 0.01)", value=1.0, min_value=0.01, step=0.01)

# --- Validate base currency ---
if from_currency not in currencies:
    st.sidebar.error("❌ Invalid base currency. Use valid 3-letter codes like USD, EUR, GBP.")

# --- Select up to 5 target currencies ---
st.sidebar.markdown("### Select up to 5 target currencies")
max_targets = 5
target_currencies = []
for i in range(max_targets):
    default_vals = ["EUR", "JPY", "GBP", "AUD", "CAD"]
    default_val = default_vals[i] if i < len(default_vals) else None
    options = [cur for cur in currencies.keys() if cur != from_currency and cur not in target_currencies]
    index_val = options.index(default_val) if (default_val in options) else 0
    cur = st.sidebar.selectbox(
        f"Target Currency #{i+1} (optional):",
        options=options,
        index=index_val,
        format_func=lambda x: f"{x} - {currencies[x]}",
        key=f"target_currency_{i}"
    )
    if cur:
        target_currencies.append(cur)

to_currencies = list(dict.fromkeys(target_currencies))

if not to_currencies:
    st.sidebar.error("❌ Select at least one target currency")

# --- Time range for trend chart ---
days_back = st.sidebar.slider("Select number of days for trend:", min_value=1, max_value=3650, value=30)

# --- Alert thresholds ---
st.sidebar.markdown("### Set alert thresholds (optional)")
alert_thresholds = {}
for cur in to_currencies:
    alert_thresholds[cur] = st.sidebar.number_input(
        f"Alert if {cur} rate above:",
        min_value=0.0,
        value=0.0,
        step=0.1,
        key=f"alert_{cur}"
    )

# --- Conversion Logic ---
def convert_currency(from_curr, to_curr, amt):
    url = f"https://api.frankfurter.app/latest?amount={amt}&from={from_curr}&to={to_curr}"
    res = requests.get(url).json()
    return res['rates'].get(to_curr, None)

@st.cache_data(show_spinner=False)
def get_history(from_curr, to_currencies, days_back):
    end = datetime.today().date()
    start = end - timedelta(days=days_back)
    to_list = ",".join(to_currencies)
    url = f"https://api.frankfurter.app/{start}..{end}?from={from_curr}&to={to_list}"
    
    res = requests.get(url)
    if not res.ok:
        st.error(f"Failed to fetch data: {res.status_code} {res.reason}")
        return pd.DataFrame()
    
    data = res.json()
    if 'rates' not in data:
        st.error(f"API response missing 'rates': {data}")
        return pd.DataFrame()
    
    df = pd.DataFrame(data['rates']).T
    df.index = pd.to_datetime(df.index)
    df = df[to_currencies]
    return df.reset_index().rename(columns={"index": "Date"})

# --- Fetch current rates ---
converted_rates = {}
for cur in to_currencies:
    conv = convert_currency(from_currency, cur, base_amount)
    converted_rates[cur] = conv

# --- Fetch historical data ---
hist_df = get_history(from_currency, to_currencies, days_back)

# --- Display Results ---
st.header(f"💰 Conversion Result for {base_amount} {from_currency}")

cols = st.columns(len(converted_rates))  # create one col per currency

for idx, (cur, val) in enumerate(converted_rates.items()):
    if val:
        flag = flags.get(cur, "")
        with cols[idx]:
            st.markdown(f"### {flag} **{cur}**")
            st.code(f"{val:.4f}")

# --- Check alerts ---
for cur, threshold in alert_thresholds.items():
    if threshold > 0 and converted_rates.get(cur, 0) > threshold:
        st.warning(f"🚨 Alert: {cur} rate is above your threshold ({threshold})!")

# --- Chart ---
fig = px.line(
    hist_df,
    x="Date",
    y=to_currencies,
    title=f"{from_currency} → {', '.join(to_currencies)} Exchange Rate (Last {days_back} Days)",
    template="plotly_dark" if dark_mode else "plotly_white",
    labels={col: f"1 {from_currency} in {col}" for col in to_currencies},
)

fig.update_traces(
    mode='lines',
    line=dict(width=2),
    hovertemplate='%{x}<br>%{y:.4f}<extra></extra>',
)

fig.update_layout(
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font=dict(color=font_color, size=14, family="Inter, sans-serif"),
    title_font=dict(size=20, color=base_color),
    
    xaxis=dict(
        title=dict(text="Date", font=dict(color=font_color)),
        tickangle=0,
        showgrid=True,
        gridcolor=grid_color,
        showline=True,
        linecolor=grid_color,
        ticks="outside",
        showspikes=True,
        spikecolor=base_color,
        spikemode="across",
        spikethickness=1,
        tickfont=dict(color=font_color),
    ),
    
    yaxis=dict(
        title=dict(text="Exchange Rate", font=dict(color=font_color)),
        showgrid=True,
        gridcolor=grid_color,
        showline=True,
        linecolor=grid_color,
        ticks="outside",
        zeroline=False,
        tickfont=dict(color=font_color),
    ),

    margin=dict(l=40, r=40, t=60, b=40),
    hovermode="x unified",
    
    legend=dict(
        title="Currencies",
        title_font=dict(color="cyan"),
        bgcolor=bg_color,
        bordercolor=base_color,
        borderwidth=1,
        font=dict(color=font_color)
    )
)

st.plotly_chart(fig, use_container_width=True)

png_bytes = pio.to_image(fig, format='png')

# --- CSV Conversion ---
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(hist_df)
png_bytes = pio.to_image(fig, format='png')  # ⏱️ Slow if inside render loop, so keep it once here

# --- Quick Styling ---
button_style = """
    <style>
    .stDownloadButton > button {{
        color: {text_color} !important;
        background-color: {bg_color} !important;
        border: 1px solid {border_color} !important;
    }}
    </style>
""".format(
    text_color="#f0f0f0" if dark_mode else "#000",
    bg_color="#222" if dark_mode else "#f9f9f9",
    border_color="#666" if dark_mode else "#ccc"
)
st.markdown(button_style, unsafe_allow_html=True)

# --- Side-by-side buttons ---
col1, col2 = st.columns(2)
with col1:
    st.download_button("⬇️ Download Historical Data CSV", csv,
        file_name=f"{from_currency}_to_{'_'.join(to_currencies)}_history.csv",
        mime="text/csv", key="csv_btn")

with col2:
    st.download_button("⬇️ Download Chart as PNG", png_bytes,
        file_name="exchange_rate_chart.png",
        mime="image/png", key="png_btn")

st.header("📰 Latest Forex News")

NEWS_API_KEY = "f23d66790cc24b07a428efe0142dae28"
news_url = f"https://newsapi.org/v2/everything?q=forex OR currency OR exchange rate&language=en&sortBy=publishedAt&pageSize=6&apiKey={NEWS_API_KEY}"

@st.cache_data(ttl=86400)  # Caches news for 24 hours
def fetch_latest_news():
    news_url = f"https://newsapi.org/v2/everything?q=forex&language=en&sortBy=publishedAt&pageSize=6&apiKey={NEWS_API_KEY}"
    try:
        return requests.get(news_url).json()
    except:
        return {"articles": []}

news_res = fetch_latest_news()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

articles = news_res.get("articles", [])

try:
    articles = news_res.get("articles", [])

    if not articles:
        st.info("No news articles found.")
    else:
        st.markdown('<div class="forex-news">', unsafe_allow_html=True)
        for art in articles:
            title = art.get("title", "No Title")
            url = art.get("url", "#")
            source = art.get("source", {}).get("name", "Unknown Source")
            date = art.get("publishedAt", "")[:10]
            desc = art.get("description", "No summary available.")

            st.markdown(f"""
                <div class="news-card">
                    <a href="{url}" target="_blank">{title}</a>
                    <div class="news-desc">{desc}</div>
                    <div class="news-meta">
                        <span>{source}</span>
                        <span>{date}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error("Failed to load news feed. Make sure your API key is valid.")

st.write("") 

st.header(f" 🔮 Forecasting Section")

# --- Forecasting Section ---
if not hist_df.empty:
    st.sidebar.markdown("### 📈 Forecast Settings")
    forecast_days = st.sidebar.number_input(
        "Forecast how many future days?",
        min_value=1, max_value=365, value=7, step=1
    )

    forecasts = {}

    for cur in to_currencies:
        df = hist_df[["Date", cur]].rename(columns={"Date": "ds", cur: "y"})
        df = df.set_index("ds")
        
        # Fit ARIMA model (using order (5,1,0) as a simple default)
        model = ARIMA(df["y"], order=(5, 1, 0))
        model_fit = model.fit()
        
        # Forecast
        forecast = model_fit.forecast(steps=forecast_days)
        conf_int = model_fit.get_forecast(steps=forecast_days).conf_int()
        
        # Create forecast DataFrame
        future_dates = pd.date_range(start=df.index[-1] + timedelta(days=1), periods=forecast_days, freq='D')
        forecast_df = pd.DataFrame({
            "ds": pd.concat([pd.Series(df.index), pd.Series(future_dates)]).reset_index(drop=True),
            "yhat": pd.concat([df["y"], pd.Series(forecast)]).reset_index(drop=True),
            "yhat_lower": pd.concat([df["y"], pd.Series(conf_int.iloc[:, 0])]).reset_index(drop=True),
            "yhat_upper": pd.concat([df["y"], pd.Series(conf_int.iloc[:, 1])]).reset_index(drop=True)
        })
        
        forecasts[cur] = forecast_df

        # --- Plot Forecast ---
        fig_forecast = px.line(
            forecast_df,
            x="ds",
            y="yhat",
            title=f"🔮 Forecast for {cur} (Next {forecast_days} Days)",
            template="plotly_dark" if dark_mode else "plotly_white",
            labels={"ds": "Date", "yhat": f"Rate ({cur})"},
        )

        fig_forecast.add_scatter(
            x=forecast_df["ds"], y=forecast_df["yhat_upper"],
            mode="lines", name="Upper Bound",
            line=dict(dash="dot", color="green")
        )

        fig_forecast.add_scatter(
            x=forecast_df["ds"], y=forecast_df["yhat_lower"],
            mode="lines", name="Lower Bound",
            line=dict(dash="dot", color="red")
        )

        fig_forecast.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=font_color, size=14, family="Inter, sans-serif"),
            title_font=dict(size=20, color=base_color),
            xaxis=dict(
                title=dict(text="Date", font=dict(color=font_color)),
                tickangle=0,
                showgrid=False,
                gridcolor=grid_color,
                showline=False,
                ticks="outside",
                tickfont=dict(color=font_color),
            ),
            yaxis=dict(
                title=dict(text=f"Rate ({cur})", font=dict(color=font_color)),
                showgrid=True,
                gridcolor=grid_color,
                ticks="outside",
                tickfont=dict(color=font_color),
            ),
            legend=dict(
                title="",
                bgcolor=bg_color,
                bordercolor=base_color,
                borderwidth=1,
                font=dict(color=font_color)
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            hovermode="x unified",
        )

        st.plotly_chart(fig_forecast, use_container_width=True)

        # --- Forecast CSV download ---
        forecast_csv = forecast_df[["ds", "yhat", "yhat_lower", "yhat_upper"]]
        forecast_csv_data = forecast_csv.to_csv(index=False).encode("utf-8")

        st.download_button(
            label=f"⬇️ Download {cur} Forecast CSV",
            data=forecast_csv_data,
            file_name=f"{from_currency}_to_{cur}_forecast.csv",
            mime="text/csv",
            key=f"forecast_download_{cur}"
        )

        # --- AI-like Explanation ---
        st.subheader(f"🧠 Why is the Forecast for {cur} Trending This Way?")
        
        trend_data = forecast_df[['ds', 'yhat']].copy()
        trend_diff = trend_data['yhat'].diff().mean()

        if trend_diff > 0.01:
            trend_msg = "📈 There's a <span style='color:cyan; font-weight:bold;'>Strong upward trend</span> in this currency's value. This could be due to positive economic indicators, central bank decisions, or rising demand globally."
        elif trend_diff < -0.01:
            trend_msg = "📉 This forecast shows a <span style='color:cyan; font-weight:bold;'>Downward trend</span>, possibly influenced by weakening economic signals, geopolitical tension, or reduced investor confidence."
        else:
            trend_msg = "🔁 The trend appears <span style='color:cyan; font-weight:bold;'>Flat or Stable</span>, indicating market indecision or equilibrium between buyers and sellers."

        st.markdown(f"""
        <div style='padding: 1rem; background-color: {"#1a1a1a" if dark_mode else "#f1f1f1"}; border-left: 5px solid {base_color}; border-radius: 8px;'>
            <p style='font-size: 18px; text-align: center;'>{trend_msg}</p>
        </div>
        """, unsafe_allow_html=True)

st.header("📊 Currency Statistics & Annualized Volatility")

returns = hist_df[to_currencies].pct_change().dropna()
volatility = returns.std() * (252 ** 0.5)

st.subheader("💥 Annualized Volatility (based on daily returns)")

cols = st.columns(len(to_currencies))

for i, cur in enumerate(to_currencies):
    with cols[i]:
        st.markdown(f"""
            <div style="text-align: center; font-size: 22px; padding: 5px;">
                <b>{cur}</b><br>
                <span style="font-size: 20px; color: #00BFFF;">{volatility[cur]:.4f}</span>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
---
*Made with ❤️ by Yeaomun Tousif — Your personal Forex tracker and more!*
""")