import os
import re
import io
import discord
import mp3
from discord.ext import commands
from discord.ext import voice_recv
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
load_dotenv()

class Nathan(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.recognizer = sr.Recognizer()

    async def on_ready(self):
        print(f"Logged in as {self.user}.")
        await self.change_presence(activity=discord.Game(name="Root"))

    async def on_command_error(self, ctx, error):
        print("")
    
    def init_commands(self):
        @self.command(name='join')
        async def join(ctx):
            def callback(user, data: voice_recv.VoiceData):
                audio_buffer = io.BytesIO()

                encoder = mp3.Encoder(audio_buffer)
                encoder.set_bit_rate(64)
                encoder.set_sample_rate(44100)
                encoder.set_channels(2)
                encoder.set_quality(5)   # 2-highest, 7-fastest
                encoder.set_mode(mp3.MODE_STEREO)

                encoder.write(data.pcm)
                encoder.flush()
                audio_buffer.seek(0)

                print(sr.AudioFile(audio_buffer))
                with sr.AudioFile(audio_buffer) as source:   
                    audio = self.recognizer.record(source)
                try:
                    words = self.recognizer.recognize_whisper(audio, language="en").lower()
                    print(words)
                    ls = re.findall("\\w*(?:er)\\b", words) # "\\w*(?:er|r|re)\\b"
                    if(len(ls) > 0):
                        print(f"{ls[-1]}? I hardly know her!")
                        tts = gTTS(text=f"{ls[-1]}? I hardly know her!", lang='en')
                        audio_buffer = io.BytesIO()
                        tts.write_to_fp(audio_buffer)
                        audio_buffer.seek(0)

                        vc.play(discord.FFmpegPCMAudio(source=audio_buffer, pipe=True))
                except sr.UnknownValueError:
                    print("couldn't understand")
                except sr.RequestError as e:
                    print(f"couldn't request, {e}")
                except:
                    exit(1)

            voice = ctx.author.voice
            if(voice == None):
                await ctx.send("You need to be in a voice channel.")
                return

            await ctx.send("Listening!")
            vc = await voice.channel.connect(cls=voice_recv.VoiceRecvClient)
            vc.listen(voice_recv.BasicSink(callback))

        @self.command(name="stop")
        async def stop(ctx):
            if(self.vc == None):
                await ctx.send("Not currently in a call.")
                return

            await ctx.send("Stopping playback.")
            await self.vc.disconnect()
    
    def start_bot(self, token):
        self.init_commands()
        self.run(token)

def main():
    token = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents(messages=True, message_content=True, guilds=True, voice_states=True)
    bot = Nathan(command_prefix="!", intents=intents)

    bot.start_bot(token)

if __name__ == "__main__":
    main()