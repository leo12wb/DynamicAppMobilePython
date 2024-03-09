from flet import App, Page, Input, Button, Label
import requests

app = App()

class DynamicPage(Page):
    def __init__(self, page_data):
        super().__init__()
        self.load_elements(page_data)

    def load_elements(self, page_data):
        for element_data in page_data['elements']:
            if element_data['type'] == 'Input':
                self.add(Input(element_data['label'], id=element_data['id']))
            elif element_data['type'] == 'Button':
                self.add(Button(element_data['label'], on_click=self.handle_button_click(element_data), method=element_data.get('method', 'GET'), url=element_data.get('action')))
            elif element_data['type'] == 'Label':
                self.add(Label(element_data['text']))

    def handle_button_click(self, element_data):
        if 'action' in element_data:
            def handler():
                response = requests.get(element_data['action'])
                if response.status_code == 200:
                    page_data = response.json()
                    app.navigate(DynamicPage(page_data))
                else:
                    self.show_alert('Erro ao carregar a página.')
            return handler

# Função para obter o JSON da página do microserviço
def get_page_data(page_name='listagem'):
    response = requests.get(f'http://seu_microservico.com/gerar_pagina?pagina={page_name}')
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Adicionar página de listagem por padrão
page_data_listagem = get_page_data()
if page_data_listagem:
    app.add_page(DynamicPage(page_data_listagem))

app.run()

# abaixo é uma simulação do json do micro serviço deste Aplicativo 
# versão 1.0 teste
"""
 {
    "cadastro": {
        "elements": [
            {
                "type": "Label",
                "text": "Página de Cadastro"
            },
            {
                "type": "Input",
                "label": "Nome:",
                "id": "nome"
            },
            {
                "type": "Input",
                "label": "Email:",
                "id": "email"
            },
            {
                "type": "Button",
                "label": "Cadastrar",
                "action": "http://seu_microservico.com/cadastrar_usuario",
                "method": "POST"
            }
        ]
    },
    "listagem": {
        "elements": [
            {
                "type": "Label",
                "text": "Lista de Usuários Cadastrados:"
            },
            {
                "type": "Button",
                "label": "Voltar",
                "action": "http://seu_microservico.com/voltar",
                "method": "GET"
            }
        ]
    }
}
"""
