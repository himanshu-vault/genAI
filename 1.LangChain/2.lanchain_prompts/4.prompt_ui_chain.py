from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, load_prompt
import streamlit as st


model = ChatOpenAI(
    model="gpt-4o-2024-08-06",
    temperature=1
)

st.header('Research Tool')
# user_input = st.text_input('Enter Your Prompt')


paper_input = st.selectbox("Select Research Paper Name",
['Attention Is All You Need',
'BERT: Pre-training of Deep Bidirectional Transformers',
'GPT-3: Language Models Need are Few-Shot Learners'
'Diffusion Models Beat GANs on Image Synthesis'])

style_input =  st.selectbox( "Select Explanation Style" ,
["Beginner-Friendly", "Code-Oriented" , "Mathematical", "Technical"])

length_input = st.selectbox( "Select Explanation Length", 
                            ["Short (1-2 paragraphs)",
                             "Medium(3-5 paragraphs)",
                             "Long (detailed explanation)"])


# template
template = load_prompt('template.json')





# if st.button("Get Summary"):
#     # fill the placeholders
#     prompt = template.invoke({
#             'paper_input' : paper_input,
#             'style_input' : style_input,
#             'length_input' : length_input
#             })

#     result = model.invoke(prompt)
#     st.write(result.content)



if st.button('Get Summary'):
    chain = template | model
    result = chain.invoke({
            'paper_input' : paper_input,
            'style_input' : style_input,
            'length_input' : length_input
            })
    
    st. write(result.content)