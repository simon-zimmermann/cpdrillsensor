
from grove.adc import ADC
import time

adc = ADC()

while True:
  value = adc.read_voltage(2)
  print("value: %f" % value)
  time.sleep(1)
