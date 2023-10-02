import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

expenses = []
incomes = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    logging.info("Received start command")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    logging.info("Received echo command")


async def expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Enter the expense amount:"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    context.user_data['mode'] = 'expense'
    logging.info("Received expe command")

async def income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Enter the income amount:"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    context.user_data['mode'] = 'income'
    logging.info("Received income command")



async def handle_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mode = context.user_data.get('mode')
    
    try:
        amount = float(update.message.text)
        
        if mode == 'expense':
            expenses.append(amount)
        elif mode == 'income':
            incomes.append(amount)
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Transaction of {amount} {mode} recorded.")
        logging.info("Received handle_transaction command")
    except ValueError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid amount. Please enter a valid number.")
    
    context.user_data.pop('mode', None)


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_expenses = sum(expenses)
    total_incomes = sum(incomes)
    print("Expenses:", expenses)
    print("Incomes:", incomes)
    balance = total_incomes - total_expenses
    
    report_text = f"Total Income: {total_incomes:.2f}\nTotal Expenses: {total_expenses:.2f}\nBalance: {balance:.2f}"
    print(report_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=report_text)
    logging.info("Received report command")

if __name__ == '__main__':
    application = ApplicationBuilder().token('6468309421:AAEkaBgZDysSDlrz_G-UIQu-AsvbQaBLlFI').build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    start_handler = CommandHandler('start', start)
    expense_handler = CommandHandler('expense', expense)
    income_handler = CommandHandler('income', income)
    report_handler = CommandHandler('report', report)
    
    application.add_handler(start_handler)
   
    application.add_handler(echo_handler)
    application.add_handler(expense_handler)
    application.add_handler(income_handler)
    application.add_handler(report_handler)
    
    application.run_polling()
