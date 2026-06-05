"""
Testes unitários para o Sistema de Gerenciamento de Biblioteca Digital
PUCPR - Programação para Ciência de Dados - Hora da Prática 2

Execute com:
    python -m unittest tests/test_biblioteca.py -v
"""

import shutil
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Garante que o módulo principal seja encontrado independente de onde os testes rodam
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import biblioteca


class TestBibliotecaDigital(unittest.TestCase):
    """Testes para todas as funcionalidades do sistema."""

    def setUp(self):
        """
        Prepara um repositório temporário antes de cada teste.
        Isso evita que os testes modifiquem a pasta 'documentos' real.
        """
        self.dir_original = biblioteca.DIRETORIO_BASE
        biblioteca.DIRETORIO_BASE = Path("documentos_teste")
        biblioteca.DIRETORIO_BASE.mkdir(exist_ok=True)
        self._criar_arquivos_exemplo()

    def tearDown(self):
        """Remove o repositório temporário após cada teste."""
        shutil.rmtree(biblioteca.DIRETORIO_BASE, ignore_errors=True)
        biblioteca.DIRETORIO_BASE = self.dir_original

    def _criar_arquivos_exemplo(self):
        """Cria arquivos de teste com conteúdo mínimo para simular documentos reais."""
        arquivos = [
            ("pdf", "2022", "relatorio_anual.pdf"),
            ("pdf", "2023", "artigo_ia.pdf"),
            ("pdf", "2023", "tese_redes.pdf"),
            ("pdf", "2024", "livro_python.pdf"),
            ("epub", "2022", "introducao_dados.epub"),
            ("epub", "2023", "machine_learning.epub"),
        ]
        for tipo, ano, nome in arquivos:
            pasta = biblioteca.DIRETORIO_BASE / tipo / ano
            pasta.mkdir(parents=True, exist_ok=True)
            # Escreve conteúdo mínimo para que stat().st_size seja calculável
            (pasta / nome).write_text("conteudo de exemplo")

    # ─────────────────────────────────────────
    # Testes: listar_documentos
    # ─────────────────────────────────────────

    def test_listar_todos_os_documentos(self):
        """Deve retornar os 6 documentos criados no setUp."""
        resultado = biblioteca.listar_documentos()
        total = sum(
            len(arqs)
            for anos in resultado.values()
            for arqs in anos.values()
        )
        self.assertEqual(total, 6)

    def test_listar_filtro_por_tipo_pdf(self):
        """Deve retornar apenas documentos PDF quando filtrado por tipo."""
        resultado = biblioteca.listar_documentos(tipo="pdf")
        self.assertIn("pdf", resultado)
        self.assertNotIn("epub", resultado)

    def test_listar_filtro_por_ano(self):
        """Deve retornar apenas documentos do ano informado."""
        resultado = biblioteca.listar_documentos(ano="2023")
        for anos in resultado.values():
            for ano_doc in anos:
                self.assertEqual(ano_doc, "2023")

    def test_listar_repositorio_vazio(self):
        """Deve retornar dicionário vazio quando não há documentos."""
        shutil.rmtree(biblioteca.DIRETORIO_BASE)
        biblioteca.DIRETORIO_BASE.mkdir()
        resultado = biblioteca.listar_documentos()
        self.assertEqual(len(resultado), 0)

    def test_listar_sem_repositorio(self):
        """Deve lidar corretamente com repositório inexistente."""
        shutil.rmtree(biblioteca.DIRETORIO_BASE)
        resultado = biblioteca.listar_documentos()
        self.assertEqual(resultado, {})

    # ─────────────────────────────────────────
    # Testes: adicionar_documento
    # ─────────────────────────────────────────

    def test_adicionar_documento_pdf_valido(self):
        """Deve copiar o arquivo para a pasta correta (pdf/2024/)."""
        temp = Path("novo_artigo.pdf")
        temp.write_text("conteudo")
        try:
            resultado = biblioteca.adicionar_documento(str(temp), "2024")
            self.assertTrue(resultado)
            destino = biblioteca.DIRETORIO_BASE / "pdf" / "2024" / "novo_artigo.pdf"
            self.assertTrue(destino.exists())
        finally:
            temp.unlink(missing_ok=True)

    def test_adicionar_arquivo_inexistente(self):
        """Deve retornar False quando o arquivo de origem não existe."""
        resultado = biblioteca.adicionar_documento("fantasma.pdf", "2023")
        self.assertFalse(resultado)

    def test_adicionar_tipo_nao_suportado(self):
        """Deve rejeitar extensões que não estão em TIPOS_SUPORTADOS."""
        temp = Path("video.mp4")
        temp.write_text("x")
        try:
            resultado = biblioteca.adicionar_documento(str(temp), "2023")
            self.assertFalse(resultado)
        finally:
            temp.unlink(missing_ok=True)

    def test_adicionar_documento_duplicado(self):
        """Deve rejeitar arquivo com mesmo nome que já existe no destino."""
        temp = Path("artigo_ia.pdf")
        temp.write_text("outro conteudo")
        try:
            # artigo_ia.pdf já existe em pdf/2023 (criado no setUp)
            resultado = biblioteca.adicionar_documento(str(temp), "2023")
            self.assertFalse(resultado)
        finally:
            temp.unlink(missing_ok=True)

    # ─────────────────────────────────────────
    # Testes: renomear_documento
    # ─────────────────────────────────────────

    def test_renomear_documento_existente(self):
        """Deve renomear o arquivo e verificar que o novo nome existe."""
        resultado = biblioteca.renomear_documento(
            "artigo_ia.pdf", "artigo_inteligencia_artificial.pdf"
        )
        self.assertTrue(resultado)
        novo = biblioteca.DIRETORIO_BASE / "pdf" / "2023" / "artigo_inteligencia_artificial.pdf"
        antigo = biblioteca.DIRETORIO_BASE / "pdf" / "2023" / "artigo_ia.pdf"
        self.assertTrue(novo.exists())
        self.assertFalse(antigo.exists())

    def test_renomear_documento_inexistente(self):
        """Deve retornar False para arquivo que não existe no repositório."""
        resultado = biblioteca.renomear_documento("nao_existe.pdf", "novo.pdf")
        self.assertFalse(resultado)

    def test_renomear_para_nome_ja_existente(self):
        """Deve retornar False se o novo nome já está em uso na mesma pasta."""
        resultado = biblioteca.renomear_documento("artigo_ia.pdf", "tese_redes.pdf")
        self.assertFalse(resultado)

    # ─────────────────────────────────────────
    # Testes: remover_documento
    # ─────────────────────────────────────────

    @patch("builtins.input", return_value="s")
    def test_remover_documento_confirmado(self, _mock):
        """Deve remover o arquivo quando o usuário digita 's'."""
        resultado = biblioteca.remover_documento("artigo_ia.pdf")
        self.assertTrue(resultado)
        removido = biblioteca.DIRETORIO_BASE / "pdf" / "2023" / "artigo_ia.pdf"
        self.assertFalse(removido.exists())

    @patch("builtins.input", return_value="n")
    def test_remover_documento_cancelado(self, _mock):
        """Deve manter o arquivo quando o usuário digita 'n'."""
        resultado = biblioteca.remover_documento("artigo_ia.pdf")
        self.assertFalse(resultado)
        existente = biblioteca.DIRETORIO_BASE / "pdf" / "2023" / "artigo_ia.pdf"
        self.assertTrue(existente.exists())

    def test_remover_documento_inexistente(self):
        """Deve retornar False para arquivo que não está no repositório."""
        resultado = biblioteca.remover_documento("nao_existe.pdf")
        self.assertFalse(resultado)

    # ─────────────────────────────────────────
    # Testes: criar_diretorio
    # ─────────────────────────────────────────

    def test_criar_diretorio_novo(self):
        """Deve criar a pasta corretamente dentro do repositório."""
        resultado = biblioteca.criar_diretorio("mobi/2025")
        self.assertTrue(resultado)
        self.assertTrue((biblioteca.DIRETORIO_BASE / "mobi" / "2025").exists())

    def test_criar_diretorio_ja_existente(self):
        """Deve retornar False quando o diretório já existe."""
        resultado = biblioteca.criar_diretorio("pdf/2023")
        self.assertFalse(resultado)

    # ─────────────────────────────────────────
    # Testes: remover_diretorio
    # ─────────────────────────────────────────

    def test_remover_diretorio_vazio(self):
        """Deve remover diretório vazio sem pedir confirmação."""
        nova_pasta = biblioteca.DIRETORIO_BASE / "temporario"
        nova_pasta.mkdir()
        resultado = biblioteca.remover_diretorio("temporario")
        self.assertTrue(resultado)
        self.assertFalse(nova_pasta.exists())

    def test_remover_diretorio_inexistente(self):
        """Deve retornar False para diretório que não existe."""
        resultado = biblioteca.remover_diretorio("nao_existe")
        self.assertFalse(resultado)

    @patch("builtins.input", return_value="s")
    def test_remover_diretorio_com_arquivos_confirmado(self, _mock):
        """Deve remover diretório com arquivos quando confirmado."""
        resultado = biblioteca.remover_diretorio("pdf/2023")
        self.assertTrue(resultado)
        self.assertFalse((biblioteca.DIRETORIO_BASE / "pdf" / "2023").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
