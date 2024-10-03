from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline


app = FastAPI()


class InferenceRequest(BaseModel):
    text: str


class Token(BaseModel):
    entity: str
    index: int
    word: str
    start: int
    end: int


class InferenceResponse(BaseModel):
    tokens: list[Token]


class ModelMock:
    def predict(self, text):
        return [
            ["Elon", "Musk", "created", "SpaceX"],
            ["pers-b", "pers-i", "o", "comp-b"],
        ]


tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)

@app.post("/inference")
async def inference(request: InferenceRequest):
    response = nlp(request.text)
    for i in response:
        i.pop('score')
    
    return Token(**i)
