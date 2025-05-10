import requests

# API_TOKEN = "wAuzeTQbBowf6RJYgqMJ3RIS2sd2r8wL" 
API_TOKEN = "wAuzeTQbBowf6RJYgqMJ3RIS2sd2r8wL"
API_URL = "https://api.deepinfra.com/v1/inference/meta-llama/Meta-Llama-3-8B-Instruct"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def GetResponse(qry):    
    # qry = "who is current president of india?"
    # # New user question about AI
    data = {
        "input": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n" + qry + "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        "stop": ["<|eot_id|>"],
        "stream": False
    }
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200: # Ok
        response_json = response.json()
        generated_text = response_json["results"][0]["generated_text"]
        
        # print("🤖 AI Response:\n", generated_text)
    else:
        print("❌ Error:", response.status_code,response.text)
    return generated_text

# r = GetResponse("hi")
# print("🤖 AI Response:\n", r)