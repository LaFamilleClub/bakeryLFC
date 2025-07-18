## Welcome!

Thank you for considering using my phone system for your game! I hope it serves you well. Please make sure to read the license in LICENSE.md and please credit me if you use it in your game. If you need support or want to work with me directly, please contact me at [luka.moe](https://luka.moe/socials) or my Discord at `kleineluka`.

## Installation

1. To add to your project, you will need to add `phone.rpy` to your `game/` folder. This is where the code lives.
2. Now copy the resources from `images/phone` and `audio/phone` to your `game/` folder. You can edit them as you see fit, and also delete extra unused skins or supporter packs to save space on your game (although it's all like, under 1MB combined, so it's fine either way).
3. Finally, you want to make sure the text box is hidden when the phone is present. This requires adding a line of code to `screens.rpy` in your `game/` folder - but fear not, we aren't changing any of the default behaviour. Find the `screen say(who, what):` block and replace it with the following code:

```python
screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        background (None if phone_mode else Image("gui/textbox.png", xalign=0.5, yalign=1.0))
        xalign 0.5
        xfill True
        yalign gui.textbox_yalign
        ysize gui.textbox_height

        if who is not None:
            text who id "who"

        text what id "what"

    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0
```
4. Done! Now customise as you see fit, and reference the demo script for how to do various things (ex. sending a message).

## Questions and (Hopefully Good) Answers

**Question:** How can I change the default chats?
<br>
**Answer:** In `phone.rpy`, find `reset_phone_data` and edit that.
<br><br>
**Question:** How can I change the phone skin?
<br>
**Answer:** Simply replace the images in `images/phone` with the provided ones in the skin folder (you can find all the skins, including the supporter ones, in `images/phone/skins`).
<br><br>
**Question:** How can I change the phone position? (or size)
<br>
**Answer:** Like everything else, see `script.rpy`. You can also edit the default transition in `phone.rpy` to change how the phone appears on screen. right above the phone screen. All code is also well-documented with comments and explanations in `phone.rpy` for you to browse as well!
<br><br>
**More?** Contact me (below)!


## Contact Me
- https://luka.moe/socials
- Discord: `kleineluka`
- Email: lukazoeysong[@]gmail.com

## Demo Attributions!
- ResidentRabbit (Eros) made the public domain sprites I used for the demo, which can be found [here](https://residentrabbit.itch.io/resident-rabbits-vn-fem-sprite-01) and [here](https://residentrabbit.itch.io/femfemale-visual-novel-sprite-set-2).
- Google Noto Colour Emoji for the emojis used in the demo (which is under Open Font License 1.1).
- Spiral Atlas for the backgrounds used in the demo (as well as in the pictures backgrounds), of which the first pack can be found [here](https://spiralatlas.itch.io/regency-backgrounds-2) and the second pack can be found [here](https://spiralatlas.itch.io/house-visual-novel-backgrounds).
- Notification sounds are from Pixabay
- These are all part of the demo. Anything for the actual phone system itself is all by me.

⠀⠀⠀⠀⠀⠀⠀   ⠀⠀⠀ ⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣶⣟⣛⠛⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⢛⣛⣷⡦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀      
                Made by an Angel.
 ⠀ ⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢀⡀⠀
  ⣴⠛⠉⠉⠱⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠞⠉⠉⠙⣦
  ⣧⠀⠀⠀⠀⠀⠙⢦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠋⠀⠀⠀⠀⠀⣼
  ⠹⣄⠀⠀⠀⠀⠀⠀⠈⠙⠲⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠖⠋⠀⠀⠀⠀⠀⠀⠀⣠⠏
  ⠀⠙⢶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢦⡀⠀⠀⠀⠀⠀⢀⡴⠋⠁⠀⠀⠀⠀⠀⠀⠀⣀⣠⡾⠋⠀
 ⠀ ⠀⡼⠋⠉⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⢹⡄⠀⠀⠀⢠⡟⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠉⠙⢧⠀⠀
 ⠀ ⠈⢧⡀⠀⠀⠀⠀⠀⢀⠀⣴⠋⡉⢳⡄⣷⠀⠀⠀⣾⢠⡞⠉⠙⣦⠀⠀⢀⠀⠀⠀⠀⢀⡼⠀⠀
  ⠀⠀⠈⠙⠒⢲⡟⠀⠀⠀⠀⢻⣄⠙⠛⣱⠇⠀⠀⠀⠸⣎⠛⠋⣠⡟⠀⠀⠈⠀⢻⡗⠒⠋⠁⠀⠀
⠀ ⠀⠀ ⠀⠀⠈⠷⣄⣀⣀⣀⣤⠟⠛⠛⠁⠀⠀⠀⠀⠀⠈⠛⠛⠻⣤⣀⣀⣀⣤⠾⠁⠀⠀⠀⠀⠀
⠀⠀  ⠀⠀⠀⠀⠀⠈⠁⠉⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠉⠈⠀⠀⠀⠀⠀⠀⠀⠀

         more of me: https://www.luka.moe
