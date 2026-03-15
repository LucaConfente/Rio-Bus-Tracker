import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Injeta script que captura todos os data-testid e mostra na tela
st.markdown("""
<div id="testid-list" style="background:#111;color:#0f0;padding:20px;font-family:monospace;font-size:12px;border-radius:8px;margin:20px 0;max-height:400px;overflow:auto;">
  Carregando...
</div>
<script>
setTimeout(function() {
    var els = document.querySelectorAll('[data-testid]');
    var ids = Array.from(els).map(function(el) {
        return el.dataset.testid;
    });
    document.getElementById('testid-list').innerHTML = 
        '<b>data-testid encontrados (' + ids.length + '):</b><br><br>' + 
        ids.join('<br>');
}, 2000);
</script>
""", unsafe_allow_html=True)

with st.sidebar:
    st.write("Sidebar funcionando!")
