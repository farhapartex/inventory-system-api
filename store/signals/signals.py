from django.dispatch import Signal

trigger_test_signal = Signal(providing_args=['owner'])

trigger_create_employee = Signal(providing_args=['request', 'employee', 'store'])
