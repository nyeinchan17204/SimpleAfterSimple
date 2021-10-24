import os
import re
import json
import lk21
import requests
import wget
import urllib.parse

import typing 
import pathlib
import ffmpeg

from lk21.extractors.bypasser import Bypass
from bs4 import BeautifulSoup
from time import sleep
from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import CustomFilters, humanbytes
from bot.helpers.downloader import download_file, utube_dl, download_fb
from bot.helpers.gdrive_utils import GoogleDrive 
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError
#Adding youtube
from bot.helpers.downloadhelper import convert_flac, sizeof_fmt, upload_hook, ytdl_download

@Client.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Download) | filters.regex('^(ht|f)tp*')) & CustomFilters.auth_users)
def _download(client, message):
  user_id = message.from_user.id
  if not message.media:
    sent_message = message.reply_text('🕵️**Checking link...**', quote=True)
    if message.command:
      link = message.command[1]
    else:
      link = message.text
#Cheack google drive link
    if 'drive.google.com' in link:
      sent_message.edit(Messages.CLONING.format(link))
      LOGGER.info(f'Copy:{user_id}: {link}')
      msg = GoogleDrive(user_id).clone(link)
      sent_message.edit(msg)
 #Cheack youtube Link  
    if 'youtu' in link:
chat_id = message.chat.id
      link = message.text
  #Adding youtube downloa code

    if message.chat.type != "private" and not message.text.lower().startswith("/ytdl"):
        logging.warning("%s, it's annoying me...🙄️ ", message.text)
    return
	
    link = re.sub(r'/ytdl\s*', '', message.text)
    logging.info("start %s", link)

    if not re.findall(r"^https?://", link.lower()):
        message.reply_text("I think you should send me a link.", quote=True)
        return

    bot_msg: typing.Union["types.Message", "typing.Any"] = message.reply_text("Processing", quote=True)
    client.send_chat_action(chat_id, 'upload_video')

    result = ytdl_download(link, DOWNLOAD_DIRECTORY, bot_msg)
    logging.info("Download complete.")


    if result["status"]:
        client.send_chat_action(chat_id, 'upload_document')
        video_paths = result["filepath"]
        bot_msg.edit_text('Download complete. Sending now...')
	for video_path in video_paths:
            filename = pathlib.Path(video_path).name
            remain = bot_text.remaining_quota_caption(chat_id)
            size = sizeof_fmt(os.stat(video_path).st_size)
            meta = get_metadata(video_path)

		msg = GoogleDrive(user_id).upload_file(video_path)
		sent_message.reply_text(msg,quote=True)
	os.remove(video_paths)
else:
        client.send_chat_action(chat_id, 'typing')
        tb = result["error"][0:4000]
        bot_msg.edit_text(f"Download failed!❌\n\n```{tb}```", disable_web_page_preview=True)

    temp_dir.cleanup()
   #xxxxxx

@Client.on_message(filters.private & filters.incoming & (filters.document | filters.audio | filters.video | filters.photo) & CustomFilters.auth_users)
def _telegram_file(client, message):
  user_id = message.from_user.id
  sent_message = message.reply_text('🕵️**...ဖိုင်ကိုစစ်ဆေးနေပါသည်....**', quote=True)
  if message.document:
    file = message.document
  elif message.video:
    file = message.video
  elif message.audio:
    file = message.audio
  elif message.photo:
  	file = message.photo
  	file.mime_type = "images/png"
  	file.file_name = f"IMG-{user_id}-{message.message_id}.png"
  sent_message.edit(Messages.DOWNLOAD_TG_FILE.format(file.file_name, humanbytes(file.file_size), file.mime_type))
  LOGGER.info(f'Download:{user_id}: {file.file_id}')
  try:
    file_path = message.download(file_name=DOWNLOAD_DIRECTORY)
    sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
    msg = GoogleDrive(user_id).upload_file(file_path, file.mime_type)
    sent_message.reply_text(msg,quote=True)
  except RPCError:
    sent_message.edit(Messages.WENT_WRONG)
  LOGGER.info(f'Deleteing: {file_path}')
  os.remove(file_path)



