from flask import Flask, jsonify, request
import NLPText
import PromptTool

app = Flask(__name__)


@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello, this is a sample API response!'})

@app.route('/api/generateAllPrompt', methods=['POST'])
def post_generate_all():
    data = request.json
    companyname = data.get('companyname')
    generateContents = {}
    for i in range(1, 9):
        methodName = f"generateNo{i}"
        method = getattr(PromptTool, methodName, None)
        if method:
            generateContent = method(companyname)
            generateContents[methodName] = generateContent
            print("返回信息：" + str(generateContent))
    return jsonify({'data': generateContents}), 201

@app.route('/api/LLM', methods=['POST'])
def post_data():
    data = request.json
    question= data.get('question','')
    promptContent=""
    picList = []
    #NLPAnalysis._judgeAndAnalyses(data)
    generateContent = NLPText.AI_intention_judge(question)
    print("返回信息："+str(generateContent))
    if str(generateContent).find('|')>0:
      content=generateContent[0]
      type=content.split('|')[1]
      companyName =content.split('|')[2]
      if content.split('|')[0] == '-1':
        promptContent = PromptTool.generateEnterprisePrompt(type,companyName)
        picList = PromptTool.generatePic(type, companyName)
    return jsonify({'data': generateContent, "content":promptContent, "picList": picList}), 201

@app.route('/api/prompt', methods=['POST'])
def postprompt_data():
    data = request.json
    companyname = data.get('companyname')
    generateContent = PromptTool.getDocByCompanyName(companyname)
    print("返回信息："+str(generateContent))
    return jsonify({'data': generateContent}), 201

@app.route('/api/abstract', methods=['POST'])
def postprompt_abstract():
    data = request.json
    companyname= data.get('companyname')
    #NLPAnalysis._judgeAndAnalyses(data)
    generateContent = PromptTool.generateAbstract(companyname)
    print("返回信息："+str(generateContent))
    return jsonify({'data': generateContent}), 201
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)