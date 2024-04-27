from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the to-do list
todo_list = []

# Define the start command handler
def start(update, context):
    update.message.reply_text('Welcome to the To-Do List Bot! Use /add to add tasks.')

# Define the add task command handler
def add_task(update, context):
    task = ' '.join(context.args)
    if task:
        todo_list.append(task)
        update.message.reply_text(f'Task "{task}" added.')
    else:
        update.message.reply_text('Please provide a task.')

# Define the show tasks command handler
def show_tasks(update, context):
    if todo_list:
        tasks_text = '\n'.join(f'{index + 1}. {task}' for index, task in enumerate(todo_list))
        update.message.reply_text('Your To-Do List:\n' + tasks_text)
    else:
        update.message.reply_text('Your To-Do List is empty.')

# Define the unknown command handler
def unknown(update, context):
    update.message.reply_text("Sorry, I didn't understand that command.")

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater("6996183526:AAFh2XcHgc2GCqerLp5Zyp4FJ84A3L-6A-E", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add_task))
    dp.add_handler(CommandHandler("show", show_tasks))

    # Register unknown command handler
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()