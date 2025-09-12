import stanza

# List of languages (Stanza codes)
languages = {
    #"fr": "French",
    #"zh-hans": "Mandarin Chinese (Simplified)",
    #"es": "Spanish",
    #"de": "German",
    #"it": "Italian",
    #"ja": "Japanese",
    #"ru": "Russian",
    #"pt": "Portuguese",
    #"ko": "Korean",
    #"en": "English",
    #"ar": "Arabic"
}

# Download models
for lang in languages.keys():
    stanza.download(lang)
