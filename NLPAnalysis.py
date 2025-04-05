import matplotlib.pyplot as plt
import pymysql as pmq
import matplotlib.font_manager as fm
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import datetime
import matplotlib
import matplotlib.pyplot as plt
import datetime
import time
import sys
import NLPText

def _judgeAndAnalyses(inputData,inputLLMdata):
    _returnType=0;
    _returnPath="";
    _returnContent="";
    _returnCallBack=0;
    _returnCommand="";
    generateContent=NLPText.AI_intention_judge(inputData)
    return generateContent
#_judgeAndAnalyses(sys.argv[1], sys.argv[2])