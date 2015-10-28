
"""A definition of the fields describing a server used in lieu of defining remotable
objects"""
ServerFields = frozenset(['id', 'uuid', 'name', 'cpu_count',
                          'local_drive_capacity', 'psu_capacity', 'psu_size',
                          'memory_mb', 'cpu_architecture', 'ipmi_password',
                          'ipmi_username', 'ipmi_priv_level',
                          'ipmi_mac_address', 'reservation_id', 'deployed'])
