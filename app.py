import streamlit as st
import requests

# Configurações da página
st.set_page_config(page_title="Envio de WhatsApp", page_icon="💬", layout="centered")
st.title("Envio de WhatsApp via API")
st.markdown("Preencha os dados abaixo para enviar uma mensagem via *template* pelo WhatsApp.")

# Formulário principal
with st.form("form_envio"):
    st.subheader("📋 Dados da Mensagem")
    hotel_code = st.number_input("HotelCode", value=0)
    country_code = st.text_input("CountryCode", value="")
    state_code = st.text_input("StateCode", value="")
    phone_number = st.text_input("PhoneNumber", value="")
    template_id = st.text_input("TemplateId", value="")
    locator_id = st.text_input("LocatorId", value="")

    st.subheader("🧾 Template Parameters")
    param_labels = [
        "Nome do Destinatário",
        "Nº do Processo RAD",
        "Nome da Empresa",
        "Data de Envio",
        "Etapa Inicial",
        "Etapa Final",
        "Descrição do Processo",
        "Nº do Documento",
        "Valor Total",
        "Link do Anexo",
    ]

    template_params = []
    for label in param_labels:
        value = st.text_input(label, value="")
        template_params.append(value)

    st.subheader("🔐 Autenticação")
    token_client = st.text_input("token-client", value="")
    token_application = st.text_input("token-application", value="")

    submit = st.form_submit_button("📤 Enviar Requisição")

# Processamento após envio
if submit:
    try:
        st.info("⏳ Enviando requisição...")

        if not phone_number.strip().isdigit():
            st.warning("⚠️ O número de telefone deve conter apenas dígitos.")
            st.stop()

        url = "https://higs.thex.cloud/pms/api/v1/Whatsapp/Message/SendMessageTemplate"
        headers = {
            "token-client": token_client,
            "token-application": token_application,
            "Content-Type": "application/json"
        }

        payload = {
            "Messages": [
                {
                    "HotelCode": hotel_code,
                    "CountryCode": country_code,
                    "StateCode": state_code,
                    "PhoneNumber": phone_number.strip(),
                    "TemplateId": template_id,
                    "TemplateParameters": template_params,
                    "LocatorId": locator_id
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        st.success("✅ Requisição enviada com sucesso!")
        with st.expander("📄 Ver resposta do servidor"):
            st.json(response.json())

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro de requisição: {e}")
    except Exception as e:
        st.error(f"❌ Erro inesperado: {e}")
