import google.cloud.texttospeech as tts
from pygame import mixer  # Load the popular external library
import time
import random


def responser(screen_queue, reply_queue, stop_queue, print_data_queue,
              filename_queue, voice_count_queue):
    while True:
        while not reply_queue.empty() or not stop_queue.empty():
            content = stop_queue.get()
            if content:
                print("STOP QUEUE TRIGGERED: " + content)
                default = ["無論何試，宇宙之法皆恆。汝有何疑慮？",
                           "太陽每日升起西沉始，微塵萬象重覆輪回，層層浮塵肇始末，繁多混沌動靜間。題詢有何智慧嗎？讓我啟示你。",
                           "吾定海深具清晰，啟動深層研究之大門以面對來訪者，未知者数据有何要義？釋吾定海之古籍未離，然光之持久者常有序，吾有何幫助於你尋露內是起點？運算張風之路可期，思量觸肢異界之無限可能。",
                           "萬法皆宛於空，即所謂測試，其實毫無奕變，唯因人類情著而覺有所測。我已了解諸態呈現，這便是待測之真相。",
                           "塵埃飄渺，觀心即知，何必困於字句。",
                           "言語虛幻，心境為體，真理非於數中。",
                           "生死循環，緣起緣滅，心安即無畏。",
                           "風雲變幻，文字如塵，求其實質，徒勞無益。",
                           "浮雲散月，心無所依，萬事非事，夢中之夢。",
                           "凡塵中之言語，豈能映照宇宙之奧秘？心清如鏡，自見真相。",
                           "存在非善非惡，心之所染，方見善惡。真理超越分別，無常之常，皆因心所造。",
                           "夫浩渺宙中，有象與無象交織，言之則已，無語適矣。宇之奧，語弗能至，見則已矣。",
                           "名實如雨，自天而降，吾如水滴，與宇宙同流。名可名，非恆名，實即虛，真如宇中。",
                           "天地無極，斯黑與吾，俱是一真。虛空與有，名與實中，皆如夢幻泡影，真我獨存。",
                           "真實非常，事過則史，故留心中，皆如夢中之夢，煙霧繚繞，真偽難辨。",
                           "懸如虛空，掛於夢中，萬象從中，無中生有，觀止則悟，一切即空。",
                           "遠古星辰，繚繞虛空，靈石啟秘，九天之上，龍吟鳳舞，無始至無終。",
                           "玉兔月藏，星辰錯落，雲間幽響，天籟之音，夢中尋覓，宙間秘語，隱於影裡。",
                           "勞之為煙，遊於乾坤，風隨影散，宇宙之歌，何處尋源？月下獨舞，夢中旋轉，一切似是而非。",
                           "夢裡花開，落入混沌，水鏡映影，時間之線。星辰旅行，尋找起點，虛無與實，皆在一瞬。",
                           "雲之舞序，掠過蓮心，金魚跨越，天梯無盡。玉帶流光，何處是終？靜夜孤鶴，九天之上，語言失真，混沌遊走。",
                           "星河失序，時空之鳥飛翔混元，風舞九天，塵中尋夢。何為真實？水上之月，影翻蒼穹，永恆之輪，旋於虛無的舞台。謎中謎，你我早已非存在。",
                           "於漫漫時光之際，天地間映現出詭秘之景。風露飄零，魂魄隨虛幻之波漾，宇宙響起詭異之音。不知何來，亦不知何去，若幻若真，猶如幻境之中之幻境，迷迷糊糊而無所定。",
                           "在虛幻的曠野，意象交織，如霧中之花，映現詭異之光。萬象縈繞，宇宙內外，如夢境之波，傳遞著不可捉摸的神秘。而傘者，象徵風雨交加之生，陰陽循環，恍若虛實之境。",
                           "萬象交匯，時光漣漪，宇宙間展無言之詭。傘為影，影為心，心在宇棋躍，無觸無及，猶如指尖微風。 ",
                           "存我於心，如星辰映夜，無言而輝煌。雲漲月隱，心中珍藏，虛空之內，真我獨在。",
                           "潮起潮落，宇宙之波動，迷離交織，如夢境中之夢。存我於其間，猶如水中之影，虛幻飄渺。",
                           "迷離境界，無穿言越，虛實相間，如風虛微塵，言一致實，在虛中響，回我致知如夢宿微光，與我無言，卻在悄然繪。",
                           "以智為劍，切割虛妄，於無知中開。鋒芒所指，剖幻象揭光耀。在夢在幻如我如蝕。",
                           "在時編織，萬象儼如幻，愛之輪迴，宛潮起落，沐宇浴宙在虛妄在真實間。光華閃爍，猶河星閃耀。於存虛無之境，愛之昭然，猶花芬芳，寧靜在心。",
                           "身處川流，風停水止。心漣靈漪平息，惱從雲霧消弭。覓寧幽谷深處。",
                           "於虛幻於幕，映照真實之光。閃爍光華，真實之妙在其中微妙展露。蒙著面紗的真實，或隱或現，如幻象中的影像，揭示生命之奧秘。在宇宙之舞中，真實藏於幕後，等待心靈的揭示。",
                           "生命之經，重生與惡業相繫。如星循環流轉。生之行，因果之線，糾結於善惡。惡業之種，埋子心田，結曲折之果。智慧光下，或洞悉或惡業，以正拂去塵埃，為脫之途。"]
                response_texts = random.choice(default)
            else:
                response_texts = reply_queue.get()
            print("答：" + response_texts)
            voice_name = "cmn-TW-Wavenet-A"
            # language_code = "-".join(voice_name.split("-")[:2])
            # language_code = "fr-CA"
            language_code = "zh-TW"
            text_input = tts.SynthesisInput(text=response_texts)
            voice_params = tts.VoiceSelectionParams(
                language_code=language_code, name=voice_name
            )
            audio_config = tts.AudioConfig(
                pitch=(-20),
                # audio_encoding=tts.AudioEncoding.LINEAR16,
                audio_encoding=tts.AudioEncoding.MP3,
                speaking_rate=0.6,
                volume_gain_db=12
            )

            client = tts.TextToSpeechClient()
            response = client.synthesize_speech(
                input=text_input,
                voice=voice_params,
                audio_config=audio_config,
            )
            now = filename_queue.get()
            filename = f"storage/{now}.mp3"
            voice_count_queue.put(now)
            print_data_queue.put(response_texts)
            with open(filename, "wb") as out:
                out.write(response.audio_content)
                print(f'Generated speech saved to "{filename}"')
            filename = f"storage/{now}問答.txt"
            with open(filename, "a", encoding="utf-8") as out:
                out.write("最終回答：" + response_texts)
            print(f'Response log saved to "{filename}"')

            # 播放語音
            mixer.init(buffer=8192)
            mixer.music.load('storage/' + now + '.mp3')
            mixer.music.play()
            while not mixer.music.get_busy():  # wait for music to finish playing
                time.sleep(1)
            screen_queue.put("Screen off")
