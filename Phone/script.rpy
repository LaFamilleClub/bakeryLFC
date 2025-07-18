# please see phone.rpy for more info and license

# this is all for the demo only, we can ignore~
image vanessa_happy = "demo/vanessa.png"
image bg bedroom = "demo/bedroom.jpg"
define vanessa = Character("Vanessa", color="#ff00ff")
transform small_sprite:
    zoom 0.25
    xalign 0.5
    yalign 0.5
transform jump_up:
    linear 0.1 yoffset -50
    linear 0.1 yoffset 0

# demo!
label start:

    # purely demo stuff, ignore again~ (please ignore, it sucks a lot lol)
    "*Isekai truck.*"
    scene bg bedroom
    show vanessa_happy at small_sprite
    "You're transported to a magical place.. an average anime bedroom."
    show vanessa_happy at jump_up
    pause 0.5
    vanessa "Oh~ hi! Thanks for coming by, I got you a new phone! It's pretty cool~~"
    vanessa "{size=30}{i}or at least I think so...{/i}{/size}"
    vanessa "But yeah, don't sweat it too much, it's what I do. I give phones to people who get isekai'd into this world."
    vanessa "I've already put me in your contacts, as well as my friend Avery. Let's get texting so you can try it out!"
    "And just like that, Vanessa pulls out the phone and starts showing it off."
    "I'm gonna clear the screen for this demo, so you can see the phone better, but that isn't required to use the phone in your own game!"
    window hide
    scene black
    hide vanessa_happy

    # phone relevant! step one: we set up the environment for the phone (only do this once per game, or whenever you want a clean phone slate to use)
    # you can either add your pre-existing channels, messages, etc. here or in the reset_phone_data function!
    $ reset_phone_data()

    # phone relevant! step two: we start the phone and show the UI
    $ phone_start()
    show screen phone_ui

    # phone relevant! step three: we send messages to the phone
    $ send_phone_message("", "Later That Day", "vanessa_dm", 1) # EXAMPLE: Time Stamp
    $ send_phone_message("Vanessa", "Hey!! I'm in your phone now!!", "vanessa_dm") # EXAMPLE: Character sending a message.
    $ send_phone_message("Vanessa", "<emoji_sob> Get me out! I'm stuck in your phone!! <emoji_sob> <emoji_sob>", "vanessa_dm", 3) # EXAMPLE: Character sending a message with emojis.
    $ send_phone_message(phone_config["phone_player_name"], "Oh, um..", "vanessa_dm") # EXAMPLE: Player sending a message.
    $ present_phone_choices([("How can I help!?", None, None), ("What do you mean?", None, None)], "vanessa_dm") # EXAMPLE: Presenting non-branching choices to the player.
    $ phone_pause(2.0) # EXAMPLE: Forcing a pause in the phone UI.
    $ send_phone_message("", "That Evening", "vanessa_dm", 1)
    $ send_phone_message("Vanessa", "Just kidding!!", "vanessa_dm")
    $ send_phone_message("Vanessa", "Wait, you didn't like.. think I was really stuck, did you?", "vanessa_dm")
    $ send_phone_message("Vanessa", "You know you can't get stuck in a phone, right?", "vanessa_dm")
    $ send_phone_message(phone_config["phone_player_name"], "I mean, yeah...", "vanessa_dm")
    $ send_phone_message(phone_config["phone_player_name"], "...", "vanessa_dm")
    $ send_phone_message("Vanessa", "Oh! Btdubs! I think Avery is gonna text you now!", "vanessa_dm")
    $ present_phone_choices([("I'll look", "I'll go check it out!", None)], "vanessa_dm") # EXAMPLE: Fake choice, basically force the user to click the message they want to send. You could do this for every message normally too that the user sends, if you want.
    
    # phone relevant! step three continued: we send more messages to the phone, this time sending some images!
    $ send_phone_message("Avery", "done working out!", "avery_dm")
    $ send_phone_message("Avery", "look at this cute photo i took while out!", "avery_dm")
    $ send_phone_message("Avery", "images/phone/media/run.png", "avery_dm", 2, summary_alt="Running Image") # EXAMPLE: Sending an image with a summary alt text.
    $ send_phone_message("Avery", "i'm so sweaty, but it was a good run!", "avery_dm")
    $ send_phone_message(phone_config["phone_player_name"], "Wow, nice!", "avery_dm")
    $ send_phone_message("Avery", "Want a workout pic? About to make food xx", "avery_dm")
    $ present_phone_choices([("Sure!", "Sure, send it!", Call("SendWorkout")), ("No thanks", "No thanks, I'm good.", Call("DontSendWorkout"))], "avery_dm") # EXAMPLE: Presenting choices that lead to different actions.
    $ send_phone_message("Avery", "oh ya im gonna add u to a group chat with vanessa", "avery_dm")
    $ send_phone_message("Avery", "kk?", "avery_dm")

    # phone relevant! step three continued: group chat time
    $ create_phone_channel("study_group", "Study Buddies", ["Vanessa", "Avery", phone_config["phone_player_name"]], "phone/icons/study_buddies.png", is_group=True) # EXAMPLE: Creating a group chat (of course, you can also do this before the phone's shown or in reset_phone_data, but this is just an example).
    $ send_phone_message("Vanessa", "Heyyy, I see you added me to the group chat!", "study_group")
    $ send_phone_message("Avery", "yep yep", "study_group")
    $ send_phone_message("Vanessa", "I love group chats, they're so fun!", "study_group")
    $ send_phone_message(phone_config["phone_player_name"], "i suppose so..", "study_group")
    $ send_phone_message(phone_config["phone_player_name"], "<emoji_dizzy>", "study_group", 3)
    $ send_phone_message(phone_config["phone_player_name"], "there's a lot to learn about how to use my new phone!", "study_group", 3)
    $ send_phone_message("Vanessa", "Don't worry, you'll get the hang of it!", "study_group")
    $ send_phone_message("Avery", "did you know you can move your phone around?", "study_group")
    $ send_phone_message("Avery", "like, you can change the position and size of it!", "study_group")

    # EXAMPLE: moving the phone around
    python:
        for i in renpy.store.range(20):
            phone_x += 0.015
            renpy.pause(0.01)
        renpy.pause(0.5)

    $ send_phone_message(phone_config["phone_player_name"], "oh, it's on the right now..", "study_group")
    $ send_phone_message("Vanessa", "watch out.. i'm gonna make it smaller now too!", "study_group")

    # EXAMPLE: changing the phone's size
    python:
        phone_zoom -= 0.3
        renpy.pause(0.5)

    $ send_phone_message("Avery", "now it's too small!!! let me put it back to normal", "study_group")

    # EXAMPLE: resetting the phone's size and position
    python:
        phone_zoom = 0.9
        phone_x = 0.5
        phone_y = 0.5
        renpy.pause(0.5)

    # phone relevant! step three continued: leaving and joining group chats
    $ send_phone_message("Avery", "pretend i get mad and storm off!!", "study_group")
    $ send_phone_message("Avery", "so i can show you how leaving and joining groups works", "study_group")
    $ send_phone_message("Avery", "dw im not actually mad at u guys lol", "study_group")
    $ remove_participant_from_group("study_group", "Avery") # EXAMPLE: Someone leaving a group chat.
    $ send_phone_message("Vanessa", "And... let me add her back!", "study_group")
    $ add_participant_to_group("study_group", "Avery", "Vanessa") # EXAMPLE: Someone joining a group chat, added by someone.
    $ send_phone_message("Vanessa", "Welcome back!", "study_group")
    $ send_phone_message("Avery", "i could've joined back myself y'know..", "study_group")
    $ remove_participant_from_group("study_group", "Avery")
    $ send_phone_message("Vanessa", "I guess she wants to show you what it looks like when someone joins on their own..", "study_group")
    $ add_participant_to_group("study_group", "Avery", None) # EXAMPLE: Someone joining a group chat, not added by anybody.
    $ send_phone_message("Vanessa", "Lastly, I'll show you how to hide, show, and delete chats.", "study_group")
    $ send_phone_message("Vanessa", "Let me switch you back to our chat.", "study_group")
    $ switch_channel_view("vanessa_dm") # EXAMPLE: Forcing the user to look in a channel.
    $ send_phone_message("Vanessa", "If you go back to the main menu, I'm going to hide and then show Avery's chat.", "vanessa_dm")
    $ switch_channel_view("channel_list") # EXAMPLE: Forcing the user to look at the channel list.
    $ hide_phone_channel("avery_dm") # EXAMPLE: Hiding a channel
    $ send_phone_message("Vanessa", "She's gone!", "vanessa_dm")
    $ switch_channel_view("channel_list") # Again just to make sure the user in the demo sees the channel appearing / vanishing..
    $ show_phone_channel("avery_dm") # EXAMPLE: Un-hiding a channel
    $ send_phone_message("Vanessa", "She's back!", "vanessa_dm")
    $ send_phone_message("Vanessa", "Now let's delete her channel...", "vanessa_dm")
    $ switch_channel_view("channel_list") # Again just to make sure the user in the demo sees the channel appearing / vanishing..
    $ delete_phone_channel("avery_dm") # EXAMPLE: Deleting (permanently) a channel.
    $ send_phone_message("Vanessa", "And.. that's all!", "vanessa_dm")

    # phone relevant! step four: we return back to the non-phone game dialogue, aka cleaning it all up~
    pause
    hide screen phone_ui
    $ phone_end()
    window show

    "And that concludes our demo with Vanessa and Avery!"
    "I hope the phone serves useful, please credit me, feel free to donate, and.. um.."
    "World peace?"
    "Oh- wait no, I mean, yes to that, but also, I meant to say show me what you make! I'll feature it and stuff!"
    "You can learn more about me and my contacts at https://luka.moe"
    "I'll probably have other Ren'Py stuff released too."
    "<3"
    return

# some demo labels, can ignore these as well~
label SendWorkout:
    $ send_phone_message("Avery", "images/phone/media/food.png", "avery_dm", 2, summary_alt="Workout Image")
    return

label DontSendWorkout:
    $ send_phone_message("Avery", "no worries!", "avery_dm")
    return
