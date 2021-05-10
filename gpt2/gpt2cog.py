import gpt2simple as gpt2
import os
import requests
import discord
from discord.ext import commands

class GPT2Discord(commands.Cog, name='GPT2Discord Module'):
  """ 
  *Work in progress!*
  Hey, how does python docstring works?? 
  """
  def __init__(self):
    super().__init__()
    # self.bot = bot
    self.selected_model = None
    self._available_models = ["124M", "355M"]
    self.tf_instance = gpt2.start_tf_sess()

  @commands.is_owner()
  @commands.command(name="install_model")
  async def select_or_install_model(self, ctx: commands.Context, select_model):
    """Selects & Installs a gpt-2 model from the `gpt_2_simple` library"""
    if (not(select_model in self._available_models)):
      __local_var = "".join(self._available_models)
      ctx.send(f"Model {select_model} invalid. Valid models are {__local_var}.")
      return
    ctx.send(f"Model {select_model} selected.")
    self.selected_model = select_model

    if not os.path.isdir(os.path.join("models", self.selected_model)):
      ctx.send("Installing model will take some time, depending on the server. The bot (should) not block incoming commands.")
      gpt2.download_gpt2(model_name=self.selected_model)   # model is saved into current directory under /models/124M/
    else:
      ctx.send("Model is already installed!")

  @commands.is_owner()
  @commands.command(name="install_dataset")
  async def install_dataset(self, ctx: commands.Context, url, filename, steps=1000):
    """If you're fancy and want to wallpost the ai. [url] [filename]"""
    if not self.selected_model:
      ctx.send("Install a model first!")
      return
    if not url or not filename:
      ctx.send("URL (first param) and filename (second param) is needed.")
      return
    if not steps:
      steps = 1000
    if not os.path.isfile(filename):
      ctx.send("Downloading {url}.")
      data = requests.get(url)
      ctx.send("Downloading done, caching data for later use")
      with open(filename, 'w') as f:
        f.write(data.text)
    else:
      ctx.send("Data already installed.")
    ctx.send("Running gpt2.finetune")
    gpt2.finetune(self.tf_instance, filename, int(steps), self.selected_model) 
    ctx.send("Finetuning done!")
    return True

  @commands.command(name="generate")
  async def shitpost(self, ctx: commands.Context, length = 1023, seed=None):
    """Let the ai throw out some gibberish. First param is length"""
    
    out = gpt2.generate(self.tf_instance, length = int(length), return_as_list=True, seed=seed)[0]
    ctx.send(out)
