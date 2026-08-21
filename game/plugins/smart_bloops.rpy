init python:

    """
    ==== KNOWN LIMITATIONS OF THIS PLUGIN ====
    - Cannot use custom tag that starts {cps...
    
    === TO USE THIS PLUGIN ===
    1. either copy the below callback method or use it as a template for your own
    2. add the callback=(function name) argument to the character you want to add bloops to (example below)

    ========
    """

    renpy.music.register_channel(name='beeps', mixer='voice')

    def callback_ex(event, what, interact=True, **kwargs):
        if event == "show" or event == "show_done":
            file = "pc_bloop.ogg"
            bloop_len = 0.134
            queue_bloops(what, file, bloop_len)
        elif event == "slow_done" or event == 'done':
            renpy.sound.stop(channel="beeps")

    def queue_bloops(text, bloopfile, bloop_len):
        import re
        reg = r'{[^}]+}'
        tags = re.findall(reg, text)
       
        cps = preferences.text_cps
        if cps == 0:
            # if text is instant this is irrelevant
            # breaks our code anyways
            return

        spc = 1/cps # seconds per character
        speed_change_factor = 0.25 # if cps is sped up by 100%, the text bloop sound will be sped up by this percent.

        cur_char = 0
        inside_silence = False
        silence_time = 0
        bloop_time = 0
        spc_modded = [spc]

        for i in range(len(tags)):
            tag = tags[i]
            n = len([s for s in tags[:i+1] if s == tag])
            tag_loc = find_nth(text, tag, n)
            active_text = text[cur_char:tag_loc]

            # TODO: see if escape characters or other non-printing
            # characters are present in the text at this stage.
            # if so, they need to be stripped from active_text

            silence = active_text == "\u200B"

            if silence:
                if bloop_time > 0:
                    renpy.sound.queue(f"<from 0 to {bloop_len}>{bloopfile}", channel="beeps")
                    bloop_time = 0
                silence_time += spc_modded[-1] # silence is always one character
                renpy.sound.queue(f"<silence {silence_time}>", channel="beeps")
                silence_time = 0

            else:
                if silence_time > 0:
                    renpy.sound.queue(f"<silence {silence_time}>", channel="beeps")
                    silence_time = 0
                bloop_time += len(active_text)*spc_modded[-1]
                while bloop_time > bloop_len:
                    if spc_modded[-1] != spc:
                        # accelerated speed = faster bloops, slowed down = slower boops
                        speedup = (spc/spc_modded[-1] - 1) * speed_change_factor + 1  # scaling directly to cps change is too much
                        renpy.sound.queue(f"<from 0 to {bloop_len/speedup}>{bloopfile}", channel="beeps")
                        bloop_time -= bloop_len/speedup
                    else:
                        # default
                        renpy.sound.queue(bloopfile, channel="beeps")
                        bloop_time -= bloop_len

            cur_char = tag_loc + len(tag)

            # dealing with tags
            if tag == "{fast}" or tag == "{w}":
                # we can't handle these, just fail elegantly
                if bloop_time > 0:
                    renpy.sound.queue(f"<from 0 to {bloop_time}>{bloopfile}", channel="beeps")
                break

            elif re.match(r'{w[^}]+}', tag):
                # wait with specified time
                wait_time = tag[tag.find("=")+1:tag.find("}")]
                wait_time = float(wait_time)
                if bloop_time > 0:
                    renpy.sound.queue(f"<from 0 to {bloop_time}>{bloopfile}", channel="beeps")
                    bloop_time = 0
                silence_time += wait_time
                renpy.sound.queue(f"<silence {silence_time}>", channel="beeps")
                silence_time = 0

            elif re.match(r'{cps[^}]+}', tag):
                # modified speed, which we need to compensate for
                # open tag, specifically
                if "*" in tag:
                    mult = tag[tag.find("*")+1:tag.find("}")]
                    mult = 1/float(mult)
                    spc_modded.append(spc_modded[-1]*mult)
                else:
                    new_speed = tag[tag.find("=")+1:tag.find("}")]
                    new_speed = 1/float(new_speed)
                    spc_modded.append(new_speed)
            elif tag == "{/cps}":
                # closing cps tag
                spc_modded.pop()

                cur_char = tag_loc + len(tag)

        # clear out text after tags, if any.
        if cur_char < len(text):
            active_text = text[cur_char:]
            bloop_time += len(active_text)*spc_modded[-1]
            while bloop_time > bloop_len:
                renpy.sound.queue(bloopfile, channel="beeps")
                bloop_time -= bloop_len
            if bloop_time > 0:
                renpy.sound.queue(f"<from 0 to {bloop_time}>{bloopfile}", channel="beeps")

    def find_nth(haystack: str, needle: str, n: int) -> int:
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+len(needle))
            n -= 1
        return start
