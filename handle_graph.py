import array
import os
import subprocess
from PIL import Image

counter = 0

def generate_graph(paths):
  color = ""
  methods = []
  output = ""

  for path in paths:
    if path["method"] == "GET":
      color = " #ccddff"
    elif path["method"] == "POST":
      color = " #ffe6b3"
    elif path["method"] == "DELETE":
      color = " #ffcccc"

    # uml start
    output = output + "@startuml\n"
    output = output + "\nskinparam object {\n ArrowColor Black\n BorderColor black\n}\n"

    # setup objects
    output = output + "\n"
    output = output + "object " + path["method"] + color + "\n"
    output = output + path["method"] + " : " + path["endpoint"] + "\n"

    output = output + "\n"
    output = output + "object Params" + color + "\n"
    for param in path["params"]:
      output = output + "Params : " + param + "\n"

    output = output + "\n"
    output = output + "object " + path["handler"]["file"] + color + "\n"
    output = output + path["handler"]["file"] + " : " + path["handler"]["code"] + "\n"

    for sh in path["subhandlers"]:
      output = output + "\n"
      output = output + "object " + sh["file"] + color + "\n"
      output = output + sh["file"] + " : " + sh["code"] + "\n"

    # links
    output = output + "\n"
    output = output + path["method"] + " -> Params\n"
    output = output + "Params -> " + path["handler"]["file"] + "\n"
    output = output + path["handler"]["file"] + " -> " + path["subhandlers"][0]["file"] + "\n"

    i = 0
    j = len(path["subhandlers"])
    for sh in path["subhandlers"]:
      if sh != path["subhandlers"][0]:
        output = output + path["subhandlers"][i]["file"] + " -> " + sh["file"] + "\n"
        i = i + 1

    # uml end
    output = output + "\n"
    output = output + "@enduml\n"

    # file output
    f = open(path["method"] + ".txt", "w+")
    f.write(output)
    f.close()
    output = ""

    # external process call
    subprocess.call(["python", "-m", "plantuml", path["method"] + ".txt"])
    methods = methods + [path["method"]]

  # merge images
  imgs = [Image.open(m + ".png") for m in methods]
  widths, heights = zip(*(i.size for i in imgs))

  width = max(widths)
  height = sum(heights)

  new_img = Image.new('RGB', (width, height))

  y_offset = 0
  for i in imgs:
    new_img.paste(i, (0, y_offset))
    y_offset += i.size[1]

  new_img.save('graph.png')

  # remove generated files
  for m in methods:
    os.remove(m + ".png")
    os.remove(m + ".txt")







def test_graph():
  # test
  get_data = {
    "endpoint": "/example/:user_id",
    "method": "GET",
    "params": ["user_id"],
    "handler": {
        "file": "Example.js",
        "code": "console.log('Request to example!')"
    },
    "subhandlers": [
        {
            "file": "Backend.js",
            "code": "console.log('Request to backend!')"
        },
        {
            "file": "Database.js",
            "code": "console.log('Request to database!')"
        }
    ]
  }
  post_data = {
    "endpoint": "/example/:user_id",
    "method": "POST",
    "params": ["user_id"],
    "handler": {
        "file": "Example.js",
        "code": "console.log('Request to example!')"
    },
    "subhandlers": [
        {
            "file": "Backend.js",
            "code": "console.log('Request to backend!')"
        },
        {
            "file": "Database.js",
            "code": "console.log('Request to database!')"
        }
    ]
  }
  delete_data = {
    "endpoint": "/example/:user_id",
    "method": "DELETE",
    "params": ["user_id"],
    "handler": {
        "file": "Example.js",
        "code": "console.log('Request to example!')"
    },
    "subhandlers": [
        {
            "file": "Backend.js",
            "code": "console.log('Request to backend!')"
        },
        {
            "file": "Database.js",
            "code": "console.log('Request to database!')"
        }
    ]
  }
  generate_graph([get_data, post_data, delete_data])

#test_graph()