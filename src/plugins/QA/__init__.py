import nonebot
import json
import re
from nonebot import on_message
from nonebot.params import EventType
from nonebot.rule import to_me
from nonebot.params import Depends
async def Rulecheck_0(event):
    message=event.get_plaintext()
    if message.startswith('QA') and '!' in message:
        return True
    else:
        return False
def saveQA(J0):
    with open(r'./src/plugins/QA/QA_1.json','w')as f1:
        json.dump(J0,f1)
def loadQA():
    with open(r'./src/plugins/QA/QA_1.json','r')as f1:
        J0=json.load(f1)
        return(J0)
async def Rulecheck_1(event):
    return event.get_plaintext().startswith('删除QA')
async def Get_mug(event):
    if event.get_session_id().startswith('group'):
        re0=re.compile(r'group_(\d+)_(\d+)')
        re1=re0.search(event.get_session_id())
        gid=re1.group(1)
        uid=re1.group(2)
        message=event.get_plaintext()
        return [message,uid,gid]
    else:
        message=event.get_plaintext()
        uid=event.get_session_id()
        return [message,uid,None]
    return event.get_session_id()
QA_create=on_message(rule=Rulecheck_0,priority=90)
QA_checkall=on_message(priority=90)
QA_kill=on_message(rule=Rulecheck_1,priority=90)
@QA_create.handle()
async def QAcreate(matcher,event,A=Depends(Get_mug)):
    if A[2]==None:
        await QA_create.finish()
    re0=re.compile(r'QA(.+)!(.+)')
    re1=re0.search(A[0])
    if re1 != None:
        Key=re1.group(1)
        Value=re1.group(2)
        J0=loadQA()
        if A[1] not in J0:
            J0[A[1]]={}
        J0[A[1]][Key]=Value
        saveQA(J0)
        await QA_create.finish('问答添加成功')
    await matcher.finish()
@QA_checkall.handle()
async def QAcheckall(matcher,event,A=Depends(Get_mug)):
    J0=loadQA()
    if A[1] in J0:
        if A[0] in J0[A[1]].keys():
            await QA_checkall.finish(f'{J0[A[1]][A[0]]}')
    await matcher.finish()
@QA_kill.handle()
async def QAkill(matcher,event,A=Depends(Get_mug)):
    J0=loadQA()
    waitstr_0=A[0][4:]
    if A[1] in J0:
        if waitstr_0 in J0[A[1]].keys():
            del J0[A[1]][waitstr_0]
            saveQA(J0)
            await QA_create.finish('已删除')
    await matcher.finish()



