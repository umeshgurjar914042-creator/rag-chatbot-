import streamlit as st
import chromadb
from google import genai

st.set_page_config(page_title="कंपनी पॉलिसी चैटबॉट")
st.title("कंपनी पॉलिसी चैटबॉट")
st.caption("छुट्टी, वेतन और ऑफिस के समय के बारे में पूछिए")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

chunks = [
    "हर कर्मचारी को साल में 12 आकस्मिक छुट्टियाँ मिलती हैं।",
    "बीमारी की छुट्टी 10 दिन की होती है और उसके लिए डॉक्टर का पर्चा ज़रूरी है।",
    "कर्मचारी वर्क फ्रॉम होम हफ्ते में 2 दिन कर सकते हैं।",
    "वेतन हर महीने की 5 तारीख को खाते में आता है।",
    "ऑफिस का समय सुबह 10 बजे से शाम 6 बजे तक है।",
]

def embed(texts):
    r = client.models.embed_content(model="gemini-embedding-001", contents=texts)
    return [e.values for e in r.embeddings]

@st.cache_resource
def collection_बनाओ():
    db = chromadb.Client()
    col = db.get_or_create_collection(name="policy", metadata={"hnsw:space": "cosine"})
    col.upsert(
        ids=[f"chunk{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embed(chunks),
    )
    return col

collection = collection_बनाओ()

def खोजो(सवाल, k=2):
    r = collection.query(query_embeddings=embed([सवाल]), n_results=k)
    return r["documents"][0]

def जवाब(सवाल, k=2):
    संदर्भ = "\n".join(खोजो(सवाल, k))
    प्रॉम्प्ट = f"""नीचे दिए संदर्भ के आधार पर ही सवाल का जवाब दो।
अगर संदर्भ में जवाब न हो तो कहो "मुझे नहीं पता"।

संदर्भ:
{संदर्भ}

सवाल: {सवाल}"""
    r = client.models.generate_content(model="gemini-3.6-flash", contents=प्रॉम्प्ट)
    return r.text

if "इतिहास" not in st.session_state:
    st.session_state.इतिहास = []

for भूमिका, संदेश in st.session_state.इतिहास:
    with st.chat_message(भूमिका):
        st.write(संदेश)

सवाल = st.chat_input("अपना सवाल पूछिए")
if सवाल:
    st.session_state.इतिहास.append(("user", सवाल))
    with st.chat_message("user"):
        st.write(सवाल)
    with st.chat_message("assistant"):
        
     try:
            उत्तर = जवाब(सवाल)
        except Exception as e:
            उत्तर = "एरर: " + str(e)
