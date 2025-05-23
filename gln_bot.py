
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Загрузка таблицы
df = pd.read_excel("Склады.xlsx")
df["Gln"] = df["Gln"].astype(str)

# Поиск по GLN
def find_warehouse_by_gln(gln):
    result = df[df["Gln"] == gln]
    if not result.empty:
        name = result.iloc[0]["Название склада Pooling"]
        warehouse_id = result.iloc[0]["PLN"]
        return f"Склад: {name}\nID склада: {warehouse_id}"
    return "Склад с таким GLN не найден."

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gln = update.message.text.strip()
    response = find_warehouse_by_gln(gln)
    await update.message.reply_text(response)

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите номер GLN:")

# Основной запуск
def main():
    app = ApplicationBuilder().token("ВАШ_ТОКЕН_БОТА").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
