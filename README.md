# Lineage 2 Interlude bot

This is a bot kind of mix of auto clicker and logic with computer vision.  

Bot is developed for interlude server. I think it is easy to adjust it for any server. The main principle - parsing of input images as templates and screenshots inside parser

Used next technologies:

* OpenCV for computer vision for looking given templates 
* Tesseract OCR for extracting text from given images
* PyAutogui for mouse movement and keyboard clicking

# Main components of the bot:

* AppLooper - main app looper that loops in a main thread. Just simple looper for iteration of given Handlers
* Handler - part of the logic. looper call **Handler.on_tick()** method every N time (depends on settings for looper)
* Parser - simple parser of the image. In takes screenshot as input and gives some result. The type of the result is unknown. Developer takes care of handling it.


# TODO
* Extract Captcha handler into separate handlers
* Improve Status handler to check MP and CP and do some action if CP decreasing. BSOE? Stop farm ?
* Get rid of BotCaptchaParser. DialogParser should be aware of extracting the text

# How to use the bot:

* Bot works only on **Windows**
* Windows screen resolution also must be **1920x1080** pixels
* Game screen resolution should be set up as **1920x1080** pixels.
* **It does not matter** is the game on a full screen or in a windowed mode

**Simple way:**
```python
target_template = cv2.imread("res/template/farm/target_template.png")
# General parser. Takes input template and return true if there is any match on the screenshot
target_parser = TemplateExistParser(env_path, target_template)
farm_handler = FarmHandler(target_parser)

looper = AppLooper(farm)
looper.loop()
```

**Full way:**
```python
# Parser of warning dialog (Just for captcha parser)
warn_template = cv2.imread("res/template/warning_template.png")
dialog_parser = WarnDialogParser(env_path, warn_template)

# Determines Group captcha dialog
group_template = cv2.imread("res/template/dualbox_template.png")
group_captcha_parser = GroupDialogParser(env_path, group_template)

# Determines user death window
death_template = cv2.imread("res/template/status/user_death_template.png")
death_parser = UserDeathStatusParser(env_path, death_template)

# Determines that player has a target
target_template = cv2.imread("res/template/farm/target_template.png")
target_parser = TemplateExistParser(env_path, target_template)

# Parser for user HP / MP count
status_template = cv2.imread("res/template/status/user_status_template.png")
status_parser = UserStatusParser(env_path, status_template)

# Parser that extracts text from
captcha_parser = BotCaptchaParser(env_path)
captcha_solver = CaptchaSolver()

# Create a bunch of handlers
captcha = CaptchaHandler(dialog_parser, captcha_parser, group_captcha_parser, captcha_solver)
death = UserDeathHandler(death_parser)
farm = FarmHandler(target_parser)
pet = PetManaHandler(status_parser, farm)
buff = BuffHandler()

#Run looper wuth any amount of handlers.
looper = AppLooper(buff, captcha, death, farm, pet)
looper.loop()
```
