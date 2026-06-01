from typing_extensions import TypedDict
from typing import Annotated, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class State(TypedDict):

    messages: Annotated[List[BaseMessage], add_messages]