# app/utils/prompt_agent.py
import uuid
import boto3

AGENT_ID       = "WJQ271GKT0"   # 你的 Agent ID
AGENT_ALIAS_ID = "HGMFSPNWAS"         # Console 裡建立的 alias
REGION         = "us-east-1"

_client = boto3.client("bedrock-agent-runtime", region_name=REGION)

def ask_agent(prompt: str, session_id: str | None = None) -> str:
    """呼叫 Bedrock Agent 並回傳完整文字"""
    if session_id is None:
        session_id = str(uuid.uuid4())

    resp = _client.invoke_agent(
        agentId       = AGENT_ID,
        agentAliasId  = AGENT_ALIAS_ID,
        sessionId     = session_id,
        inputText     = prompt,
        enableTrace   = False          # 若要觀察推理過程可設 True
    )

    # Bedrock 以 event stream 回傳 → 將 chunk 串起來
    answer = ""
    for event in resp["completion"]:
        answer += event["chunk"]["bytes"].decode("utf-8")
    return answer
