from flask import Flask, request, jsonify, render_template
import random
import string
import hashlib
import re

app = Flask(__name__)

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def hash_function(name):
    return hashlib.sha256(name.encode()).hexdigest()[:8]

def obfuscate_lua_code(lua_code):
    pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
    matches = pattern.findall(lua_code)
    obfuscation_map = {match: generate_random_string(8) for match in matches}
    
    obfuscated_code = lua_code
    for original, obfuscated in obfuscation_map.items():
        obfuscated_code = re.sub(r'\b' + re.escape(original) + r'\b', obfuscated, obfuscated_code)
    
    function_pattern = re.compile(r'\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*)\b')
    function_matches = function_pattern.findall(lua_code)
    for function in function_matches:
        hashed_name = hash_function(function)
        obfuscated_code = re.sub(r'\b' + re.escape(function) + r'\b', hashed_name, obfuscated_code)
    
    return obfuscated_code

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obfuscate', methods=['POST'])
def obfuscate():
    data = request.json
    lua_code = data.get('code')
    
    if not lua_code:
        return jsonify({"error": "No code provided"}), 400
    
    obfuscated_code = obfuscate_lua_code(lua_code)
    return jsonify({"obfuscatedCode": obfuscated_code})

if __name__ == '__main__':
    app.run(debug=True)
