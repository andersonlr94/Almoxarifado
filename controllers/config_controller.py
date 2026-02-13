import os
from models.config_model import salvar_config


def criar_controller(page, txt_pasta, lbl_status):

    def salvar(e):
        caminho = txt_pasta.value.strip()

        if not caminho:
            lbl_status.value = "Informe o caminho da pasta."
            lbl_status.color = "red"
            page.update()
            return

        if not os.path.isdir(caminho):
            lbl_status.value = "O caminho informado não existe."
            lbl_status.color = "red"
            page.update()
            return

        salvar_config({"pasta_dados": caminho})

        lbl_status.value = "Configuração salva com sucesso!"
        lbl_status.color = "green"
        page.update()

    return salvar
