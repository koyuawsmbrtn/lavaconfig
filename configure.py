#!/usr/bin/python3
import os.path
import os
appspath = "/usr/share/applications/"

home = os.path.expanduser("~")

if not os.path.exists(home+"/.config/lavalauncher"):
    os.mkdir(home+"/.config/lavalauncher")

if os.path.exists(home+"/.config/lavalauncher/lavalauncher"):
    os.system("rm -r "+home+"/.config/lavalauncher/lavalauncher")
else:
    os.system("touch "+home+"/.config/lavalauncher/lavalauncher")

def validappfile(appfile):
    f = open(appfile, "r")
    x = f.read()
    validapps = ["Name=", "Exec=", "Icon="]
    if all(app in x for app in validapps):
        return True
    else:
        f.close()
        return False

appfiles = []
for file in os.listdir(appspath):
    if file.endswith(".desktop"):
        f = open(appspath+file, "r")
        if validappfile(appspath+file):
            appfiles.append(appspath+file)
        f.close()

for file in os.listdir(home+"/.local/share/applications/"):
    if file.endswith(".desktop"):
        f = open(home+"/.local/share/applications/"+file, "r")
        if validappfile(home+"/.local/share/applications/"+file):
          appfiles.append(home+"/.local/share/applications/"+file)
        f.close()

def getappexec(appfile):
    exec = ""
    overrides = {
        "mullvad": "mullvad-vpn",
        "gnome-terminal": "kitty",
        "libreoffice": "libreoffice",
        "spotify": "gnome-terminal -e spotify_player",
        "inkscape": "env GDK_BACKEND=x11 inkscape",
        "amfora": "gnome-terminal -e amfora",
        "vlc": "vlc"
    }
    with open(appfile, "r") as file:
        for line in file:
            if line.startswith("Exec="):
                exec = line[5:]
    clean = ["%U", "%u", "%F", "%f", "%k", "%c", "%i", "%d", "%D", "%n", "%N", "%m", "%v", "%w", "--new-tab", "--new-window", "--open-url", "--incognito", "--ProfileManager", "--", "-quit"]
    for c in clean:
        exec = exec.replace(" "+c, "")
    exec = exec.replace("\n", "")
    exec = exec.replace("\"", "")
    for override in overrides:
        if override in exec:
            exec = overrides[override]
    return exec

def getappicon(appfile):
    with open(appfile, "r") as file:
        for line in file:
            if line.startswith("Icon="):
                return line[5:]

def icon2path(icon):
    if icon.startswith("/"):
        return icon
    else:
        if os.path.exists("/usr/share/icons/hicolor/48x48/apps/"+icon.replace("\n", "")+".png"):
            return "/usr/share/icons/hicolor/48x48/apps/"+icon.replace("\n", "")+".png"
        elif os.path.exists("/usr/share/icons/hicolor/64x64/apps/"+icon.replace("\n", "")+".png"):
            return "/usr/share/icons/hicolor/64x64/apps/"+icon.replace("\n", "")+".png"
        elif os.path.exists("/usr/share/pixmaps/"+icon.replace("\n", "")+".png"):
            return "/usr/share/pixmaps/"+icon.replace("\n", "")+".png"
        elif os.path.exists("/usr/share/icons/hicolor/scalable/apps/"+icon.replace("\n", "")+".svg"):
            return "/usr/share/icons/hicolor/scalable/apps/"+icon.replace("\n", "")+".svg"
        elif os.path.exists("/usr/share/icons/Adwaita/scalable/apps/"+icon.replace("\n", "")+".svg"):
            return "/usr/share/icons/Adwaita/scalable/apps/"+icon.replace("\n", "")+".svg"
        elif os.path.exists("/usr/share/icons/hicolor/256x256/apps/"+icon.replace("\n", "")+".png"):
            return "/usr/share/icons/hicolor/256x256/apps/"+icon.replace("\n", "")+".png"
        elif os.path.exists("/usr/share/icons/"+icon.replace("\n", "")+".png"):
            return "/usr/share/icons/"+icon.replace("\n", "")+".png"
        elif os.path.exists("/var/lib/flatpak/exports/share/icons/hicolor/512x512/apps/"+icon.replace("\n", "")+".png"):
            return "/var/lib/flatpak/exports/share/icons/hicolor/512x512/apps/"+icon.replace("\n", "")+".png"
        else:
            return "/usr/share/icons/Adwaita/scalable/mimetypes/application-x-executable.svg"

def createbutton(appfile):
    appexec = getappexec(appfile)
    appicon = getappicon(appfile)
    iconpath = icon2path(appicon)
    with open(home+"/.config/lavalauncher/lavalauncher", "a") as file:
        file.write("button\n{\n")
        file.write("image-path = "+iconpath+";\n")
        file.write("command = "+appexec+";\n")
        file.write("}\n\n")

def create_custom(appfile, appexec, icon=""):
    appicon = getappicon(appfile)
    if icon == "":
        iconpath = icon2path(appicon)
    else:
        iconpath = home+"/lavaconfig/icons/"+icon+".png"
    with open(home+"/.config/lavalauncher/lavalauncher", "a") as file:
        file.write("button\n{\n")
        file.write("image-path = "+iconpath+";\n")
        file.write("command = "+appexec+";\n")
        file.write("}\n\n")

