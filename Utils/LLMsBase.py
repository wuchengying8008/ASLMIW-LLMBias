import DeepSeekAPI
import NLPConstant

def getDeepSeekAnswer(promptText):
 answerDS=DeepSeekAPI.api_chat_completions(NLPConstant.DS_URL, NLPConstant.DS_KEY,
                      NLPConstant, str(uuid.uuid4()), promptText)
 return answerDS