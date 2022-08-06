from transformers import BertTokenizer, BertForQuestionAnswering
import torch
import time


class InformationExtractor:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained("deepset/bert-base-cased-squad2")
        self.model = BertForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")

    def __call__(self, question, passage):
        inputs = self.tokenizer(question, str(passage), return_tensors="pt", truncation=True, max_length=512, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)

        answer_start_index = outputs.start_logits.argmax()
        answer_end_index = outputs.end_logits.argmax()

        predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
        answer = self.tokenizer.decode(predict_answer_tokens)
        return answer

# information_extractor = InformationExtractor()
# passage = "Anne of Green Gables is a 1908 novel by Canadian author Lucy Maud Montgomery (published as L. M. Montgomery). Written for all ages, it has been considered a classic children's novel since the mid-20th century. Set in the late 19th century, the novel recounts the adventures of Anne Shirley, an 11-year-old orphan girl, who is sent by mistake to two middle-aged siblings, Matthew and Marilla Cuthbert, who had originally intended to adopt a boy to help them on their farm in the fictional town of Avonlea in Prince Edward Island, Canada. The novel recounts how Anne makes her way through life with the Cuthberts, in school, and within the town."
# question = "Who is the protagonist?"

# time_st = time.time()
# print(information_extractor(question, passage))
# end = time.time()
# print("time taken: ", end - time_st)