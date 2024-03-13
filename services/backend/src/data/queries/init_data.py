# Standard Library imports
from uuid import UUID

# Core FastAPI imports

# Third-party imports

# App imports
from src.data.models import Device, InfoDevice


"""

    Тестовые данные

"""

bulk_new_devices = [Device(id=UUID("dd2713ba-d5db-4c1d-8317-fa970a4f6a03")),
                    Device(id=UUID("7c2b1c83-0414-4e59-b0f6-467a0a1bc802"))]

bulk_new_info_device = [InfoDevice(device_id=bulk_new_devices[0].id, x=1.1, y=1.2, z=1.3),
                        InfoDevice(device_id=bulk_new_devices[0].id, x=1.1, y=1.2, z=1.3),
                        InfoDevice(device_id=bulk_new_devices[0].id, x=1.1, y=1.2, z=1.3),
                        InfoDevice(device_id=bulk_new_devices[0].id, x=10.1, y=10.2, z=10.3),
                        InfoDevice(device_id=bulk_new_devices[1].id, x=1.1, y=1.2, z=1.3),
                        InfoDevice(device_id=bulk_new_devices[1].id, x=1.1, y=1.2, z=1.3),
                        InfoDevice(device_id=bulk_new_devices[1].id, x=1.1, y=1.2, z=1.3),
                        InfoDevice(device_id=bulk_new_devices[1].id, x=1000.1, y=1000.2, z=1000.3),
                        ]
