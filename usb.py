import usb.core
import usb.util

# Encuentra el dispositivo USB
dev = usb.core.find(find_all=True)

# ¿Se encontró el dispositivo?
if dev is None:
    raise ValueError('Dispositivo no encontrado')

# Establece la configuración activa
dev.set_configuration()

# Obtén la configuración activa
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

# Encuentra el descriptor de endpoint
ep = usb.util.find_descriptor(
    intf,
    # Coincide con el primer endpoint de salida (OUT)
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
)

assert ep is not None

# Escribe los datos
data = b'test'
ep.write(data)
