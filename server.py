import streamlit as st
import pandas as pd
import openai
import io
import re
import os
from docx import Document

# Set page config for tech/futuristic theme
st.set_page_config(
	page_title="AI Server Log Agent",
	page_icon="🖥️",
	layout="wide",
	initial_sidebar_state="expanded"
)

# Custom CSS for tech/futuristic look
st.markdown(
	"""
	<style>
	body {
		background: linear-gradient(135deg, #232526 0%, #414345 100%);
		color: #fff;
	}
	.stApp {
		background-image: url('https://wallpaperbat.com/img/41625311-datacenter-wallpaper-for-desktop-free.jpg');
		background-size: cover;
		background-repeat: no-repeat;
		background-attachment: fixed;
	}
	.stButton>button {
		background-color: #222;
		color: #fff;
		border-radius: 8px;
		border: 1px solid #00ffe7;
		padding: 0.7em 1.2em;
		font-size: 1.1em;
	}
	.stTextInput>div>input {
		background-color: #222;
		color: #fff;
		font-size: 1em;
	}
	.center-title {
		display: flex;
		justify-content: center;
		align-items: center;
		text-align: center;
		margin-top: 30px;
		margin-bottom: 10px;
		color: #fff;
		font-size: 2.2rem;
		font-weight: bold;
		letter-spacing: 2px;
		text-shadow: 0 2px 8px #232526;
	}
	.subtitle {
		text-align: center;
		color: #fff;
		font-size: 1.65rem;
		margin-bottom: 30px;
		white-space: normal;
		overflow: visible;
		text-overflow: unset;
		max-width: 98vw;
		margin-left: auto;
		margin-right: auto;
	}
	.white-text {
		color: #fff !important;
	}
	/* Responsive styles */
	@media (max-width: 900px) {
		.center-title {
			font-size: 1.5rem;
		}
		.subtitle {
			font-size: 1.1rem;
			padding: 0 8px;
		}
	}
	@media (max-width: 600px) {
		.center-title {
			font-size: 1.1rem;
			margin-top: 18px;
		}
		.subtitle {
			font-size: 0.98rem;
			margin-bottom: 18px;
			padding: 0 4px;
		}
		.stButton>button {
			font-size: 1em;
			padding: 0.6em 1em;
		}
		.stTextInput>div>input {
			font-size: 0.98em;
		}
		/* Make all custom containers full width on mobile */
		div[style*="background: rgba(34,34,34"] {
			max-width: 98vw !important;
			width: 98vw !important;
			font-size: 0.97em !important;
			padding-left: 2vw !important;
			padding-right: 2vw !important;
		}
	}
	</style>
	""",
	unsafe_allow_html=True
)



st.markdown('<div class="center-title">🖥️ AI Server Log Agent</div>', unsafe_allow_html=True)
st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Intelligent server analysis engineered to streamline debugging workflows.</div>', unsafe_allow_html=True)
st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)


# Load OpenAI API key from secrets.toml

# Use Streamlit Cloud secrets management
openai_api_key = st.secrets.get("OPENAI_API_KEY", "")



