from http.server import BaseHTTPRequestHandler, HTTPServer
import os
#http://localhost:8000/map/1/a/0/0.png
class ImageServer(BaseHTTPRequestHandler):
    # Директория с изображениями
    IMAGE_DIR = "images"  # Укажите путь к вашей папке с изображениями
    
    def do_GET(self):
        # Обработка запросов к корню
        print(self.path)
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Отправляем HTML с кириллицей, кодируя в utf-8
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Image Server</title>
            </head>
            <body>
                <h1>Image Server</h1>
                <p>Доступные изображения:</p>
                {}
            </body>
            </html>
            """
            
            self.wfile.write(html_content.encode('utf-8'))
            return
        
        # Попытка найти и отправить изображение
        try:
            # Безопасное формирование пути к файлу
            path = self.path.lstrip('/')
            #full_path = os.path.join(self.path, os.path.basename(path))
            full_path = path
            print(path,full_path, os.path.basename(path))
            # Проверка существования файла и что он в разрешенной директории
            if not os.path.exists(full_path) or not os.path.isfile(full_path):
                raise FileNotFoundError
            
            # Определение Content-Type по расширению файла
            ext = os.path.splitext(full_path)[1].lower()
            content_type = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif'
            }.get(ext, 'application/octet-stream')
            
            # Чтение и отправка файла
            with open(full_path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(f.read())
                
        except FileNotFoundError:
            self.send_error(404, "File Not Found")
        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")

def run(server_class=HTTPServer, handler_class=ImageServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Сервер запущен на порту {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    # Создаем директорию для изображений, если ее нет
    if not os.path.exists(ImageServer.IMAGE_DIR):
        os.makedirs(ImageServer.IMAGE_DIR)
        print(f"Создана директория {ImageServer.IMAGE_DIR}. Добавьте туда изображения.")
    
    run()