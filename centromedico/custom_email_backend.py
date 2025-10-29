import ssl
from django.core.mail.backends.smtp import EmailBackend

# La clase hereda el comportamiento normal de Django
class NonVerifyingEmailBackend(EmailBackend):
    """
    Un backend de correo personalizado que desactiva la verificación SSL/TLS
    para resolver el error SSLCertVerificationError en entornos locales.
    """
    def open(self):
        if self.connection:
            return True
        try:
            # Crea un contexto SSL/TLS donde la verificación está deshabilitada
            self.ssl_context = ssl.create_default_context()
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE
            
            # Llama al método open original con el nuevo contexto
            return super().open()
        except Exception:
            # En caso de error, cierra la conexión
            if not self.fail_silently:
                raise