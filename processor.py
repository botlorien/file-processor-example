import chardet
from chardet.universaldetector import UniversalDetector


class FileProcessor:

    def read_file(self,file_path:str,encoding:str) -> str:
        try:
            with open(file_path,'rb') as f:
                content_bytes = f.read()
                content = content_bytes.decode(encoding)
                return content
        except UnicodeDecodeError as e:
            print(f"Erro de decodificação: {e}")
            result = chardet.detect(content_bytes)
            print(f"O encoding mais provavel para o conteudo pelo chardet.detect é: {result}")
            detector = UniversalDetector()
            with open(file_path,'rb') as f:
                for line in f:
                    detector.feed(line)
                    if detector.done:
                        break
            detector.close()
            print(f"O encoding mais provavel para o conteudo pelo chardet.universaldetector é: {detector.result}")
            return ""


    def write_file(self,file_path:str, content:str, encoding:str) -> None:
        try:
            content_bytes = content.encode(encoding)
            with open(file_path,'wb') as f:
                f.write(content_bytes)
        except UnicodeEncodeError as e:
            print(f"Erro de codificação: {e}")

    def convert_encoding(self,source_file:str,dest_file:str,source_encoding:str, dest_encoding:str) -> None:
        content = self.read_file(source_file,source_encoding)
        if content:
            self.write_file(dest_file,content,dest_encoding)

    def process_bytes(self,content:bytes) -> bytearray:
        array = bytearray(content)
        for i in range(len(array)):
            if array[i] == ord('a'):
                array[i] = ord('A')
        return array

if __name__=='__main__':
    # Criando uma instancia
    fp = FileProcessor()

    # Lendo o arquivo utf-8 sem erros
    content_s = fp.read_file('exemplo_utf8.txt','utf-8')
    print("Conteudo sem erros: ",content_s)

    # Lendo o arquivo utf-8 com erros
    content_c = fp.read_file('exemplo_utf8.txt','ascii')
    print("Conteudo com erros",content_c)

    # Escrevendo uma arquivo sem erros
    print("Escrevendo sem erros")
    fp.write_file('test_write_sem_erros.txt',content_s,'utf-8')
    
    # Escrevendo um arquivo com erros
    print("Escrevendo com erros")
    fp.write_file('test_write_com_erros.txt',content_s,'ascii')

    # Convertendo um arquivo utf-8 para ascii
    print("Convertendo um arquivo")
    fp.convert_encoding('exemplo_ascii.txt','test_conversion.txt','ascii','utf8')

    # Processando os bytes
    print("Processando os bytes")
    array = fp.process_bytes(bytes(content_s,'utf8'))
    print(array.decode('utf8'))