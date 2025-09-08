import stanza

# List of languages (Stanza codes)
languages = {
    #"fr": "French",
    #"zh": "Mandarin Chinese",
    #"es": "Spanish",
    #"de": "German",
    #"it": "Italian",
    #"ja": "Japanese",
    #"ru": "Russian",
    #"pt": "Portuguese",
    #"ko": "Korean",
    "en": "English"
}

# Download models
for lang in languages.keys():
    stanza.download(lang)
