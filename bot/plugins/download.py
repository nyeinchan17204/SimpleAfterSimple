import os
import re
import json
import lk21
import requests
import wget
import urllib.parse
import ffmpeg
import logging
import typing
import pathlib
import tempfile

from lk21.extractors.bypasser import Bypass
from bs4 import BeautifulSoup
from time import sleep
from pyrogram import Client, filters, types
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import CustomFilters, humanbytes
from bot.helpers.downloader import download_file, utube_dl, download_fb
from bot.helpers.gdrive_utils import GoogleDrive 
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError
#this is for you
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.helpers.ytdownloader import convert_flac, sizeof_fmt, upload_hook, ytdl_download
from bot.helpers.ytutils import customize_logger
from tgbot_ping import get_runtime

@Client.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Download) | filters.regex('^(ht|f)tp*')) & CustomFilters.auth_users)
def _download(client, message):
  user_id = message.from_user.id
  if not message.media:
    sent_message = message.reply_text('🕵️**Checking link...**', quote=True)
    if message.command:
      link = message.command[1]
    else:
      link = message.text
    if 'drive.google.com' in link:
      sent_message.edit(Messages.CLONING.format(link))
      LOGGER.info(f'Copy:{user_id}: {link}')
      msg = GoogleDrive(user_id).clone(link)
      sent_message.edit(msg)
    
    if 'facebook' in link:
      url = message.text
      try:
        r  = requests.post("https://yt1s.io/api/ajaxSearch/facebook", data={"q": url, "vt": "facebook"}).text
        bs = BeautifulSoup(r, "html5lib")

        js = str(bs).replace('<html><head></head><body>{"status":"ok","p":"facebook","links":', '').replace('</body></html>', '').replace('},', ',')
        text_file = open(str(user_id) + "fb.txt", "w")
        n = text_file.write(js)
        text_file.close()
        with open(str(user_id) + "fb.txt") as f:
            contents = json.load(f)
            try:
              durl = str(contents['hd']).replace('&amp;', '&')
              link = durl.strip()
              filename = os.path.basename(link)
              dl_path = DOWNLOAD_DIRECTORY
              LOGGER.info(f'Download:{user_id}: {link}')
              sent_message.edit(Messages.DOWNLOADING.format(link))
              result, file_path = download_file(link, dl_path)

              if os.path.exists(file_path):
                sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
                msg = GoogleDrive(user_id).upload_file(file_path)
                sent_message.edit(msg)
                LOGGER.info(f'Deleteing: {file_path}')
                os.remove(file_path)  
            except:
              durl = str(contents['sd']).replace('&amp;', '&')
              link = durl.strip()
              filename = os.path.basename(link)
              dl_path = DOWNLOAD_DIRECTORY
              LOGGER.info(f'Download:{user_id}: {link}')
              sent_message.edit(Messages.DOWNLOADING.format(link))
              result, file_path = download_file(link, dl_path)

              if os.path.exists(file_path):
                sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
                msg = GoogleDrive(user_id).upload_file(file_path)
                sent_message.edit(msg)
                LOGGER.info(f'Deleteing: {file_path}')
                os.remove(file_path)  
        
        
      except:
        sent_message = message.reply_text('🕵️**Your Facebook Link is Private & SO i cAnNot Download**', quote=True)
        
   
    if 'solidfiles' in link:
      url = message.text
      headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
        }
      try:
        pageSource = requests.get(url, headers = headers).text
        mainOptions = str(re.search(r'viewerOptions\'\,\ (.*?)\)\;', pageSource).group(1))
        dl_url = json.loads(mainOptions)["downloadUrl"]
        link = dl_url.strip()
        filename = os.path.basename(link)
        dl_path = DOWNLOAD_DIRECTORY
        LOGGER.info(f'Download:{user_id}: {link}')
        sent_message.edit(Messages.DOWNLOADING.format(link))
        result, file_path = download_file(link, dl_path)
        if os.path.exists(file_path):
          sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
          msg = GoogleDrive(user_id).upload_file(file_path)
          sent_message.edit(msg)
          LOGGER.info(f'Deleteing: {file_path}')
          os.remove(file_path)
      except:
        sent_message = message.reply_text('🕵️**Solidfiles link error...**', quote=True)
    
    if 'anonfiles' in link:
      url = message.text
      try:
        bypasser = lk21.Bypass()
        dl_url=bypasser.bypass_anonfiles(url)
        link = dl_url.strip()
        filename = os.path.basename(link)
        dl_path = DOWNLOAD_DIRECTORY
        LOGGER.info(f'Download:{user_id}: {link}')
        sent_message.edit(Messages.DOWNLOADING.format(link))
        result, file_path = download_file(link, dl_path)
        if os.path.exists(file_path):
          sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
          msg = GoogleDrive(user_id).upload_file(file_path)
          sent_message.edit(msg)
          LOGGER.info(f'Deleteing: {file_path}')
          os.remove(file_path)
      except:
        sent_message = message.reply_text('🕵️**Anonfiles link error...**', quote=True)
      
    if 'mediafire.com' in link:
      url = message.text
      try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
      except IndexError:
        sent_message = message.reply_text('🕵️**mediafire link error...**', quote=True)
      page = BeautifulSoup(requests.get(link).content, 'lxml')
      info = page.find('a', {'aria-label': 'Download file'})
      dl_url = info.get('href')
      link = dl_url.strip()
      filename = os.path.basename(link)
      dl_path = DOWNLOAD_DIRECTORY
      LOGGER.info(f'Download:{user_id}: {link}')
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if os.path.exists(file_path):
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message = message.reply_text('🕵️**mediafire link error...**', quote=True)
    if 'zippyshare.com' in link:
      url = message.text
      dl_url = ''
      try:
        link = re.findall(r'\bhttps?://.*zippyshare\.com\S+', url)[0]
      except IndexError:
        sent_message = message.reply_text('🕵️**zippy link error...**', quote=True)
      session = requests.Session()
      base_url = re.search('http.+.com', link).group()
      response = session.get(link)
      page_soup = BeautifulSoup(response.content, "lxml")
      scripts = page_soup.find_all("script", {"type": "text/javascript"})
      for script in scripts:
        if "getElementById('dlbutton')" in script.text:
          url_raw = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                              script.text).group('url')
          math = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                           script.text).group('math')
          dl_url = url_raw.replace(math, '"' + str(eval(math)) + '"')
          break
      dl_url = base_url + eval(dl_url)
      link = dl_url.strip()
      filename = urllib.parse.unquote(dl_url.split('/')[-1])
      dl_path = DOWNLOAD_DIRECTORY
      LOGGER.info(f'Download:{user_id}: {link}')
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if os.path.exists(file_path):
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path),
                                                                  humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message = message.reply_text('🕵️** zippy link error...**', quote=True)

    if 'pornhub.com' in link:
      link = message.text
      LOGGER.info(f'YTDL:{user_id}: {link}')
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = utube_dl(link)
      if result:
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message = message.reply_text('🕵️**PORNHUB ERROR**', quote=True) 
   

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

