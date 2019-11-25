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

  # remove existing graph
  if path.exists("graph.png"):
    os.remove("graph.png")

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

    if len(n["params"]) != 0:
      output = output + "\n"
      output = output + "object Params" + color + "\n"
      for param in n["params"]:
        output = output + "Params : " + param + "\n"

    if len(n["handler"]["body"]) != 0:
      output = output + "\n"
      output = output + "object Body" + color + "\n"
      for b in n["handler"]["body"]:
        output = output + "Body : " + b + "\n"

    output = output + "\n"
    output = output + "object " + n["handler"]["file"] + color + "\n"
    codes = n["handler"]["code"].split('\n')
    for c in codes:
      if c != "":
        new_c = c #.replace("  ", "\\t")
        output = output + n["handler"]["file"] + " : |" + new_c + "\n"

    i = 1
    for sh in n["subhandlers"]:
      output = output + "\n"
      output = output + "object " + str(i) + "." + sh["file"] + color + "\n"
      codes = sh["code"].split('\n')
      for c in codes:
        if c != "":
          new_c = c #.replace("  ", "\\t")
          output = output + str(i) + "." + sh["file"] + " : |" + new_c + "\n"
      i = i + 1

    # links
    output = output + "\n"
    if len(n["params"]) != 0:
      output = output + n["method"] + " -> Params\n"
    elif len(n["handler"]["body"]) != 0:
      output = output + n["method"] + " -> Body\n"
    else:
      output = output + n["method"] + " -> " + n["handler"]["file"] + "\n"
    if len(n["params"]) != 0:
      output = output + "Params -> Body\n"
    if len(n["handler"]["body"]) != 0:
      output = output + "Body -> " + n["handler"]["file"] + "\n"
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
      subprocess.call(["java", "-DPLANTUML_LIMIT_SIZE=8192", "-jar", "plantuml.jar", str(counter) + ".txt"])

      # merge images
      if path.exists("graph.png"):
        imgs = [Image.open(img) for img in ["graph.png", str(counter) + ".png"]]
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
  try:
    for i in range(0, counter):
      os.remove(str(i) + ".png")
      os.remove(str(i) + ".txt")
  except:
    print("Could not remove generated files")

  graph = Image.open('graph.png')
  graph.show()

  print("Done")
