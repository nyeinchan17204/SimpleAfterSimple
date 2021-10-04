class config:
    BOT_TOKEN = "1979532614:AAH2w66o6716S0m9ocjkkdkPUa1ti5egDNo"
    APP_ID = "7693500"
    API_HASH = "8d82e2ae3917b001afb9a3e2c1ba2ce6"
    DATABASE_URL = "postgresql://postgres:6Qiza4CC09mGdvMm4n0E@containers-us-west-3.railway.app:6203/railway"
    SUDO_USERS = "1952030175 1317820373" # Sepearted by space.
    DOWNLOAD_DIRECTORY = "./downloads/"
    G_DRIVE_CLIENT_ID = "262285355738-kpmavuv7ibhsg3l5bck6lakh9fe39ltr.apps.googleusercontent.com"
    G_DRIVE_CLIENT_SECRET = "V9RGxtqrNtO9LVnpkrYQcZw8"
    SUPPORT_CHAT_LINK = "https://t.me/moedyiu"
 

class BotCommands:
  Download = ['download', 'dl']
  Authorize = ['auth', 'authorize']
  SetFolder = ['setfolder', 'setfl']
  Revoke = ['revoke']
  Clone = ['copy', 'clone']
  Delete = ['delete', 'del']
  EmptyTrash = ['emptyTrash']
  YtDl = ['ytdl']

