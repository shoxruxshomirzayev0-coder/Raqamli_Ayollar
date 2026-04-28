import requests
from telegram import *
from telegram.ext import *
import config
import db

app = ApplicationBuilder().token(config.TOKEN).build()

# YouTube info
def get_video_info(url):
    try:
        api = f"https://www.youtube.com/oembed?url={url}&format=json"
        data = requests.get(api).json()
        return data['title'], data['thumbnail_url']
    except:
        return None, None

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = []
    for cat in db.get_categories():
        buttons.append([InlineKeyboardButton(cat[1], callback_data=f"cat_{cat[0]}")])

    await update.message.reply_text(
        "📚 Darsliklarni tanlang:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# CATEGORY BOSILDI
async def category_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    cat_id = int(query.data.split("_")[1])
    videos = db.get_videos(cat_id)

    if not videos:
        await query.message.reply_text("❌ Bu kategoriyada hali video yo‘q")
        return

    for v in videos:
        keyboard = [[InlineKeyboardButton("▶️ Ko‘rish", url=v[3])]]
        await query.message.reply_photo(
            photo=v[4],
            caption=v[2],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ADMIN: kategoriya qo‘shish
async def add_category_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != config.ADMIN_ID:
        return

    name = " ".join(context.args)
    db.add_category(name)
    await update.message.reply_text("✅ Kategoriya qo‘shildi")

# ADMIN: video qo‘shish
async def add_video_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != config.ADMIN_ID:
        return

    try:
        cat_id = int(context.args[0])
        url = context.args[1]

        title, thumb = get_video_info(url)

        if title:
            db.add_video(cat_id, title, url, thumb)
            await update.message.reply_text("✅ Video qo‘shildi")
        else:
            await update.message.reply_text("❌ Video olinmadi")
    except:
        await update.message.reply_text("❗ Format: /addvideo category_id youtube_link")

# HANDLERS
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addcat", add_category_cmd))
app.add_handler(CommandHandler("addvideo", add_video_cmd))
app.add_handler(CallbackQueryHandler(category_click, pattern="cat_"))

print("Bot ishlayapti...")
app.run_polling()