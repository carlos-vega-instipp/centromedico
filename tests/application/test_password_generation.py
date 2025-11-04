from application.utils import generar_contraseña


def test_generar_contrasena_basico():
    pwd = generar_contraseña()
    assert len(pwd) >= 8
    assert any(c.isupper() for c in pwd)
    assert any(c.islower() for c in pwd)
    assert any(c.isdigit() for c in pwd)
    assert any(c in '@.!_$' for c in pwd)
