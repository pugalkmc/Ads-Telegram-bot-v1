# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import pymongo
import telegram
from telegram.ext import *
from telegram import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton

client = pymongo.MongoClient("mongodb+srv://pugalkmc:pugalkmc@cluster0.ey2yh.mongodb.net/mydb?retryWrites=true&w=majority")
mydb = client.get_default_database()

bot = telegram.Bot(token="5394324389:AAGvCQN8ogbnwj1MStLHmvu7Kb9e3uQiF_4")

def main_buttons(update, context):
    reply_keyboard = [['Do Task💸', '', 'Create Task📜'], ['Balance⚖', 'Deposit➕'], ['Referal link📎', 'More❕']]

    update.message.reply_text("Main Menu",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                               one_time_keyboard=True))


def start(update, context):
    sender = update.message.reply_text
    chat_id = update.message.chat_id
    username = update.message.chat.username
    text = update.message.text
    if str(username) == "None":
        sender("No username found for your account")
        sender("Please set username for your telegram\n1)Go telegram account settings\n2)Click username\n3)Set unique and simplified username")
    else:
        checking_exist = mydb["people"]
        bot.sendMessage(chat_id=chat_id, text ="This KMC TRX earning bot"
                                               "\nYou can earn TRX by doing tasks"
                                               "\nAlso You can create task for other to do")

        main_buttons(update, context)
        for i in checking_exist.find({}):
            if username == i["username"]:
                break
        else:
            rand_num = random.randrange(11023648,12023648)
            rand_text = random.choice('qwertyuiopasfghjklzxcvbnm')
            link = "https://telegram.me/earn_trx_ind_bot?start="+str(rand_num)+rand_text
            checking_exist.insert_one({"_id": chat_id, "username": username , "referal":link , "ref_count":0})
            bot.sendMessage(chat_id=1291659507, text="New user found @" + str(username))
            referal(text, username)

def referal(text , username):
    referal = text.replace("/start ", '')
    if len(referal) > 0:
        ref = mydb["people"]
        link = "https://telegram.me/earn_trx_ind_bot?start="+str(referal)
        try:
            get = ref.find_one({"referal": link})
            get_invitee = get["_id"]
            get_count = get["ref_count"]
            ref.update_one({"_id": get_invitee}, {"$set": {"ref_count": get_count+1}})
            bot.sendMessage(chat_id=get_invitee, text=f"You got new referal: @{username}")
        except:
            get = ref.find_one({"referal":"https://telegram.me/earn_trx_ind_bot?start=11299293i"})
            get_invitee = get["_id"]
            get_count = get["ref_count"]
            ref.update_one({"_id": get_invitee}, {"$set": {"ref_count": get_count+1}})

def msg_hand(update, context):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    sender = update.message.reply_text
    text = update.message.text
    if 'Do Task💸' == text:
        task_list(update, context)
    elif 'Create Task📜' == text:
        pass
    elif 'Balance⚖' == text:
        pass
    elif 'Deposit➕' == text:
        bot.sendMessage("This is deposit option")
    elif 'Referal link📎' == text:
        get_link = mydb['people']
        get = get_link.find_one({"_id":chat_id})
        bot.sendMessage(chat_id=chat_id, text=f"Your referal link:\n{get['referal']}")
    elif "Withdraw➕" == text:
        pass

    if text == "More❕":
        reply_keyboard = [["Rules", "About"], ["Rank", "Support"], ["Withdraw➕","Back↩"]]
        update.message.reply_text("Use below buttons for quick access",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                               one_time_keyboard=True))
    elif text == "Back↩":
        # update.message.reply_text(text = 'test')
        main_buttons(update, context)


def do_task(update, context):
    text = update.message.text
    text = text.replace("/",'')
    find_task = mydb["tasks"]
    get = find_task.find_one({"cmd_id":text})
    keyboard = [
        [InlineKeyboardButton("Send Proof📥", callback_data=f"{get['cmd_id']}")],
        [InlineKeyboardButton("Skip⏩", callback_data="skip")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard,  one_time_keyboard=True , resize_keyboard=True)
    bot.sendMessage(chat_id = update.message.chat_id, text = f"Task id : /{get['cmd_id']}\n"
                                                             f"Title: {get['title']}\n"
                                                             f"Reward: {get['reward']} TRX\n", reply_markup=reply_markup)

    return SELECTING_COMMAND

def task_list(update , context):
    chat_id = update.message.chat_id
    tasks_list = mydb["tasks"]
    list1 = []
    total = 0
    for i in tasks_list.find({}):
        total += 1
        text = f"Task No: {total}\n" \
               f"Title: {i['title']}\n" \
               f"Reward: {i['reward']} TRX\n" \
               f"Task id : /{i['cmd_id']}"
        list1.append(text)

    update.message.reply_text("Total task found:{0}\n\n{1}\n\n".format(total, '\n'.join(x for x in list1)))


SELECTING_COMMAND = 1

def inline(update, CallbackContext):
    print("clicked")
    button_text = update.callback_query.data
    if button_text == "skip":
        pass
    else:
        update.effective_message.reply_text("Now send your task proof")
# bot.answer_callback_query(callback_query_id=call.id, text='you disliked it!')
    return 1

def com():
    tasks_list = mydb["tasks"]
    task = ["empty"]
    for i in tasks_list.find({}):
        task.append(i["cmd_id"])
    return task

def main():
    updater = Updater("5394324389:AAGvCQN8ogbnwj1MStLHmvu7Kb9e3uQiF_4", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler(com(), do_task))
    dp.add_handler(MessageHandler(Filters.text, msg_hand))
    dp.add_handler(CallbackQueryHandler(inline))
    print("Bot started")
    updater.start_polling()
    updater.idle()


main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