# Add visible instruction above uploader
st.markdown(
	'''<div style="background: rgba(34,34,34,0.7); padding: 12px 0; border-radius: 8px; text-align: left; margin-bottom: 10px; color: #fff; font-size: 1.1rem; font-weight: 500; width: 420px; max-width: 90%; margin-left: 0;">Upload your server error log to begin analysis.</div>''',
	unsafe_allow_html=True
)
uploaded_file = st.file_uploader(" ", type=["txt", "log", "docx"], key="log_file_uploader")
log_content = None
if uploaded_file is not None:
	file_name = uploaded_file.name.lower()
	if file_name.endswith('.docx'):
		# Read docx file
		doc = Document(uploaded_file)
		log_content = '\n'.join([para.text for para in doc.paragraphs])
	else:
		# Read as text
		log_content = uploaded_file.read().decode("utf-8")


	# Show success message in a box that covers the file info
	themed_file_message = f"<span style='color:#00ffe7;'>Log file received: <b>{uploaded_file.name}</b> ({round(uploaded_file.size/1024, 1)} KB)</span>"
	st.markdown(
		'<div style="position: relative; width: 340px; height: 38px; margin-bottom: 10px; margin-top: -60px;">'
		'<div style="background: #000; color: #00ff6a; padding: 12px 18px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 500; width: 340px; height: 38px; position: absolute; top: 0; left: 0; z-index: 2;">Log file uploaded successfully!</div>'
		# File info is hidden underneath
		f'<div style="color: #00ffe7; font-size: 1.01rem; width: 340px; height: 38px; position: absolute; top: 0; left: 0; z-index: 1; opacity: 0;">{themed_file_message}</div>'
		'</div>',
		unsafe_allow_html=True
	)

	# Add spacing and transparent background to log preview
	st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
	st.markdown(
		f'<div style="background: rgba(34,34,34,0.7); color: #00ffe7; padding: 12px 16px; border-radius: 8px; font-family: monospace; font-size: 1.01rem; margin-bottom: 10px;">{log_content[:2000].replace(chr(10), "<br>")}</div>',
		unsafe_allow_html=True
	)

	# Analyze log with OpenAI
	if openai_api_key:
		openai.api_key = openai_api_key
		st.markdown('<div style="height: 44px;"></div>', unsafe_allow_html=True)
		if st.button("Analyze Log with AI"):
			# Custom spinner with theme color
			spinner_html = '''
			<div style="display: flex; align-items: center; margin-bottom: 16px;">
				<svg width="28" height="28" viewBox="0 0 50 50" style="margin-right: 10px;"><circle cx="25" cy="25" r="20" fill="none" stroke="#00ffe7" stroke-width="5" stroke-linecap="round" stroke-dasharray="31.415, 31.415" transform="rotate(72.0001 25 25)"><animateTransform attributeName="transform" type="rotate" from="0 25 25" to="360 25 25" dur="1s" repeatCount="indefinite"/></circle></svg>
				<span style="color: #00ffe7; font-size: 1.08rem; font-weight: 500;">Analyzing log with OpenAI...</span>
			</div>
			'''
			st.markdown(spinner_html, unsafe_allow_html=True)
			# Removed default st.spinner to avoid duplicate spinners
			try:
				response = openai.chat.completions.create(
					model="gpt-4",
					messages=[
						{"role": "system", "content": (
							"You are an expert server log analyst. "
							"Given a server error log, always respond in the following format and requirements: "
							"\n\n1. An initial short inference (1-2 sentences) about what is most likely causing the error, labeled 'Inference'. This section must always be present and non-empty. "
							"\n2. A bulleted list of at least 3 actionable troubleshooting steps (label this section 'Troubleshooting Steps'). Each step should be clear, specific, and directly related to resolving the error. "
							"\n3. A separate bulleted list of at least 3 recommended Linux commands for debugging or analysis (label this section 'Suggested Linux Commands'). For each command, provide the command itself in bold or code formatting, followed by a short explanation (one sentence) of what the command does and why it is useful for this situation. If you cannot find 3 relevant commands, provide the most useful general Linux diagnostic commands with explanations. "
							"\nUse clear section headers and bullet points. If you cannot find troubleshooting steps, infer possible causes and still provide actionable advice."
						)},
						{"role": "user", "content": log_content[:4000]}
					],
					max_tokens=1200
				)
				ai_result = response.choices[0].message.content
				st.markdown(
					"""
					<div style='background: rgba(34,34,34,0.85); border-radius: 8px; padding: 14px 18px 10px 18px; margin-bottom: 12px; display: inline-block;'>
						<span style='font-size:1.25rem; color:#00ffe7; font-weight:600;'>AI Recommendations</span>
					</div>
					""",
					unsafe_allow_html=True
				)

				# Improved extraction logic
				inference = ""
				steps = []
				commands = []
				in_inference = False
				in_steps = False
				in_cmds = False
				for line in ai_result.split('\n'):
					l = line.strip()
					# Section headers
					if re.match(r'(?i)inference', l):
						in_inference = True
						in_steps = False
						in_cmds = False
						continue
					if re.match(r'(?i)troubleshooting steps', l):
						in_inference = False
						in_steps = True
						in_cmds = False
						continue
					if re.match(r'(?i)suggested linux commands', l):
						in_inference = False
						in_steps = False
						in_cmds = True
						continue
					# Collect inference (first non-empty line after header)
					if in_inference and l:
						if not inference:
							inference = l
					# Collect steps (bulleted only)
					elif in_steps and re.match(r'^[-*•]', l):
						steps.append(l.lstrip('-*•').strip())
					# Collect commands (bulleted or code)
					elif in_cmds and (re.match(r'^[-*•]', l) or re.match(r'^\$?\s*(sudo |apt-get |systemctl |journalctl |ls |cat |grep |tail |service |docker |kubectl|df |du |ps |top |htop |dmesg |netstat |ss |ping |traceroute |uptime |free |vmstat |lsof |strace )', l)):
						commands.append(l.lstrip('-*•').strip())

				# Fallback: if no steps found, try to extract any actionable advice
				if not steps:
					for line in ai_result.split('\n'):
						if re.search(r'(check|try|ensure|verify|restart|review|investigate|analyze|look for|consider|possible cause|possible solution|actionable)', line, re.I):
							steps.append(line.strip())

				# Show inference
				# Always show three sections
				# Ensure at least one inference is shown
				shown_inference = inference if inference else "No clear root cause was identified, but please review the troubleshooting steps and commands below for further investigation."
				st.markdown(f"<div style='background: rgba(34,34,34,0.7); color: #00ffe7; padding: 10px 16px; border-radius: 8px; font-size: 1.08rem; margin-bottom: 10px;'><b>Inference:</b> {shown_inference}</div>", unsafe_allow_html=True)

				st.markdown("<div style='background: rgba(34,34,34,0.7); color: #00ffe7; padding: 10px 16px; border-radius: 8px; font-size: 1.08rem; margin-bottom: 10px;'><b>Troubleshooting Steps:</b><ul style='margin-bottom:0;'>" + (''.join([f"<li style='margin-bottom:4px'>{step}</li>" for step in steps[:3]]) if steps else "<li>No troubleshooting steps found.</li>") + "</ul></div>", unsafe_allow_html=True)

				# Ensure at least 3 commands if possible
				if len(commands) < 3:
					# Add generic diagnostic commands with explanations if not enough found
					generic_cmds = [
						("dmesg | tail -20", "Shows the last 20 kernel log messages, useful for diagnosing hardware or driver issues."),
						("journalctl -xe", "Displays recent systemd journal entries, helpful for finding recent errors and warnings."),
						("systemctl status", "Shows the status of all systemd services, useful for checking if critical services are running."),
						("cat /var/log/syslog | tail -20", "Displays the last 20 lines of the syslog, which may contain relevant error messages."),
						("df -h", "Shows disk space usage in human-readable format, useful for checking if the disk is full."),
						("free -m", "Displays memory usage in megabytes, helpful for identifying memory exhaustion issues."),
						("ps aux | grep -i error", "Searches running processes for the word 'error', which may indicate failing processes."),
						("ls -l /var/log/", "Lists log files in /var/log, useful for finding additional logs to investigate.")
					]
					for cmd, expl in generic_cmds:
						# Only add if not already present (by command substring)
						if not any(cmd in c for c in commands):
							commands.append(f"{cmd} -- {expl}")
						if len(commands) >= 3:
							break
				# Parse commands for explanations if present
				def split_cmd_expl(cmd):
					if ' -- ' in cmd:
						c, e = cmd.split(' -- ', 1)
						return c.strip(), e.strip()
					# Try to split if AI used ':' or '-' or similar
					for sep in [': ', ' - ', ' — ', '– ']:
						if sep in cmd:
							c, e = cmd.split(sep, 1)
							return c.strip(), e.strip()
					return cmd.strip(), ''

				st.markdown("""
				<div style='background: rgba(34,34,34,0.7); color: #00ffe7; padding: 10px 16px; border-radius: 8px; font-size: 1.08rem; margin-bottom: 10px; margin-top: 10px;'>
					<b>Suggested Linux Commands:</b>
					<ul style='margin-bottom:0;'>
				""" + (
					''.join([
						f"<li style='margin-bottom:8px'><code style='color:#00ffe7;background:transparent;font-size:1em;'>{split_cmd_expl(cmd)[0]}</code>"
						+ (f"<br><span style='font-size:0.97em;color:#b2f7ef;'>{split_cmd_expl(cmd)[1]}</span>" if split_cmd_expl(cmd)[1] else "")
						+ "</li>"
						for cmd in commands[:3]
					]) if commands else "<li>No Linux commands found.</li>"
				) + """
					</ul>
				</div>
				""", unsafe_allow_html=True)

				# Export to Excel
			except Exception as e:
				st.error(f"OpenAI API error: {e}")


