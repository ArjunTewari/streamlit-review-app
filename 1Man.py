import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI

template = """\
For the following text, extract the following \
information:

sentiment: Is the customer happy with the product? 
Answer Positive if yes, Negative if \
not, Neutral if either of them, or Unknown if unknown.

delivery_days: How many days did it take \
for the product to arrive? If this \
information is not found, output No information about this.

price_perception: How does it feel the customer about the price? 
Answer Expensive if the customer feels the product is expensive, 
Cheap if the customer feels the product is cheap,
not, Neutral if either of them, or Unknown if unknown.

Further_action : What could be improvised in the product, 
This is only applicable when review is negative,
It should be short and concise.

Format the output as bullet-points text with the \
following keys:
- Sentiment
- How long took it to deliver?
- How was the price perceived?
- Further action to be taken

Input example:
This dress is pretty amazing. It arrived in two days, just in time for my wife's anniversary present. It is cheaper than the other dresses out there, but I think it is worth it for the extra features.

Output example:
- Sentiment: Positive
- How long took it to deliver? 2 days
- How was the price perceived? Cheap

text: {review}
"""

prompt = PromptTemplate(
    input_variables=["review"],
    template=template
)

def load_llm(openai_api_key):
    llm = OpenAI(openai_api_key = openai_api_key)
    return llm

st.set_page_config(page_title="Key info from review")
st.header("Key information extraction from the reviews")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        Key information included :
        1. Sentiment
        2. How long it took to deliver
        3. How was its price perceived
        4. Further action to be taken
        """
    )
with col2:
    st.write("If you have any issue with the response generated, [Contact](https://mail.google.com/mail/u/0/#inbox?compose=new)")

st.markdown("## Enter your OPENAI API Key")

def get_api_key():
    api_key = st.text_input(label="Text", label_visibility="collapsed", placeholder="Enter the API key", key="openai_api_key")
    return api_key
openai_api_key = get_api_key()

st.markdown("## Enter the review")
def get_review():
    review = st.text_input(label="Text", label_visibility="collapsed", placeholder="Review of the text", key="review")
    return review
review = get_review()

st.markdown("## Key data extracted: ")

if review:
    if not openai_api_key:
        st.warning("Please enter the api key", icon="⚠️")
        st.stop()
    llm = load_llm(openai_api_key=openai_api_key)

    final_prompt = prompt.format(
        review=review
    )

    data_extracted = llm(final_prompt)
    st.write(data_extracted)

