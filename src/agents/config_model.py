"""
File: config_model.py
Project: adk-data-analytics
File Created: Wednesday, 7th May 2025
Author: Dinesh Selvaraj
-------------------------------------------------------------
Copyright 2025 Your Company LLC. This software is provided as-is, without
warranty or representation for any use or purpose. Your use of it is
subject to your agreement with Your Company.
"""

from google.genai import types

GEMINI_PRO_MODEL = "gemini-2.5-pro"
GEMINI_FLASH_MODEL = "gemini-2.5-flash"
GEMINI_LIVE_MODEL_1 = "gemini-2.0-flash-exp"
GEMINI_LIVE_MODEL_2 = "gemini-live-2.5-flash"
GEMINI_LIVE_MODEL_3 = "gemini-live-2.5-flash-preview-native-audio"

GEMINI_MODEL_TO_USE = GEMINI_FLASH_MODEL

GEMINI_LIVE_MODEL_TO_USE = GEMINI_LIVE_MODEL_3

APP_NAME = "test_app"

TEMPERATURE_GROUNDED = 0.1
TEMPERATURE_CREATIVE = 0.3
TOP_P = 0.95
SEED = 2

GEMINI_THINKING_CONFIG = types.ThinkingConfig(
  thinking_budget=256,
  include_thoughts=True
)

SAFETY_SETTINGS = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
]

GENERATE_CONTENT_CONFIG = types.GenerateContentConfig(
  temperature = TEMPERATURE_GROUNDED,
  top_p = TOP_P,
  seed = SEED,
  safety_settings = SAFETY_SETTINGS,
)

THINKING_CONFIG = types.ThinkingConfig(
  thinking_budget=0,
  include_thoughts=False
)