#This is my modify
@Client.on_message(filters.incoming & filters.private & filters.command(BotCommands.YtDl) & CustomFilters.auth_users)
def download_handler(client: "Client", message: "types.Message"):

    if message.chat.type != "private" and not message.text.lower().startswith("/ytdl"):
        logging.warning("%s, it's annoying me...🙄️ ", message.text)
        return

    url = re.sub(r'/ytdl\s*', '', message.text)
    logging.info("start %s", url)

    if not re.findall(r"^https?://", url.lower()):
        Redis().update_metrics("bad_request")
        message.reply_text("I think you should send me a link.", quote=True)
        return

    Redis().update_metrics("video_request")
    bot_msg: typing.Union["types.Message", "typing.Any"] = message.reply_text("Processing", quote=True)
    client.send_chat_action(chat_id, 'upload_video')
    temp_dir = tempfile.TemporaryDirectory()

    result = ytdl_download(url, temp_dir.name, bot_msg)
    logging.info("Download complete.")

    markup = InlineKeyboardMarkup(
        [
            [  # First row
                InlineKeyboardButton(  # Generates a callback query when pressed
                    "audio",
                    callback_data="audio"
                )
            ]
        ]
    )

    if result["status"]:
        client.send_chat_action(chat_id, 'upload_document')
        video_paths = result["filepath"]
        bot_msg.edit_text('Download complete. Sending now...')
        for video_path in video_paths:
            filename = pathlib.Path(video_path).name
            remain = bot_text.remaining_quota_caption(chat_id)
            size = sizeof_fmt(os.stat(video_path).st_size)
            meta = get_metadata(video_path)
            client.send_video(chat_id, video_path,
                              supports_streaming=True,
                              caption=f"`{filename}`\n\n{url}\n\nsize: {size}\n\n{remain}",
                              progress=upload_hook, progress_args=(bot_msg,),
                              reply_markup=markup,
                              **meta
                              )
            Redis().update_metrics("video_success")
        bot_msg.edit_text('Download success!✅')
    else:
        client.send_chat_action(chat_id, 'typing')
        tb = result["error"][0:4000]
        bot_msg.edit_text(f"Download failed!❌\n\n```{tb}```", disable_web_page_preview=True)

    temp_dir.cleanup
def get_metadata(video_path):
    width, height, duration = 1280, 720, 0
    try:
        video_streams = ffmpeg.probe(video_path, select_streams="v")
        for item in video_streams.get("streams", []):
            height = item["height"]
            width = item["width"]
        duration = int(float(video_streams["format"]["duration"]))
    except Exception as e:
        logging.error(e)
    return dict(height=height, width=width, duration=duration)
