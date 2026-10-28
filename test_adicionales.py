"""Cinco escenarios complementarios al Laboratorio 7."""

import pytest

import library
import main
from book import Book
from library import Library
from user import User


@pytest.fixture
def biblioteca(monkeypatch):
    """Cada caso recibe datos nuevos y una configuracion aislada."""
    monkeypatch.setitem(library.settings, "loans_enabled", True)
    lib = Library()
    lib.add_book(Book("1984", "George Orwell", 1949, "ISBN001"))
    lib.add_user(User("Anna", "U001"))
    return lib


@pytest.mark.adicionales
@pytest.mark.integration
def test_prestamos_deshabilitados_no_modifican_estado(biblioteca, monkeypatch, capsys):
    """PA-01: la configuracion bloquea el prestamo sin cambiar libro ni historial."""
    monkeypatch.setitem(library.settings, "loans_enabled", False)

    biblioteca.borrow_book("U001", "ISBN001")

    assert capsys.readouterr().out == "Loans are disabled\n"
    assert biblioteca.books[0].borrowed is False
    assert biblioteca.users[0].get_history() == []


@pytest.mark.adicionales
@pytest.mark.integration
def test_devolucion_con_usuario_inexistente_no_modifica_estado(biblioteca):
    """PA-02: una devolucion invalida no libera un libro ni altera el historial."""
    biblioteca.borrow_book("U001", "ISBN001")
    historial_anterior = list(biblioteca.users[0].get_history())

    with pytest.raises(ValueError, match="^User not found$"):
        biblioteca.return_book("U999", "ISBN001")

    assert biblioteca.books[0].borrowed is True
    assert biblioteca.users[0].get_history() == historial_anterior
    assert len(biblioteca.users) == 1


@pytest.mark.adicionales
@pytest.mark.integration
def test_isbn_inexistente_no_modifica_estado(biblioteca):
    """PA-03: un ISBN desconocido genera ValueError sin registrar un prestamo."""
    with pytest.raises(ValueError, match="^Book not found$"):
        biblioteca.borrow_book("U001", "ISBN999")

    assert biblioteca.books[0].borrowed is False
    assert biblioteca.users[0].get_history() == []
    assert len(biblioteca.books) == 1


@pytest.mark.adicionales
@pytest.mark.system
def test_consultar_historial_vacio_desde_menu(monkeypatch, capsys):
    """PA-04: la opcion 3 consulta un usuario sin movimientos y permite salir."""
    entradas = iter(["3", "U001", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(entradas))

    main.run()

    salida = capsys.readouterr().out
    assert "User history: []" in salida
    assert "Error:" not in salida
    assert salida.count("--- Library System ---") == 2


@pytest.mark.adicionales
@pytest.mark.system
def test_menu_se_recupera_de_opcion_invalida(monkeypatch, capsys):
    """PA-05: tras una opcion invalida se puede consultar historial y salir."""
    entradas = iter(["opcion-invalida", "3", "U001", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(entradas))

    main.run()

    salida = capsys.readouterr().out
    assert salida.count("Invalid option") == 1
    assert "User history: []" in salida
    assert "Error:" not in salida
    assert salida.index("Invalid option") < salida.index("User history: []")
    assert salida.count("--- Library System ---") == 3
