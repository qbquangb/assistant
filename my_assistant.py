import speech_recognition
import pyttsx3
from gtts import gTTS
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
import os
import pygame
import re

def say(robot_brain):
	tts = gTTS(text = robot_brain, lang="vi")
	# Dừng phát nhạc và giải phóng tài nguyên trước khi xóa tệp
	pygame.mixer.music.stop()
	pygame.mixer.quit()
	if os.path.exists("robot_brain.mp3"):
		os.remove("robot_brain.mp3")
	tts.save("robot_brain.mp3")
	pygame.mixer.init()
	pygame.mixer.music.load("robot_brain.mp3")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		continue

def convert(text):
	# Loại bỏ các tiêu đề (ví dụ: #, ##)
	text = re.sub(r'^#+\s', '', text, flags=re.MULTILINE)

	# Loại bỏ các ký tự đánh dấu in đậm và in nghiêng (*, **)
	text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
	text = re.sub(r'\*(.*?)\*', r'\1', text)

	# Loại bỏ tất cả các dấu *
	text = text.replace('*', '')

	# ... (thêm các quy tắc loại bỏ khác tùy thuộc vào cấu trúc Markdown) ...
	return text

generation_config = GenerationConfig(
	temperature=0.7,
	max_output_tokens=300
)

# Lấy API key từ biến môi trường
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
	raise ValueError("GOOGLE_API_KEY environment variable not set.")

# Cấu hình SDK với API key
genai.configure(api_key=api_key)

# Chọn mô hình (ví dụ: gemini-1.5-flash)
# Bạn có thể tìm danh sách các mô hình có sẵn trong tài liệu của Google
model = genai.GenerativeModel('gemini-1.5-flash-latest') # Hoặc 'gemini-1.0-pro', 'gemini-pro'

robot_ear = speech_recognition.Recognizer()
robot_brain = ""
pygame.mixer.init()

while True:
	with speech_recognition.Microphone() as mic:
		print("Robot: Tôi đang nghe bạn nói...")
		audio = robot_ear.listen(mic)

	try:
		you = robot_ear.recognize_google(audio, language="vi-VN")
	except:
		you = ""

	print("You: " + you)

	print("Robot: ...")
	chat = model.start_chat(history=[])
	
	if "bye" in you or "tạm biệt" in you:
		try:
			robot_brain = chat.send_message(you, generation_config=generation_config)
			robot_brain = robot_brain.text
			robot_brain = convert(robot_brain)
		except:
			robot_brain = "Tạm biệt bạn, hẹn gặp lại lần sau."
		print("Robot: " + robot_brain)
		say(robot_brain)
		break
	elif you == "":
		robot_brain = "Tôi không nghe bạn nói, hãy thử lại."
		print("Robot: " + robot_brain)
		say(robot_brain)
		continue
	try:
		robot_brain = chat.send_message(you, generation_config=generation_config)
		robot_brain = robot_brain.text
		robot_brain = convert(robot_brain)
	except:
		robot_brain = "Tôi đang bận, vui lòng thử lại sau."

	print("Robot: " + robot_brain)

	say(robot_brain)
	

# from google import genai
# from google.genai.types import (
#     FunctionDeclaration,
#     GenerateContentConfig,
#     GoogleSearch,
#     HarmBlockThreshold,
#     HarmCategory,
#     MediaResolution,
#     Part,
#     Retrieval,
#     SafetySetting,
#     Tool,
#     ToolCodeExecution,
#     VertexAISearch,
# )

# import os

# PROJECT_ID = "[your-project-id]"  # @param {type: "string", placeholder: "[your-project-id]", isTemplate: true}
# if not PROJECT_ID or PROJECT_ID == "[your-project-id]":
#     PROJECT_ID = str(os.environ.get("GOOGLE_CLOUD_PROJECT"))

# LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "global")

# client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# API_KEY = ""  # @param {type: "string", placeholder: "[your-api-key]", isTemplate: true}

# if not API_KEY or API_KEY == "[your-api-key]":
#     raise Exception("You must provide an API key to use Vertex AI in express mode.")

# client = genai.Client(vertexai=True, api_key=API_KEY)

# MODEL_ID = "gemini-2.0-flash-001"  # @param {type: "string"}

# response = client.models.generate_content(
#     model=MODEL_ID, contents="hôm nay là ngày 21 tháng 5 năm 2025"
# )

# print(response.text)


# import google.generativeai as genai
# from google.generativeai.types import GenerationConfig
# import os

# generation_config = GenerationConfig(
# 	temperature=0.7,
# 	max_output_tokens=200
# )

# # Lấy API key từ biến môi trường
# api_key = os.getenv("GOOGLE_API_KEY")

# if not api_key:
# 	raise ValueError("GOOGLE_API_KEY environment variable not set.")

# # Cấu hình SDK với API key
# genai.configure(api_key=api_key)

# # Chọn mô hình (ví dụ: gemini-1.5-flash)
# # Bạn có thể tìm danh sách các mô hình có sẵn trong tài liệu của Google
# model = genai.GenerativeModel('gemini-1.5-flash-latest') # Hoặc 'gemini-1.0-pro', 'gemini-pro'

# try:
# 	# # Gửi một prompt đơn giản
# 	# prompt = "thông tin về thành phố đà nẵng, việt nam"
# 	# response = model.generate_content(prompt)

# 	# # In kết quả
# 	# print(response.text)

# 	# Ví dụ cho chat (hội thoại)
# 	chat = model.start_chat(history=[])

# 	response = chat.send_message("Tôi muốn biết thông tin về thành phố đà nẵng", generation_config=generation_config)
# 	print(response.text)

# except Exception as e
# 	print(f"An error occurred: {e}")
# 	if hasattr(e, 'response') and e.response: # Lỗi từ API
# 		print(f"API Error Details: {e.response}")
# 	# Một số lỗi phổ biến:
# 	# - google.api_core.exceptions.PermissionDenied: 403 API key not valid. Please pass a valid API key.
# 	#   (Kiểm tra lại API key, hoặc có thể bạn chưa bật API cho dự án nếu dùng Google Cloud project)
# 	# - google.api_core.exceptions.InvalidArgument: 400 Request payload is invalid.
# 	#   (Kiểm tra lại cấu trúc prompt hoặc các tham số gửi đi)