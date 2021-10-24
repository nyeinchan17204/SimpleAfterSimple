import os
import wget
import glob
import youtube_dl as ytdl
from youtube_dl import DownloadError
from pySmartDL import SmartDL
from urllib.error import HTTPError
from bot import DOWNLOAD_DIRECTORY, LOGGER


def download_file(url, dl_path):
  try:
    dl = SmartDL(url, dl_path, progress_bar=False)
    LOGGER.info(f'Downloading: {url} in {dl_path}')
    dl.start()
    return True, dl.get_dest()
  except HTTPError as error:
    return False, error
  except Exception as error:
    try:
      filename = wget.download(url, dl_path)
      return True, os.path.join(f"{DOWNLOAD_DIRECTORY}/{filename}")
    except HTTPError:
      return False, error

def utube_dl(link):
  ytdl_opts = {
    'outtmpl' : os.path.join(DOWNLOAD_DIRECTORY, '%(title).50s.%(ext)s'),
    'noplaylist' : True,
    'logger': LOGGER,
    'format': 'bestvideo+bestaudio/best',
    'geo_bypass_country': 'IN'
  }
  with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
    try:
      meta = ytdl.extract_info(link, download=True)
    except DownloadError as e:
      return False, str(e)
    for path in glob.glob(os.path.join(DOWNLOAD_DIRECTORY, '*')):
      if path.endswith(('.avi', '.mov', '.flv', '.wmv', '.3gp','.mpeg', '.webm', '.mp4', '.mkv')) and \
          path.startswith(ytdl.prepare_filename(meta)):
        return True, path
    return False, 'Something went wrong! No video file exists on server.'
    #Adding
def mytube_dl(url):
ytdl_opts = {
    'outtmpl' : os.path.join(DOWNLOAD_DIRECTORY, '%(title).50s.%(ext)s'),
    'noplaylist' : True,
    'logger': LOGGER
  }
    formats = [
        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio",
        "bestvideo[vcodec^=avc]+bestaudio[acodec^=mp4a]/best[vcodec^=avc]/best",
        ""
    ]
    # TODO it appears twitter download on macOS will fail. Don't know why...Linux's fine.
    for f in formats:
        if f:
            ydl_opts["format"] = f
        try:
            logging.info("Downloading for %s with format %s", url, f)
            with ytdl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            break

        except DownloadError as e:
                 return False, str(e)
            logging.error("Download failed for %s ", url)
            
            # can't return here
        except ValueError as e:
                 return False, str(e)
        except Exception as e:
        	      return False, str(e)
            logging.error("UNKNOWN EXCEPTION: %s", e)

    for path in glob.glob(os.path.join(DOWNLOAD_DIRECTORY, '*')):
      if path.endswith(('.avi', '.mov', '.flv', '.wmv', '.3gp','.mpeg', '.webm', '.mp4','.m4a', '.mkv')) :
        return True, path
    return False, 'Something went wrong! No video file exists on server.'

#convert mp4 if need
