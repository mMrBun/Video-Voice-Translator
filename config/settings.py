import os
import sys
# if you don't have local model please download model first, or use Helsinki-NLP/opus-mt-en-zh instead
EN_TO_ZH_MODEL_PATH = os.path.join(sys.path[0], "models", "opus-mt-en-zh")
project_config = {
    # launch mode
    'launch': 'cli'
}
