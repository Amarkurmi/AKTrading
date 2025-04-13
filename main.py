import yfinance as yf
import pandas as pd
from ta.trend import MACD, ADXIndicator
from ta.momentum import StochRSIIndicator
from ta.volatility import AverageTrueRange
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from threading import Thread
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout as PopupBoxLayout
from kivy.uix.button import Button as PopupButton
import os
from twilio.rest import Client  # <-- Added for WhatsApp

class AKTradingApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.layout.add_widget(Label(
            text="📈 WELCOME TO AK TRADING PORTAL", font_size=24, size_hint=(1, 0.1)))

        controls = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.strategy_var = Spinner(text="Buy/Sell signal", values=["Buy/Sell signal", "20%up"])
        self.scan_btn = Button(text="▶️ Run Strategy", size_hint=(0.3, 1))
        self.clear_btn = Button(text="🧹 Clear Output", size_hint=(0.3, 1))
        self.export_btn = Button(text="💾 Save Data", size_hint=(0.3, 1))

        self.scan_btn.bind(on_press=self.run_strategy_threaded)
        self.clear_btn.bind(on_press=lambda x: setattr(self.output_area, 'text', ''))
        self.export_btn.bind(on_press=self.export_to_csv_prompt)

        controls.add_widget(self.strategy_var)
        controls.add_widget(self.scan_btn)
        controls.add_widget(self.clear_btn)
        controls.add_widget(self.export_btn)
        self.layout.add_widget(controls)

        self.progress_bar = ProgressBar(max=100, size_hint=(1, 0.05))
        self.layout.add_widget(self.progress_bar)

        self.output_area = TextInput(
            size_hint=(1, 0.8), multiline=True, readonly=True, font_size=16)
        self.layout.add_widget(self.output_area)

        return self.layout

    def update_output(self, text):
        self.output_area.text += text

    def set_status(self, status):
        self.output_area.text += f"Status: {status}\n"

    def run_strategy_threaded(self, instance):
        Thread(target=self.run_strategy).start()

    def run_strategy(self):
        Clock.schedule_once(lambda dt: self.update_output("🔄 Running strategy...\n"))
        strategy = self.strategy_var.text

        STOCK_LIST = [
    "MRF", "SHREECEM", "SOLARINDS", "NAUKRI", "COFORGE", "BOSCHLTD", "ULTRACEMCO",
    "BRITANNIA", "PERSISTENT", "APOLLOHOSP", "LTIM", "POLYCAB", "INDIGO", "PIIND",
    "TCS", "DIVISLAB", "EICHERMOT", "BAJFINANCE", "PIDILITIND", "CUMMINSIND",
    "HDFCAMC", "KOTAKBANK", "MPHASIS", "DALBHARAT", "PATANJALI", "BAJAJ-AUTO",
    "LUPIN", "ABB", "SRF", "MCX", "GRASIM", "M&M", "HAL", "NESTLEIND", "ACC", "INFY",
    "MARUTI", "CHOLAFIN", "JSWSTEEL", "GODREJPROP", "TECHM", "SBICARD", "TATACOMM",
    "KEI", "DEEPAKNTR", "RAMCOCEM", "MGL", "SIEMENS", "LT", "ICICIBANK",
    "PHOENIXLTD", "BALKRISIND", "GODREJCP", "TATACHEM", "ADANIENSOL", "TITAN",
    "TIINDIA", "COLPAL", "TORNTPHARM", "TRENT", "ADANIENT", "SBILIFE", "HINDALCO",
    "DMART", "HEROMOTOCO", "POLICYBZR", "SUNPHARMA", "DIXON", "HCLTECH",
    "MAXHEALTH", "TVSMOTOR", "ICICIPRULI", "BAJAJFINSV", "BHARTIARTL", "DABUR",
    "INDHOTEL", "JSWENERGY", "INDUSINDBK", "AXISBANK", "HINDUNILVR", "ZYDUSLIFE",
    "HDFCBANK", "LICHSGFIN", "PNBHOUSING", "HAVELLS", "TATACONSUM", "AUROPHARMA",
    "ASIANPAINT", "HINDPETRO", "SBIN", "RELIANCE", "NTPC", "ADANIGREEN", "ESCORTS",
    "MARICO", "BANKBARODA", "UNITDSPR", "IRCTC", "ASTRAL", "BEL", "CGPOWER",
    "JUBLFOOD", "PEL", "MFSL", "CROMPTON", "AMBUJACEM", "CONCOR", "HDFCLIFE",
    "DLF", "TATAMOTORS", "RBLBANK", "PAYTM", "CIPLA", "BHEL", "LAURUSLABS",
    "MANAPPURAM", "CESC", "RECLTD", "NYKAA", "TATASTEEL", "COALINDIA", "BSOFT",
    "ADANIPORTS", "JINDALSTEL", "ITC", "SHRIRAMFIN", "EXIDEIND", "INDUSTOWER",
    "UPL", "MUTHOOTFIN", "ICICIGI", "PRESTIGE", "VEDL", "TATAPOWER", "VBL",
    "HINDCOPPER", "IDFCFIRSTB", "ABCAPITAL", "ASHOKLEY", "APOLLOTYRE", "BPCL",
    "JIOFIN", "PFC", "MOTHERSON", "ONGC", "LICI", "IEX", "PETRONET", "CANBK",
    "NATIONALUM", "BANDHANBNK", "GLENMARK", "BIOCON", "GRANULES", "OIL", "ZOMATO",
    "GAIL", "NMDC", "HFCL", "SAIL", "YESBANK", "PNB", "IOC", "NCC", "GMRAIRPORT",
    "IDEA", "OFSS", "NBCC", "IIFL", "BANKINDIA", "WIPRO", "SUPREMEIND", "IRB",
    "DELHIVERY", "SYNGENE", "NHPC", "AARTIIND", "ABFRL", "UNIONBANK", "POWERGRID",
    "INOXWIND", "APLAPOLLO", "CYIENT", "JSL", "HUDCO", "SJVN", "IRFC", "CHAMBLFERT",
    "VOLTAS", "FEDERALBNK", "M&MFIN", "TORNTPOWER", "KALYANKJIL", "HINDZINC",
    "BERGEPAINT", "ATGL", "INDIANB", "LTF", "BSE", "POONAWALLA", "IGL", "SONACOMS",
    "AUBANK", "IREDA", "TITAGARH", "OBEROIRLTY", "KPITTECH", "DRREDDY",
    "BHARATFORG", "LODHA", "TATATECH", "ALKEM", "CDSL", "CAMS", "TATAELXSI",
    "ANGELONE", "PAGEIND"]  # Reduced for testing (use your full list)

        strategy_func = {
            "Buy/Sell signal": self.strategy_buy_sell_signal,
            "20%up": self.strategy_20_percent_up
        }.get(strategy)

        if not strategy_func:
            Clock.schedule_once(lambda dt: self.update_output("❗ Invalid strategy selected\n"))
            return

        total_stocks = len(STOCK_LIST)
        processed_stocks = 0
        self.result_data = []

        for symbol in STOCK_LIST:
            try:
                df = yf.download(f"{symbol}.NS", period="6mo", interval="1d", progress=False)
                if df.empty:
                    continue

                df.reset_index(inplace=True)
                df.set_index('Date', inplace=True)
                df.columns = df.columns.get_level_values(0) if isinstance(df.columns, pd.MultiIndex) else df.columns
                for col in ['Close', 'High', 'Low', 'Open', 'Volume']:
                    if col in df.columns:
                        df[col] = df[col].squeeze()

                df = self.calculate_indicators(df)
                signals = strategy_func(df)
                if signals:
                    last = signals[-1]
                    Clock.schedule_once(lambda dt, t=last: self.update_output(
                        f"\n━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"{'✅' if t[0] == 'Buy' or t[0] == '20% Up' else '🔻'} {symbol} - {t[0]}\n"
                        f"📅 Date: {t[1].strftime('%Y-%m-%d')}\n"
                        f"💰 Price: ₹{t[2]:,.2f}\n"
                        f"📈 ADX: {df['ADX'].iloc[-1]:.1f}\n"
                        f"📊 MACD Hist: {df['Hist'].iloc[-1]:.2f}\n"
                        f"📉 Stoch: {df['Stoch_K'].iloc[-1]:.1f}\n"
                        f"📈 Supertrend: {df['Supertrend'].iloc[-1]:.2f}\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    ))

                    self.result_data.append({
                        "Stock": symbol,
                        "Signal": last[0],
                        "Date": last[1].strftime('%Y-%m-%d'),
                        "Price": last[2],
                        "ADX": df['ADX'].iloc[-1],
                        "MACD Hist": df['Hist'].iloc[-1],
                        "Stoch": df['Stoch_K'].iloc[-1],
                        "Supertrend": df['Supertrend'].iloc[-1]
                    })

                    # ✅ Send WhatsApp for Buy or 20% Up
                    if last[0] in ["Buy", "20% Up"]:
                        msg = (
                            f"📈 {last[0]} Signal!\n"
                            f"Stock: {symbol}\n"
                            f"Date: {last[1].strftime('%Y-%m-%d')}\n"
                            f"Price: ₹{last[2]:,.2f}\n"
                            f"ADX: {df['ADX'].iloc[-1]:.1f}\n"
                            f"MACD Hist: {df['Hist'].iloc[-1]:.2f}\n"
                            f"Stoch: {df['Stoch_K'].iloc[-1]:.1f}\n"
                            f"Supertrend: {df['Supertrend'].iloc[-1]:.2f}"
                        )
                        self.send_whatsapp(msg)

                processed_stocks += 1
                Clock.schedule_once(lambda dt, p=int((processed_stocks / total_stocks) * 100): self.update_progress(p))

            except Exception as e:
                Clock.schedule_once(lambda dt, s=symbol, err=e: self.update_output(f"❌ Error with {s}: {err}\n"))

        Clock.schedule_once(lambda dt: self.update_output("✅ Strategy completed!\n"))

    def update_progress(self, progress):
        self.progress_bar.value = progress

    def calculate_indicators(self, df):
        adx = ADXIndicator(high=df['High'], low=df['Low'], close=df['Close'])
        macd = MACD(close=df['Close'])
        stoch = StochRSIIndicator(close=df['Close'])
        atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'])

        df['ADX'] = adx.adx()
        df['+DI'] = adx.adx_pos()
        df['-DI'] = adx.adx_neg()
        df['MACD'] = macd.macd()
        df['Signal'] = macd.macd_signal()
        df['Hist'] = macd.macd_diff()
        df['Stoch_K'] = stoch.stochrsi_k()
        df['Stoch_D'] = stoch.stochrsi_d()
        df['ATR'] = atr.average_true_range()
        df['Supertrend'] = df['Close'] - (df['ATR'] * 1.5)

        return df

    def strategy_buy_sell_signal(self, df):
        signals = []
        for i in range(1, len(df)):
            if (
                df['+DI'].iloc[i] > df['-DI'].iloc[i] and
                df['MACD'].iloc[i] > df['Signal'].iloc[i] and
                df['Hist'].iloc[i] > df['Hist'].iloc[i-1] and
                df['Stoch_K'].iloc[i] > df['Stoch_D'].iloc[i] and
                df['Close'].iloc[i] > df['Supertrend'].iloc[i]
            ):
                signals.append(("Buy", df.index[i], df['Close'].iloc[i]))
            elif (
                df['-DI'].iloc[i] > df['+DI'].iloc[i] and
                df['MACD'].iloc[i] < df['Signal'].iloc[i] and
                df['Hist'].iloc[i] < df['Hist'].iloc[i-1] and
                df['Stoch_K'].iloc[i] < df['Stoch_D'].iloc[i] and
                df['Close'].iloc[i] < df['Supertrend'].iloc[i]
            ):
                signals.append(("Sell", df.index[i], df['Close'].iloc[i]))
        return signals

    def strategy_20_percent_up(self, df):
        if len(df) < 2:
            return []
        start, end = df['Close'].iloc[0], df['Close'].iloc[-1]
        if (end - start) / start >= 0.2:
            return [("20% Up", df.index[-1], end)]
        return []

    def export_to_csv_prompt(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        filechooser = FileChooserListView(path=os.getcwd(), dirselect=True)
        content.add_widget(filechooser)

        filename_input = TextInput(hint_text="Enter file name (e.g., results.csv)", size_hint_y=None, height=40)
        content.add_widget(filename_input)

        btn_layout = BoxLayout(size_hint_y=0.2)
        cancel_btn = Button(text="Cancel")
        save_btn = Button(text="Save")

        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(save_btn)
        content.add_widget(btn_layout)

        popup = Popup(title="Save CSV File", content=content, size_hint=(0.9, 0.9))
        cancel_btn.bind(on_press=popup.dismiss)
        save_btn.bind(on_press=lambda inst: self.save_file_with_name(filechooser, filename_input.text, popup))
        popup.open()

    def save_file_with_name(self, filechooser, filename, popup):
        if not filename:
            self.update_output("❗ Please enter a file name.\n")
            return
        if not filename.endswith('.csv'):
            filename += '.csv'
        if filechooser.selection:
            folder = filechooser.selection[0]
            filepath = os.path.join(folder, filename)
            self.export_to_csv(filepath, popup)
        else:
            self.update_output("❗ Please select a folder to save the file.\n")

    def export_to_csv(self, filepath, popup):
        df = pd.DataFrame(self.result_data)
        df.to_csv(filepath, index=False)
        self.update_output(f"✅ File saved: {filepath}\n")
        popup.dismiss()

    def send_whatsapp(self, message):
        account_sid = "AC6ab336214c17698e4419fca4494bc39a"
        auth_token = "65b9c1f329d092fe9e1d26dd2ef06272"
        from_whatsapp_number = "whatsapp:+14155238886"  # Twilio sandbox
        to_whatsapp_number = "whatsapp:+919323668605"   # Your verified number

        try:
            client = Client(account_sid, auth_token)
            client.messages.create(
                body=message,
                from_=from_whatsapp_number,
                to=to_whatsapp_number
            )
            print("✅ WhatsApp notification sent!")
        except Exception as e:
            print(f"❌ WhatsApp send failed: {e}")


if __name__ == "__main__":
    AKTradingApp().run()
