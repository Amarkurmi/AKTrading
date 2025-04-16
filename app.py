import yfinance as yf
import pandas as pd
from ta.trend import MACD, ADXIndicator
from ta.momentum import StochRSIIndicator
from ta.volatility import AverageTrueRange
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.filemanager import MDFileManager
from kivy.clock import Clock
from threading import Thread
import os
from twilio.rest import Client
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.chip import MDChip
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

class Content(MDBoxLayout):
    pass

class AKTradingApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.result_data = []
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )
        self.dialog = None
        self.strategy_options = ["Buy/Sell signal", "20%up"]
        self.STOCK_LIST = [
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
            "ANGELONE", "PAGEIND"
        ]

    def build(self):
        self.screen = MDScreen()
        
        # Main layout
        self.layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Toolbar
        self.toolbar = MDTopAppBar(
            title="📈 AK TRADING PORTAL",
            md_bg_color=self.theme_cls.primary_color,
            left_action_items=[["menu", lambda x: self.open_settings()]],
            right_action_items=[["dots-vertical", lambda x: self.show_about()]],
            elevation=10
        )
        self.layout.add_widget(self.toolbar)
        
        # Strategy selection card
        strategy_card = MDCard(
            size_hint=(1, None),
            height=dp(100),
            padding=dp(15),
            spacing=dp(10),
            elevation=3,
            radius=[15,]
        )
        
        strategy_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        
        # Strategy segmented control
        self.strategy_control = MDSegmentedControl(
            MDSegmentedControlItem(text="Buy/Sell Signal", on_release=self.set_strategy),
            MDSegmentedControlItem(text="20% Up", on_release=self.set_strategy),
            size_hint=(1, None),
            height=dp(40),
        )
        strategy_layout.add_widget(self.strategy_control)
        
        # Buttons
        button_layout = MDBoxLayout(spacing=dp(10))
        self.scan_btn = MDRaisedButton(
            text="▶️ Run Strategy",
            on_release=self.run_strategy_threaded,
            size_hint=(0.3, None),
            height=dp(40)
        )
        self.clear_btn = MDRaisedButton(
            text="🧹 Clear Output",
            on_release=lambda x: setattr(self.output_area, 'text', ''),
            size_hint=(0.3, None),
            height=dp(40)
        )
        self.export_btn = MDRaisedButton(
            text="💾 Save Data",
            on_release=self.export_to_csv_prompt,
            size_hint=(0.3, None),
            height=dp(40)
        )
        button_layout.add_widget(self.scan_btn)
        button_layout.add_widget(self.clear_btn)
        button_layout.add_widget(self.export_btn)
        strategy_layout.add_widget(button_layout)
        strategy_card.add_widget(strategy_layout)
        self.layout.add_widget(strategy_card)
        
        # Progress bar
        self.progress_bar = MDProgressBar(
            max=100,
            size_hint=(1, None),
            height=dp(10)
        )
        self.layout.add_widget(self.progress_bar)
        
        # Output area
        self.output_area = MDTextField(
            hint_text="Results will appear here...",
            mode="fill",
            multiline=True,
            readonly=True,
            font_size="16sp",
            size_hint=(1, 1)
        )
        scroll = MDScrollView()
        scroll.add_widget(self.output_area)
        self.layout.add_widget(scroll)
        
        self.screen.add_widget(self.layout)
        return self.screen
    
    def set_strategy(self, instance):
        self.current_strategy = instance.text
    
    def update_output(self, text):
        self.output_area.text += text
    
    def update_progress(self, progress):
        self.progress_bar.value = progress
    
    def run_strategy_threaded(self, instance):
        Thread(target=self.run_strategy).start()
    
    def run_strategy(self):
        Clock.schedule_once(lambda dt: self.update_output("🔄 Running strategy...\n"))
        
        if not hasattr(self, 'current_strategy'):
            self.current_strategy = "Buy/Sell Signal"
        
        strategy_func = {
            "Buy/Sell Signal": self.strategy_buy_sell_signal,
            "20% Up": self.strategy_20_percent_up
        }.get(self.current_strategy)
        
        if not strategy_func:
            Clock.schedule_once(lambda dt: self.update_output("❗ Invalid strategy selected\n"))
            return
        
        total_stocks = len(self.STOCK_LIST)
        processed_stocks = 0
        self.result_data = []
        
        for symbol in self.STOCK_LIST:
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
        self.file_manager.show(os.getcwd())
    
    def exit_manager(self, *args):
        self.file_manager.close()
    
    def select_path(self, path):
        self.exit_manager()
        self.show_save_dialog(path)
    
    def show_save_dialog(self, folder):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Save CSV File",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                    MDRaisedButton(text="SAVE", on_release=lambda x: self.save_file(folder))
                ],
            )
        self.dialog.open()
    
    def save_file(self, folder):
        filename = self.dialog.content_cls.ids.filename_input.text
        if not filename:
            self.show_error("Please enter a file name")
            return
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        filepath = os.path.join(folder, filename)
        self.export_to_csv(filepath)
        self.dialog.dismiss()
    
    def export_to_csv(self, filepath):
        df = pd.DataFrame(self.result_data)
        df.to_csv(filepath, index=False)
        self.update_output(f"✅ File saved: {filepath}\n")
    
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
    
    def show_error(self, message):
        MDDialog(
            title="Error",
            text=message,
            buttons=[MDRaisedButton(text="OK")]
        ).open()
    
    def show_about(self):
        MDDialog(
            title="About AK Trading Portal",
            text="Version 1.0\n\nA trading analysis tool with WhatsApp notifications",
            buttons=[MDRaisedButton(text="OK")]
        ).open()

if __name__ == "__main__":
    AKTradingApp().run()