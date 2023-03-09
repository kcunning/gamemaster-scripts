# Trying this again, with instructions from the docs

import fitz

fn = "GatewalkersPlayersGuide.pdf"

doc = fitz.open(fn)
print("Got doc", doc)

images = doc.extract_image()