def writeheader():
    with open(home+"/.config/lavalauncher/lavalauncher", "w") as file:
        file.write("global-settings\n{\n")
        file.write("watch-config-file = false;\n")
        file.write("}\n\n")
        file.write("bar\n{\n")
        file.write("position = bottom;\n")
        file.write("background-colour = \"#202020\";\n")
        file.write("condition-resolution = wider-than-high;\n")
        file.write("config\n{\n")
        file.write("condition-resolution = higher-than-wide;\n")
        file.write("position = left;\n")
        file.write("}\n")

def writefooter():
    with open(home+"/.config/lavalauncher/lavalauncher", "a") as file:
        file.write("}\n")


sortcategories = [
    "Network",
    "Internet",
    "Office",
    "System",
    "Graphics",
    "Multimedia",
    "Education",
    "Game",
    "Audio",
    "Utility",
    "Development"
]

def getcategory(appfile):
    category = ""
    with open(appfile, "r") as file:
        for line in file:
            if line.startswith("Categories="):
                category = line[11:]
    if ";" in category:
        categories = category.split(";")
        for cat in categories:
            if cat in sortcategories:
                category = cat
    return category

blacklist = [
    "nyxt",
    "inkscape",
    "prismlauncher",
    "ranger",
    "nnn",
    "freedesktop",
    "gnupg",
    "org.gnome",
    "vim",
    "htop",
    "hplip",
    "org.kde",
    "nm",
    "java",
    "gcr",
    "electron",
    "bssh",
    "bvnc",
    "cmake",
    "feh",
    "qvidcap",
    "qv4l2",
    "solaar",
    "weechat",
    "wine",
    "pavucontrol",
    "com.mattjakeman.ExtensionManager",
    "im.dino",
    "avahi",
    "url",
    "mpv",
    "bitwarden",
    "code",
    "system-config-printer",
    "cups",
    "firefox",
    "chrom",
    "brave",
    "foot",
    "btop",
    "sm64",
    "openttd",
    "xfce",
    "transmission",
    "chrome",
    "signal-tray",
    "notion",
    "zen",
    "yubico",
    "chatterino",
    "waydroid",
    "mcpe",
    "byobu",
    "links",
    "galculator",
    "scrcpy",
    "virtualbox",
    "amfora",
    "vlc",
    "elementary",
    "terminology",
    "kitty",
]

def writecustomapps():
    customapps = {
        "ani-cli": ["gnome-terminal -e ani-cli", "ani-cli"],
    }
    for app in customapps:
        with open(home+"/.config/lavalauncher/lavalauncher", "a") as file:
            file.write("button\n{\n")
            file.write("image-path = /home/koyu/lavaconfig/icons/"+customapps[app][1]+".png;\n")
            file.write("command = "+customapps[app][0]+";\n")
            file.write("}\n\n")

def sortapps(appfiles):
    sortedapps = []
    for category in sortcategories:
        for appfile in appfiles:
            if category in getcategory(appfile) and "libreoffice" not in appfile:
                sortedapps.append(appfile)
        if category == "Office":
            if os.path.exists(appspath+"libreoffice-startcenter.desktop"):
                sortedapps.append(appspath+"libreoffice-startcenter.desktop")
    return sortedapps

def getsystemflatpaks():
    systemflatpaks = []
    if os.path.exists("/var/lib/flatpak/exports/share/applications"):
        for file in os.listdir("/var/lib/flatpak/exports/share/applications"):
            if file.endswith(".desktop"):
                systemflatpaks.append("/var/lib/flatpak/exports/share/applications/"+file)
    return systemflatpaks

def isinstalled(app):
    isinstalled = False
    for appfile in appfiles:
        if app in appfile:
            isinstalled = True
    return isinstalled

writeheader()
if isinstalled("firefox"):
    createbutton(appspath+"firefox.desktop")
if isinstalled("chromium"):
    createbutton(appspath+"chromium.desktop")
if isinstalled("brave"):
    createbutton(appspath+"brave-browser.desktop")
#if isinstalled("google-chrome"):
#    createbutton(appspath+"google-chrome.desktop")
if isinstalled("zen"):
     createbutton(appspath+"zen.desktop")
for appfile in sortapps(appfiles):
    if not any(bl in appfile for bl in blacklist):
        createbutton(appfile)
if isinstalled("scrcpy"):
    create_custom(appspath+"scrcpy.desktop", "scrcpy")
if isinstalled("inkscape"):
    create_custom(appspath+"org.inkscape.Inkscape.desktop", "inkscape")
for flatpak in getsystemflatpaks():
    createbutton(flatpak)
writecustomapps()
if os.path.exists(appspath+"code.desktop"):
    createbutton(appspath+"code.desktop")
if os.path.exists(appspath+"org.gnome.Terminal.desktop"):
    createbutton(appspath+"org.gnome.Terminal.desktop")
writefooter()
