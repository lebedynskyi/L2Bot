# Lineage 2 bot 

![Python unit tests](https://github.com/lebedynskyi/L2Bot/actions/workflows/main.yaml/badge.svg)

This bot - is kind of mix of auto clicker and computer vision.
Bot has general logic and specific **Parsers** for different L2 chronicles. Parsers are using computer vision to determine current HP of target, find target on the screen and etc  

Here I've used next technologies:

* **OpenCV** for computer vision for template matching and graphic filtering 
* **Tesseract** for text recognition
* **Arduino micro** for emulating native keyboard to bypass game protectors
* **Python multithreading** for hotkey listening and main bot looping
* 3rd party libraries like Pillow, PyAutoGUI, pywin32 ,etc

# Main components of the bot:
* **BaseApp** - main app looper that loops in a main thread. Just simple looper for  iterating given handlers
* **Handler** - part of the logic. Looper call **Handler.on_tick()** method every N time (depends on settings for looper)
* **Parser** - simple parser of the image. In takes screenshot as input and gives some result. The type of the result is unknown. Developer takes care of handling it.

# TODO
* The biggest issue is to teach bot how to find targets. Even if scroll camera. On some servers some limitation of range. Titles not seen. Need to move mouse to target the mob.
* Add checking if target under the mouse pointer before click. Additional time for target selection. But it will help to avoid movement around environment
* Need to introduce apropriate tests for near targets. it will help not to break OCR


# How to use the bot:

**Simple way:**
```python
pass
```

**Full way:**
```python
pass
```