class Messages:
    START_MSG = "**Hi there {}.**\n__I'm Google Drive Uploader Bot V3.You can use me to upload any file / video to Google Drive from direct link or Telegram Files.__\n__You can know more from /help.__ \n***Supported Direct Link***\nFacebook Video\nGoogle Drive\nYoutube\nSolidfiles\nAnonfiles\nMediafire\nZippyshare\nPornhub "

    HELP_MSG = [
        ".",
        "**Google Drive Uploader**\n__I can upload files from direct link or Telegram Files to your Google Drive. All i need is to authenticate me to your Google Drive Account and send a direct download link or Telegram File.__\n\nI have more features... ! Wanna know about it ? Just walkthrough this tutorial and read the messages carefully.",
        
        f"**Authenticating Google Drive**\n__Send the /{BotCommands.Authorize[0]} commmand and you will receive a URL, visit URL and follow the steps and send the received code here. Use /{BotCommands.Revoke[0]} to revoke your currently logged Google Drive Account.__\n\n**Note: I will not listen to any command or message (except /{BotCommands.Authorize[0]} command) until you authorize me.\nSo, Authorization is mandatory !**",
        
        f"**Direct Links**\n__Send me a direct download link for a file and i will download it on my server and Upload it to your Google Drive Account. You can rename files before uploading to GDrive Account. Just send me the URL and new filename separated by ' | '.__\n\n**__Examples:__**\n```https://example.com/AFileWithDirectDownloadLink.mkv | New FileName.mkv```\n\n**Telegram Files**\n__To Upload telegram files in your Google drive Account just send me the file and i will download and upload it to your Google Drive Account. Note: Telegram Files Downloading are slow. it may take longer for big files.__\n\n**YouTube-DL Support**\n__Download files via youtube-dl.\nUse /{BotCommands.YtDl[0]} (YouTube Link/YouTube-DL Supported site link)__",
        
        f"**Custom Folder for Upload**\n__Want to upload in custom folder or in__ **TeamDrive** __ ?\nUse /{BotCommands.SetFolder[0]} (Folder URL) to set custom upload folder.\nAll the files are uploaded in the custom folder you provide.__",
        
        f"**Delete Google Drive Files**\n__Delete google drive files. Use /{BotCommands.Delete[0]} (File/Folder URL) to delete file or reply /{BotCommands.Delete[0]} to bot message.\nYou can also empty trash files use /{BotCommands.EmptyTrash[0]}\nNote: Files are deleted permanently. This process cannot be undone.\n\n**Copy Google Drive Files**\n__Yes, Clone or Copy Google Drive Files.\n__Use /{BotCommands.Clone[0]} (File id / Folder id or URL) to copy Google Drive Files in your Google Drive Account.__",
        
        "**Rules & Precautions**\n__1. Don't copy BIG Google Drive Files/Folders. It may hang the bot and your files maybe damaged.\n2. Send One request at a time unless bot will stop all processes.\n3. Don't send slow links @transload it first.\n4. Don't misuse, overload or abuse this free service.__",
        
        # Dont remove this ↓ if you respect developer.
         
        "**Join Channel @modbots**"
        ]
     
    RATE_LIMIT_EXCEEDED_MESSAGE = "❗ **Rate Limit Exceeded.**\n__User rate limit exceeded try after 24 hours.__"
    
    FILE_NOT_FOUND_MESSAGE = "❗ **File/Folder မတွေ့ပါ..**\n__File id - {} Not found. Make sure it\'s exists and accessible by the logged account.__"
    
    INVALID_GDRIVE_URL = "❗ **Google Drive လင့်မဟုတ်ပါ..**\nGoogle Drive လင့်ဖြစ်ကြောင်းသေချာမှထည့်ပါ.."
    
    COPIED_SUCCESSFULLY = "✅ **အောင်မြင်စွာကူးယူပြီးပါပြီ...**\n[{}]({}) __({})__"
    
    NOT_AUTH = f"🔑 **Google Account မထည့်သွင်းရသေးပါ..**\n__Send /{BotCommands.Authorize[0]} to authenticate.__"
    
    DOWNLOADED_SUCCESSFULLY = "📤 **Upload တင်နေသည်......**\n**Filename:** ```{}```\n**Size:** ```{}```"
    
    UPLOADED_SUCCESSFULLY = "✅ **အောင်မြင်စွာတင်ပြီးပါပြီ...**\n[{}]({}) __({})__"
    
    DOWNLOAD_ERROR = "❗**ဒေါင်းလုပ်ဆွဲမှု မအောင်မြင်ပါ...**\n{}\n__Link - {}__"
    
    DOWNLOADING = "📥 **ဒေါင်းလုပ်ဆွဲနေပါသည်.....\nLink:** ```{}```"
    
    ALREADY_AUTH = "🔒 **Google Account ထည့်ပြီးသားဖြစ်နေပါသည်..**\n__တခြားအကောင့်ပြောင်းလိုပါက  /revoke ကိုသုံးပါ ..__\n__Google Drive ကိုတင်လိုပါက Direct Link ပို့ပါ..__"
    
    FLOW_IS_NONE = f"❗ **Authorize ကုတ်မှားနေပါသည် ...**\n__Run {BotCommands.Authorize[0]} first.__"
    
    AUTH_SUCCESSFULLY = '🔐 **Google Drive account အောင်မြင်စွာထည့်ပြီးပါပြီ..**'
    
    INVALID_AUTH_CODE = '❗ **Authorizeကုတ်မှားနေပါသည်..**\n__သင်ထည့်သွင်းသော ကုတ်မှာ မှားနေတာ သို့မဟုတ် သုံးပြီးသားဖြစ်နေပါသည်..Authorization URL ကိုနိပ်ပြီးနောက်ထပ်အသစ်ထပ်လုပ်ပါ.__'
    
    AUTH_TEXT = "⛓️ **GoogleAccount ထည့်ၕရန် ဒီလင့်ကိုနိပ် . [URL]({}) and send the generated code here.**\n__Visit the URL > Allow permissions > you will get a code > copy it > Send it here__"
    
    DOWNLOAD_TG_FILE = "📥 **ဖိုင်ဒေါင်းနေပါသည်....**\n**ဖိုင်အမည်:** ```{}```\n**ဖိုင်အရွယ်အစား:** ```{}```\n**MimeType:** ```{}```"
    
    PARENT_SET_SUCCESS = '🆔✅ **သိမ်းဆည်းမည့်နေရာထည့်ပြီးပါပြီ..**\n__သင့်ရဲ့ folder id - {}\nပယ်ဖျက်လိုပါက__ ```/{} clear``` __ကိုသုံးပါ.__'
    
    PARENT_CLEAR_SUCCESS = f'🆔🚮 **သိမ်းဆည်းမည့်နေရာ ပယ်ဖျက်ပြီးပါပြီ.**\n__အသစ်ထားရန်.__ ```/{BotCommands.SetFolder[0]} (Folder Link)``` __ကိုသုံးပါ။__.'
    
    CURRENT_PARENT = "🆔 **သင့်ရဲ့ Folder ID - {}**\n__ပြောင်းလဲရန်အတွက်__ ```/{} (Folder link)``` __ကိုသုံးပါ.__"
    
    REVOKED = f"🔓 **Google Account ဖယ်ရှားပီးပါပြီ.**\n__အသစ်ပြန်ထည့်ရန်အတွက် /{BotCommands.Authorize[0]} ကိုသုံးပါ.__"
    
    NOT_FOLDER_LINK = "❗ **Folder link မှားယွင်းနေပါသည်.**\n__သင်ထည့်သွင်းသောလင့်မှာ Folder လင့်မဟုတ်ပါ.__"
    
    CLONING = "🗂️ **Google Drive ကလုန်းပွားနေပါသည်...**\n__G-Drive Link - {}__"
    
    PROVIDE_GDRIVE_URL = "**❗ ယခု Command ကို Google Drive လင့်နှင့်တွဲသုံးပါ.**\n__Usage - /{} (GDrive Link)__"
    
    INSUFFICIENT_PERMISSONS = "❗ **ယခု ဖိုင်ကိုကူးရန်အတွင့် သင့်တွင်ခွင့်ပြုချက်မရှိပါ.**\n__File id - {}__"
    
    DELETED_SUCCESSFULLY = "🗑️✅ **ဖိုင်ကို အောင်မြင်စွာဖျက်ပြီးပါပြီ.**\n__အောင်မြင်စွာဖျက်ပြီး !\nFile id - {}__"
    
    WENT_WRONG = "⁉️ **ဂါးးးး: တစ်ခုခုမှားယွင်းနေပါသည်။**\n__Please try again later.__"
    
    EMPTY_TRASH = "🗑️🚮**အမှိုက်ပုံးရှင်းပြီးပါပြီ !**"
    
    PROVIDE_YTDL_LINK = "❗**Provide a valid YouTube-DL supported link.**"
