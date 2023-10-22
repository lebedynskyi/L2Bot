# Lineage 2 bot 

![Python unit tests](https://github.com/lebedynskyi/L2Bot/actions/workflows/main.yaml/badge.svg)

This is a bot - kind of mix of auto clicker and computer vision.
Bot has general logic and specific **Parsers** for different L2 chronicles. Parser is using computer vision to determine current hp of target, find target and etc  

Here I've used next technologies:

* **OpenCV** for computer vision for template matching and graphic filtering 
* **Tesseract** for text recognition
* **Arduino micro** for emulating native keyboard to bypass some game protections
* 3rd party libraries like Pillow, PyAutoGUI, pywin32 ,etc

# Main components of the bot:
* **BaseApp** - main app looper that loops in a main thread. Just simple looper for  iterating given handlers
* **Handler** - part of the logic. Looper call **Handler.on_tick()** method every N time (depends on settings for looper)
* **Parser** - simple parser of the image. In takes screenshot as input and gives some result. The type of the result is unknown. Developer takes care of handling it.


# TODO
* Check admin permission not working
* Finish at least auto farm
* Unittest. Some magic with start folder. Need to teach 

# How to use the bot:


**Simple way:**
```python

```

**Full way:**
```python

```
