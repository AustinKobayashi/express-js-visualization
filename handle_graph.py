import array
import os
from os import path
import subprocess
from PIL import Image

counter = 0

def generate_graph(nodes):
  global counter

  color = ""
  output = ""

  for n in nodes:
    # set color
    if n["method"] == "GET":
      color = " #ccddff"
    elif n["method"] == "POST":
      color = " #ffe6b3"
    elif n["method"] == "DELETE":
      color = " #ffcccc"

    # uml start
    output = output + "@startuml\n"
    output = output + "\nskinparam object {\n ArrowColor Black\n BorderColor black\n}\n"

    # setup objects
    output = output + "\n"
    output = output + "object " + n["method"] + color + "\n"
    output = output + n["method"] + " : " + n["endpoint"] + "\n"

    output = output + "\n"
    output = output + "object Params" + color + "\n"
    for param in n["params"]:
      output = output + "Params : " + param + "\n"

    output = output + "\n"
    output = output + "object " + n["handler"]["file"] + color + "\n"
    codes = n["handler"]["code"].split('\n')
    for c in codes:
      if c != "":
        output = output + n["handler"]["file"] + " : " + c + "\n"

    i = 1
    for sh in n["subhandlers"]:
      output = output + "\n"
      output = output + "object " + str(i) + "." + sh["file"] + color + "\n"
      codes = sh["code"].split('\n')
      for c in codes:
        if c != "":
          output = output + str(i) + "." + sh["file"] + " : " + c + "\n"
      i = i + 1

    # links
    output = output + "\n"
    output = output + n["method"] + " -> Params\n"
    output = output + "Params -> " + n["handler"]["file"] + "\n"
    if len(n["subhandlers"]) != 0:
      output = output + n["handler"]["file"] + " -> 1." + n["subhandlers"][0]["file"] + "\n"

    i = 1
    j = len(n["subhandlers"])
    for sh in n["subhandlers"]:
      if sh != n["subhandlers"][0]:
        output = output + str(i) + "." + n["subhandlers"][i - 1]["file"] + " -> " + str(i + 1) + "." + sh["file"] + "\n"
        i = i + 1

    # uml end
    output = output + "\n"
    output = output + "@enduml\n"

    # file output
    f = open(str(counter) + ".txt", "w+")
    f.write(output)
    f.close()
    output = ""

    try:
      # external process call
      subprocess.call(["python", "-m", "plantuml", str(counter) + ".txt"])

      # merge images
      if path.exists("graph.png"):
        imgs = [Image.open(m + ".png") for m in ["graph", str(counter)]]
      else:
        imgs = [Image.open(str(counter) + ".png")]
      widths, heights = zip(*(i.size for i in imgs))

      width = max(widths)
      height = sum(heights)

      new_img = Image.new('RGB', (width, height))

      y_offset = 0
      for i in imgs:
        new_img.paste(i, (0, y_offset))
        y_offset += i.size[1]

      new_img.save('graph.png')
    except:
      print("Could not generate graph for " + n["method"])

    counter = counter + 1

  # remove generated files
  for i in range(0, counter):
    os.remove(str(i) + ".png")
    #os.remove(m + ".txt")
