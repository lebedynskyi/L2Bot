# Lineage 2 Interlude bot

This s a bot kind of mix of auto clicker and logic with computer vision.  

Bot is developed for interlude server. I think it easy to adjust it for any server. The main principle is parsing of input images.

Used next technologies:

* OpenCV for computer vision for looking given templates 
* Tesseract OCR for extracting text from given images

# Main components of the bot:

* AppLooper - main app looper that loops in a main thread. Just simple looper for iteration of given Handlers
* Handler - part of the logic. looper call **Handler.on_tick()** method every N time (depends on settings for looper)
* Parser - simple parser of the image. In takes screenshot as input and gives some result. The type of the result is unknown. Developer takes care of handling it.


**TODO:**
* Extract Captcha handler into separate handlers
* Implement complex handler for farming of Splendor mobs
* Improve Status handler to check MP and CP and do some action if CP decreasing. BSOE? Stop farm ?