import logging
logging.basicConfig(level = logging.DEBUG)

class Word:
    format = Struct('')

    def __init__(self, frequency: int, sequencies: List[Dict]) -> None:
        logging.info(f'Inicializando registro (frequencia: {frequency}, sequencias: {sequencies}).')
        self._frequency = frequency
        self._sequencies = sequencies

    @classmethod
    def new_empty(cls): # -> Word
        logging.info(f'Criando registro vazio.')
        return cls(0, [])

    @classmethod 
    def from_bytes(cls, data: bytes): #-> Entry
        logging.info(f'Deserializando registro.')

    def into_bytes(self) -> bytes:
        logging.info(f'Serializando registro.')
        return bytes()

    @classmethod
    def size(cls) -> int:
        logging.info(f'Calculando tamanho do registro.') 
        return 0