import yfinance as yf
import pandas as pd

# 1. سحب بيانات سهم الراجحي (1120.SR) من السوق السعودي
ticker = "1120.SR"
df = yf.download(ticker, period="2y", interval="1d")

# تسطيح الأعمدة إذا كانت متعددة المستويات في الإصدارات الحديثة من yfinance
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# 2. حساب المتوسطات المتحركة البسيطة (SMA 20 و SMA 50)
df['SMA_20'] = df['Close'].rolling(window=20).mean()
df['SMA_50'] = df['Close'].rolling(window=50).mean()

# 3. حساب مؤشر القوة النسبية (RSI - 14 يوم) برمجياً
delta = df['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
df['RSI'] = 100 - (100 / (1 + rs))

# 4. بناء قاعدة استراتيجية كمية بسيطة:
# إشارة شراء: عندما يتقاطع متوسط 20 فوق متوسط 50، ويكون السهم غير متشبع شرائياً (RSI < 65)
df['Buy_Signal'] = (df['SMA_20'] > df['SMA_50']) & (df['SMA_20'].shift(1) <= df['SMA_50'].shift(1)) & (df['RSI'] < 65)

# عرض آخر الأيام التي ظهرت فيها إشارة شراء
buy_dates = df[df['Buy_Signal'] == True]
print(f"عدد إشارات الشراء المكتشفة: {len(buy_dates)}")
print(buy_dates[['Close', 'SMA_20', 'SMA_50', 'RSI']].tail())


