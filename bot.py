import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import google.generativeai as genai
import os

# --- INIZIA LA CONFIGURAZIONE ---

# Leggi le chiavi segrete dalle variabili d'ambiente per la sicurezza
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Configura l'intelligenza artificiale di Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- FINE DELLA CONFIGURAZIONE ---


# --- FUNZIONI DEL BOT ---

# Questa funzione si attiva quando un utente scrive /start
async def start(update, context):
    """Invia un messaggio di benvenuto."""
    user_name = update.effective_user.first_name
    await update.message.reply_text(f'Ciao {user_name}! Sono un bot collegato a Gemini. Chiedimi qualsiasi cosa!')

# Questa funzione si attiva per ogni messaggio di testo normale
async def handle_message(update, context):
    """Risponde ai messaggi di testo usando Gemini."""
    user_text = update.message.text
    
    # Invia un messaggio di attesa per far sapere all'utente che stiamo lavorando
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.constants.ChatAction.TYPING)

    try:
        # Invia il testo dell'utente a Gemini per ottenere una risposta
        response = model.generate_content(user_text)
        
        # Invia la risposta di Gemini all'utente su Telegram
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Errore durante la chiamata a Gemini: {e}")
        await update.message.reply_text("Ops! Qualcosa è andato storto. Riprova più tardi.")

# --- FUNZIONE PRINCIPALE PER AVVIARE IL BOT ---

def main():
    """Funzione principale per avviare il bot."""
    print("Avvio del bot in corso...")

    # Crea l'applicazione del bot con il token di Telegram
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Aggiunge i "gestori" per i comandi e i messaggi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Avvia il bot
    print("Bot avviato e in ascolto...")
    application.run_polling()

if __name__ == '__main__':
    main()