import book
import pytest
import library
import user


@pytest.mark.unit
def test_borrow_book():
    book1 = book.Book("Orgullo y prejuicio", "Tenoch M", 2026, "ISBN0001")
    assert book1.title == "Orgullo y prejuicio"

    book1.borrow()
    assert book1.borrowed


@pytest.mark.unit
def test_borrow_two_times_book():
    book1 = book.Book("Orgullo y prejuicio", "Tenoch M", 2026, "ISBN0001")
    book1.borrow()
    assert book1.borrowed == True
    with pytest.raises(ValueError, match="The book is already borrowed"):
        book1.borrow()


@pytest.mark.unit
def test_return_book():
    book1 = book.Book("Orgullo y prejuicio", "Tenoch M", 2026, "ISBN0001")
    assert book1.title == "Orgullo y prejuicio"

    book1.borrow()
    assert book1.borrowed
    book1.return_book()
    assert book1.borrowed == False


@pytest.mark.unit
def test_borrow_and_try_exception():
    book1 = book.Book("Orgullo y prejuicio", "Tenoch M", 2026, "ISBN0001")
    book1.borrow()
    assert book1.borrowed == True
    with pytest.raises(ValueError, match="The book is already borrowed"):
        book1.borrow()


@pytest.fixture
def lib_init():
    lib = library.Library()
    book_tenoch = book.Book("Orgullo y prejuicio", "Tenoch M", 2026, "ISBN0001")
    lib.add_book(book_tenoch)
    Tenoch = user.User("Tenoch", "0001")
    lib.add_user(Tenoch)

    return lib

@pytest.mark.unit
def test_library_init(lib_init):
    lib = lib_init
    lib.borrow_book("ISBN0001", "0001")

    assert lib.books[0].borrowed == True


@pytest.mark.wip
def test_library_init_ID_not_registered(lib_init):
    lib = lib_init

    with pytest.raises(ValueError, match="User ID not registered"):
        lib.borrow_book("ISBN0001", "0002")
