import os
import sys

# Asegura que la raíz del proyecto esté en sys.path durante la colección de pytest
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
